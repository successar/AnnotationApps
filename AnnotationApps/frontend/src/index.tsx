import { Streamlit, RenderData } from "streamlit-component-lib"
import $ from "jquery"
import { highlight, highlight_return } from "./highlight"
import { checkbox_return, select_return } from "./widgets"


function setup() {
    $(".highlight").on("mouseup", highlight);
}


function get_component_values() {
    let values = [];
    values = values.concat($("input[type=checkbox].db").map(checkbox_return).get());
    values = values.concat($(".highlight").map(highlight_return).get());
    // values.concat($("select.db").map(element => select_return(element)));

    console.log(values);
    return values;
};

function onstreamlitupdate() {
    $("#savenext").on("click", function(){
        let values = get_component_values();
        Streamlit.setComponentValue({
            "done" : true,
            "next" : true,
            "values" : values
        })
    });

    $("#save").on("click", function(){
        let values = get_component_values();
        Streamlit.setComponentValue({
            "done" : true,
            "next" : false,
            "values" : values
        })
    });
    
};

function onRender(event: Event): void {
    const data = (event as CustomEvent<RenderData>).detail
    $("#docdiv").html(data.args["data"]);
    console.log("Updating");
    setup();
    onstreamlitupdate();
    Streamlit.setFrameHeight()
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight()