from typing import Any, Dict

import streamlit as st
from AnnotationApps import html_element as anno
from AnnotationApps.basic_annotator import basic_annotator

st.set_page_config(layout="wide")


def selectors() -> Dict[str, Any]:
    return {}


@st.cache(allow_output_mutation=True)
def get_dataset() -> Dict[str, Any]:
    return {}


@st.cache(max_entries=1)
def display(document: Any, username: str, assignment_id: str, key: str) -> anno.Page:
    page = anno.Page(
        {
            "username": username,
        }
    )

    return page


basic_annotator(get_dataset, display, selectors=selectors)
