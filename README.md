# tkhtmlview
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbauripalash%2Ftkhtmlview.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbauripalash%2Ftkhtmlview?ref=badge_shield)

HTML widgets for tkinter

> Fork of [tk_html_widgets](https://github.com/paolo-gurisatti/tk_html_widgets)

## Overview
This module is a collection of tkinter widgets whose text can be set in HTML format.
A HTML widget isn't a web browser frame, it's only a simple and lightweight HTML parser that formats the tags used by the tkinter Text base class.
The widgets behaviour is similar to the PyQt5 text widgets (see the [PyQt5 HTML markup subset](http://doc.qt.io/qt-5/richtext-html-subset.html)).

## Installation
``pip install tkhtmlview``
 
## Requirements
 - [Python 3.4 or later](https://www.python.org/downloads/) with tcl/tk support
 - [Pillow 5.3.0](https://github.com/python-pillow/Pillow)
 - requests

## Example
```python
import tkinter as tk
from tkhtmlview import HTMLLabel

root = tk.Tk()
html_label = HTMLLabel(root, html='<h1 style="color: red; text-align: center"> Hello World </H1>')
html_label.pack(fill="both", expand=True)
html_label.fit_height()
root.mainloop()
```

## Documentation

### Classes:
All widget classes inherits from the tkinter.Text() base class.

#### class HTMLScrolledText(tkinter.Text)
> Text-box widget with vertical scrollbar
#### class HTMLText(tkinter.Text)
> Text-box widget without vertical scrollbar
#### class HTMLLabel(tkinter.Text)
> Text-box widget with label appereance
 
### Methods:
#### def set_html(self, html, strip=True):
> **Description:** Sets the text in HTML format. <br>
> **Args:**
>  - *html*: input HTML string
>  - *strip*: if True (default) handles spaces in HTML-like style 

#### def fit_height(self):
> **Description:** Fit widget height in order to display all wrapped lines

### HTML support:
Only a subset of the whole HTML tags and attributes are supported (see table below).
Where is possibile, I hope to add more HTML support in the next releases.

 **Tags** | **Attributes**  | **Notes** 
--- | --- | ---
a| style, href | 
b| style | 
br|| 
code | style | 
div | style | 
em| style | 
h1 | style | 
h2 | style | 
h3 | style | 
h4 | style | 
h5 | style | 
h6 | style | 
i| style | 
img| src, width, height | experimental support for remote images
li| style | 
mark| style | 
ol| style, type | 1, a, A list types only
p | style | 
pre | style | 
span| style | 
strong| style | 
u| style | 
ul| style | bullet glyphs only




## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fbauripalash%2Ftkhtmlview.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fbauripalash%2Ftkhtmlview?ref=badge_large)