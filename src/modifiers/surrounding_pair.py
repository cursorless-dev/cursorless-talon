from talon import Module, app, Context
from ..paired_delimiter import paired_delimiters_map
from ..csv_overrides import init_csv_and_watch_changes

mod = Module()
ctx = Context()


mod.list(
    "cursorless_delimiter_inclusion",
    desc="Whether to include delimiters in surrounding range",
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


# TODO: add these to a "modifiers" csv
# def on_ready():
#     init_csv_and_watch_changes(
#         "modifiers",
#         {
#             "delimiter_inclusion": delimiter_inclusions,
#         },
#     )


# app.register("ready", on_ready)
