"""
HTML parser
"""
import os
import webbrowser
import tkinter as tk
from tkinter import font
from copy import deepcopy
from PIL import Image, ImageTk
from html.parser import HTMLParser
from collections import OrderedDict
import requests
from io import BytesIO


# __________________________________________________________________________________________________
class Defs:
    DEFAULT_TEXT_FONT_FAMILY = ("Segoe ui", "Calibri", "Helvetica", "TkTextFont")
    FONT_SIZE = 14
    PREFORMATTED_FONT_FAMILY = ("Courier", "DejaVu Sans Mono", "TkFixedFont")
    HEADINGS_FONT_SIZE = {
        "h1": 32,
        "h2": 24,
        "h3": 18,
        "h4": 16,
        "h5": 13,
        "h6": 10,
    }


class HTML:
    # ----------------------------------------------------------------------------------------------
    """
    List of supported HTML tags and attrs
    """

    class Tag:
        BR = "br"
        UL = "ul"
        OL = "ol"
        LI = "li"
        IMG = "img"
        A = "a"
        B = "b"
        STRONG = "strong"
        I = "i"
        EM = "em"
        U = "u"
        MARK = "mark"
        SPAN = "span"
        DIV = "div"
        P = "p"
        PRE = "pre"
        CODE = "code"
        H1 = "h1"
        H2 = "h2"
        H3 = "h3"
        H4 = "h4"
        H5 = "h5"
        H6 = "h6"
        TABLE = "table"
        TR = "tr"
        TH = "th"
        TD = "td"

    class Attrs:
        STYLE = "style"
        HREF = "href"
        SRC = "src"
        WIDTH = "width"
        HEIGHT = "height"
        TYPE = "type"

    class TypeOrderedList:
        _1 = "1"
        a = "a"
        A = "A"

    class Style:
        COLOR = "color"
        BACKGROUND_COLOR = "background-color"
        FONT_FAMILY = "font-family"
        FONT_SIZE = "font-size"
        TEXT_ALIGN = "text-align"
        TEXT_DECORATION = "text-decoration"

    class StyleTextDecoration:
        UNDERLINE = "underline"
        LINE_THROUGH = "line-through"

    HEADING_TAGS = (
        Tag.H1,
        Tag.H2,
        Tag.H3,
        Tag.H4,
        Tag.H5,
        Tag.H6,
    )

    TEXT_ALIGN_TAGS = HEADING_TAGS + (
        Tag.UL,
        Tag.OL,
        Tag.LI,
        Tag.DIV,
        Tag.P,
        Tag.PRE,
        Tag.CODE,
        Tag.TD,
        Tag.TH,
    )

    NEW_LINE_TAGS = HEADING_TAGS + (
        Tag.UL,
        Tag.OL,
        Tag.DIV,
        Tag.P,
        Tag.PRE,
        #Tag.CODE,
        Tag.TABLE,
        Tag.TR,
    )

    STYLE_TAGS = TEXT_ALIGN_TAGS + (
        Tag.A,
        Tag.B,
        Tag.STRONG,
        Tag.I,
        Tag.EM,
        Tag.U,
        Tag.MARK,
        Tag.SPAN,
        Tag.TD,
        Tag.TH,
    )


# --------------------------------------------------------------------------------------------------
# Text widget defs


class WCfg:
    KEY = "config"
    BACKGROUND = "background"
    FOREGROUND = "foreground"
    JUSTIFY = "justify"
    TABS = "tabs"


class Fnt:
    KEY = "font"
    FAMILY = "family"
    SIZE = "size"
    WEIGHT = "weight"
    SLANT = "slant"
    UNDERLINE = "underline"
    OVERSTRIKE = "overstrike"


class Bind:
    KEY = "bind"
    LINK = "link"
    IMAGE = "image"


class WTag:
    START_INDEX = "start_index"
    END_INDEX = "end_index"


DEFAULT_STACK = {
    WCfg.KEY: {
        WCfg.BACKGROUND: [],
        WCfg.FOREGROUND: [("__DEFAULT__", "black")],
        WCfg.JUSTIFY: [("__DEFAULT__", "left")],
        WCfg.TABS: [("__DEFAULT__", ())],
    },
    Fnt.KEY: {
        Fnt.FAMILY: [],
        Fnt.SIZE: [("__DEFAULT__", Defs.FONT_SIZE)],
        Fnt.WEIGHT: [("__DEFAULT__", "normal")],
        Fnt.SLANT: [("__DEFAULT__", "roman")],
        Fnt.UNDERLINE: [("__DEFAULT__", False)],
        Fnt.OVERSTRIKE: [("__DEFAULT__", False)],
    },
    Bind.KEY: {
        Bind.LINK: [("__DEFAULT__", None)],
    },
}


# __________________________________________________________________________________________________
# functions
def get_existing_font(font_families):
    # ------------------------------------------------------------------------------------------
    try:
        return next(
            filter(
                lambda f: f.lower() in (f.lower() for f in font.families()),
                font_families,
            )
        )
    except Exception:
        return "TkTextFont"


# __________________________________________________________________________________________________
# classes
class HLinkSlot:
    # ----------------------------------------------------------------------------------------------

    def __init__(self, w, tag_name, url):
        # ------------------------------------------------------------------------------------------
        self._w = w
        self.tag_name = tag_name
        self.URL = url

    def call(self, event):
        # ------------------------------------------------------------------------------------------
        webbrowser.open(self.URL)
        self._w.tag_config(self.tag_name, foreground="purple")

    def enter(self, event):
        # ------------------------------------------------------------------------------------------
        self._w.config(cursor="hand2")

    def leave(self, event):
        # ------------------------------------------------------------------------------------------
        self._w.config(cursor="")


class ListTag:
    # ----------------------------------------------------------------------------------------------
    def __init__(self, ordered: bool, list_type=None):
        # ------------------------------------------------------------------------------------------
        self.ordered = ordered
        self.type = list_type
        self.index = 0

    def add(self):
        # ------------------------------------------------------------------------------------------
        if self.ordered:
            self.index += 1

    def line_index(self):
        if not self.ordered:
            return chr(8226)
        if self.type == HTML.TypeOrderedList._1:
            return str(self.index)
        elif self.type == HTML.TypeOrderedList.a:
            return self._index_to_str(self.index).lower()
        elif self.type == HTML.TypeOrderedList.A:
            return self._index_to_str(self.index).upper()

    def _index_to_str(self, index):
        # ------------------------------------------------------------------------------------------
        prefix = ""
        if index > 26:
            prefix = self._index_to_str(index // 26)
            index = index % 26

        return prefix + chr(0x60 + index)


class HTMLTextParser(HTMLParser):
    # ----------------------------------------------------------------------------------------------

    def __init__(self):
        # ------------------------------------------------------------------------------------------
        super().__init__()
        # set list tabs
        self.cached_images = {}

        self.DEFAULT_TEXT_FONT_FAMILY = get_existing_font(Defs.DEFAULT_TEXT_FONT_FAMILY)
        self.PREFORMATTED_FONT_FAMILY = get_existing_font(Defs.PREFORMATTED_FONT_FAMILY)

    def _parse_attrs(self, attrs):
        # ------------------------------------------------------------------------------------------
        attrs_dict = {
            HTML.Attrs.STYLE: {},
            HTML.Attrs.HREF: None,
            HTML.Attrs.SRC: None,
            HTML.Attrs.WIDTH: None,
            HTML.Attrs.HEIGHT: None,
            HTML.Attrs.TYPE: None,
        }
        for k, v in attrs:
            k = k.lower()
            if k == HTML.Attrs.STYLE:
                for p in v.split(";"):
                    try:
                        p_key = p.split(":")[0].strip().lower()
                        p_value = p.split(":")[1].strip().lower()
                        attrs_dict[HTML.Attrs.STYLE][p_key] = p_value
                    except:
                        pass
            elif k in (
                HTML.Attrs.HREF,
                HTML.Attrs.SRC,
                HTML.Attrs.WIDTH,
                HTML.Attrs.HEIGHT,
                HTML.Attrs.TYPE,
            ):
                attrs_dict[k] = v
        return attrs_dict

    def _w_tags_add(self):
        # ------------------------------------------------------------------------------------------
        tag = {WCfg.KEY: {}, Fnt.KEY: {}, Bind.KEY: {}}

        for k1 in (WCfg.KEY, Fnt.KEY, Bind.KEY):
            for k2 in DEFAULT_STACK[k1]:
                tag[k1][k2] = self.stack[k1][k2][-1][1]

        self._w_tags[self._w.index("end-1c")] = tag

    def _stack_get_main_key(self, key):
        # ------------------------------------------------------------------------------------------
        if key in WCfg.__dict__.values():
            main_key = WCfg.KEY
        elif key in Fnt.__dict__.values():
            main_key = Fnt.KEY
        elif key in Bind.__dict__.values():
            main_key = Bind.KEY
        else:
            raise ValueError(f"key {key} doesn't exists")

        return main_key

    def _stack_add(self, tag, key, value=None):
        # ------------------------------------------------------------------------------------------
        main_key = self._stack_get_main_key(key)

        if value is None:
            # if value is none, add the previous value
            value = self.stack[main_key][key][-1][1]

        self.stack[main_key][key].append((tag, value))

    def _stack_index(self, tag, key):
        # ------------------------------------------------------------------------------------------
        main_key = self._stack_get_main_key(key)
        index = None
        for i, v in enumerate(self.stack[main_key][key]):
            if v[0] == tag:
                index = i

        return index

    def _stack_pop(self, tag, key):
        # ------------------------------------------------------------------------------------------
        main_key = self._stack_get_main_key(key)

        index = None
        if len(self.stack[main_key][key]) > 1:
            index = self._stack_index(tag, key)

        if index is not None:
            return self.stack[main_key][key].pop(index)[1]

    def _parse_styles(self, tag, attrs):
        # ------------------------------------------------------------------------------------------
        # -------------------------------------------------------------------------------- [ COLOR ]
        if HTML.Style.COLOR in attrs[HTML.Attrs.STYLE].keys():
            self._stack_add(
                tag, WCfg.FOREGROUND, attrs[HTML.Attrs.STYLE][HTML.Style.COLOR]
            )
        elif tag == HTML.Tag.A and attrs[HTML.Attrs.HREF]:
            self._stack_add(tag, WCfg.FOREGROUND, "blue")
        else:
            self._stack_add(tag, WCfg.FOREGROUND)

        # ---------------------------------------------------------------------- [ BACKGROUND_COLOR ]
        if HTML.Style.BACKGROUND_COLOR in attrs[HTML.Attrs.STYLE].keys():
            self._stack_add(
                tag,
                WCfg.BACKGROUND,
                attrs[HTML.Attrs.STYLE][HTML.Style.BACKGROUND_COLOR],
            )
        elif tag == HTML.Tag.MARK:
            self._stack_add(tag, WCfg.BACKGROUND, "yellow")
        else:
            self._stack_add(tag, WCfg.BACKGROUND)

        # -------------------------------------------------------------------------- [ FONT_FAMILY ]
        # font family
        if HTML.Style.FONT_FAMILY in attrs[HTML.Attrs.STYLE].keys():
            font_family = Defs.DEFAULT_TEXT_FONT_FAMILY
            for f in attrs[HTML.Attrs.STYLE][HTML.Style.FONT_FAMILY].split(","):
                f = f.strip()
                if f in map(lambda f: f.lower(), font.families()):
                    font_family = f
                    break
            self._stack_add(tag, Fnt.FAMILY, font_family)
        elif tag in (HTML.Tag.PRE, HTML.Tag.CODE):
            self._stack_add(tag, Fnt.FAMILY, self.PREFORMATTED_FONT_FAMILY)
        else:
            self._stack_add(tag, Fnt.FAMILY)

        # ---------------------------------------------------------------------------- [ FONT_SIZE ]
        if HTML.Style.FONT_SIZE in attrs[HTML.Attrs.STYLE].keys():
            size = Defs.FONT_SIZE
            if attrs[HTML.Attrs.STYLE][HTML.Style.FONT_SIZE].endswith("px"):
                if attrs[HTML.Attrs.STYLE][HTML.Style.FONT_SIZE][:-2].isdigit():
                    size = int(attrs[HTML.Attrs.STYLE][HTML.Style.FONT_SIZE][:-2])
            elif attrs[HTML.Attrs.STYLE][HTML.Style.FONT_SIZE].endswith(r"%"):
                if attrs[HTML.Attrs.STYLE][HTML.Style.FONT_SIZE][:-1].isdigit():
                    size = int(
                        (
                            int(attrs[HTML.Attrs.STYLE][HTML.Style.FONT_SIZE][:-1])
                            * Defs.FONT_SIZE
                        )
                        / 100
                    )
            self._stack_add(tag, Fnt.SIZE, size)
        elif tag.startswith("h") and len(tag) == 2:
            self._stack_add(tag, Fnt.SIZE, Defs.HEADINGS_FONT_SIZE[tag])
        else:
            self._stack_add(tag, Fnt.SIZE)

        # --------------------------------------------------------------------------- [ TEXT_ALIGN ]
        if (
            HTML.Style.TEXT_ALIGN in attrs[HTML.Attrs.STYLE].keys()
            and tag in HTML.TEXT_ALIGN_TAGS
        ):
            self._stack_add(
                tag, WCfg.JUSTIFY, attrs[HTML.Attrs.STYLE][HTML.Style.TEXT_ALIGN]
            )
        else:
            self._stack_add(tag, WCfg.JUSTIFY)

        # ---------------------------------------------------------------------- [ TEXT_DECORATION ]
        if HTML.Style.TEXT_DECORATION in attrs[HTML.Attrs.STYLE].keys():
            if tag == HTML.Tag.STRONG:
                self._stack_add(tag, Fnt.UNDERLINE, False)
                self._stack_add(tag, Fnt.OVERSTRIKE, False)
            elif (
                HTML.StyleTextDecoration.UNDERLINE
                in attrs[HTML.Attrs.STYLE][HTML.Style.TEXT_DECORATION]
            ):
                self._stack_add(tag, Fnt.UNDERLINE, True)
                self._stack_add(tag, Fnt.OVERSTRIKE, False)
            elif (
                HTML.StyleTextDecoration.LINE_THROUGH
                in attrs[HTML.Attrs.STYLE][HTML.Style.TEXT_DECORATION]
            ):
                self._stack_add(tag, Fnt.UNDERLINE, False)
                self._stack_add(tag, Fnt.OVERSTRIKE, True)
            else:
                self._stack_add(tag, Fnt.UNDERLINE)
                self._stack_add(tag, Fnt.OVERSTRIKE)
        elif tag == HTML.Tag.A and attrs[HTML.Attrs.HREF]:
            self._stack_add(tag, Fnt.UNDERLINE, True)
            self._stack_add(tag, Fnt.OVERSTRIKE, False)
        elif tag == HTML.Tag.U:
            self._stack_add(tag, Fnt.UNDERLINE, True)
            self._stack_add(tag, Fnt.OVERSTRIKE, False)
        else:
            self._stack_add(tag, Fnt.UNDERLINE)
            self._stack_add(tag, Fnt.OVERSTRIKE)

    def handle_starttag(self, tag, attrs):
        # ------------------------------------------------------------------------------------------
        tag = tag.lower()
        attrs = self._parse_attrs(attrs)

        if tag in HTML.STYLE_TAGS:
            # ---------------------------------------------------------------------- [ STYLED_TAGS ]
            self._parse_styles(tag, attrs)

            if tag in (HTML.Tag.B, HTML.Tag.STRONG) or tag in HTML.HEADING_TAGS:
                self._stack_add(tag, Fnt.WEIGHT, "bold")

            elif tag in (HTML.Tag.I, HTML.Tag.EM):
                self._stack_add(tag, Fnt.SLANT, "italic")

            elif tag == HTML.Tag.A:
                self._stack_add(tag, Bind.LINK, attrs[HTML.Attrs.HREF])

            elif tag == HTML.Tag.OL:
                # ---------------------------------------------------------------- [ ORDERED_LISTS ]
                if (
                    attrs[HTML.Attrs.TYPE]
                    and attrs[HTML.Attrs.TYPE] in HTML.TypeOrderedList.__dict__.values()
                ):
                    list_type = attrs[HTML.Attrs.TYPE]
                else:
                    list_type = HTML.TypeOrderedList._1
                self.list_tags.append(ListTag(ordered=True, list_type=list_type))

                tabs = []
                for i in range(len(self.list_tags)):
                    offset = 30 * (i + 1)
                    tabs += [offset, tk.RIGHT, offset + 5, tk.LEFT]
                self._stack_add(tag, WCfg.TABS, tabs)

            elif tag == HTML.Tag.UL:
                # -------------------------------------------------------------- [ UNORDERED_LISTS ]
                self.list_tags.append(ListTag(ordered=False))

                tabs = []
                for i in range(len(self.list_tags)):
                    offset = 30 * (i + 1)
                    tabs += [offset, tk.RIGHT, offset + 5, tk.LEFT]
                self._stack_add(tag, WCfg.TABS, tabs)

            elif tag == HTML.Tag.LI:
                level = len(self.list_tags)
                if level:
                    self.list_tags[-1].add()

                    if self.strip:
                        self._insert_new_line()

                    line_index = self.list_tags[-1].line_index()
                    if self.list_tags[-1].ordered:
                        line_index = "\t" + "\t\t" * (level - 1) + line_index + ".\t"
                    else:
                        line_index = "\t" + "\t\t" * (level - 1) + line_index + "\t"

                    self._stack_add(tag, Fnt.UNDERLINE, False)
                    self._stack_add(tag, Fnt.OVERSTRIKE, False)
                    self._w_tags_add()
                    self._w.insert(tk.INSERT, line_index)
                    self._stack_pop(tag, Fnt.UNDERLINE)
                    self._stack_pop(tag, Fnt.OVERSTRIKE)

            elif tag in (HTML.Tag.TH, HTML.Tag.TD):
                    self._w.insert(tk.INSERT, "\t")

        elif tag == HTML.Tag.IMG and attrs[HTML.Attrs.SRC]:
            # -------------------------------------------------------------------- [ UNSTYLED_TAGS ]
            image = None
            # print(attrs[HTML.Attrs.SRC] , self.cached_images)
            if attrs[HTML.Attrs.SRC].startswith(("https://", "ftp://", "http://")):
                if attrs[HTML.Attrs.SRC] in self.cached_images.keys():
                    image = deepcopy(self.cached_images[attrs[HTML.Attrs.SRC]])
                else:
                    try:
                        image = Image.open(
                            BytesIO(requests.get(attrs[HTML.Attrs.SRC]).content)
                        )
                        self.cached_images[attrs[HTML.Attrs.SRC]] = deepcopy(image)
                    except:
                        pass

            if attrs[HTML.Attrs.SRC] in self.cached_images.keys():
                image = deepcopy(self.cached_images[attrs[HTML.Attrs.SRC]])
            elif os.path.exists(attrs[HTML.Attrs.SRC]):
                image = Image.open(attrs[HTML.Attrs.SRC])
                self.cached_images[attrs[HTML.Attrs.SRC]] = deepcopy(image)
            if image:
                width = image.size[0]
                height = image.size[1]
                resize = False
                if str(attrs[HTML.Attrs.WIDTH]).isdigit():
                    width = int(attrs[HTML.Attrs.WIDTH])
                    resize = True
                if str(attrs[HTML.Attrs.HEIGHT]).isdigit():
                    height = int(attrs[HTML.Attrs.HEIGHT])
                    resize = True
                if resize:
                    image = image.resize((width, height), Image.ANTIALIAS)
                self.images.append(ImageTk.PhotoImage(image))
                self._w.image_create(tk.INSERT, image=self.images[-1])

        elif tag == HTML.Tag.TABLE:
                tabs = []
                for i in range(30): # HF was len(self.list_tags)):
                    offset = 40 * (i + 1)
                    tabs += [offset, tk.LEFT ]
                self._stack_add(tag, WCfg.TABS, tabs)

        if self.strip:
            if tag == HTML.Tag.BR:
                self._insert_new_line()
            else:
                self.html_tags.append(tag)

        if (
            tag in HTML.NEW_LINE_TAGS
            and self.strip
            and self._w.index("end-1c") != "1.0"
        ):
            if tag in (HTML.Tag.DIV,):
                self._insert_new_line()
            elif tag in (HTML.Tag.UL, HTML.Tag.OL):
                if len(self.list_tags) == 1:
                    self._insert_new_line(double=True)
                else:
                    self._insert_new_line(double=False)
            else:
                self._insert_new_line(double=True)

        self._w_tags_add()

    def handle_charref(self, data):
        # ------------------------------------------------------------------------------------------
        try:
            char = chr(int(data))
            self._w.insert(tk.INSERT, char)
        except:
            pass

    def _insert_new_line(self, double=False):
        # ------------------------------------------------------------------------------------------
        self._remove_last_space()
        if self._w.get("end-3c", "end-1c") == "\n\n":
            pass
        elif self._w.get("end-2c", "end-1c") == "\n":
            if double:
                self._w.insert(tk.INSERT, "\n")
        elif double:
            self._w.insert(tk.INSERT, "\n\n")
        else:
            self._w.insert(tk.INSERT, "\n")

    def _text_rstrip(self):
        # ------------------------------------------------------------------------------------------
        for _ in range(3):
            if self._w.get("end-2c", "end-1c") in (" ", "\n"):
                self._w.delete("end-2c", "end-1c")

    def _remove_last_space(self):
        # ------------------------------------------------------------------------------------------
        if self._w.get("end-2c", "end-1c") == " ":
            self._w.delete("end-2c", "end-1c")

    def _remove_multi_spaces(self, data):
        # ------------------------------------------------------------------------------------------
        data = data.replace("  ", " ")
        if "  " in data:
            data = self._remove_multi_spaces(data)
        return data

    def handle_data(self, data):
        if HTML.Tag.PRE in self.html_tags:
            pass
        elif not data.strip():
            if self.strip:
                data = ""
        elif self.strip:
            # left strip
            if self._w.index("end-1c").endswith(".0"):
                data = data.lstrip()
            elif self._w.get("end-2c", "end-1c") == " ":
                data = data.lstrip()

            data = data.replace("\n", " ").replace("\t", " ")
            data = f"{data}" # FIXME: attaching a space in blind is wrong - SPACE REMOVED
            data = self._remove_multi_spaces(data)
            if len(self.html_tags) and self.html_tags[-1] in (
                HTML.Tag.UL,
                HTML.Tag.OL,
            ):
                self._w.insert(tk.INSERT, "\t" * 2 * len(self.list_tags))

        self._w.insert(tk.INSERT, data)

    def handle_endtag(self, tag):
        # ------------------------------------------------------------------------------------------
        tag = tag.lower()

        try:
            index = len(self.html_tags) - self.html_tags[::-1].index(tag) - 1
            self.html_tags.pop(index)
        except:
            pass

        if tag in HTML.STYLE_TAGS:
            self._stack_pop(tag, WCfg.FOREGROUND)
            self._stack_pop(tag, WCfg.BACKGROUND)
            self._stack_pop(tag, WCfg.JUSTIFY)
            self._stack_pop(tag, Fnt.FAMILY)
            self._stack_pop(tag, Fnt.SIZE)
            self._stack_pop(tag, Fnt.UNDERLINE)
            self._stack_pop(tag, Fnt.OVERSTRIKE)

            if tag == HTML.Tag.B or tag == HTML.Tag.STRONG or tag in HTML.HEADING_TAGS:
                self._stack_pop(tag, Fnt.WEIGHT)

            elif tag in (HTML.Tag.I, HTML.Tag.EM):
                self._stack_pop(tag, Fnt.SLANT)

            elif tag == HTML.Tag.A:
                self._stack_pop(tag, Bind.LINK)

            elif tag in (HTML.Tag.OL, HTML.Tag.UL):
                if len(self.list_tags):
                    self.list_tags = self.list_tags[:-1]

                self._stack_pop(tag, WCfg.TABS)

        if tag in HTML.NEW_LINE_TAGS and self.strip:
            self._insert_new_line()

        self._w_tags_add()

        if tag in HTML.NEW_LINE_TAGS and self.strip:
            if tag in (HTML.Tag.DIV, HTML.Tag.UL, HTML.Tag.OL):
                if not len(self.list_tags):
                    self._insert_new_line(double=True)
            else:
                self._insert_new_line(double=True)

    def _w_tags_apply_all(self):
        # ------------------------------------------------------------------------------------------
        # update indexes
        if self.strip:
            self._text_rstrip()
        end_index = tk.END
        for key, tag in reversed(tuple(self._w_tags.items())):
            tag[WTag.START_INDEX] = key
            tag[WTag.END_INDEX] = end_index
            end_index = key

        # add tags
        self.hlink_slots = []
        for key, tag in self._w_tags.items():
            if "config" in tag: # HF change justify to left for tkinter (only supports left, right, center)
                if tag["config"].get("justify") == "justify":
                    tag["config"]["justify"] = "left"
            self._w.tag_add(key, tag[WTag.START_INDEX], tag[WTag.END_INDEX])
            self._w.tag_config(key, font=font.Font(**tag[Fnt.KEY]), **tag[WCfg.KEY])
            if tag[Bind.KEY][Bind.LINK]:
                self.hlink_slots.append(
                    HLinkSlot(self._w, key, tag[Bind.KEY][Bind.LINK])
                )
                self._w.tag_bind(key, "<Button-1>", self.hlink_slots[-1].call)
                self._w.tag_bind(key, "<Leave>", self.hlink_slots[-1].leave)
                self._w.tag_bind(key, "<Enter>", self.hlink_slots[-1].enter)

    def w_set_html(self, w, html, strip):
        # ------------------------------------------------------------------------------------------
        self._w = w
        self.stack = deepcopy(DEFAULT_STACK)
        self.stack[WCfg.KEY][WCfg.BACKGROUND].append(
            ("__DEFAULT__", self._w.cget("background"))
        )
        self.stack[Fnt.KEY][Fnt.FAMILY].append(
            ("__DEFAULT__", self.DEFAULT_TEXT_FONT_FAMILY)
        )
        self._w_tags = OrderedDict()
        self.html_tags = []
        self.images = []
        self.list_tags = []
        self.strip = strip
        self._w_tags_add()
        self.feed(html)
        self._w_tags_apply_all()
        del self._w
