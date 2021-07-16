from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

mod.list("cursorless_subtoken", desc="Supported subcomponent types")
ctx.lists["self.cursorless_subtoken"] = {"word": "word", "char": "character"}


@mod.capture(rule="<user.ordinals> | last")
def ordinal_or_last(m) -> str:
    """An ordinal or the word 'last'"""
    if m[0] == "last":
        return -1
    return m.ordinals - 1


@mod.capture(rule="<user.ordinal_or_last> [past <user.ordinal_or_last>]")
def cursorless_ordinal_range(m) -> str:
    """Ordinal range"""
    return {
        "startIndex": m.ordinal_or_last_list[0],
        "endIndex": m.ordinal_or_last_list[-1] + 1 or None,
    }


@mod.capture(rule="(first | last) <number_small>")
def cursorless_first_last_range(m) -> str:
    """First/last range"""
    if m[0] == "first":
        return {"startIndex": 0, "endIndex": m.number_small}
    return {"startIndex": -m.number_small, "endIndex": -1}


@mod.capture(
    rule=(
        "(<user.cursorless_ordinal_range> | <user.cursorless_first_last_range>)"
        "{user.cursorless_subtoken}"
    )
)
def cursorless_subtoken(m) -> str:
    """Subtoken ranges such as subwords or characters"""
    try:
        range = m.cursorless_ordinal_range
    except AttributeError:
        range = m.cursorless_first_last_range
    return {
        "modifier": {"type": "subpiece", "pieceType": m.cursorless_subtoken, **range}
    }
