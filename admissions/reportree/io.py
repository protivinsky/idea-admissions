import os
from abc import ABC, abstractmethod
from matplotlib.figure import Figure
import re
import unicodedata
from yattag import indent


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)


class IWriter(ABC):
    """IWriter saves an HTML page or a matplotlib figure to a given path. Can be subclassed to allow
    for storing the reports in distributed storages such as on AWS or GCP.
    """

    @staticmethod
    @abstractmethod
    def write_text(path: str, text: str):
        ...

    @staticmethod
    @abstractmethod
    def write_figure(path: str, figure: Figure):
        ...


class LocalWriter(IWriter):
    """Default writer that stores pages and images only locally."""

    @staticmethod
    def write_text(path: str, text: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    @staticmethod
    def write_figure(path: str, figure: Figure):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        figure.savefig(path)


class InjectWriter(IWriter):
    """Writer that injects a certain text before a provided pattern in the resulting HTML. Handy for including custom
    CSS styles, google fonts or other content into head.
    """

    _pattern = "</head>"
    _value = ""
    _writer = LocalWriter

    def __init__(self, pattern=_pattern, value=_value, writer=_writer):
        self.pattern = pattern
        self.value = value
        self.writer = writer

    def write_text(self, path: str, text: str):
        text = text.replace(self.pattern, self.value + self.pattern)
        text = indent(text)
        self.writer.write_text(path, text)

    def write_figure(self, path: str, figure: Figure):
        self.writer.write_figure(path, figure)
