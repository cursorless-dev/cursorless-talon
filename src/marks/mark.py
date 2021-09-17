from dataclasses import dataclass
from ..conventions import get_cursorless_list_name
from talon import Module, app, Context
from ..csv_overrides import init_csv_and_watch_changes

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
    "-ex": "fourPointStar",
    "-fox": "chevron",
    "-wing": "threePointStar",
    "-hole": "hole",
    "-frame": "frame",
    "-curve": "curve",
    "-eye": "eye",
    "-play": "play",
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


def on_ready():
    init_csv_and_watch_changes(
        "special_marks",
        {
            "special_mark": special_marks_defaults,
        },
    )
    init_csv_and_watch_changes(
        "hat_styles",
        {
            "hat_color": hat_colors,
            "hat_shape": hat_shapes,
        },
    )


app.register("ready", on_ready)
