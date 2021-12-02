from talon import Module

mod = Module()


mod.list("cursorless_head_tail", desc="Cursorless modifier for head or tail of line")


@mod.capture(rule="{user.cursorless_head_tail}")
def cursorless_head_tail(m) -> dict:
    return {"modifier": {"type": m.cursorless_head_tail}}
