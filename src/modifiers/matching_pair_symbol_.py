from talon import Context, Module
from dataclasses import dataclass

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

@dataclass
class ModifierTerm:
    term: str
    info: dict

matching_pair_symbol = ModifierTerm(
    "matching",  {"transformation": {"type": "matchingPairSymbol"}}
)

@mod.capture(rule=matching_pair_symbol.term)
def cursorless_matching_pair_symbol(m) -> str:
    return cursorless_matching_pair_symbol.info
