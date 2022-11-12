from typing import Any

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