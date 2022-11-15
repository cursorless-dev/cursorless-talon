from typing import Any
from contextlib import suppress

previous_next_modifiers = {"previous": "previous", "next": "next"}
forward_backward_modifiers = {
    "forward": "forward",
    "backward": "backward",
}

def cursorless_relative_direction(m) -> str:
    """Previous/next"""
    return "backward" if m["_node"].words()[0] == "previous" else "forward"


def cursorless_relative_scope_singular(m) -> dict[str, Any]:
    """Relative previous/next singular scope, eg `"next funk"` or `"third next funk"`."""
    ordinals_small = 1
    with suppress(KeyError):
        ordinals_small = m["ordinals_small"]
    return create_relative_scope_modifier(
        m["scope_type"],
        ordinals_small,
        1,
        m["relative_direction"],
    )


def cursorless_relative_scope_plural(m) -> dict[str, Any]:
    """Relative previous/next plural scope. `next three funks`"""
    return create_relative_scope_modifier(
        m["scope_type_plural"],
        1,
        m["number_small"],
        m["relative_direction"],
    )


def cursorless_relative_scope_count(m) -> dict[str, Any]:
    """Relative count scope. `three funks`"""
    forward_backward_modifier = "forward"
    with suppress(KeyError):
        forward_backward_modifier = m["forward_backward_modifier"]
    return create_relative_scope_modifier(
        m["scope_type_plural"],
        0,
        m["number_small"],
        forward_backward_modifier,
    )


def cursorless_relative_scope_one_backward(m) -> dict[str, Any]:
    """Take scope backward, eg `funk backward`"""
    return create_relative_scope_modifier(
        m["scope_type"],
        0,
        1,
        m["forward_backward_modifier"],
    )

# def cursorless_relative_scope(m) -> dict[str, Any]:
#     """Previous/next scope"""
#     return m["_node"].words()[0]


def create_relative_scope_modifier(
    scope_type: dict, offset: int, length: int, direction: str
) -> dict[str, Any]:
    return {
        "type": "relativeScope",
        "scopeType": scope_type,
        "offset": offset,
        "length": length,
        "direction": direction,
    }