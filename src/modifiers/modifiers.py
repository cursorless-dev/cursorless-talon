from talon import app
from ..csv_overrides import init_csv_and_watch_changes
from .range_type import range_types


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md

delimiter_inclusions = {
    "inside": "interiorOnly",
    "bound": "excludeInterior",
}


def on_ready():
    init_csv_and_watch_changes(
        "modifiers",
        {
            "delimiter_inclusion": delimiter_inclusions,
            "range_type": range_types,
        },
    )


app.register("ready", on_ready)
