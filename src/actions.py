from .primitive_target import BASE_TARGET, STRICT_HERE
from talon import Context, actions, ui, Module, app, clip

mod = Module()

ctx = Context()
ctx.matches = r"""
app: vscode
"""

# TODO A lot of these could be supported by supporting a proper "pop back"
# Would basically use the same logic that is used for updating token ranges
mod.list("cursorless_simple_action", desc="Supported actions for cursorless navigation")
ctx.lists["self.cursorless_simple_action"] = {
    # Accepts any single extent
    # "spring": "setSelection",  # Removed because conflicts with "bring"
    "take": "setSelection",
    "pree": "setSelectionBefore",
    "post": "setSelectionAfter",
    "chuck": "delete",
    "clear": "clear",
    "drink": "insertLineBefore",
    "pour": "insertLineAfter",
    # "sort": "sortLines",
    # "join": "joinLines",
    # "float": "insertEmptyLineBelow",
    # "drop": "insertEmptyLineAbove",
    # Sort children?? (would need to sort only named ones to avoid commas)
    # Reverse children
    "carve": "cut",
    "copy": "copy",
    # FIND: "findInFile",
    # f"{FIND} last": "findBackwardsInFile",
    # f"{FIND} all": "findAll",
    "fold": "fold",
    "unfold": "unfold",
    # "stack": "addCursorAt",
    # "cursor all": "addCursorToAllLines",
    # "remove cursor": "removeCursor",
    # "tab": "indent",
    # "retab": "dedent",
    # "comment": "comment",
    # "github open": "openInGithub",
    # "smear": "cloneLineDown",
    # # Accepts only single token
    # "rename": "rename",
    # "ref show": "showReferences",
    # "def show": "showDefinition",
    # "hover show": "showHover",
    "top": "scrollToTop",
    "center": "scrollToCenter",
    "bottom": "scrollToBottom",
    # "breakpoint": "addBreakPoint",
    # # Accepts position
    # "paste": "paste",
}

wrappers = {
    "square": ["[", "]"],
    "round": ["(", ")"],
    "curly": ["{", "}"],
    "angle": ["<", ">"],
    "twin": ["'", "'"],
    "quad": ['"', '"'],
    "brick": ["`", "`"],
    "escaped twin": ["\\'", "\\'"],
    "escaped quad": ['\\"', '\\"']
}

mod.list("cursorless_wrapper", desc="Supported wrappers for cursorless wrap action")
ctx.lists["self.cursorless_wrapper"] = wrappers.keys()

@mod.capture(rule=("{user.cursorless_wrapper}"))
def cursorless_wrapper(m) -> list[str]:
    return wrappers[m.cursorless_wrapper]


@mod.capture(rule=("swap [<user.cursorless_target>] with <user.cursorless_target>"))
def cursorless_swap(m) -> str:
    target_list = m.cursorless_target_list

    if len(target_list) == 1:
        target_list = [BASE_TARGET] + target_list

    return target_list


@mod.capture(rule=("bring <user.cursorless_target> [to <user.cursorless_target>]"))
def cursorless_use(m) -> str:
    target_list = m.cursorless_target_list

    if len(target_list) == 1:
        target_list = target_list + [STRICT_HERE]

    return target_list




{
    # Require 1 extent of any kind, and 1 format string (eg "camel foo bar",
    # "phrase hello world" etc, "spell air bat cap")
    # Note: these should actually be of the form "replace <range> with"
    # Could also except a second extent, and that would replace it with that
    # extent
    "replace with": "replaceWith",
    # Require 1 extent of any kind, and 1 format type (eg camel, uppercase,
    # phrase etc)
    # Note: these should actually be of the form "reformat <range> as"
    "reformat as": "reformatAs",
}
"<user.search_engine>"
"phones"
