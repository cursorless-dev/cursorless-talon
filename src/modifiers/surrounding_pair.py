from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

surrounding_pairs = {
    "angle": "angleBrackets",
    "diamond": "angleBrackets",
    "curly": "curlyBrackets",
    "round": "parentheses",
    "square": "squareBrackets",
    "quad": "doubleQuotes",
    "twin": "singleQuotes",
}

mod.list("cursorless_surrounding_pair", desc="A surrounding air symbol")
ctx.lists["self.cursorless_surrounding_pair"] = surrounding_pairs


@mod.capture(rule=("{user.cursorless_surrounding_pair}"))
def cursorless_surrounding_pair(m) -> str:
    """Supported extents for cursorless navigation"""
    return {
        "transformation": {
            "type": "surroundingPair",
            "delimiter": m.cursorless_surrounding_pair
        }
    }
