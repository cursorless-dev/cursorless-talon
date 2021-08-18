from talon import Module, Context

mod = Module()
ctx = Context()


wrappers = {
    "square": ["[", "]"],
    "round": ["(", ")"],
    "curly": ["{", "}"],
    "diamond": ["<", ">"],
    "twin": ["'", "'"],
    "quad": ['"', '"'],
    "brick": ["`", "`"],
    "escaped twin": ["\\'", "\\'"],
    "escaped quad": ['\\"', '\\"'],
    "space": [" ", " "],
}

mod.list("cursorless_wrap_action", desc="Cursorless wrap action")
mod.list("cursorless_wrapper", desc="Supported wrappers for cursorless wrap action")
ctx.lists["self.cursorless_wrapper"] = wrappers.keys()


@mod.capture(rule=("{user.cursorless_wrapper}"))
def cursorless_wrapper(m) -> list[str]:
    return wrappers[m.cursorless_wrapper]
