from talon import Context, Module, actions, app
from dataclasses import dataclass
from ..csv_overrides import init_csv_and_watch_changes
from .homophones import run_homophones_action
from .find import run_find_action
from .call import run_call_action

mod = Module()

ctx = Context()


@dataclass
class MakeshiftAction:
    term: str
    identifier: str
    vscode_command_id: str
    pre_command_sleep: float = 0
    post_command_sleep: float = 0


makeshift_actions = [
    MakeshiftAction("drink cell", "editNewCellAbove", "jupyter.insertCellAbove"),
    MakeshiftAction("define", "revealDefinition", "editor.action.revealDefinition"),
    MakeshiftAction("hover", "showHover", "editor.action.showHover"),
    MakeshiftAction("inspect", "showDebugHover", "editor.debug.action.showDebugHover"),
    MakeshiftAction("pour cell", "editNewCellBelow", "jupyter.insertCellBelow"),
    MakeshiftAction(
        "quick fix", "quickFix", "editor.action.quickFix", pre_command_sleep=0.3
    ),
    MakeshiftAction("reference", "showReferences", "references-view.find"),
    MakeshiftAction("rename", "rename", "editor.action.rename", post_command_sleep=0.1),
]

makeshift_action_map = {action.identifier: action for action in makeshift_actions}


@dataclass
class CallbackAction:
    term: str
    identifier: str
    callback: callable


callbacks = [
    CallbackAction("call", "call", run_call_action),
    CallbackAction("scout", "find", run_find_action),
    CallbackAction("phones", "nextHomophone", run_homophones_action),
]

callbacks_map = {callback.identifier: callback.callback for callback in callbacks}


mod.list("cursorless_simple_action", desc="Supported actions for cursorless navigation")


simple_actions = {
    "bottom": "scrollToBottom",
    "breakpoint": "setBreakpoint",
    "carve": "cut",
    "center": "scrollToCenter",
    "chuck": "delete",
    "clear": "clear",
    "clone up": "copyLinesUp",
    "clone": "copyLinesDown",
    "comment": "commentLines",
    "copy": "copy",
    "crown": "scrollToTop",
    "dedent": "outdentLines",
    "drink": "editNewLineAbove",
    "drop": "insertEmptyLineAbove",
    "extract": "extractVariable",
    "float": "insertEmptyLineBelow",
    "fold": "fold",
    "indent": "indentLines",
    "paste to": "paste",
    "post": "setSelectionAfter",
    "pour": "editNewLineBelow",
    "pre": "setSelectionBefore",
    "puff": "insertEmptyLinesAround",
    "reverse": "reverse",
    "scout all": "findInFiles",
    "sort": "sort",
    "take": "setSelection",
    "unfold": "unfold",
    **{action.term: action.identifier for action in makeshift_actions},
    **{callback.term: callback.identifier for callback in callbacks},
}


@mod.action_class
class Actions:
    def cursorless_simple_action(action: str, targets: dict):
        """Perform cursorless simple action"""
        if action in callbacks_map:
            return callbacks_map[action](targets)
        elif action in makeshift_action_map:
            return run_makeshift_action(action, targets)
        else:
            return actions.user.cursorless_single_target_command(action, targets)


def run_makeshift_action(action: str, targets: dict):
    """Execute makeshift action"""
    makeshift_action = makeshift_action_map[action]
    actions.user.cursorless_single_target_command("setSelection", targets)
    actions.sleep(makeshift_action.pre_command_sleep)
    actions.user.vscode(makeshift_action.vscode_command_id)
    actions.sleep(makeshift_action.post_command_sleep)


all_actions = [
    ["simple", simple_actions],
    ["swap", {"swap": "swap"}],
    ["move_bring", {"bring": "bring", "move": "move"}],
    ["wrap", {"wrap": "wrap"}],
    ["reformat", {"format": "format"}],
]

action_list_names = [line[0] for line in all_actions]
default_action_values = [line[1] for line in all_actions]


def on_csv_change(updated_dicts):
    for i in range(len(action_list_names)):
        list_name = action_list_names[i]
        ctx.lists[f"self.cursorless_{list_name}_action"] = updated_dicts[i]


def on_ready():
    init_csv_and_watch_changes("actions", default_action_values, on_csv_change)


app.register("ready", on_ready)
