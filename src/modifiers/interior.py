# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
interior_modifiers = {
    "inside": "interiorOnly",
}

def cursorless_interior_modifier(m) -> dict[str, str]:
    """Cursorless interior modifier"""
    return {
        "type": m["interior_modifier"],
    }