from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""


mod.list("cursorless_pair_symbol", desc="A symbol that comes in pairs, eg brackets")
ctx.lists["self.cursorless_pair_symbol"] = {
    "skis": "backtickQuotes",
    "curly": "curlyBrackets",
    "diamond": "angleBrackets",
    "quad": "doubleQuotes",
    "round": "parentheses",
    "square": "squareBrackets",
    "twin": "singleQuotes",
}

mod.list(
    "cursorless_delimiter_inclusion",
    desc="Whether to include delimiters in surrounding range",
)
ctx.lists["self.cursorless_delimiter_inclusion"] = {
    "inside": "excludeDelimiters",
    "outside": "includeDelimiters",
    "pair": "delimitersOnly",
}


@mod.capture(
    rule=(
        "[{user.cursorless_delimiter_inclusion}] {user.cursorless_pair_symbol} | "
        "{user.cursorless_delimiter_inclusion}"
    )
)
def cursorless_surrounding_pair(m) -> str:
    """Surrounding pair modifier"""
    return {
        "modifier": {
            "type": "surroundingPair",
            "delimiter": getattr(m, "cursorless_pair_symbol", None),
            "delimiterInclusion": getattr(
                m, "cursorless_delimiter_inclusion", "includeDelimiters"
            ),
        },
    }
