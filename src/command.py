from talon import actions, Module
import json
from typing import Any, List


mod = Module()


class NotSet:
    def __repr__(self):
        return "<argument not set>"


@mod.action_class
class Actions:
    def cursorless_single_target_command(
        action: str,
        target: str,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute single-target cursorlses command"""
        args = list(filter(lambda x: x is not NotSet, [arg1, arg2, arg3]))
        actions.user.vscode_with_plugin_and_wait(
            "cursorless.command",
            action,
            [json.loads(target)],
            *args,
        )

    def cursorless_single_target_command_args(
        action: str,
        target: str,
        args: list[Any]
    ):
        """Execute single-target cursorlses command with arguments list"""
        actions.user.vscode_with_plugin_and_wait(
            "cursorless.command",
            action,
            [json.loads(target)],
            *args,
        )

    def cursorless_multiple_target_command(
        action: str,
        targets: List[str],
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet,
    ):
        """Execute single-target cursorlses command"""
        args = list(filter(lambda x: x is not NotSet, [arg1, arg2, arg3]))
        actions.user.vscode_with_plugin_and_wait(
            "cursorless.command",
            action,
            [json.loads(target) for target in targets],
            *args,
        )
