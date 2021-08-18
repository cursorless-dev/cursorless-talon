from talon import Module, app
from ..csv_overrides import init_csv_and_watch_changes

mod = Module()


mod.list("cursorless_scope_type", desc="Supported scope types")

scope_types = {
    "arg": "argumentOrParameter",
    "arrow": "arrowFunction",
    "attribute": "attribute",
    "call": "functionCall",
    "class name": "className",
    "class": "class",
    "comment": "comment",
    "funk name": "functionName",
    "funk": "namedFunction",
    "if state": "ifStatement",
    "item": "collectionItem",
    "key": "collectionKey",
    "list": "list",
    "map": "dictionary",
    "name": "name",
    "regex": "regex",
    "state": "statement",
    "string": "string",
    "type": "type",
    "value": "value",
    #  XML, JSX
    "element": "xmlElement",
    "tags": "xmlBothTags",
    "start tag": "xmlStartTag",
    "end tag": "xmlEndTag",
}


@mod.capture(rule="[every] {user.cursorless_scope_type}")
def cursorless_containing_scope(m) -> str:
    """Expand to containing scope"""
    return {
        "modifier": {
            "type": "containingScope",
            "scopeType": m.cursorless_scope_type,
            "includeSiblings": m[0] == "every",
        }
    }


def on_ready():
    default_values = {"scope_type": scope_types}
    init_csv_and_watch_changes("scope_types", default_values)


app.register("ready", on_ready)
