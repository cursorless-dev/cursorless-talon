from talon import Context, Module, actions
from dataclasses import dataclass
from .homophones import run_homophones_action
from .find import run_find_action

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.cursorless
"""


@dataclass
class MakeshiftAction:
    term: str
    vscode_command_id: str
    pre_command_sleep: float = 0
    post_command_sleep: float = 0


makeshift_actions = [
    MakeshiftAction("define", "editor.action.revealDefinition"),
    MakeshiftAction("drink cell", "jupyter.insertCellAbove"),
    MakeshiftAction("hover", "editor.action.showHover"),
    MakeshiftAction("inspect", "editor.debug.action.showDebugHover"),
    MakeshiftAction("pour cell", "jupyter.insertCellBelow"),
    MakeshiftAction("quick fix", "editor.action.quickFix", pre_command_sleep=0.3),
    MakeshiftAction("reference", "references-view.find"),
    MakeshiftAction("rename", "editor.action.rename", post_command_sleep=0.1),
]

makeshift_action_map = {action.term: action for action in makeshift_actions}


@dataclass
class CallbackAction:
    term: str
    action: str
    callback: callable


callbacks = [
    CallbackAction("find", "find", run_find_action),
    CallbackAction("phones", "nextHomophone", run_homophones_action),
]

callbacks_map = {callback.action: callback.callback for callback in callbacks}


mod.list("cursorless_simple_action", desc="Supported actions for cursorless navigation")
ctx.lists["self.cursorless_simple_action"] = {
    "bottom": "scrollToBottom",
    "breakpoint": "setBreakpoint",
    "carve": "cut",
    "center": "scrollToCenter",
    "chuck": "delete",
    "clear": "clear",
    "comment": "commentLines",
    "copy": "copy",
    "dedent": "outdentLines",
    "drink": "editNewLineAbove",
    "drop": "insertEmptyLineAbove",
    "clone": "copyLinesDown",
    "clone up": "copyLinesUp",
    "extract": "extractVariable",
    "find all": "findInFiles",
    "float": "insertEmptyLineBelow",
    "fold": "fold",
    "indent": "indentLines",
    "paste to": "paste",
    "post": "setSelectionAfter",
    "pour": "editNewLineBelow",
    "pre": "setSelectionBefore",
    "puff": "insertEmptyLinesAround",
    "reverse": "reverse",
    "sort": "sort",
    "take": "setSelection",
    "top": "scrollToTop",
    "unfold": "unfold",
    **{callback.term: callback.action for callback in callbacks},
    **{action.term: action.term for action in makeshift_actions},
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
