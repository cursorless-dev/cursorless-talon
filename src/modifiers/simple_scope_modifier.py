from typing import Any

simple_scope_modifiers = {"every": "every"}

def cursorless_simple_scope_modifier(m) -> dict[str, Any]:
    """Containing scope, every scope, etc"""
    return {
        "type": "everyScope" if m["_node"].words()[0] == "every" else "containingScope",
        "scopeType": m["scope_type"],
    }
