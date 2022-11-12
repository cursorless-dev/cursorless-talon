from ..csv_overrides import SPOKEN_FORM_HEADER, init_csv_and_watch_changes

custom_action_defaults = {}

def on_ready():
    init_csv_and_watch_changes(
        "experimental/actions_custom",
        custom_action_defaults,
        headers=[SPOKEN_FORM_HEADER, "VSCode command"],
        allow_unknown_values=True,
        default_list_name="custom_action",
    )

on_ready()