from typing import Union
from ..paired_delimiter import paired_delimiters_map
from talon import Module, Context


mod = Module()
ctx = Context()


mod.list("cursorless_wrap_action", desc="Cursorless wrap action")
mod.list("cursorless_wrapper_scope_type", desc="Cursorless wrapper scope type")
ctx.lists["user.cursorless_wrapper_scope_type"] = {"try catch": "tryCatchStatement"}


@mod.capture(
    rule=("{user.cursorless_paired_delimiter} | {user.cursorless_wrapper_scope_type}")
)
def cursorless_wrapper(m) -> Union[list[str], str]:
    try:
        paired_delimiter_info = paired_delimiters_map[m.cursorless_paired_delimiter]
    except AttributeError:
        return [m.cursorless_wrapper_scope_type]
    return [paired_delimiter_info.left, paired_delimiter_info.right]
