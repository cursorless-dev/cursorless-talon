from talon import Module

mod = Module()


@mod.capture(rule="head | tail")
def cursorless_head_tail(m) -> str:
    return {"modifier": {"type": m[0]}}
