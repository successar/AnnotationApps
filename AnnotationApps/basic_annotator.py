from typing import Any, Dict, List, Tuple

import streamlit as st
import secrets

from AnnotationApps import annotation_block
from AnnotationApps.dbserver.api import add, delete
from AnnotationApps.history import get_history, update_history
import AnnotationApps.SessionState as SessionState


def save(annotations: List[dict]):
    for annotation in annotations:
        tablename = annotation["tablename"]
        keys = annotation["keys"]
        value = annotation["value"]
        if annotation["api"] == "add":
            add(tablename, keys, value)
        elif annotation["api"] == "delete":
            delete(tablename, keys, value)


def basic_annotator(get_dataset, display, selector_elements=None):
    username = st.sidebar.text_input(label="Enter Username", key="username")

    if selector_elements is not None:
        values = selector_elements()
    else:
        values = {}

    if username != "":
        dataset: Dict[str, Any] = get_dataset(**values)

        state = SessionState.get(key=secrets.token_hex(128), assignments={}, get_next=True)

        if state.get_next:
            assignments: Dict[str, bool] = get_history(dataset_idx=list(dataset.keys()), username=username)
            state.assignments = assignments
            state.get_next = False
        else:
            assignments = state.assignments

        format_func = lambda x: (u"✅ " if assignments[x] else "❌ ") + x
        selected_assignment = st.sidebar.selectbox(
            label="Assignments", options=list(assignments.keys()), format_func=format_func
        )

        with st.spinner("Loading document"):
            state = SessionState.get(key=secrets.token_hex(128))
            annotations = annotation_block(
                page=display(
                    dataset[selected_assignment],
                    username=username,
                    assignment=selected_assignment,
                    key=state.key
                ),
                key=state.key,
            )

            print("=" * 50)
            print(annotations)
            print("=" * 50)

        if annotations is not None:
            save(annotations["values"])

            if annotations["next"] == True:
                if assignments[selected_assignment] == False:
                    update_history(assignment=selected_assignment, username=username)
                state.get_next = True

            state.key = secrets.token_hex(128)
            st.experimental_rerun()
