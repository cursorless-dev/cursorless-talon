from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

pair_symbols = {
    "diamond": "angleBrackets",
    "curly": "curlyBrackets",
    "round": "parentheses",
    "square": "squareBrackets",
    "quad": "doubleQuotes",
    "twin": "singleQuotes",
}

mod.list("cursorless_pair_symbol", desc="A symbol that comes in pairs, eg brackets")
ctx.lists["self.cursorless_pair_symbol"] = pair_symbols


@mod.capture(
    rule=(
        "matching | {user.cursorless_pair_symbol} | pair [{user.cursorless_pair_symbol}] "
    )
)
def cursorless_surrounding_pair(m) -> str:
    """Surrounding pair modifiers"""
    try:
        cursorless_pair_symbol = m.cursorless_pair_symbol
    except AttributeError:
        cursorless_pair_symbol = None
    return {
        "modifier": {
            "type": "surroundingPair",
            "delimiter": cursorless_pair_symbol,
            "delimitersOnly": m[0] == "pair",
        }
    }
