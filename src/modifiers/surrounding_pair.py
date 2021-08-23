from talon import Module, app
from dataclasses import dataclass
from ..csv_overrides import init_csv_and_watch_changes

mod = Module()


@dataclass
class PairedDelimiter:
    defaultSpokenForm: str
    cursorlessIdentifier: str
    left: str
    right: str


mod.list(
    "cursorless_paired_delimiter", desc="A symbol that comes in pairs, eg brackets"
)

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/master/docs/customization.md
paired_delimiters = [
    PairedDelimiter("curly", "curlyBrackets", "{", "}"),
    PairedDelimiter("diamond", "angleBrackets", "<", ">"),
    PairedDelimiter("escaped quad", "escapedDoubleQuotes", '\\"', '\\"'),
    PairedDelimiter("escaped twin", "escapedSingleQuotes", "\\'", "\\'"),
    PairedDelimiter("quad", "doubleQuotes", '"', '"'),
    PairedDelimiter("round", "parentheses", "(", ")"),
    PairedDelimiter("skis", "backtickQuotes", "`", "`"),
    PairedDelimiter("space", "spaces", " ", " "),
    PairedDelimiter("square", "squareBrackets", "[", "]"),
    PairedDelimiter("twin", "singleQuotes", "'", "'"),
]

paired_delimiters_map = {term.cursorlessIdentifier: term for term in paired_delimiters}

paired_delimiters_defaults = {
    term.defaultSpokenForm: term.cursorlessIdentifier for term in paired_delimiters
}

mod.list(
    "cursorless_delimiter_inclusion",
    desc="Whether to include delimiters in surrounding range",
)

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/master/docs/customization.md
delimiter_inclusions = {
    "inside": "excludeDelimiters",
    "outside": "includeDelimiters",
    "pair": "delimitersOnly",
}


@mod.capture(
    rule=(
        "[{user.cursorless_delimiter_inclusion}] {user.cursorless_paired_delimiter} | "
        "{user.cursorless_delimiter_inclusion}"
    )
)
def cursorless_surrounding_pair(m) -> str:
    """Surrounding pair modifier"""
    paired_delimiter = getattr(m, "cursorless_paired_delimiter", None)
    if paired_delimiter is None:
        paired_delimiter_identifier = None
    else:
        paired_delimiter_identifier = paired_delimiters_map[
            paired_delimiter
        ].cursorlessIdentifier
    return {
        "modifier": {
            "type": "surroundingPair",
            "delimiter": paired_delimiter_identifier,
            "delimiterInclusion": getattr(
                m, "cursorless_delimiter_inclusion", "includeDelimiters"
            ),
        },
    }


def on_ready():
    init_csv_and_watch_changes(
        "paired_delimiters",
        {
            "paired_delimiter": paired_delimiters_defaults,
        },
    )
    init_csv_and_watch_changes(
        "delimiter_inclusions",
        {
            "delimiter_inclusion": delimiter_inclusions,
        },
    )


app.register("ready", on_ready)
