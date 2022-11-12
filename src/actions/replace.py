from ..command import Actions as command_actions


class Actions:
    def cursorless_replace(target: dict, texts: list[str] or dict):
        """Replace targets with texts"""
        command_actions.cursorless_single_target_command("replace", target, texts)
