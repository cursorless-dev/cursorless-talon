from dragonfly import Compound, Choice, ShortIntegerRef
from ..cursorless_lists import get_ref
from ..modifiers import compounds as modifier_compounds

from . import mark
from . import lines_number

''' grapheme '''

grapheme_compound = Compound(
    spec="<any_alphanumeric_key> | <unknown_symbol>",
    name="grapheme",
    extras=[
            get_ref("unknown_symbol"),
            modifier_compounds.any_alphanumeric_key_compound,
        ],
    value_func=lambda node, extras: mark.cursorless_grapheme(extras),
)

#''' <action_or_ide_command> <target> '''

''' decorated_symbol '''

decorated_symbol_compound = Compound(
    spec="[<hat_color>] [<hat_shape>] <grapheme>",
    name="decorated_symbol",
    extras=[
            get_ref("hat_color"),
            get_ref("hat_shape"),
            grapheme_compound
        ],
    value_func=lambda node, extras: mark.cursorless_decorated_symbol(extras),
)

''' line_number '''

line_number_compound = Compound(
    spec="<line_direction> <n100_1>  [<range_connective> <n100_2>]",
    name="line_number",
    extras=[
            get_ref("line_direction"),
            ShortIntegerRef("n100_1", 0, 100),
            get_ref("range_connective"),
            ShortIntegerRef("n100_2", 0, 100),
        ],
    value_func=lambda node, extras: lines_number.cursorless_line_number(extras),
)
    
''' mark '''

mark_compound = Compound(
    spec="<decorated_symbol> | <special_mark> | <line_number>",
    name="mark",
    extras=[
            decorated_symbol_compound,
            get_ref("special_mark"),
            line_number_compound,
        ],
    value_func=lambda node, extras: mark.cursorless_mark(extras),
)
    