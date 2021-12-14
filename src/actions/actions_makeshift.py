from talon import Module
from dataclasses import dataclass


@dataclass
class MakeshiftAction:
    term: str
    identifier: str
    vscode_command_id: str
    restore_selection: bool = False
    pre_command_sleep: int = None
    post_command_sleep: int = None


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
        "quick fix", "showQuickFix", "editor.action.quickFix", restore_selection=True
    ),
    MakeshiftAction(
        "reference", "showReferences", "references-view.find", restore_selection=True
    ),
    MakeshiftAction("rename", "rename", "editor.action.rename", restore_selection=True),
]

makeshift_action_defaults = {
    action.term: action.identifier for action in makeshift_actions
}

mod = Module()
mod.list(
    "cursorless_makeshift_action",
    desc="Supported makeshift actions for cursorless navigation",
)


def get_parameters(action: MakeshiftAction):
    command = action.vscode_command_id
    arguments = {
        "restoreSelection": action.restore_selection,
    }
    if action.pre_command_sleep:
        arguments["preCommandSleep"] = action.pre_command_sleep
    if action.post_command_sleep:
        arguments["postCommandSleep"] = action.post_command_sleep
    return command, arguments


makeshift_action_map = {
    action.identifier: get_parameters(action) for action in makeshift_actions
}
