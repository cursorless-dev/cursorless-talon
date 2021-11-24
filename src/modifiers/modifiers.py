from talon import app
from ..csv_overrides import init_csv_and_watch_changes

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
delimiter_inclusions = {
    "inside": "interiorOnly",
    "pair": "excludeInterior",
}


def on_ready():
    init_csv_and_watch_changes(
        "modifiers",
        {
            "delimiter_inclusion": delimiter_inclusions,
        },
    )


app.register("ready", on_ready)
