from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""


mod.list("cursorless_pair_symbol", desc="A symbol that comes in pairs, eg brackets")
ctx.lists["self.cursorless_pair_symbol"] = {
    "diamond": "angleBrackets",
    "curly": "curlyBrackets",
    "round": "parentheses",
    "square": "squareBrackets",
    "quad": "doubleQuotes",
    "twin": "singleQuotes",
    "brick": "backtickQuotes"
}


@mod.capture(rule=("(matching | pair) [{user.cursorless_pair_symbol}]"))
def cursorless_surrounding_pair(m) -> str:
    """Surrounding pair modifier"""
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
