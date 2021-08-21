from ..modifiers.surrounding_pair import paired_delimiters_map
from talon import Module


mod = Module()


mod.list("cursorless_wrap_action", desc="Cursorless wrap action")


@mod.capture(rule=("{user.cursorless_paired_delimiter}"))
def cursorless_wrapper(m) -> list[str]:
    paired_delimiter_info = paired_delimiters_map[m.cursorless_paired_delimiter]
    return [paired_delimiter_info.left, paired_delimiter_info.right]
