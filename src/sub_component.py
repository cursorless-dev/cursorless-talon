from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
app: vscode
"""


@mod.capture(rule=("<user.ordinals> | last"))
def ordinal_or_last(m) -> str:
    """Supported extents for cursorless navigation"""
    if m[0] == "last":
        return -1
    return m.ordinals - 1

mod.list("cursorless_sub_component_type", desc="Supported subcomponent types")

ctx.lists["self.cursorless_sub_component_type"] = {
    "word": "subtoken",
    "char": "character"
}

@mod.capture(
    rule=(
        "<user.ordinal_or_last> [past <user.ordinal_or_last>] {user.cursorless_sub_component_type}"
    )
)
def cursorless_subcomponent(m) -> str:
    """Word subcomponents such as subwords or characters"""
    return {
        "transformation": {
            "type": "subpiece",
            "pieceType": m.cursorless_sub_component_type,
            "startIndex": m.ordinal_or_last_list[0],
            "endIndex": m.ordinal_or_last_list[-1] + 1 or None,
        }
    }


