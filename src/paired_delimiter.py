from talon import Module, app
from dataclasses import dataclass
from .csv_overrides import init_csv_and_watch_changes

mod = Module()
mod.list(
    "cursorless_paired_delimiter", desc="A symbol that comes in pairs, eg brackets"
)
mod.list(
    "cursorless_wrappable_only_paired_delimiter",
    desc="A paired delimiter that can be used as a wrapper",
)
mod.list(
    "cursorless_selectable_only_paired_delimiter",
    desc="A paired delimiter that can be used as a scope type",
)
mod.list(
    "cursorless_wrappable_selectable_paired_delimiter",
    desc="A paired delimiter that can be used as a scope type and as a wrapper",
)


@dataclass
class PairedDelimiter:
    defaultSpokenForm: str
    cursorlessIdentifier: str
    left: str
    right: str

    # Indicates whether the delimiter can be used to wrap a target
    is_wrappable: bool = True

    # Indicates whether the delimiter can be used for expanding to surrounding
    # pair.
    is_selectable: bool = True


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
paired_delimiters = [
    PairedDelimiter("curly", "curlyBrackets", "{", "}"),
    PairedDelimiter("diamond", "angleBrackets", "<", ">"),
    PairedDelimiter("escaped quad", "escapedDoubleQuotes", '\\"', '\\"'),
    PairedDelimiter("escaped twin", "escapedSingleQuotes", "\\'", "\\'"),
    PairedDelimiter("escaped round", "escapedParentheses", "\\(", "\\)"),
    PairedDelimiter("quad", "doubleQuotes", '"', '"'),
    PairedDelimiter("round", "parentheses", "(", ")"),
    PairedDelimiter("skis", "backtickQuotes", "`", "`"),
    PairedDelimiter("void", "whitespace", " ", " ", is_selectable=False),
    PairedDelimiter("square", "squareBrackets", "[", "]"),
    PairedDelimiter("twin", "singleQuotes", "'", "'"),
    PairedDelimiter("outside", "any", "", "", is_wrappable=False),
]

paired_delimiters_map = {term.cursorlessIdentifier: term for term in paired_delimiters}

wrappable_paired_delimiters_defaults = {
    term.defaultSpokenForm: term.cursorlessIdentifier
    for term in paired_delimiters
    if term.is_wrappable and not term.is_selectable
}

selectable_paired_delimiters_defaults = {
    term.defaultSpokenForm: term.cursorlessIdentifier
    for term in paired_delimiters
    if term.is_selectable and not term.is_wrappable
}

wrappable_selectable_paired_delimiters_defaults = {
    term.defaultSpokenForm: term.cursorlessIdentifier
    for term in paired_delimiters
    if term.is_selectable and term.is_wrappable
}


@mod.capture(
    rule=(
        "{user.cursorless_wrappable_only_paired_delimiter} |"
        "{user.cursorless_wrappable_selectable_paired_delimiter}"
    )
)
def cursorless_wrappable_paired_delimiter(m) -> str:
    try:
        return m.cursorless_wrappable_only_paired_delimiter
    except AttributeError:
        return m.cursorless_wrappable_selectable_paired_delimiter


@mod.capture(
    rule=(
        "{user.cursorless_selectable_only_paired_delimiter} |"
        "{user.cursorless_wrappable_selectable_paired_delimiter}"
    )
)
def cursorless_selectable_paired_delimiter(m) -> str:
    try:
        return m.cursorless_selectable_only_paired_delimiter
    except AttributeError:
        return m.cursorless_wrappable_selectable_paired_delimiter


def on_ready():
    init_csv_and_watch_changes(
        "paired_delimiters",
        {
            "wrappable_only_paired_delimiter": wrappable_paired_delimiters_defaults,
            "selectable_only_paired_delimiter": selectable_paired_delimiters_defaults,
            "wrappable_selectable_paired_delimiter": wrappable_selectable_paired_delimiters_defaults,
        },
    )


app.register("ready", on_ready)
