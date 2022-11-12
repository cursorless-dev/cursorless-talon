from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from contextlib import suppress

from ..compound_targets import is_active_included, is_anchor_included

@dataclass
class CustomizableTerm:
    defaultSpokenForm: str
    cursorlessIdentifier: str
    type: str
    formatter: Callable


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
directions = [
    CustomizableTerm(
        "row", "lineNumberModulo100", "modulo100", lambda number: number - 1
    ),
    CustomizableTerm("up", "lineNumberRelativeUp", "relative", lambda number: -number),
    CustomizableTerm(
        "down", "lineNumberRelativeDown", "relative", lambda number: number
    ),
]

directions_map = {d.cursorlessIdentifier: d for d in directions}
DEFAULT_DIRECTIONS = {d.defaultSpokenForm: d.cursorlessIdentifier for d in directions}


def cursorless_line_number(m) -> dict[str, Any]:
    direction = directions_map[m["line_direction"]]
    numbers = [m["n100_1"]]
    with suppress(KeyError):
        numbers.append(m["n100_2"])
        
    anchor = create_line_number_mark(
        direction.type, direction.formatter(numbers[0])
    )
    if len(numbers) > 1:
        active = create_line_number_mark(
            direction.type, direction.formatter(numbers[1])
        )
        include_anchor = is_anchor_included(m["range_connective"])
        include_active = is_active_included(m["range_connective"])
        return {
            "type": "range",
            "anchor": anchor,
            "active": active,
            "excludeAnchor": not include_anchor,
            "excludeActive": not include_active,
        }
    return anchor


def create_line_number_mark(line_number_type: str, line_number: int) -> dict[str, Any]:
    return {
        "type": "lineNumber",
        "lineNumberType": line_number_type,
        "lineNumber": line_number,
    }
