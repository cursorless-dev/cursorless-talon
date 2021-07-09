from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

inside_outside = {
    "inner": {"insideOutsideType": "inside"},
    "outer": {"insideOutsideType": "outside"}
}

mod.list("cursorless_inside_outside", desc="Supported inside/outside types")
ctx.lists["self.cursorless_inside_outside"] = inside_outside.keys()

@mod.capture(rule=("{user.cursorless_inside_outside}"))
def cursorless_inside_outside(m) -> str:
    return inside_outside[m.cursorless_inside_outside]
