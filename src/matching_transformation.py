from talon import Context, Module
from dataclasses import dataclass

mod = Module()
ctx = Context()

ctx.matches = r"""
app: vscode
"""

@dataclass
class ModifierTerm:
    term: str
    info: dict

matching_transformation = ModifierTerm(
    "matching",  {"transformation": {"type": "matchingPairSymbol"}}
)

@mod.capture(rule=matching_transformation.term)
def cursorless_matching(m) -> str:
    return matching_transformation.info
