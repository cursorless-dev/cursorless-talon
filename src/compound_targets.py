from typing import Any
from contextlib import suppress

from .connective import default_range_connective
from .primitive_target import BASE_TARGET

def cursorless_range_connective_with_type(m) -> dict[str, Any]:
    connective = default_range_connective
    with suppress(KeyError):
        connective = m["range_connective"]
    
    range_type = None
    with suppress(KeyError):
        range_type = m["range_type"]
    
    return {
        "connective": connective,
        "type": range_type,
    }

def cursorless_range(m) -> dict[str, Any]:
    primitive_targets = [m["primitive_target1"]]
    with suppress(KeyError):
        primitive_targets.append(m["primitive_target2"])
    
    range_connective_with_type = {}
    try:
        range_connective_with_type = m["range_connective_with_type"]
    except KeyError:
        return primitive_targets[0]

    if len(primitive_targets) == 1:
        anchor = BASE_TARGET.copy()
    else:
        anchor = primitive_targets[0]

    range_connective = range_connective_with_type["connective"]
    range_type = range_connective_with_type["type"]

    range = {
        "type": "range",
        "anchor": anchor,
        "active": primitive_targets[-1],
        "excludeAnchor": not is_anchor_included(range_connective),
        "excludeActive": not is_active_included(range_connective),
    }

    if range_type:
        range["rangeType"] = range_type

    return range


def is_anchor_included(range_connective: str):
    return range_connective not in ["rangeExclusive", "rangeExcludingStart"]


def is_active_included(range_connective: str):
    return range_connective not in ["rangeExclusive", "rangeExcludingEnd"]


def cursorless_target(m) -> dict:
    ranges = [m["range"]]
    range_repeating = m["range_repetition"]
    for connective_range in range_repeating:
        range_dict = connective_range[1]
        ranges.append(range_dict)
    
    if len(ranges) == 1:
        return ranges[0]            
    return {
        "type": "list",
        "elements": ranges,
    }
    
    # ranges = [m["range1"]]
    # with suppress(KeyError):
    #     ranges.append(m["range2"])
    #     ranges.append(m["range3"])
    #     ranges.append(m["range4"])
    #     ranges.append(m["range5"])
    
    # if len(ranges) == 1:
    #     return ranges[0]            
    # return {
    #     "type": "list",
    #     "elements": ranges,
    # }
    