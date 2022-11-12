from contextlib import suppress

head_tail_modifiers = {
    "head": "extendThroughStartOf",
    "tail": "extendThroughEndOf",
}

def cursorless_head_tail_modifier(m) -> dict[str, str]:
    """Cursorless head and tail modifier"""
    modifiers = []

    with suppress(KeyError):
        modifiers.append(m["interior_modifier"])

    with suppress(KeyError):
        modifiers.append(m["head_tail_swallowed_modifier"])

    result = {
        "type": m["head_tail_modifier"],
    }

    if modifiers:
        result["modifiers"] = modifiers

    return result
