Streamlit based Annotation App
==============================

Main goal - customizability of interface 

Can be used to show long documents, short documents , medium documents.
Can use checkboxes, select boxes, highlights, text boxes in the same interface in any order.
Data can be input in any format. 

Installation
------------

`pip install git+https://github.com/successar/AnnotationApps.git#egg=AnnotationApps`

Usage
------

Need to provide two functions - 

1. `get_dataset` -- Returns your data . This should be a dict of type Dict[str, Any] . The key of the dict identify the data point for annotation, value can be anything.
2. `display` -- Create a display for your data point. Use widgets from AnnotationApps.html_elements .

Serving
-------

1. `export DBPATH=...` add a path to the db where you want to store the annotations.
2. `streamlit run <path to annotator file> --server.port <port number>`
3. At end, when you want to get the annotations, just do `python -m AnnotationApps.export_to_jsonl <dbpath> <file-prefix>` . 
    * `dbpath` : Path to DB
    * `file_prefix` : File prefix when exporting tables in db. All tables are exported in jsonl format . The file for each table is of form `<file prefix>.<table-name>.jsonl`