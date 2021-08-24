from talon import app
from .csv_overrides import init_csv_and_watch_changes

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/master/docs/customization.md
range_connectives = {
    "between": "rangeExclusive",
    "past": "rangeInclusive",
    "-": "rangeExcludingStart",
    "until": "rangeExcludingEnd",
}


def on_ready():
    init_csv_and_watch_changes(
        "target_connectives",
        {
            "range_connective": range_connectives,
            "list_connective": {"and": "listConnective"},
            "swap_connective": {"swap": "swapConnective"},
            "source_destination_connective": {"to": "sourceDestinationConnective"},
        },
    )


app.register("ready", on_ready)
