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
    "plum": "purple",
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
            "character": m.any_alphanumeric_key,
        }
    }


special_marks = {
    "this": {"mark": {"type": "cursor"}},
    "that": {"mark": {"type": "that"}},
    "source": {"mark": {"type": "source"}}
    # "last cursor": {"mark": {"type": "lastCursorPosition"}} # Not implemented
}

mod.list("cursorless_special_mark", desc="Cursorless special marks")
ctx.lists["self.cursorless_special_mark"] = special_marks.keys()


@mod.capture(
    rule=(
        "<user.cursorless_decorated_symbol> | "
        "{user.cursorless_special_mark} |"
        # Because of problems with performance we have to have a simple version for now
        # "<user.cursorless_line_number>" # row, up, down
        "<user.cursorless_line_number_simple>" # up, down
    )
)
def cursorless_mark(m) -> str:
    try: return m.cursorless_decorated_symbol
    except AttributeError: pass
    try: return special_marks[m.cursorless_special_mark]
    except AttributeError: pass
    return m.cursorless_line_number_simple
