import { Streamlit, RenderData } from "streamlit-component-lib"
import $ from "jquery"
import { highlight, highlight_return } from "./highlight"
import { checkbox_return, select_return } from "./widgets"

let state = "idle";

function setup() {
    $(".highlight").on("mouseup", highlight);
}


function get_component_values() {
    let values = [];
    values = values.concat($("input[type=checkbox].db").map(checkbox_return).get());
    values = values.concat($(".highlight").map(highlight_return).get());
    values = values.concat($("select.db").map(select_return).get());
    return values;
};

function onstreamlitupdate() {
    $("#savenext").on("click", function(){
        let values = get_component_values();
        Streamlit.setComponentValue({
            "done" : true,
            "next" : true,
            "values" : values
        });

        state = "clicked";
    });

    $("#save").on("click", function(){
        let values = get_component_values();
        Streamlit.setComponentValue({
            "done" : true,
            "next" : false,
            "values" : values
        });
        state = "clicked";
    });
};

function onRender(event: Event): void {
    const data = (event as CustomEvent<RenderData>).detail
    if (state == "clicked") {
        state = "idle";
        return;
    }
    $("#docdiv").html(data.args["data"]);
    $("#head-style").append(data.args["css"]);
    setup();
    onstreamlitupdate();
    Streamlit.setFrameHeight()
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight()