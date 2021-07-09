from talon import actions, Module
from typing import Any, List

mod = Module()


class NotSet:
    def __repr__(self):
        return "<argument not set>"


@mod.action_class
class Actions:
    def cursorless_single_target_command(
        action: str,
        target: dict,
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet
    ):
        """Execute single-target cursorless command"""
        actions.user.cursorless_multiple_target_command(
            action, [target], arg1, arg2, arg3
        )

    def cursorless_single_target_command_with_arg_list(
        action: str,
        target: str,
        args: list[Any]
    ):
        """Execute single-target cursorless command with argument list"""
        actions.user.cursorless_single_target_command(
            action,
            target,
            *args,
        )

    def cursorless_single_target_command_with_arg_list(
        action: str,
        target: str,
        args: list[Any]
    ):
        """Execute single-target cursorless command with argument list"""
        actions.user.cursorless_single_target_command(
            action,
            target,
            *args,
        )

    def cursorless_multiple_target_command(
        action: str,
        targets: List[dict],
        arg1: Any = NotSet,
        arg2: Any = NotSet,
        arg3: Any = NotSet
    ):
        """Execute multi-target cursorless command"""
        args = list(filter(lambda x: x is not NotSet, [arg1, arg2, arg3]))
        actions.user.vscode_with_plugin_and_wait(
            "cursorless.command",
            action,
            targets,
            *args,
        )
