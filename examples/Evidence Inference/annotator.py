import json
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import streamlit as st
from AnnotationApps import html_element as anno
from AnnotationApps.basic_annotator import basic_annotator

st.set_page_config(layout="wide")


@dataclass
class Document:
    annotation_id: str
    document: str
    query: str
    label: str
    rationale: List[Tuple[int, int]]

    def __hash__(self):
        return hash((self.document, self.query))

    def __eq__(self, other):
        return self.document == other.document and self.query == other.query


@st.cache(allow_output_mutation=True)
def get_dataset() -> Dict[str, Any]:
    data = sorted(
        list(set([Document(**json.loads(line)) for line in open("data.jsonl")])),
        key=lambda x: x.annotation_id,
    )
    documents = {}
    for doc in data:
        idx = doc.annotation_id.split("_")[0]
        documents.setdefault(idx, []).append(doc)

    return dict(list(documents.items())[:5])


@st.cache(max_entries=1)
def display(document: Any, username: str, assignment: str, key: str) -> anno.Page:
    print("******************* Running again display ********************")
    page = anno.Page({"username": username, "document_id": assignment})

    for para in document:
        document_words = para.document.split()
        table = anno.Table()

        table.add_row([anno.Text("Document :")], colspans=[2])
        table.add_row(
            [
                anno.TypedTextBlock(
                    words=[
                        anno.Text(text=word, info_dict={"word_id": i})
                        for i, word in enumerate(document_words)
                    ],
                    tablename="rationale_words",
                    info_dict={"annotation_id": para.annotation_id},
                    entity_labels=["P", "I", "O", "C"],
                )
            ],
            colspans=[2],
        )
        table.add_row(
            [
                anno.TextBlock(words=[anno.Text("Query: "), anno.Text(para.query)]),
                anno.Choice(
                    label="Label",
                    options=[
                        "no significant difference",
                        "significantly increased",
                        "significantly decreased",
                    ],
                    tablename="label",
                    info_dict={"annotation_id": para.annotation_id},
                ),
            ],
        )

        page.add(table)
        page.add(anno.HorizontalLine())

    return page


basic_annotator(get_dataset, display)
