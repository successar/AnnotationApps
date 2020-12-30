import $ from "jquery"

export function highlight_return() {
    let common_data = $("div[data-type=common]").data();
    let specific_data = $(this).data();

    let db_data = { ...common_data, ...specific_data };
    delete db_data["type"];

    let tablename = db_data["tablename"];
    delete db_data["tablename"];

    let highlights = $(this).find(".highlightable.rationale").map(function() {
        return $(this).data();
    }).get();

    let api = (highlights.length > 0) ? "add" : "delete";

    return {
        "api" : api,
        "tablename" : tablename,
        "keys" : db_data,
        "value" : JSON.stringify(highlights)
    }
} 

export function highlight() {
    var sel = window.getSelection();
    if (sel) {
        var range = sel.getRangeAt(0);
        var selectedNodes = getRangeSelectedNodes(range);
        var highlightable_nodes = filter_to_highlightable(selectedNodes);
        highlightable_nodes.forEach(element => $(element).toggleClass("rationale"));
        sel.removeAllRanges();
    }
};

function filter_to_highlightable(selected_nodes) {
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