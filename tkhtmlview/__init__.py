"""
tkinter HTML text widgets
"""
import sys
import tkinter as tk
from tkhtmlview import html_parser
from tkhtmlview.utils import RenderHTML

VERSION = "0.3.1"


class _ScrolledText(tk.Text):
    def __init__(self, master=None, **kw):
        self.frame = tk.Frame(master)

        self.vbar = tk.Scrollbar(self.frame)
        self.xscroll = tk.Scrollbar(self.frame, orient="horizontal")

        if "xscroll" in kw:
            # self.vbar.orient = "vertical"
            # print("vs")
            kw["xscrollcommand"] = self.xscroll.set
            self.xscroll.pack(side=tk.BOTTOM, fill="x")
            self.xscroll["command"] = self.xview
            del kw["xscroll"]

        kw["yscrollcommand"] = self.vbar.set
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.vbar["command"] = self.yview

        tk.Text.__init__(self, self.frame, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)


class HTMLScrolledText(_ScrolledText):

    """
    HTML scrolled text widget
    """

    def __init__(self, *args, html=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._w_init(kwargs)
        self.html_parser = html_parser.HTMLTextParser()
        if isinstance(html, str):
            self.set_html(html)
        elif isinstance(html, RenderHTML):
            self.set_html(html.get_html())

    def _w_init(self, kwargs):
        if "wrap" not in kwargs.keys():
            self.config(wrap="word")
        if "background" not in kwargs.keys():
            if sys.platform.startswith("win"):
                self.config(background="SystemWindow")
            else:
                self.config(background="white")

    def fit_height(self):
        """
        Fit widget height to wrapped lines
        """
        for h in range(1, 4):
            self.config(height=h)
            self.master.update()
            if self.yview()[1] >= 1:
                break
        else:
            self.config(height=0.5 + 3 / self.yview()[1])

    def set_html(self, html, strip=True):
        """
        Set HTML widget text. If strip is enabled (default) it ignores spaces and new lines.
        """
        prev_state = self.cget("state")
        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        for tag in self.tag_names():
            self.tag_delete(tag)

        self.html_parser.w_set_html(self, html, strip=strip)
        self.config(state=prev_state)


class HTMLText(HTMLScrolledText):

    """
    HTML text widget
    """

    def _w_init(self, kwargs):
        super()._w_init(kwargs)
        self.vbar.pack_forget()

    def fit_height(self):
        super().fit_height()
        # self.master.update()
        self.vbar.pack_forget()


class HTMLLabel(HTMLText):

    """
    HTML label widget
    """

    def _w_init(self, kwargs):
        super()._w_init(kwargs)
        if "background" not in kwargs.keys():
            if sys.platform.startswith("win"):
                self.config(background="SystemButtonFace")
            else:
                self.config(background="#d9d9d9")

        if "borderwidth" not in kwargs.keys():
            self.config(borderwidth=0)

        if "padx" not in kwargs.keys():
            self.config(padx=3)

    def set_html(self, *args, **kwargs):
        super().set_html(*args, **kwargs)
        self.config(state=tk.DISABLED)
