from talon import Context, Module
from dataclasses import dataclass

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""


@mod.capture(rule="matching")
def cursorless_matching_pair_symbol(m) -> str:
    return {"modifier": {"type": "matchingPairSymbol"}}
