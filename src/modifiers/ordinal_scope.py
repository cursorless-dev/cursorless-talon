from typing import Any
from contextlib import suppress

from ..compound_targets import is_active_included, is_anchor_included

def ordinal_or_last(m) -> int:
    """An ordinal or the word 'last'"""
    if m["_node"].words()[0] == "last":
        return -1
    return m["ordinals_small"] - 1

def cursorless_ordinal_range(m) -> dict[str, Any]:
    """Ordinal range"""
    ordinal_or_last_list = [m["ordinal_or_last1"]]
    with suppress(KeyError):
        ordinal_or_last_list.append(m["ordinal_or_last2"])

    if len(ordinal_or_last_list) > 1:
        range_connective = m["range_connective"]
        include_anchor = is_anchor_included(range_connective)
        include_active = is_active_included(range_connective)
        anchor = create_ordinal_scope_modifier(
            m["scope_type"], ordinal_or_last_list[0]
        )
        active = create_ordinal_scope_modifier(
            m["scope_type"], ordinal_or_last_list[1]
        )
        return {
            "type": "range",
            "anchor": anchor,
            "active": active,
            "excludeAnchor": not include_anchor,
            "excludeActive": not include_active,
        }
    else:
        return create_ordinal_scope_modifier(
            m["scope_type"], ordinal_or_last_list[0]
        )

def cursorless_first_last(m) -> dict[str, Any]:
    """First/last `n` scopes; eg "first three funk"""
    if m["_node"].words()[0] == "first":
        return create_ordinal_scope_modifier(
            m["scope_type"], 0, m["number_small"]
        )
    return create_ordinal_scope_modifier(
        m["scope_type"], -m["number_small"], m["number_small"]
    )

def create_ordinal_scope_modifier(scope_type: Any, start: int, length: int = 1):
    return {
        "type": "ordinalScope",
        "scopeType": scope_type,
        "start": start,
        "length": length,
    }
