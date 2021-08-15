from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

mod.list("cursorless_head_tail", desc="Cursorless modifier for head or tail of line")
ctx.lists["self.cursorless_head_tail"] = {"head", "tail"}


@mod.capture(rule="{user.cursorless_head_tail}")
def cursorless_head_tail(m) -> str:
    return {"modifier": {"type": m.cursorless_head_tail}}
