import $ from "jquery"

export function highlight_setup() {
    $(".highlight").on("mouseup", highlight);
    $(".highlight").find("mark").each((index, element) => appendButtonToMark(element));
}

export function highlight_return() {
    let common_data = $("div[data-type=common]").data();
    let specific_data = $(this).data();

    let db_data = { ...common_data, ...specific_data };
    delete db_data["type"];

    let tablename = db_data["tablename"];
    delete db_data["tablename"];

    let marked_spans = $(this).find("mark").map(function () {
        let data = $(this).find(".highlightable").map(function () {
            return $(this).data();
        }).get();

        let map = dictionary(data);

        map["span-start"] = $(this).attr("data-span-start");
        map["span-end"] = $(this).attr("data-span-end");

        delete map["block_pos"];

        map["span-type"] = $(this).attr("data-span-type");

        return map;
    }).get();

    let api = (marked_spans.length > 0) ? "add" : "delete";

    return {
        "api": api,
        "tablename": tablename,
        "keys": db_data,
        "value": JSON.stringify(marked_spans)
    }
}

function dictionary(list) {
    var map = {};
    list.forEach(element => {
        Object.entries(element).forEach(([key, value], l) => {
            let strkey = (key as unknown) as string
            if (!map[strkey]) {
                map[strkey] = [];
            }
            map[strkey].push(value);
        })
    });

    return map;
}

function appendButtonToMark(mark_element) {
    let mark_button = document.createElement("button");
    $(mark_button).on("click", rel_button_click);
    mark_button.classList.add("btn", "btn-success", "rel-button");
    mark_button.innerHTML = $(mark_element).attr("data-span-type");
    mark_element.appendChild(mark_button);
}

export function highlight() {
    var sel = window.getSelection();
    if (sel) {
        var range = sel.getRangeAt(0);
        var selectedNodes = getRangeSelectedNodes(range);
        let highlightable_nodes: Array<Node> = filter_to_highlightable(selectedNodes);
        removeMarked(highlightable_nodes);
        if (highlightable_nodes.length > 0 && highlightable_nodes.every(node => node.parentNode === highlightable_nodes[0].parentNode)) {
            let marked_range = new Range();
            marked_range.setStartBefore(highlightable_nodes[0]);
            marked_range.setEndAfter(highlightable_nodes[highlightable_nodes.length - 1]);

            // Create a Mark element to surround the selection
            let mark_element = document.createElement("mark");

            // Add Span Type to the Mark
            let parent = highlightable_nodes[0].parentNode;
            let span_type_radio_id = $(parent).children("div[data-type=type-selector]").attr("data-radio-id");
            let span_type: string = ($(`input[name=${span_type_radio_id}]:checked`).val() as string);
            span_type = span_type ? span_type : "UNK";
            $(mark_element).attr("data-span-type", span_type);

            // Calculate Span Start and Span End Positions 
            let positions = highlightable_nodes.map(node => parseInt($(node).attr("data-block_pos")));
            let span_start = Math.min(...positions);
            let span_end = Math.max(...positions) + 1;

            $(mark_element).attr("data-span-start", span_start);
            $(mark_element).attr("data-span-end", span_end);

            marked_range.surroundContents(mark_element);
            appendButtonToMark(mark_element);
        }

        sel.removeAllRanges();
    }
};

function rel_button_click(e: Event) {
    let block = $(this).closest(".highlight").get(0); // Find which block it lives in
    if (block) {
        let other_clicked = $(block).find("button.clicked").get(0); // Find if another span is already clicked.
        if (other_clicked) {
            let other_mark = $(other_clicked).closest("mark").get(0);
            let span_1_start = $(other_mark).attr("data-span-start");
            let span_1_end = $(other_mark).attr("data-span-end");

            let my_mark = $(this).closest("mark").get(0);
            let span_2_start = $(my_mark).attr("data-span-start");
            let span_2_end = $(my_mark).attr("data-span-end");

            let relation = $(document.createElement("div"));
            relation.addClass("relation");
            relation.attr("data-span-a-start", span_1_start);
            relation.attr("data-span-a-end", span_1_end);
            relation.attr("data-span-b-start", span_2_start);
            relation.attr("data-span-b-end", span_2_end);

            let relation_mark_1 = $(document.createElement("span"));
            relation_mark_1.addClass("rel-mark");
            relation_mark_1.html($(other_mark).find(".highlightable").text());
            
            let relation_mark_2 = $(document.createElement("span"));
            relation_mark_2.addClass("rel-mark");
            relation_mark_2.html($(my_mark).find(".highlightable").text());

            relation.append(relation_mark_1);
            relation.append(" - ");
            relation.append(relation_mark_2);

            $(block).find("div[data-type=relation-area]").append(relation);
            $(other_clicked).removeClass("clicked");
        }
        else {
            $(this).addClass("clicked");
            $(this).blur(); // lose focus immediately so css rendering can occur
        }
    }
    e.stopPropagation();
}

function nextNode(node) {
    if (node.hasChildNodes()) {
        return node.firstChild;
    } else {
        while (node && !node.nextSibling) {
            node = node.parentNode;
        }
        if (!node) {
            return null;
        }
        return node.nextSibling;
    }
}

function getRangeSelectedNodes(range) {
    var node = range.startContainer;
    var endNode = range.endContainer;

    // Special case for a range that is contained within a single node
    if (node == endNode) {
        return [node];
    }

    // Iterate nodes until we hit the end container
    var rangeNodes = [];
    while (node && node != endNode) {
        rangeNodes.push(node = nextNode(node));
    }

    // Add partially selected nodes at the start of the range
    node = range.startContainer;
    while (node && node != range.commonAncestorContainer) {
        rangeNodes.unshift(node);
        node = node.parentNode;
    }

    return rangeNodes;
}

function filter_to_highlightable(selected_nodes): Array<Node> {
    selected_nodes = selected_nodes.map(node => {
        if (node.nodeType === Node.TEXT_NODE) {
            node = node.parentNode;
            node = $(node).closest(".highlightable");
            node = node ? node.get(0) : node;
        }

        if (node && node.classList.contains("highlightable")) {
            return [node];
        }
        else {
            return [];
        }
    });

    return Array.from(new Set(selected_nodes.flat()));
}

function removeMarked(selected_nodes) {
    let marked_nodes = selected_nodes.map(element => {
        return $(element).closest("mark");
    });

    marked_nodes = Array.from(new Set(marked_nodes.flat()));

    marked_nodes.forEach(element => {
        $(element).find("button").remove();
        var cnt = $(element).contents();
        $(element).replaceWith(cnt);
    })
}