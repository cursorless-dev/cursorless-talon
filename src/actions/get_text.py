from typing import Optional

from ..command import Actions  as command_actions

def get_text(
    target: dict,
    show_decorations: Optional[bool] = None,
    ensure_single_target: Optional[bool] = None,
):
    """Get target texts"""
    return command_actions.cursorless_single_target_command_get(
        "getText",
        target,
        {
            "showDecorations": show_decorations,
            "ensureSingleTarget": ensure_single_target,
        },
    )
