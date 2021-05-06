import os
import streamlit.components.v1 as components

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")

if "DEBUG_MODE" in os.environ :
    _component_func = components.declare_component("document_viewer", url="http://gil.ccs.neu.edu:5010",)
else :
    _component_func = components.declare_component("document_viewer", path=build_dir)

def annotation_block(page, key) :
    return _component_func(data=page.html(), css=page.css(), key=key)