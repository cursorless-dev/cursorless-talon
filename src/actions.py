from .primitive_target import BASE_TARGET, STRICT_HERE
from talon import Context, actions, ui, Module, app, clip

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.cursorless
"""

# TODO A lot of these could be supported by supporting a proper "pop back"
# Would basically use the same logic that is used for updating token ranges
mod.list("cursorless_simple_action", desc="Supported actions for cursorless navigation")
ctx.lists["self.cursorless_simple_action"] = {
    "bottom": "scrollToBottom",
    "carve": "cut",
    "center": "scrollToCenter",
    "chuck": "delete",
    "clear": "clear",
    "clone": "copyLinesDown",
    "comment": "commentLines",
    "copy": "copy",
    "dedent": "outdentLines",
    "drink": "editNewLineAbove",
    "drop": "insertEmptyLineAbove",
    "dupe": "copyLinesUp",
    "find all": "findInFiles",
    "float": "insertEmptyLineBelow",
    "fold": "fold",
    "indent": "indentLines",
    "paste": "paste",
    "post": "setSelectionAfter",
    "pour": "editNewLineBelow",
    "pree": "setSelectionBefore",
    "puff": "insertEmptyLinesAround",
    "take": "setSelection",
    "top": "scrollToTop",
    "unfold": "unfold",
}

mod.list("cursorless_move_bring_action", desc="Cursorless move or bring actions")
ctx.lists["self.cursorless_move_bring_action"] = {"bring", "move"}


@mod.capture(rule=("swap [<user.cursorless_target>] with <user.cursorless_target>"))
def cursorless_swap(m) -> str:
    target_list = m.cursorless_target_list

    if len(target_list) == 1:
        target_list = [BASE_TARGET] + target_list

    return target_list


@mod.capture(rule=("<user.cursorless_target> [to <user.cursorless_target>]"))
def cursorless_move_bring_targets(m) -> str:
    target_list = m.cursorless_target_list

    if len(target_list) == 1:
        target_list = target_list + [STRICT_HERE]

    return target_list
