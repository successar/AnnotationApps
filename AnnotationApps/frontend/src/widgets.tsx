import $ from "jquery"

export function select_return(element) {
    let common_data = $("div[data-type=common]").data();
    let specific_data = $(this).data();
    let db_data = {...common_data, ...specific_data};
    delete db_data["type"];

    let tablename = db_data["tablename"];
    delete db_data["tablename"]

    db_data["value"] = $(this).find(":selected").val()

    return {
        "api" : "add_or_delete",
        "tablename" : tablename,
        "keys" : db_data,
        "value" : true
    }
    

}

export function checkbox_return() {
    let common_data = $("div[data-type=common]").data();
    let specific_data = $(this).data();
    let db_data = {...common_data, ...specific_data};
    delete db_data["type"];

    let tablename = db_data["tablename"];
    delete db_data["tablename"]

    return {
        "api" : "add_or_delete",
        "tablename" : tablename,
        "keys" : db_data,
        "value" : $(this).prop("checked")
    }
}