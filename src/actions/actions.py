from typing import Any
from talon import Module, app
from ..csv_overrides import init_csv_and_watch_changes
from .actions_simple import simple_action_defaults
from .actions_callback import callback_action_defaults
from .actions_makeshift import makeshift_action_defaults
from .actions_custom import custom_action_defaults

mod = Module()


@mod.capture(
    rule=(
        "<user.cursorless_simple_action> |"
        "<user.cursorless_makeshift_action> |"
        "<user.cursorless_callback_action> |"
        "<user.cursorless_custom_action>"
    )
)
def cursorless_action(m) -> callable:
    return m[0]


@mod.action_class
class Actions:
    def cursorless_action(callback: Any, targets: dict):
        """Perform cursorless action"""
        return callback(targets)


default_values = {
    "simple_action": simple_action_defaults,
    "callback_action": callback_action_defaults,
    "makeshift_action": makeshift_action_defaults,
    "custom_action": custom_action_defaults,
    "swap_action": {"swap": "swapTargets"},
    "move_bring_action": {"bring": "replaceWithTarget", "move": "moveToTarget"},
    "wrap_action": {"wrap": "wrapWithPairedDelimiter", "repack": "rewrap"},
    "reformat_action": {"format": "applyFormatter"},
}


ACTION_LIST_NAMES = default_values.keys()


def on_ready():
    init_csv_and_watch_changes("actions", default_values)


app.register("ready", on_ready)
