from talon import Module, app, Context
from ..paired_delimiter import paired_delimiters_map
from ..csv_overrides import init_csv_and_watch_changes

mod = Module()
ctx = Context()


mod.list(
    "cursorless_delimiter_inclusion",
    desc="Whether to include delimiters in surrounding range",
)

# NB: This is a hack until we support having inside and outside on arbitrary
# scope types
mod.list(
    "cursorless_surrounding_pair_scope_type",
    desc="Scope types that can function as surrounding pairs",
)

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
delimiter_inclusions = {
    "inside": "excludeDelimiters",
    "outside": "includeDelimiters",
    "pair": "delimitersOnly",
}

ctx.lists["user.cursorless_delimiter_inclusion"] = delimiter_inclusions


@mod.capture(
    rule=(
        "[{user.cursorless_delimiter_inclusion}] <user.cursorless_surrounding_pair_scope_type> | "
        "{user.cursorless_delimiter_inclusion}"
    )
)
def cursorless_surrounding_pair(m) -> str:
    """Surrounding pair modifier"""
    try:
        surrounding_pair_scope_type = m.cursorless_surrounding_pair_scope_type
    except AttributeError:
        surrounding_pair_scope_type = "any"

    return {
        "modifier": {
            "type": "surroundingPair",
            "delimiter": surrounding_pair_scope_type,
            "delimiterInclusion": getattr(
                m, "cursorless_delimiter_inclusion", "includeDelimiters"
            ),
        },
    }


@mod.capture(
    rule=(
        "{user.cursorless_paired_delimiter} |"
        "{user.cursorless_surrounding_pair_scope_type}"
    )
)
def cursorless_surrounding_pair_scope_type(m) -> str:
    """Surrounding pair scope type"""
    try:
        return m.cursorless_surrounding_pair_scope_type
    except AttributeError:
        return paired_delimiters_map[m.cursorless_paired_delimiter].cursorlessIdentifier


# TODO: add these to a "modifiers" csv
# def on_ready():
#     init_csv_and_watch_changes(
#         "modifiers",
#         {
#             "delimiter_inclusion": delimiter_inclusions,
#         },
#     )


# app.register("ready", on_ready)
