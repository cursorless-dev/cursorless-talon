from talon import Module

mod = Module()


@mod.capture(rule="matching")
def cursorless_matching_pair_symbol(m) -> str:
    return {"modifier": {"type": "matchingPairSymbol"}}
