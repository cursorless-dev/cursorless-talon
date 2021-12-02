from talon import Module

mod = Module()


mod.list(
    "cursorless_identity",
    desc="Cursorless modifier for identity. Use to break inference.",
)


@mod.capture(rule="{user.cursorless_identity}")
def cursorless_head_tail(m) -> dict:
    return {"modifier": {"type": "identity"}}
