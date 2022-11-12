from contextlib import suppress
from typing import Any

from ..paired_delimiter import paired_delimiters_map

def cursorless_surrounding_pair_scope_type(m) -> str:
    """Surrounding pair scope type"""
    try:
        return m["surrounding_pair_scope_type"]
    except KeyError:
        return paired_delimiters_map[
            m["selectable_paired_delimiter"]
        ].cursorlessIdentifier

def cursorless_surrounding_pair(m) -> dict[str, Any]:
    """Expand to containing surrounding pair"""
    surrounding_pair_scope_type = "any"
    with suppress(KeyError):
        surrounding_pair_scope_type = m["surrounding_pair_scope_type"]
    
    scope_type = {
        "type": "surroundingPair",
        "delimiter": surrounding_pair_scope_type,
    }

    with suppress(KeyError):
        scope_type["forceDirection"] = m["delimiter_force_direction"]

    return {
        "type": "containingScope",
        "scopeType": scope_type,
    }
