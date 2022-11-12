from ..csv_overrides import init_csv_and_watch_changes
from .head_tail import head_tail_modifiers
from .interior import interior_modifiers
from .range_type import range_types

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
simple_modifiers = {
    "bounds": "excludeInterior",
    "just": "toRawSelection",
    "leading": "leading",
    "trailing": "trailing",
}

def cursorless_simple_modifier(m) -> dict[str, str]:
    """Simple cursorless modifiers that only need to specify their type"""
    return {
        "type": m["simple_modifier"],
    }


# These are the modifiers that will be "swallowed" by the head/tail modifier.
# For example, saying "head funk" will result in a "head" modifier that will
# select past the start of the function.
# Note that we don't include "inside" here, because that requires slightly
# special treatment to ensure that "head inside round" swallows "inside round"
# rather than just "inside".
head_tail_swallowed_modifiers = [
    "<user.cursorless_simple_modifier>",  # bounds, just, leading, trailing
    "<user.cursorless_containing_scope>",  # funk, state, class
    "<user.cursorless_ordinal_scope>",  # first past second word
    "<user.cursorless_relative_scope>",  # next funk
    "<user.cursorless_surrounding_pair>",  # matching/pair [curly, round]
]

modifiers = [
    "<user.cursorless_interior_modifier>",  # inside
    "<user.cursorless_head_tail_modifier>",  # head, tail
    *head_tail_swallowed_modifiers,
]

def on_ready():
    init_csv_and_watch_changes(
        "modifiers",
        {
            "simple_modifier": simple_modifiers,
            "interior_modifier": interior_modifiers,
            "head_tail_modifier": head_tail_modifiers,
            "range_type": range_types,
        },
    )

on_ready()