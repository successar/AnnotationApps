print("Running html")
import AnnotationApps.dbserver.api as dbapi
from AnnotationApps.dbserver.models import create_table, exist_table
import json
from typing import Dict, List
from secrets import token_hex


def create_table_from_info(tablename, info_dict, value):
    if not exist_table(tablename):
        columns = {k: type(v) for k, v in info_dict.items()}
        columns["value"] = type(value)
        create_table(tablename, columns)


class Page:
    def __init__(self, common_dict):
        self._elements = []
        self._common_dict = common_dict
        self._css = {}

        data_string = " ".join([f'data-{key}="{value}"' for key, value in common_dict.items()])
        common_block = f'<div data-type="common" {data_string}></div>'
        self._elements.append(common_block)

        self._add_saving_group()

    def add_format(self, label: str, format: Dict[str, str]):
        self._css[label] = "{\n" + "\n".join(f"{k}: {v};" for k, v in format.items()) + "\n}"

    def html(self):
        return " ".join(self._elements)

    def css(self):
        return "\n".join([f".{k} {v}\n" for k, v in self._css.items()])

    @staticmethod
    def _block(html):
        return f'<div class="row mt-3"><div class="col">{html}</div></div>'

    def add(self, widget):
        self._elements.append(self._block(widget.construct(self._common_dict)))

    @staticmethod
    def _button(label: str, _id: str, _type: str = "primary"):
        return f'<button type="button" class="btn btn-{_type}" id="{_id}">{label}</button>'

    def _add_saving_group(self):
        self._elements.append(
            f"""
            <div class="btn-group" role="group">
                {self._button("Save And Next", "savenext", "success")}
                {self._button("Save", "save", "primary")}
            </div>
            """
        )

    def __hash__(self):
        return hash(self.html())


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
        data_string = " ".join([f'data-{key}="{value}"' for key, value in self._info_dict.items()])
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
        value = dbapi.get_value(tablename=self._tablename, keys=combined_info_dict) or ""
        data_string = " ".join([f'data-{key}="{value}"' for key, value in self._info_dict.items()])
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
        data_string = " ".join([f'data-{key}="{value}"' for key, value in self._info_dict.items()])

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
    def __init__(self, text, classes=None, info_dict=None):
        self._text = text
        self._classes = classes
        self._info_dict = info_dict

    def construct(self, info_dict=None):
        data_string = ""
        classes = " ".join(self._classes) if self._classes is not None else ""
        if self._info_dict is not None:
            data_string = " ".join([f'data-{key}="{value}"' for key, value in self._info_dict.items()])

        return f'<span class="{classes}" {data_string}>{self._text}</span>'


class TextBlock(Widget):
    def __init__(self, words):
        self._words = words

    def construct(self, info_dict=None):
        return " ".join([word.construct() for word in self._words])


class TypedTextBlock(Widget):
    def __init__(self, words, tablename, info_dict, entity_labels, relation_labels=None):
        self._words = words
        self._tablename = tablename
        self._info_dict = info_dict
        self._entity_labels = entity_labels
        self._relation_labels = relation_labels
        self._random_id = "typed-" + token_hex(10)

    def create_label_selector(self):
        buttons = "\n".join(
            [
                f"""<input type=\"radio\" class=\"btn-check\" name=\"{self._random_id}\" id=\"{self._random_id}-{e}\" autocomplete=\"off\" value=\"{e}\"> 
                <label class=\"btn btn-outline-primary\" for=\"{self._random_id}-{e}\">{e}</label>"""
                for e in self._entity_labels
            ]
        )
        return f"""
        <div class="btn-group" role="group" data-type="type-selector" data-radio-id="{self._random_id}">
            {buttons}
        </div><br>
        """

    def construct(self, info_dict):
        combined_info_dict = {**info_dict, **self._info_dict}
        create_table_from_info(self._tablename, combined_info_dict, value="")

        value = dbapi.get_value(tablename=self._tablename, keys=combined_info_dict)
        if value is not None:
            value = json.loads(value)
        else:
            value = []

        for position, word in enumerate(self._words) :
            word._classes = ["highlightable"] + (word._classes or [])
            word._info_dict["block_pos"] = position

        words = [word.construct() for word in self._words]

        marked_words = []
        start = 0
        for span in value :
            span_type = span["span-type"]
            span_start = span["span-start"]
            span_end = span["span-end"]

            marked_words += words[start:span_start]
            marked_words.append(f"<mark data-span-type=\"{span_type}\" data-span-start={span_start} data-span-end={span_end}>")
            marked_words += words[span_start:span_end]
            marked_words.append("</mark>")

            start = span_end 

        marked_words += words[start:]


        html = " ".join(marked_words)
        data_string = " ".join([f'data-{key}="{value}"' for key, value in self._info_dict.items()])
        return f'''
            <div class="highlight" data-tablename="{self._tablename}" {data_string}>
                {self.create_label_selector()} 
                {html}
                <div data-type="relation-area"></div>
            </div>
            '''


class Table(Widget):
    def __init__(self, data=None) :
        if data is not None:
            self._data = data
        else :
            self._data = []

    def add_row(self, cells, rowspans=None, colspans=None) :
        if rowspans is None :
            rowspans = [None] * len(cells)

        if colspans is None :
            colspans = [None] * len(cells)

        self._data.append(list(zip(cells, rowspans, colspans)))

    def construct(self, info_dict) :
        html = []
        html.append("<table class=\"table table-borderless align-middle\">")
        for row in self._data :
            html.append("<tr>")
            for cell, rowspan, colspan in row :
                rowspan = "" if rowspan is None else f" rowspan=\"{rowspan}\""
                colspan = "" if colspan is None else f" colspan=\"{colspan}\""
                html.append(f"<td{rowspan}{colspan}>")
                html.append(cell.construct(info_dict))
                html.append("</td>")
            html.append("</tr>")
        html.append("</table>")

        return "\n".join(html)
