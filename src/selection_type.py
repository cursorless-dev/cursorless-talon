from talon import Context, Module
from dataclasses import dataclass

mod = Module()
ctx = Context()

ctx.matches = r"""
app: vscode
"""

SELECTION_TYPE_KEY = "selectionType"


@dataclass
class SelectionType:
    singular: str
    plural: str
    json_name: str
    rank: int

    @property
    def json_repr(self):
        return {SELECTION_TYPE_KEY: self.json_name}


TOKEN = SelectionType("token", "tokens", "token", 0)
LINE = SelectionType("line", "lines", "line", 1)
BLOCK = SelectionType("block", "blocks", "block", 2)
FILE = SelectionType("file", "files", "document", 3)

SELECTION_TYPES = [
    TOKEN,
    LINE,
    BLOCK,
    FILE
]

RANKED_SELECTION_TYPES = {
    selection_type.json_name: selection_type.rank for selection_type in SELECTION_TYPES
}

selection_type_map = {
    st.singular: st.json_repr for st in  SELECTION_TYPES
}

mod.list("cursorless_selection_type", desc="Types of selection_types")
ctx.lists["self.cursorless_selection_type"] = selection_type_map.keys()

@mod.capture(rule="{user.cursorless_selection_type}")
def cursorless_selection_type(m) -> str:
    return selection_type_map[m.cursorless_selection_type]
