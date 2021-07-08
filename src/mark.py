from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

mod.list("cursorless_symbol_color", desc="Supported symbol colors for cursorless")
ctx.lists["self.cursorless_symbol_color"] = {
    "gray": "default",
    "blue": "blue",
    "green": "green",
    "rose": "red",
    "squash": "yellow",
    "plum": "purple"
}


@mod.capture(rule="[{user.cursorless_symbol_color}] <user.any_alphanumeric_key>")
def cursorless_decorated_symbol(m) -> str:
    """A decorated symbol"""
    try:
        symbol_color = m.cursorless_symbol_color
    except AttributeError:
        symbol_color = "default"
    return {
        "mark": {
            "type": "decoratedSymbol",
            "symbolColor": symbol_color,
            "character": m.any_alphanumeric_key
        }
    }


special_marks = {
    "this": {"mark": {"type": "cursor"}},
    "that": {"mark": {"type": "that"}}

    # "last cursor": {"mark": {"type": "lastCursorPosition"}} # Not implemented
}

mod.list("cursorless_mark", desc="Cursorless marks")
ctx.lists["self.cursorless_mark"] =  special_marks.keys()

@mod.capture(rule=(
    "<user.cursorless_decorated_symbol> | "
    "{user.cursorless_mark}"
))
def cursorless_mark(m) -> str:
    try:
        return m.cursorless_decorated_symbol
    except AttributeError:
        return special_marks[m.cursorless_mark]
