from talon import Context, Module
from dataclasses import dataclass

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

mod.list("cursorless_selection_type", desc="Types of selection_types")
ctx.lists["self.cursorless_selection_type"] = {
    "token": "token",
    "line": "line",
    "block": "paragraph",
    "file": "document",
}


@mod.capture(rule="{user.cursorless_selection_type}")
def cursorless_selection_type(m) -> str:
    return {"selectionType": m.cursorless_selection_type}
