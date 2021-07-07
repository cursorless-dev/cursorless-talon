from talon import Context, Module
from .selection_type import LINE

mod = Module()
ctx = Context()

ctx.matches = r"""
app: vscode
"""


positions = {
    "after": {"position": "after"},
    "before": {"position": "before"},
    "start of": {"position": "before", "insideOutsideType": "inside"},
    "end of": {"position": "after", "insideOutsideType": "inside"},
    "above": {"position": "before", **LINE.json_repr},
    "below": {"position": "after", **LINE.json_repr}
}

mod.list("cursorless_position", desc="Types of positions")
ctx.lists["self.cursorless_position"] = positions.keys()

@mod.capture(rule="{user.cursorless_position}")
def cursorless_position(m) -> str:
    return positions[m.cursorless_position]
