from dataclasses import dataclass
from talon import Context, Module
from .modifiers.selection_type import SELECTION_TYPE_KEY, RANKED_SELECTION_TYPES

ctx = Context()
mod = Module()

ctx.matches = r"""
tag: user.cursorless
"""

BASE_TARGET = {"type": "primitive"}
STRICT_HERE = {
    "type": "primitive",
    "mark": {"type": "cursor"},
    "selectionType": "token",
    "position": "contents",
    "transformation": {"type": "identity"},
    "insideOutsideType": "inside"
}

parameters = [
    "<user.cursorless_position>",             # before, above, end of
    "<user.cursorless_selection_type>",       # token, line, file
    "<user.cursorless_containing_scope>",     # funk, state, class
    "<user.cursorless_subtoken>"              # first past second word

    # "<user.cursorless_inside_outside>",       # inner, outer
    # "<user.cursorless_surrounding_pair>",     # curly, round
    # "<user.cursorless_matching_pair_symbol>", # matching
]

parameters_and_mark = (
    f"({'|'.join(parameters)})* "   # 0 or more parameters
    "<user.cursorless_mark>"        # 1 mark
)

parameters_only = (
    f"({'|'.join(parameters)})+"   # 1 or more parameters
)


@mod.capture(rule=f"({parameters_and_mark}) | ({parameters_only})")
def cursorless_primitive_target(m) -> str:
    """Supported extents for cursorless navigation"""
    object = BASE_TARGET.copy()
    for capture in m:
        for key, value in capture.items():
            if (
                key in object
                and key == SELECTION_TYPE_KEY
                and RANKED_SELECTION_TYPES[value] < RANKED_SELECTION_TYPES[object[key]]
            ):
                continue
            object[key] = value
    return object
