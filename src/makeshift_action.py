from dataclasses import dataclass

from talon import actions, Module, Context
from typing import Any, List


@dataclass
class MakeshiftAction:
    term: str
    vscode_command_id: str
    pre_command_sleep: float = 0
    post_command_sleep: float = 0


makeshift_actions = [
    MakeshiftAction("def show", "editor.action.revealDefinition"),
    MakeshiftAction("drink cell", "jupyter.insertCellAbove"),
    MakeshiftAction("hover show", "editor.action.showHover"),
    MakeshiftAction("pour cell", "jupyter.insertCellBelow"),
    MakeshiftAction("quick fix", "editor.action.quickFix", pre_command_sleep=0.3),
    MakeshiftAction("ref show", "references-view.find"),
    MakeshiftAction("rename", "editor.action.rename", post_command_sleep=0.1),
]

makeshift_action_map = {action.term: action for action in makeshift_actions}

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

mod.list("cursorless_makeshift_action", desc="Makeshift cursorless actions")
ctx.lists["self.cursorless_makeshift_action"] = makeshift_action_map.keys()


@mod.capture(rule="{user.cursorless_makeshift_action}")
def cursorless_makeshift_action(m) -> str:
    return makeshift_action_map[m.cursorless_makeshift_action]


@mod.action_class
class Actions:
    def cursorless_run_makeshift_action(
        makeshift_action: MakeshiftAction,
        target: dict,
    ):
        """Execute makeshift action"""
        actions.user.cursorless_single_target_command("setSelection", target)
        actions.sleep(makeshift_action.pre_command_sleep)
        actions.user.vscode(makeshift_action.vscode_command_id)
        actions.sleep(makeshift_action.post_command_sleep)
