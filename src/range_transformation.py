from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
app: vscode
"""


@mod.capture(
    rule=(
        "<user.cursorless_surrounding_pair> |"
        "<user.cursorless_simple_transformations> |"
        "<user.cursorless_containing_scope>"
    )
)
def cursorless_range_transformation(m) -> str:
    """Supported positions for cursorless navigation"""
    return m[0]
