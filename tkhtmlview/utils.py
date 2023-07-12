import os


class RenderHTML:
    def __init__(self, file, encoding = "utf-8"):
        self._file = file
        if not os.path.exists(self._file):
            raise FileNotFoundError(f"No such HTML file: {self._file}")

        with open(file, "r", encoding=encoding) as f:
            self._html = f.read()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self._file}>"

    def get_html(self):
        return str(self._html)

    __str__ = get_html
