from talon import Module, app
from dataclasses import dataclass
from .csv_overrides import init_csv_and_watch_changes

mod = Module()
mod.list(
    "cursorless_paired_delimiter", desc="A symbol that comes in pairs, eg brackets"
)


@dataclass
class PairedDelimiter:
    defaultSpokenForm: str
    cursorlessIdentifier: str
    left: str
    right: str


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
    PairedDelimiter("void", "whitespace", " ", " "),
    PairedDelimiter("square", "squareBrackets", "[", "]"),
    PairedDelimiter("twin", "singleQuotes", "'", "'"),
]

paired_delimiters_map = {term.cursorlessIdentifier: term for term in paired_delimiters}

paired_delimiters_defaults = {
    term.defaultSpokenForm: term.cursorlessIdentifier for term in paired_delimiters
}


def on_ready():
    init_csv_and_watch_changes(
        "paired_delimiters",
        {
            "paired_delimiter": paired_delimiters_defaults,
        },
    )


app.register("ready", on_ready)
