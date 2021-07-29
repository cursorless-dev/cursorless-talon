from talon import Module

mod = Module()


@mod.capture(rule=("(row <number>) | ((up | down) <number_small>)"))
def cursorless_line(m) -> str:
    if m[0] == "row":
        isRelative = False
        lineNumber = m.number - 1
    else:
        isRelative = True
        lineNumber = m.number_small if m[0] == "down" else -m.number_small
    return {
        "selectionType": "line",
        "modifier": {
            "type": "lineNumber",
            "lineNumber": lineNumber,
            "isRelative": isRelative,
        },
    }
