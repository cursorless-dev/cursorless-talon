from talon import Context, Module

mod = Module()
ctx = Context()

mod.list("cursorless_line_direction", desc="Supported directions for line modifier")

directions = {
    # The simplified version uses a module based row number
    # "row": {"type": "absolute", "transformation": lambda number: number - 1},
    "row": {"type": "modulo", "transformation": lambda number: number - 1},
    "up": {"type": "relative", "transformation": lambda number: -number},
    "down": {"type": "relative", "transformation": lambda number: number},
}

ctx.lists["self.cursorless_line_direction"] = directions.keys()


def parse_line(line: dict):
    direction = directions[line["direction"]]
    line_number = line["lineNumber"]
    return {
        "lineNumber": direction["transformation"](line_number),
        "type": direction["type"],
    }


@mod.capture(rule="{user.cursorless_line_direction} <number>")
def cursorless_line_number_anchor(m) -> str:
    return {"direction": m.cursorless_line_direction, "lineNumber": m.number}


@mod.capture(rule="past [{user.cursorless_line_direction}] <number>")
def cursorless_line_number_active(m) -> str:
    try:
        direction = m.cursorless_line_direction
    except AttributeError:
        direction = None
    return {"direction": direction, "lineNumber": m.number}


# For now this capture is not used because it's too complex and increase compilation time too much
@mod.capture(
    rule="<user.cursorless_line_number_anchor> [<user.cursorless_line_number_active>]"
)
def cursorless_line_number(m) -> str:
    anchor = m.cursorless_line_number_anchor
    try:
        active = m.cursorless_line_number_active
        # Infer missing direction from anchor
        if active["direction"] == None:
            active["direction"] = anchor["direction"]
    except AttributeError:
        active = anchor
    return {
        "selectionType": "line",
        "mark": {
            "type": "lineNumber",
            "anchor": parse_line(anchor),
            "active": parse_line(active),
        },
    }


# This is the simplified version that we are using for now that only implements a subset of the features
@mod.capture(rule="(up | down | row) <number_small>")
def cursorless_line_number_simple(m) -> str:
    position = {"direction": m[0], "lineNumber": m.number_small}
    return {
        "selectionType": "line",
        "mark": {
            "type": "lineNumber",
            "anchor": parse_line(position),
            "active": parse_line(position),
        },
    }
