from typing import Any, Dict, List, Callable

import streamlit as st
import secrets

from AnnotationApps import annotation_block
from AnnotationApps import html_element as anno
from AnnotationApps.dbserver.api import add, delete
from AnnotationApps.history import get_history, mark_as_completed
import AnnotationApps.SessionState as SessionState


def save(annotations: List[dict]):
    for annotation in annotations:
        tablename = annotation["tablename"]
        keys = annotation["keys"]
        if annotation["api"] == "add":
            value = annotation["value"]
            add(tablename, keys, value)
        elif annotation["api"] == "delete":
            delete(tablename, keys)


def basic_annotator(
    get_dataset: Callable[..., Dict[str, Any]],
    display: Callable[[Any, str, str, str], anno.Page],
    selectors: Callable[[], dict] = None,
):
    username = st.sidebar.text_input(label="Enter Username", key="username")

    if username != "":
        if selectors is not None:
            values: dict = selectors()
        else:
            values = {}

        dataset: Dict[str, Any] = get_dataset(**values)

        # Why do we do this ? So if the dataset changes, we reload the assignments fron scratch.
        # Time saving Hackery.
        dataset_hash = hash(frozenset(dataset.keys()))

        state = SessionState.get(
            key=secrets.token_hex(128),
            username=username,
            assignments={},
            get_next=True,
            dataset_hash=dataset_hash,
        )

        should_load_assignments = (
            state.get_next # Assignment Done 
            or state.dataset_hash != dataset_hash # Dataset Changes
            or state.username != username # Username Changes
        )
        if should_load_assignments:
            assignments: Dict[str, bool] = get_history(
                dataset_ids=list(dataset.keys()), username=username
            )
            state.assignments = assignments
            state.dataset_hash = dataset_hash
            state.username = username
            state.get_next = False
        else:
            assignments = state.assignments

        format_func = lambda x: (u"✅ " if assignments[x] else "❌ ") + x
        selected_assignment = st.sidebar.selectbox(
            label="Assignments",
            options=list(assignments.keys()),
            format_func=format_func,
        )

        with st.spinner("Loading document"):
            state = SessionState.get(key=secrets.token_hex(128))
            annotations = annotation_block(
                page=display(
                    dataset[selected_assignment],
                    username=username,
                    assignment=selected_assignment,
                    key=state.key,
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
                    mark_as_completed(
                        assignment_id=selected_assignment, username=username
                    )
                state.get_next = True

            state.key = secrets.token_hex(128)
            st.experimental_rerun()
