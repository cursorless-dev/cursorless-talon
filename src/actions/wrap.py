from typing import Union
from ..paired_delimiter import paired_delimiters_map
from talon import Module, actions, app
from ..csv_overrides import init_csv_and_watch_changes


mod = Module()


mod.list("cursorless_wrap_action", desc="Cursorless wrap action")
mod.list("cursorless_wrapper_snippet", desc="Cursorless wrapper scope type")


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
wrapper_snippets = {
    "else state": "cursorless.wrapper.ifElseStatementElseBranch",
    "if else": "cursorless.wrapper.ifElseStatementIfBranch",
    "if state": "cursorless.wrapper.ifStatement",
    "try catch": "cursorless.wrapper.tryCatchStatement",
}


@mod.capture(
    rule=(
        "({user.cursorless_paired_delimiter} | {user.cursorless_wrapper_snippet}) {user.cursorless_wrap_action}"
    )
)
def cursorless_wrapper(m) -> Union[list[str], str]:
    try:
        paired_delimiter_info = paired_delimiters_map[m.cursorless_paired_delimiter]
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
        "wrapper_snippets",
        {
            "wrapper_snippet": wrapper_snippets,
        },
        allow_unknown_values=True,
        default_list_name="wrapper_snippet",
    )


app.register("ready", on_ready)
