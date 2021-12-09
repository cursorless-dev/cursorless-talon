from talon import Module, actions
from dataclasses import dataclass


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

makeshift_action_defaults = {
    action.term: action.identifier for action in makeshift_actions
}

makeshift_action_map = {action.identifier: action for action in makeshift_actions}


mod = Module()
mod.list(
    "cursorless_makeshift_action",
    desc="Supported makeshift actions for cursorless navigation",
)


@mod.capture(rule="{user.cursorless_makeshift_action}")
def cursorless_makeshift_action(m) -> callable:
    return lambda targets: run_makeshift_action(m.cursorless_makeshift_action, targets)


def run_makeshift_action(action: str, targets: dict):
    """Execute makeshift action"""
    makeshift_action = makeshift_action_map[action]
    actions.user.cursorless_single_target_command("setSelection", targets)
    actions.sleep(makeshift_action.pre_command_sleep)
    actions.user.vscode(makeshift_action.vscode_command_id)
    actions.sleep(makeshift_action.post_command_sleep)
