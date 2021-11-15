from ..csv_overrides import init_csv_and_watch_changes
from talon import Module, actions, app, Context

mod = Module()

mod.tag(
    "cursorless_experimental_snippets",
    desc="tag for enabling experimental snippet support",
)

experimental_quick_code_actions_ctx = Context()
experimental_quick_code_actions_ctx.matches = r"""
tag: user.cursorless_experimental_quick_code_actions
"""


def on_ready():
    init_csv_and_watch_changes(
        "experimental/quick_code_actions",
        {
            "wrapper_snippet": wrapper_snippets,
        },
        allow_unknown_values=True,
        default_list_name="wrapper_snippet",
        ctx=experimental_quick_code_actions_ctx,
    )


app.register("ready", on_ready)