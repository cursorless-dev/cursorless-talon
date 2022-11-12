from contextlib import suppress
from typing import Any


BASE_TARGET: dict[str, Any] = {"type": "primitive"}
IMPLICIT_TARGET = {"type": "primitive", "isImplicit": True}


def cursorless_primitive_target(m) -> dict[str, Any]:
    """Supported extents for cursorless navigation"""
    result = BASE_TARGET.copy()

    position_list = []
    with suppress(KeyError):
        position_list = m["position"]
    
    modifier_list = []
    with suppress(KeyError):
        modifier_list.append(m["modifier1"])
        modifier_list.append(m["modifier2"])
        modifier_list.append(m["modifier3"])
        modifier_list.append(m["modifier4"])
    
    modifiers = [
        *position_list,
        *modifier_list,
    ]

    if modifiers:
        result["modifiers"] = modifiers

    with suppress(KeyError):
        result["mark"] = m["mark"]

    return result
