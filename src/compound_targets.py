from .primitive_target import BASE_TARGET
from talon import Module, app
from .csv_overrides import init_csv_and_watch_changes

mod = Module()


mod.list(
    "cursorless_range_specifier",
    desc="A range joiner that indicates whether to include or exclude anchor and active",
)


@mod.capture(
    rule=(
        "[{user.cursorless_range_specifier}] <user.cursorless_primitive_target> | "
        "<user.cursorless_primitive_target> {user.cursorless_range_specifier} <user.cursorless_primitive_target>"
    )
)
def cursorless_range(m) -> str:
    primitive_targets = m.cursorless_primitive_target_list
    range_specifier = getattr(m, "cursorless_range_specifier", None)

    if range_specifier is None:
        return primitive_targets[0]

    if len(primitive_targets) == 1:
        start = BASE_TARGET.copy()
    else:
        start = primitive_targets[0]

    return {
        "type": "range",
        "start": start,
        "end": primitive_targets[-1],
        "excludeStart": range_specifier in ["excludeBoth", "excludeAnchor"],
        "excludeEnd": range_specifier in ["excludeBoth", "excludeActive"],
    }


@mod.capture(rule="<user.cursorless_range> (and <user.cursorless_range>)*")
def cursorless_target(m) -> str:
    if len(m.cursorless_range_list) == 1:
        return m.cursorless_range
    return {"type": "list", "elements": m.cursorless_range_list}


range_specifiers = {
    "between": "excludeBoth",
    "past": "includeBoth",
    "skip past": "excludeAnchor",
    "until": "excludeActive",
}


def on_ready():
    init_csv_and_watch_changes(
        "range_specifiers",
        {
            "range_specifier": range_specifiers,
        },
    )


app.register("ready", on_ready)