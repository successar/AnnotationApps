import json
from typing import Any, Dict

import streamlit as st
from AnnotationApps import html_element as anno


@st.cache(allow_output_mutation=True)
def get_dataset(username: str):
    return json.load(open(f"{username}.json"))


@st.cache(max_entries=1)
def display(document: Any, username: str, assignment_id: str, key: str) -> anno.Page:
    page = anno.Page({"username": username, "assignment_id": assignment_id}, add_next=False)

    page.add(
        anno.Textbox(label="List the top-5 most probable artifacts:", tablename="artifacts", info_dict={})
    )
    page.add(
        anno.Textbox(
            label="Which label is it associated with ?", tablename="associated_label", info_dict={}
        )
    )

    for example in document:
        text = example["text"]
        gold_label = example["gold_label"]
        predicted_label = example["predicted_label"]

        positive_attrs = example["positives"]
        negative_attrs = example["negatives"]

        page.add(anno.TextBlock(elements=[anno.Text(text)]))
        page.add(anno.TextBlock(elements=[anno.Text(f"<b>Gold Label </b>: {gold_label}, <b>Predicted Label</b> : {predicted_label}")]))

        page.add(anno.TextBlock(elements=[anno.Text("<h5>Positive Attributions</h5>")]))
        for ex in positive_attrs:
            page.add(anno.TextBlock(elements=[anno.Text(ex)]))

        page.add(anno.TextBlock(elements=[anno.Text("<h5>Negative Attributions</h5>")]))
        for ex in negative_attrs:
            page.add(anno.TextBlock(elements=[anno.Text(ex)]))

        page.add(anno.HorizontalLine())



    return page


import secrets
from typing import Any, Callable, Dict, List

import streamlit as st

st.set_page_config(layout="wide")

import AnnotationApps.SessionState as SessionState
from AnnotationApps import annotation_block
from AnnotationApps import html_element as anno
from AnnotationApps.dbserver.api import add, delete


def save(annotations: List[dict]):
    for annotation in annotations:
        tablename = annotation["tablename"]
        keys = annotation["keys"]
        if annotation["api"] == "add":
            value = annotation["value"]
            add(tablename, keys, value)
        elif annotation["api"] == "delete":
            delete(tablename, keys)


def basic_annotator():
    username = st.sidebar.text_input(label="Enter Username", key="username")

    if username != "":
        dataset: Dict[str, Any] = get_dataset(username)
        methods = list(dataset.keys())

        method = st.sidebar.selectbox(label="Attribution Method", options=methods)

        state = SessionState.get(
            key=secrets.token_hex(128),
            username=username,
        )

        with st.spinner("Loading document"):
            state = SessionState.get(key=secrets.token_hex(128))
            annotations = annotation_block(
                page=display(
                    dataset[method],
                    username=username,
                    assignment_id=method,
                    key=state.key,
                ),
                key=state.key,
            )

            print("=" * 50)
            print(annotations)
            print("=" * 50)

        if annotations is not None:
            save(annotations["values"])
            state.key = secrets.token_hex(128)

basic_annotator()