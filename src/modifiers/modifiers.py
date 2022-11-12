from ..csv_overrides import init_csv_and_watch_changes
from .head_tail import head_tail_modifiers
from .interior import interior_modifiers
from .ordinal_scope import first_modifiers, last_modifiers
from .range_type import range_types
<<<<<<< HEAD
from .relative_scope import forward_backward_modifiers, previous_next_modifiers
from .simple_scope_modifier import simple_scope_modifiers
=======
>>>>>>> 9162137b7b93ff1450ed8be4b41bc47737eb3283

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
simple_modifiers = {
    "bounds": "excludeInterior",
    "just": "toRawSelection",
    "leading": "leading",
    "trailing": "trailing",
    "content": "keepContentFilter",
    "empty": "keepEmptyFilter",
    "its": "inferPreviousMark",
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
    "<user.cursorless_simple_scope_modifier>",  # funk, state, class, every funk
    "<user.cursorless_ordinal_scope>",  # first past second word
    "<user.cursorless_relative_scope>",  # next funk, 3 funks
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
            "simple_scope_modifier": simple_scope_modifiers,
            "first_modifier": first_modifiers,
            "last_modifier": last_modifiers,
            "previous_next_modifier": previous_next_modifiers,
            "forward_backward_modifier": forward_backward_modifiers,
        },
    )

on_ready()