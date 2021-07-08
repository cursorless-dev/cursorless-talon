from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""


@mod.capture(rule=("<user.ordinals> | last"))
def ordinal_or_last(m) -> str:
    """An ordinal or the word 'last'"""
    if m[0] == "last":
        return -1
    return m.ordinals - 1

mod.list("cursorless_subtoken", desc="Supported subcomponent types")

ctx.lists["self.cursorless_subtoken"] = {
    "word": "subtoken",
    "char": "character"
}

@mod.capture(
    rule=(
        "<user.ordinal_or_last> [past <user.ordinal_or_last>] {user.cursorless_subtoken}"
    )
)
def cursorless_subtoken(m) -> str:
    """Subtoken ranges such as subwords or characters"""
    return {
        "transformation": {
            "type": "subpiece",
            "pieceType": m.cursorless_subtoken,
            "startIndex": m.ordinal_or_last_list[0],
            "endIndex": m.ordinal_or_last_list[-1] + 1 or None,
        }
    }
