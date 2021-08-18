from talon import Module, app
from dataclasses import dataclass
from ..csv_overrides import init_csv_and_watch_changes

mod = Module()


mod.list("cursorless_selection_type", desc="Types of selection_types")

selection_types = {
    "token": "token",
    "line": "line",
    "block": "paragraph",
    "file": "document",
}


@mod.capture(rule="{user.cursorless_selection_type}")
def cursorless_selection_type(m) -> str:
    return {"selectionType": m.cursorless_selection_type}


def on_ready():
    default_values = {"selection_type": selection_types}
    init_csv_and_watch_changes("selection_types", default_values)


app.register("ready", on_ready)
