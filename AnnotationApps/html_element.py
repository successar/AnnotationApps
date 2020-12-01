print("Running html")
import AnnotationApps.dbserver.api as dbapi
from AnnotationApps.dbserver.models import create_table, exist_table
import json


def create_table_from_info(tablename, info_dict, value):
    if not exist_table(tablename):
        columns = {k: type(v) for k, v in info_dict.items()}
        columns["value"] = type(value)
        create_table(tablename, columns)


class Page:
    def __init__(self, common_dict):
        self._elements = []
        self._common_dict = common_dict

        data_string = " ".join(
            [f'data-{key}="{value}"' for key, value in common_dict.items()]
        )
        common_block = f'<div data-type="common" {data_string}></div>'
        self._elements.append(common_block)

        self._add_saving_group()

    def html(self):
        return " ".join(self._elements)

    def _block(self, html):
        return f'<div class="row mt-3"><div class="col">{html}</div></div>'

    def add(self, widget):
        self._elements.append(self._block(widget.construct(self._common_dict)))

    def _button(self, label: str, _id: str, _type: str = "primary"):
        return (
            f'<button type="button" class="btn btn-{_type}" id="{_id}">{label}</button>'
        )

    def _add_saving_group(self):
        self._elements.append(
            f"""
            <div class="btn-group" role="group">
                {self._button("Save And Next", "savenext", "success")}
                {self._button("Save", "save", "primary")}
            </div>
            """
        )


class Widget:
    _html = ""

    def construct(self, info_dict):
        return self._html


class HorizontalLine(Widget):
    _html = "<hr>"


class LineBreak(Widget):
    _html = "<br>"


class Checkbox(Widget):
    def __init__(self, label, tablename, info_dict):
        self._label = label
        self._tablename = tablename
        self._info_dict = info_dict

    def construct(self, info_dict):
        combined_info_dict = {**info_dict, **self._info_dict}
        create_table_from_info(self._tablename, combined_info_dict, value=0)
        value = dbapi.get_value(tablename=self._tablename, keys=combined_info_dict)
        checked = "checked" if value is not None else ""
        data_string = " ".join(
            [f'data-{key}="{value}"' for key, value in self._info_dict.items()]
        )
        return f"""
            <div class="form-check">
                <label class="form-check-label">
                    <input class="form-check-input db" type="checkbox" data-tablename=\"{self._tablename}\" {data_string} {checked}>
                    {self._label}
                </label>
            </div>
            """


class Textbox(Widget):
    def __init__(self, label, tablename, info_dict):
        self._label = label
        self._tablename = tablename
        self._info_dict = info_dict

    def construct(self, info_dict):
        combined_info_dict = {**info_dict, **self._info_dict}
        create_table_from_info(self._tablename, combined_info_dict, value="")
        value = (
            dbapi.get_value(tablename=self._tablename, keys=combined_info_dict) or ""
        )
        data_string = " ".join(
            [f'data-{key}="{value}"' for key, value in self._info_dict.items()]
        )
        return f"""
            <label class="form-label">
                {self._label} <input type="text" class="form-control db" data-tablename=\"{self._tablename}\" {data_string} value=\"{value}\">
            </label>
            """


class Choice(Widget):
    def __init__(self, label, options, tablename, info_dict):
        self._label = label
        self._tablename = tablename
        self._info_dict = info_dict
        self._options = options

    def construct(self, info_dict):
        combined_info_dict = {**info_dict, **self._info_dict}
        create_table_from_info(self._tablename, combined_info_dict, value="")
        value = dbapi.get_value(tablename=self._tablename, keys=combined_info_dict)
        data_string = " ".join(
            [f'data-{key}="{value}"' for key, value in self._info_dict.items()]
        )

        return (
            f"""
            <label class="form-label"> {self._label}
                <select class="form-control db" data-tablename=\"{self._tablename}\" {data_string}>
            """
            + "\n".join(
                [
                    f'<option value="{option}" {"selected" if option == value else ""}>{option}</option>'
                    for option in self._options
                ]
            )
            + """
                </select>
            </label>
            """
        )


class Text(Widget):
    def __init__(self, text, classes, info_dict=None):
        self._text = text
        self._classes = classes
        self._info_dict = info_dict

    def construct(self, info_dict=None):
        data_string = ""
        classes = " ".join(self._classes)
        if self._info_dict is not None:
            data_string = " ".join(
                [f'data-{key}="{value}"' for key, value in self._info_dict.items()]
            )

        return f'<span class="{classes}" {data_string}>{self._text}</span>'


class TextBlock(Widget):
    def __init__(self, words):
        self._words = words

    def construct(self, info_dict=None):
        return " ".join([word.construct() for word in self._words])


class HighlightableText(Text):
    def construct(self, is_highlighted):
        self._classes = self._classes + ["highlightable"]
        if is_highlighted:
            self._classes = self._classes + ["rationale"]

        return super().construct()


class HighlightableTextBlock(Widget):
    def __init__(self, words, tablename, info_dict):
        self._words = words
        self._tablename = tablename
        self._info_dict = info_dict

    def construct(self, info_dict):
        combined_info_dict = {**info_dict, **self._info_dict}
        create_table_from_info(self._tablename, combined_info_dict, value="")

        value = dbapi.get_value(tablename=self._tablename, keys=combined_info_dict)
        if value is not None:
            value = json.loads(value)
        else:
            value = []

        words = [
            word.construct(is_highlighted=word._info_dict in value)
            for word in self._words
        ]
        html = " ".join(words)
        data_string = " ".join(
            [f'data-{key}="{value}"' for key, value in self._info_dict.items()]
        )
        return f'<div class="highlight" data-tablename="{self._tablename}" {data_string}>{html}</div>'

