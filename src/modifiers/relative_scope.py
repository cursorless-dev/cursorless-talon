from typing import Any

previous_next_modifiers = {"previous": "previous", "next": "next"}
forward_backward_modifiers = {
    "forward": "forward",
    "backward": "backward",
}

def cursorless_relative_direction(m) -> str:
    """Previous/next"""
    return "backward" if m[0] == "previous" else "forward"


def cursorless_relative_scope_singular(m) -> dict[str, Any]:
    """Relative previous/next singular scope, eg `"next funk"` or `"third next funk"`."""
    return create_relative_scope_modifier(
        m.cursorless_scope_type,
        getattr(m, "ordinals_small", 1),
        1,
        m.cursorless_relative_direction,
    )


def cursorless_relative_scope_plural(m) -> dict[str, Any]:
    """Relative previous/next plural scope. `next three funks`"""
    return create_relative_scope_modifier(
        m.cursorless_scope_type_plural,
        1,
        m.private_cursorless_number_small,
        m.cursorless_relative_direction,
    )


def cursorless_relative_scope_count(m) -> dict[str, Any]:
    """Relative count scope. `three funks`"""
    return create_relative_scope_modifier(
        m.cursorless_scope_type_plural,
        0,
        m.private_cursorless_number_small,
        getattr(m, "cursorless_forward_backward_modifier", "forward"),
    )


def cursorless_relative_scope_one_backward(m) -> dict[str, Any]:
    """Take scope backward, eg `funk backward`"""
    return create_relative_scope_modifier(
        m.cursorless_scope_type,
        0,
        1,
        m.cursorless_forward_backward_modifier,
    )


def cursorless_relative_scope(m) -> dict[str, Any]:
    """Previous/next scope"""
    direction = "forward"
    words = m["_node"].words()
    if words[0] == "previous" or words[0] == "prior":
        direction = "backward"
    return {
        "type": "relativeScope",
        "scopeType": m["scope_type"],
        "offset": 1,
        "length": 1,
        "direction": direction,
    }
