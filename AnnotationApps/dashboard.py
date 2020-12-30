from typing import Any, Dict

import streamlit as st
import secrets

from AnnotationApps import annotation_block
from AnnotationApps.history import get_history, get_all_usernames


def basic_annotator(get_dataset, display, selector_elements=None):
    all_usernames = get_all_usernames()
    username = st.sidebar.selectbox(label="Select Username", options=all_usernames, key="username")

    if selector_elements is not None:
        values = selector_elements()
    else:
        values = {}

    dataset: Dict[str, Any] = get_dataset(**values)
    assignments: Dict[str, bool] = get_history(dataset_idx=list(dataset.keys()), username=username)

    format_func = lambda x: (u"✅ " if assignments[x] else "❌ ") + x
    selected_assignment = st.sidebar.selectbox(
        label="Assignments", options=list(assignments.keys()), format_func=format_func
    )

    with st.spinner("Loading document"):
        key = secrets.token_hex(128)
        annotation_block(
            page=display(
                dataset[selected_assignment], username=username, assignment=selected_assignment, key=key
            ),
            key=key,
        )
