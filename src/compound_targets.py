from .primitive_target import BASE_TARGET
from talon import Module

mod = Module()

mod.list(
    "cursorless_range_connective",
    desc="A range joiner that indicates whether to include or exclude anchor and active",
)
mod.list(
    "cursorless_list_connective",
    desc="A list joiner",
)


@mod.capture(
    rule=(
        "<user.cursorless_primitive_target> | "
        "[<user.cursorless_range_type>] {user.cursorless_range_connective} <user.cursorless_primitive_target> | "
        "<user.cursorless_primitive_target> [<user.cursorless_range_type>] {user.cursorless_range_connective} <user.cursorless_primitive_target>"
    )
)
def cursorless_range(m) -> str:
    primitive_targets = m.cursorless_primitive_target_list
    range_connective = getattr(m, "cursorless_range_connective", None)

    if range_connective is None:
        return primitive_targets[0]

    if len(primitive_targets) == 1:
        start = BASE_TARGET.copy()
    else:
        start = primitive_targets[0]

    try:
        range_type = m.cursorless_range_type
    except AttributeError:
        range_type = None

    return {
        "type": "range",
        "start": start,
        "end": primitive_targets[-1],
        "excludeStart": not is_anchor_included(range_connective),
        "excludeEnd": not is_active_included(range_connective),
        "rangeType": range_type,
    }


def is_anchor_included(range_connective: str):
    return range_connective not in ["rangeExclusive", "rangeExcludingStart"]


def is_active_included(range_connective: str):
    return range_connective not in ["rangeExclusive", "rangeExcludingEnd"]


@mod.capture(
    rule="<user.cursorless_range> ({user.cursorless_list_connective} <user.cursorless_range>)*"
)
def cursorless_target(m) -> dict:
    if len(m.cursorless_range_list) == 1:
        return m.cursorless_range
    return {"type": "list", "elements": m.cursorless_range_list}
