from talon import Module

mod = Module()


@mod.capture(rule="count [from <number_small>]")
def cursorless_range_generator(m) -> str:
    try:
        start = m.number_small
    except AttributeError:
        start = 0
    return {"type": "range", "start": start}


@mod.capture(rule="{user.cursorless_pair_symbol}")
def cursorless_pair_generator(m) -> str:
    return {"type": "pair", "pair": m.cursorless_pair_symbol}


@mod.capture(
    rule=("<user.cursorless_range_generator> |" "<user.cursorless_pair_generator>")
)
def cursorless_insert_value(m) -> str:
    return m[0]
