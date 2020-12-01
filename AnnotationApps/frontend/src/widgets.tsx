import $ from "jquery"

export function select_return() {
    let common_data = $("div[data-type=common]").data();
    let specific_data = $(this).data();
    let db_data = { ...common_data, ...specific_data };
    delete db_data["type"];

    let tablename = db_data["tablename"];
    delete db_data["tablename"]

    return {
        "api": $(this).find(":selected").val() ? "add" : "delete",
        "tablename": tablename,
        "keys": db_data,
        "value": $(this).find(":selected").val()
    }
}

export function checkbox_return() {
    let common_data = $("div[data-type=common]").data();
    let specific_data = $(this).data();
    let db_data = { ...common_data, ...specific_data };
    delete db_data["type"];

    let tablename = db_data["tablename"];
    delete db_data["tablename"]

    return {
        "api": $(this).prop("checked") ? "add" : "delete",
        "tablename": tablename,
        "keys": db_data,
        "value": 1
    }
}