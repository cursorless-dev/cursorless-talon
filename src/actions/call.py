from ..primitive_target import STRICT_HERE
from talon import Module, actions

mod = Module()


def run_call_action(target: dict):
    targets = [target, STRICT_HERE]
    actions.user.cursorless_multiple_target_command("callAsFunction", targets)
