from typing import Any, Dict, List

import streamlit as st
from AnnotationApps.dbserver.utilities import get_history, update_history
import AnnotationApps.dbserver.api as dbapi
from AnnotationApps.viewer import annotation_block
from AnnotationApps.viewer import html_element as anno
from data_utilities.loading import get_data_from_split

st.set_page_config(layout="wide")


@st.cache(allow_output_mutation=True)
def get_dataset(dataset_split):
    data = get_data_from_split(dataset_split)
    data = {doc.document_id: doc for doc in data}
    return data


def display(document, username, assignment):
    print("Running again")
    page = anno.Page({"username": username, "pmid": document.document_id})

    negative_relations = list(
        set([(relation.drug, relation.variant) for relation in document.relations if relation.label == False])
    )

    for para in document.paragraphs:
        for sentence in para.sentences:
            for drug, variant in negative_relations:
                if sentence.has_entity(drug) and sentence.has_entity(variant):
                    words = []
                    for i, (token, mentions) in enumerate(sentence.annotated_tokens):
                        token_type = "other"
                        words.append(
                            anno.HighlightableText(
                                text=token, classes=[token_type], info_dict={"word_id": i},
                            )
                        )

                    words = anno.HighlightableTextBlock(
                        words=words,
                        tablename="rationale_words",
                        info_dict={
                            "para_id": para.paragraph_id,
                            "sent_id": sentence.sentence_id,
                            "relation": "_".join((drug, variant)),
                        },
                    )

                    page.add(words)

                    page.add(
                        anno.Checkbox(
                            label="Has Relations ?",
                            tablename="has_relation",
                            info_dict={
                                "para_id": para.paragraph_id,
                                "sent_id": sentence.sentence_id,
                                "relation": "_".join((drug, variant)),
                            },
                        )
                    )

                    page.add(
                        anno.Choice(
                            label="Relation Type ?",
                            options=["inhibitor", "mediator", "connective"],
                            tablename="relation_type",
                            info_dict={
                                "para_id": para.paragraph_id,
                                "sent_id" : sentence.sentence_id,
                                "relation": "_".join((drug, variant)),
                            }
                        )
                    )

                    page.add(
                        anno.Textbox(
                            label="Add Comment",
                            tablename="comment",
                            info_dict={
                                "para_id": para.paragraph_id,
                                "sent_id": sentence.sentence_id,
                                "relation": "_".join((drug, variant)),
                            },
                        )
                    )

                    page.add(anno.HorizontalLine())

    return page


## Loading Block
username = st.sidebar.text_input(label="Enter Username", key="username")

## You widgets
dataset_type = st.sidebar.selectbox(
    label="Which Dataset ?", options=["----", "ckb_dev", "ckb_test"], key="dataset_type"
)

if username != "" and dataset_type != "----":
    dataset: Dict[str, Any] = get_dataset(dataset_type)
    assignments: Dict[str, bool] = get_history(dataset_idx=list(dataset.keys()), username=username)

    format_func = lambda x: x + (u" ✅" if assignments[x] else " ❌")
    selected_assignment = st.sidebar.selectbox(
        label="Assignments", options=list(assignments.keys()), format_func=format_func
    )

    with st.spinner("Loading document") :
        values = annotation_block(
            page=display(dataset[selected_assignment], username=username, assignment=selected_assignment),
            key=selected_assignment,
        )

        print(values)

    if values is not None and values["next"] == True:
        update_history(assignment=selected_assignment, username=username)
        st.experimental_rerun()
