from typing import Any

from ..csv_overrides import init_csv_and_watch_changes

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
positions = {
    "start of": "start",
    "end of": "end",
    "before": "before",
    "after": "after",
}


def construct_positional_modifier(position: str) -> dict[str, Any]:
    return {"type": "position", "position": position}

def on_ready():
    init_csv_and_watch_changes(
        "positions",
        {"position": positions},
    )

on_ready()