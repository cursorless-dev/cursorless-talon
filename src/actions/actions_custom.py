from talon import Module, app, actions
from ..csv_overrides import init_csv_and_watch_changes

custom_action_defaults = {}


mod = Module()
mod.list(
    "cursorless_custom_action",
    desc="Supported custom actions for cursorless navigation",
)


@mod.capture(rule="{user.cursorless_custom_action}")
def cursorless_custom_action(m) -> callable:
    return lambda targets: actions.user.cursorless_single_target_command(
        "runCommandOnSelection", targets, m.cursorless_custom_action
    )


def on_ready():
    init_csv_and_watch_changes(
        "actions_custom",
        custom_action_defaults,
        allow_unknown_values=True,
        default_list_name="custom_action",
    )


app.register("ready", on_ready)
