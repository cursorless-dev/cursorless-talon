import os
from tempfile import gettempdir
from dataclasses import dataclass
from pathlib import Path
from ..conventions import get_cursorless_list_name
from talon import Module, actions, app, Context, fs, cron
from ..csv_overrides import init_csv_and_watch_changes
from ..read_json_with_timeout import read_json_with_timeout

mod = Module()
ctx = Context()


mod.list("cursorless_hat_color", desc="Supported hat colors for cursorless")
mod.list("cursorless_hat_shape", desc="Supported hat shapes for cursorless")

# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
hat_colors = {
    "blue": "blue",
    "green": "green",
    "rose": "red",
    "plum": "pink",
    "squash": "yellow",
}

hat_shapes = {
    "ex": "ex",
    "fox": "fox",
    "wing": "wing",
    "hole": "hole",
    "frame": "frame",
    "curve": "curve",
    "eyeball": "eye",
    "play": "play",
    "cross": "crosshairs",
    "bolt": "bolt",
}


@mod.capture(
    rule="[{user.cursorless_hat_color}] [{user.cursorless_hat_shape}] <user.any_alphanumeric_key>"
)
def cursorless_decorated_symbol(m) -> str:
    """A decorated symbol"""
    hat_color = getattr(m, "cursorless_hat_color", "default")
    try:
        hat_style_name = f"{hat_color}-{m.cursorless_hat_shape}"
    except AttributeError:
        hat_style_name = hat_color
    return {
        "mark": {
            "type": "decoratedSymbol",
            "symbolColor": hat_style_name,
            "character": m.any_alphanumeric_key,
        }
    }


@dataclass
class CustomizableTerm:
    defaultSpokenForm: str
    cursorlessIdentifier: str
    value: any


# NOTE: Please do not change these dicts.  Use the CSVs for customization.
# See https://github.com/pokey/cursorless-talon/blob/main/docs/customization.md
special_marks = [
    CustomizableTerm("this", "currentSelection", {"mark": {"type": "cursor"}}),
    CustomizableTerm("that", "previousTarget", {"mark": {"type": "that"}}),
    CustomizableTerm("source", "previousSource", {"mark": {"type": "source"}}),
    # "last cursor": {"mark": {"type": "lastCursorPosition"}} # Not implemented
]

special_marks_map = {term.cursorlessIdentifier: term for term in special_marks}

special_marks_defaults = {
    term.defaultSpokenForm: term.cursorlessIdentifier for term in special_marks
}


mod.list("cursorless_special_mark", desc="Cursorless special marks")


@mod.capture(
    rule=(
        "<user.cursorless_decorated_symbol> | "
        "{user.cursorless_special_mark} |"
        # Because of problems with performance we have to have a simple version for now
        # "<user.cursorless_line_number>" # row, up, down
        "<user.cursorless_line_number_simple>"  # up, down
    )
)
def cursorless_mark(m) -> str:
    try:
        return m.cursorless_decorated_symbol
    except AttributeError:
        pass
    try:
        return special_marks_map[m.cursorless_special_mark].value
    except AttributeError:
        pass
    return m.cursorless_line_number_simple


unsubscribe_hat_styles = None


def setup_hat_styles_csv():
    global unsubscribe_hat_styles

    cursorless_enablements_path = get_cursorless_enablements_path()
    hat_enablements = read_json_with_timeout(cursorless_enablements_path)

    active_hat_colors = {
        spoken_form: value
        for spoken_form, value in hat_colors.items()
        if value in hat_enablements["colors"]
    }
    active_hat_shapes = {
        spoken_form: value
        for spoken_form, value in hat_shapes.items()
        if value in hat_enablements["shapes"]
    }

    if unsubscribe_hat_styles is not None:
        unsubscribe_hat_styles()

    unsubscribe_hat_styles = init_csv_and_watch_changes(
        "hat_styles",
        {
            "hat_color": active_hat_colors,
            "hat_shape": active_hat_shapes,
        },
        [*hat_colors.values(), *hat_shapes.values()],
    )


def get_cursorless_enablements_path():
    if hasattr(os, "getuid"):
        suffix = f"-{os.getuid()}"

    return Path(gettempdir()) / f"cursorless-enablements{suffix}.json"


hat_style_job = None


def on_ready():
    init_csv_and_watch_changes(
        "special_marks",
        {
            "special_mark": special_marks_defaults,
        },
    )

    setup_hat_styles_csv()

    cursorless_enablements_path = get_cursorless_enablements_path().resolve()

    def on_watch(path, flags):
        global hat_style_job
        cron.cancel(hat_style_job)
        hat_style_job = cron.after("500ms", setup_hat_styles_csv)

    fs.watch(cursorless_enablements_path, on_watch)


app.register("ready", on_ready)
