from typing import Union
from ..paired_delimiter import paired_delimiters_map
from talon import Module, actions, app, Context
from ..csv_overrides import init_csv_and_watch_changes


mod = Module()

mod.tag(
    "cursorless_experimental_snippets",
    desc="tag for enabling experimental snippet support",
)

mod.list("cursorless_wrap_action", desc="Cursorless wrap action")
mod.list("cursorless_wrapper_snippet", desc="Cursorless wrapper snippet")

experimental_snippets_ctx = Context()
experimental_snippets_ctx.matches = r"""
tag: user.cursorless_experimental_snippets
"""


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
wrapper_snippets = {
    "else": "ifElseStatement.alternative",
    "if else": "ifElseStatement.consequence",
    "if": "ifStatement.consequence",
    "try": "tryCatchStatement.body",
}


@mod.capture(
    rule=(
        "(<user.cursorless_wrapper_paired_delimiter> | {user.cursorless_wrapper_snippet}) {user.cursorless_wrap_action}"
    )
)
def cursorless_wrapper(m) -> Union[list[str], str]:
    try:
        paired_delimiter_info = paired_delimiters_map[
            m.cursorless_wrapper_paired_delimiter
        ]
        return {
            "action": "wrapWithPairedDelimiter",
            "extra_args": [paired_delimiter_info.left, paired_delimiter_info.right],
        }
    except AttributeError:
        return {
            "action": "wrapWithSnippet",
            "extra_args": [m.cursorless_wrapper_snippet],
        }


@mod.action_class
class Actions:
    def cursorless_wrap(cursorless_wrapper: dict, targets: dict):
        """Perform cursorless wrap action"""
        actions.user.cursorless_single_target_command_with_arg_list(
            cursorless_wrapper["action"], targets, cursorless_wrapper["extra_args"]
        )


def on_ready():
    init_csv_and_watch_changes(
        "experimental/wrapper_snippets",
        {
            "wrapper_snippet": wrapper_snippets,
        },
        allow_unknown_values=True,
        default_list_name="wrapper_snippet",
        ctx=experimental_snippets_ctx,
    )


app.register("ready", on_ready)