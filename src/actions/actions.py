from talon import Module, actions, app
from dataclasses import dataclass
from ..csv_overrides import init_csv_and_watch_changes
from .homophones import run_homophones_action
from .find import run_find_action
from .call import run_call_action

mod = Module()


@dataclass
class MakeshiftAction:
    term: str
    identifier: str
    vscode_command_id: str
    pre_command_sleep: float = 0
    post_command_sleep: float = 0


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
makeshift_actions = [
    MakeshiftAction("define", "revealDefinition", "editor.action.revealDefinition"),
    MakeshiftAction(
        "type deaf", "revealTypeDefinition", "editor.action.goToTypeDefinition"
    ),
    MakeshiftAction("hover", "showHover", "editor.action.showHover"),
    MakeshiftAction("inspect", "showDebugHover", "editor.debug.action.showDebugHover"),
    MakeshiftAction(
        "quick fix", "showQuickFix", "editor.action.quickFix", pre_command_sleep=0.3
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


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
callbacks = [
    CallbackAction("call", "callAsFunction", run_call_action),
    CallbackAction("scout", "findInDocument", run_find_action),
    CallbackAction("phones", "nextHomophone", run_homophones_action),
]

callbacks_map = {callback.identifier: callback.callback for callback in callbacks}


@dataclass
class ComplexAction:
    defaultSpokenForm: str
    identifier: str
    action: str
    args: list[any]


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
complex_actions = [
    ComplexAction(
        "-quick list",
        "experimentalListCodeActions",
        "executeCodeAction",
        [{"onlyDisplayInfo": True}],
    ),
]

complex_action_map = {action.identifier: action for action in complex_actions}


mod.list("cursorless_simple_action", desc="Supported actions for cursorless navigation")


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
simple_actions = {
    "bottom": "scrollToBottom",
    "breakpoint": "toggleLineBreakpoint",
    "carve": "cutToClipboard",
    "center": "scrollToCenter",
    "chuck": "remove",
    "clear": "clearAndSetSelection",
    "clone up": "insertCopyBefore",
    "clone": "insertCopyAfter",
    "comment": "toggleLineComment",
    "copy": "copyToClipboard",
    "crown": "scrollToTop",
    "dedent": "outdentLine",
    "drink": "editNewLineBefore",
    "drop": "insertEmptyLineBefore",
    "extract": "extractVariable",
    "float": "insertEmptyLineAfter",
    "fold": "foldRegion",
    "indent": "indentLine",
    "paste to": "pasteFromClipboard",
    "post": "setSelectionAfter",
    "pour": "editNewLineAfter",
    "pre": "setSelectionBefore",
    "puff": "insertEmptyLinesAround",
    "reverse": "reverseTargets",
    "scout all": "findInWorkspace",
    "sort": "sortTargets",
    "take": "setSelection",
    "unfold": "unfoldRegion",
    **{action.term: action.identifier for action in makeshift_actions},
    **{callback.term: callback.identifier for callback in callbacks},
    **{
        complex_action.defaultSpokenForm: complex_action.identifier
        for complex_action in complex_actions
    },
}


@mod.action_class
class Actions:
    def cursorless_simple_action(action: str, targets: dict):
        """Perform cursorless simple action"""
        if action in callbacks_map:
            return callbacks_map[action](targets)
        elif action in makeshift_action_map:
            return run_makeshift_action(action, targets)
        elif action in complex_action_map:
            action_info = complex_action_map[action]
            return actions.user.cursorless_single_target_command(
                action_info.action, targets, *action_info.args
            )
        else:
            return actions.user.cursorless_single_target_command(action, targets)


def run_makeshift_action(action: str, targets: dict):
    """Execute makeshift action"""
    makeshift_action = makeshift_action_map[action]
    actions.user.cursorless_single_target_command("setSelection", targets)
    actions.sleep(makeshift_action.pre_command_sleep)
    actions.user.vscode(makeshift_action.vscode_command_id)
    actions.sleep(makeshift_action.post_command_sleep)


@mod.capture(
    rule=(
        "{user.cursorless_simple_action} | "
        "{user.cursorless_experimental_quick_code_action}"
    )
)
def cursorless_simple_action(m) -> str:
    try:
        return m.cursorless_simple_action
    except AttributeError:
        return m.cursorless_experimental_quick_code_action


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
default_values = {
    "simple_action": simple_actions,
    "swap_action": {"swap": "swapTargets"},
    "move_bring_action": {"bring": "replaceWithTarget", "move": "moveToTarget"},
    "wrap_action": {"wrap": "wrapWithPairedDelimiter"},
    "reformat_action": {"format": "applyFormatter"},
}

ACTION_LIST_NAMES = default_values.keys()


def on_ready():
    init_csv_and_watch_changes("actions", default_values)


app.register("ready", on_ready)
