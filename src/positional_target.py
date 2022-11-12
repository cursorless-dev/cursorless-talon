from typing import Any

from .modifiers.position import construct_positional_modifier

def cursorless_positional_target(m) -> dict[str, Any]:
    target: dict[str, Any] = m["target"]
    try:
        modifier = construct_positional_modifier(m["position"])
        return update_first_primitive_target(target, modifier)
    except KeyError:
        return target


def update_first_primitive_target(target: dict[str, Any], modifier: dict[str, Any]):
    if target["type"] == "primitive":
        if "modifiers" not in target:
            target["modifiers"] = []
        target["modifiers"].insert(0, modifier)
        return target
    elif target["type"] == "range":
        return {
            **target,
            "anchor": update_first_primitive_target(target["anchor"], modifier),
        }
    else:
        elements = target["elements"]
        return {
            **target,
            "elements": [
                update_first_primitive_target(elements[0], modifier),
                *elements[1:],
            ],
        }
