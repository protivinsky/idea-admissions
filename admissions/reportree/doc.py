from __future__ import annotations
import os
import io
import importlib
import base64
import json
from typing import Optional, Callable
import yattag as yt
import sass
import markdown
import numpy as np
import pandas as pd
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import seaborn as sns
from .generic_tree import GenericTree
from .html_parts import css_base, js_doc_tree_script
from .io import LocalWriter, IWriter


def _fig_to_image_data(fig: Figure, format="png"):
    image = io.BytesIO()
    fig.savefig(image, format=format)
    return base64.encodebytes(image.getvalue()).decode("utf-8")


def _idx_str(idx):
    return "".join([f"_{i + 1}" for i in idx])


class Switcher(GenericTree):
    """A tree of Docs. Provides the button and javascript to switch between the leaf pages."""

    _javascript = None

    @classmethod
    def get_javascript(cls):
        # TODO: turn into a proper package asset later
        if cls._javascript is None:
            with open(
                os.path.join(os.path.dirname(__file__), "assets", "switcher.js"), "r"
            ) as file:
                cls._javascript = file.read()
        return cls._javascript

    def collector(self, f_node, f_leaf, _idx=()):
        if self.is_leaf():
            return f_leaf(self.get_value(), _idx)

        collected_children = []
        for i, v in enumerate(self.values()):
            next_idx = (*_idx, i)
            collected_children.append(v.collector(f_node, f_leaf, next_idx))

        return f_node(self, _idx, collected_children)

    def to_hierarchy(self):
        def hierarchy_f_leaf(_, idx):
            return {"id": "page" + _idx_str(idx), "firstChildId": None, "children": {}}

        def hierarchy_f_node(_, idx, children):
            mapped_children = {
                "btn" + _idx_str(idx) + "_" + str(i + 1): ch
                for i, ch in enumerate(children)
            }
            if not idx:
                return mapped_children
            return {
                "id": "page" + _idx_str(idx),
                "firstChildId": "page" + _idx_str(idx) + "_1",
                "children": mapped_children,
            }

        return self.collector(hierarchy_f_node, hierarchy_f_leaf)

    def to_buttons(self):
        def buttons_f_leaf(v, _):
            return v

        def buttons_f_node(n, idx, children):
            doc = Doc()
            for i, k in enumerate(n.keys()):
                doc.line("button", k, id="btn" + _idx_str(idx) + "_" + str(i + 1))
            doc.stag("br")
            doc.stag("br")
            for i, (k, v) in enumerate(zip(n.keys(), children)):
                with doc.tag(
                    "div", id="page" + _idx_str(idx) + "_" + str(i + 1), klass="content"
                ):
                    # doc.line("h" + str(min(4, len(idx) + 2)), k)
                    doc.asis(v.getvalue())
            return doc

        return self.collector(buttons_f_node, buttons_f_leaf)


class Doc(yt.Doc):
    _base_style = None
    _cdn = [
        # bootstrap icons
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css",
        # milligram
        # "https://fonts.googleapis.com/css?family=Roboto:300,300italic,700,700italic",
        # "https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css",
        # "https://cdnjs.cloudflare.com/ajax/libs/milligram/1.4.1/milligram.css",
        # skeleton
        # "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.css",
        # picnic
        # "https://cdn.jsdelivr.net/npm/picnic",
    ]

    @classmethod
    def get_base_style(cls):
        # TODO: turn into a proper package asset later
        if cls._base_style is None:
            with open(
                os.path.join(os.path.dirname(__file__), "assets", "style.scss"), "r"
            ) as file:
                cls._base_style = file.read()
        return cls._base_style

    def __init__(self, *args, **kwargs):
        self._wrap_kwargs = {}
        if "max_width" in kwargs:
            self._wrap_kwargs["max_width"] = kwargs.pop("max_width")
        if "title" in kwargs:
            self._wrap_kwargs["title"] = kwargs.pop("title")
        super().__init__(*args, **kwargs)
        self._has_switcher = False

    def wrap_to_page(self, head_doc: Optional[yt.Doc] = None, **kwargs):
        """Wrap the content of the document into a full HTML page.

        Args:
            title: Title of the page.
            head_doc: Document containing the content of the `head` tag.
        """
        kwargs = {**self._wrap_kwargs, **kwargs}
        body_klass = "container" if "max_width" in kwargs else "container full-width"
        sass_content = f"""
        $max_width: {kwargs.pop("max_width") if "max_width" in kwargs else 1900}px;

        {Doc.get_base_style()}
        """
        css_style = sass.compile(string=sass_content)
        title = kwargs.pop("title", "ReporTree Doc")

        doc = Doc()
        doc.asis("<!DOCTYPE html>")
        with doc.tag("html"):
            with doc.tag("head"):
                doc.stag("meta", charset="UTF-8")
                doc.line("title", title)
                with doc.tag("style"):
                    doc.asis(css_style)
                for cdn in self._cdn:
                    doc.stag("link", rel="stylesheet", href=cdn)
                doc.stag(
                    "link",
                    rel="stylesheet",
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                    integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
                    crossorigin="anonymous",
                )
            with doc.tag("body", klass=body_klass):
                doc.asis(self.getvalue())
        return doc

    def md(self, md):
        self.asis(markdown.markdown(md))
        return self

    def figure_as_b64(self, fig, format="png", **kwargs):
        fig = fig.get_figure() if isinstance(fig, Axes) else fig
        self.stag(
            "image",
            src=f"data:image/{format};base64,{_fig_to_image_data(fig, format=format)}",
            **kwargs,
        )
        return self

    def figures(self, figs, **kwargs):
        figs = figs if isinstance(figs, list) else [figs]
        with self.tag("div", klass="figures"):
            for fig in figs:
                self.figure_as_b64(fig, **kwargs)
        return self

    def switcher(self, switch: Switcher):
        if self._has_switcher:
            raise ValueError("Only one switcher is allowed per document.")

        self._has_switcher = True
        self.asis(switch.to_buttons().getvalue())
        hierarchy = (
            json.dumps(switch.to_hierarchy(), indent=2)
            .replace('  "', "  ")
            .replace('":', ":")
        )
        with self.tag("script"):
            self.asis("\n")
            self.asis("var buttonHierarchy = " + hierarchy + ";")
            self.asis("\n")
            self.asis(Switcher.get_javascript())
            self.asis("\n")

        return self

    def toggle_width(self):
        with self.tag("div"):
            self.line(
                "button", "Toggle width", id="toggleButton", klass="switcher-button"
            )
            with self.tag("script"):
                self.asis(
                    """
                    const toggleButton = document.getElementById('toggleButton');
                    const container = document.querySelector('.container');

                    toggleButton.addEventListener('click', () => {
                      container.classList.toggle('full-width');
                    });
                """
                )

    def color_table(
        self,
        table,
        minmax=None,
        shared=True,
        cmap="RdYlGn",
        n_bins=51,
        eps=1e-8,
        formatter=None,
        label_width=None,
    ):
        if shared:
            if minmax is None:
                minmax = (table.min().min(), table.max().max())
                minmax = (
                    1.5 * minmax[0] - 0.5 * minmax[1],
                    1.5 * minmax[1] - 0.5 * minmax[0],
                )
            bins = (
                [-np.inf]
                + list(np.linspace(minmax[0] - eps, minmax[1] + eps, n_bins - 2)[1:-1])
                + [np.inf]
            )

        if not isinstance(cmap, list):
            cmap = sns.color_palette(cmap, n_colors=n_bins).as_hex()

        with self.tag("table", klass="color_table"):
            with self.tag("thead"):
                with self.tag("tr"):
                    self.line("th", "")
                    for c in table.columns:
                        self.line("th", c)
            with self.tag("tbody"):
                for i, row in table.iterrows():
                    if not shared:
                        minmax = (row.min(), row.max())
                        minmax = (
                            1.5 * minmax[0] - 0.5 * minmax[1],
                            1.5 * minmax[1] - 0.5 * minmax[0],
                        )
                        bins = (
                            [-np.inf]
                            + list(
                                np.linspace(
                                    minmax[0] - eps, minmax[1] + eps, n_bins - 2
                                )[1:-1]
                            )
                            + [np.inf]
                        )

                    cidx = pd.cut(row, bins, labels=False)

                    with self.tag("tr"):
                        if label_width is not None:
                            self.line(
                                "td", i, klass="row_label", width=f"{label_width}px"
                            )
                        else:
                            self.line("td", i, klass="row_label")
                        for r, ci in zip(row, cidx):
                            if formatter is not None:
                                if isinstance(formatter, Callable):
                                    r = formatter(r)
                                else:
                                    r = formatter.format(r)
                            elif isinstance(r, float):
                                r = f"{r:.3g}"
                            self.line("td", r, bgcolor=cmap[ci])

        return self

    def save(
        self,
        path: str,
        writer: IWriter = LocalWriter,
        entry: str = "index.html",
        **kwargs,
    ):
        value = self.getvalue()

        # If it does not seem valid html - is it sane?
        if not (
            value[:100].lower().strip().startswith("<!doctype")
            or value[:100].lower().strip().startswith("<html")
        ):
            value = self.wrap_to_page(**kwargs).getvalue()

        content = yt.indent(value)
        writer.write_text(os.path.join(path, entry), content)
        return os.path.join(path, entry)
