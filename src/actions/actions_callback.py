from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .call import run_call_action
from .homophones import run_homophones_action
from ..apps.cursorless_vscode import Actions as vscode_actions


@dataclass
class CallbackAction:
    term: str
    identifier: str
    callback: Callable[[dict], Any]


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://www.cursorless.org/docs/user/customization/
callbacks = [
    CallbackAction("call", "callAsFunction", run_call_action),
    CallbackAction(
        "scout", "findInDocument", vscode_actions.cursorless_private_run_find_action
    ),
    # CallbackAction("phones", "nextHomophone", run_homophones_action),
]

callback_action_defaults = {
    callback.term: callback.identifier for callback in callbacks
}
callback_action_map = {callback.identifier: callback.callback for callback in callbacks}