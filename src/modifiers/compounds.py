from dragonfly import Compound, Choice, ShortIntegerRef, RuleWrap, RuleRef
from ..cursorless_lists import get_ref, get_dict
from .. import compound_targets

from . import scopes
from . import surrounding_pair
from . import ordinal_scope
from . import relative_scope
from . import head_tail
from . import range_type
from . import position
from . import interior
from . import modifiers
from . import simple_scope_modifier


try:  # Try first loading from caster user directory
    from caster_user_content.rules.alphabet_rules import alphabet_support
except ImportError:
    from castervoice.rules.core.alphabet_rules import alphabet_support
try:  # Try first loading from caster user directory
    from caster_user_content.rules.punctuation_rules.punctuation_support import text_punc_dict
except ImportError:
    from castervoice.rules.core.punctuation_rules.punctuation_support import text_punc_dict

#''' <action_or_ide_command> <target> '''

''' scope_type '''

scope_type_compound = Compound(
    # spec="<scope_type>",
    spec="<scope_type> | <custom_regex_scope_type>",
    name="scope_type",
    extras=[
            get_ref("scope_type"),
            get_ref("custom_regex_scope_type")
        ],
    value_func=lambda node, extras: scopes.cursorless_scope_type(extras),
)


scope_type_plural_compound = Compound(
    # spec="<scope_type>",
    spec="<scope_type_plural> | <custom_regex_scope_type_plural>",
    name="scope_type_plural",
    extras=[
            get_ref("scope_type_plural"),
            get_ref("custom_regex_scope_type_plural")
        ],
    value_func=lambda node, extras: scopes.cursorless_scope_type_plural(extras),
)

''' surrounding_pair '''

selectable_only_paired_delimiters = get_dict("selectable_only_paired_delimite") 
wrapper_selectable_paired_delimiters = get_dict("wrapper_selectable_paired_delimiter")
selectable_paired_delimiters = selectable_only_paired_delimiters | wrapper_selectable_paired_delimiters

surrounding_pair_scope_types = scopes.surrounding_pair_scope_types

surrounding_pair_scope_type_compound = Compound(
    spec="<selectable_paired_delimiter> | <surrounding_pair_scope_type>",
    name="surrounding_pair_scope_type",
    extras=[
            Choice("selectable_paired_delimiter", selectable_paired_delimiters),
            Choice("surrounding_pair_scope_type", surrounding_pair_scope_types),
        ],
    value_func=lambda node, extras: surrounding_pair.cursorless_surrounding_pair_scope_type(extras),
)

delimiter_force_directions = ["left", "right"]
    
surrounding_pair_compound = Compound(
    spec="[<delimiter_force_direction>] <surrounding_pair_scope_type>",
    name="surrounding_pair",
    extras=[
            Choice("delimiter_force_direction", delimiter_force_directions),
            surrounding_pair_scope_type_compound,
        ],
    value_func=lambda node, extras: surrounding_pair.cursorless_surrounding_pair(extras),
)

''' ordinal_scope '''

ordinal_or_last_compound = Compound(
    spec="<ordinals_small> | [<ordinals_small>] <last_modifier>",
    name="ordinal_or_last",
    extras=[
            ShortIntegerRef("ordinals_small", 0, 10),
            get_ref("last_modifier"),
        ],
    value_func=lambda node, extras: ordinal_scope.ordinal_or_last(extras),
)
ordinal_or_last_rule = RuleWrap("", ordinal_or_last_compound).rule

ordinal_range_compound = Compound(
    spec="<ordinal_or_last1>"
            "[<range_connective> <ordinal_or_last2>]"
            "<scope_type>",
    name="ordinal_range",
    extras=[
            RuleRef(ordinal_or_last_rule, "ordinal_or_last1"),
            get_ref("range_connective"),  
            RuleRef(ordinal_or_last_rule, "ordinal_or_last2"),
            scope_type_compound,
        ],
    value_func=lambda node, extras: ordinal_scope.cursorless_ordinal_range(extras),
)

first_last_compound = Compound(
    spec="(<first_modifier> | <last_modifier>) <number_small> <scope_type_plural>",
    name="first_last",
    extras=[
            get_ref("first_modifier"),
            get_ref("last_modifier"),
            ShortIntegerRef("number_small", 0, 10),
            scope_type_plural_compound,
        ],
    value_func=lambda node, extras: ordinal_scope.cursorless_first_last(extras),
)

ordinal_scope_compound = Compound(
    spec="<ordinal_range> | <first_last>",
    name="ordinal_scope",
    extras=[
            ordinal_range_compound,
            first_last_compound,
        ],
    # returns exact
    # value_func=lambda node, extras: _func(extras), 
)

''' relative_scope '''

relative_direction_compound = Compound(
    spec="<previous_next_modifier>",
    name="relative_direction",
    extras=[
            get_ref("previous_next_modifier"),
        ],
    value_func=lambda node, extras: relative_scope.cursorless_relative_direction(extras),
)

relative_scope_singular_compound = Compound(
    spec="[<ordinals_small>] <relative_direction> <scope_type>",
    name="relative_scope_singular",
    extras=[
            ShortIntegerRef("ordinals_small", 0, 10),
            relative_direction_compound,
            scope_type_compound,
        ],
    value_func=lambda node, extras: relative_scope.cursorless_relative_scope_singular(extras),
)

relative_scope_plural_compound = Compound(
    spec="<relative_direction> <number_small> <scope_type_plural>",
    name="relative_scope_plural",
    extras=[
            relative_direction_compound,
            ShortIntegerRef("number_small", 0, 10),
            scope_type_plural_compound,
        ],
    value_func=lambda node, extras: relative_scope.cursorless_relative_scope_plural(extras),
)

relative_scope_count_compound = Compound(
    spec="<number_small> <scope_type_plural> [<forward_backward_modifier>]",
    name="relative_scope_count",
    extras=[
            ShortIntegerRef("number_small", 0, 10),
            scope_type_plural_compound,
            get_ref("forward_backward_modifier"),
        ],
    value_func=lambda node, extras: relative_scope.cursorless_relative_scope_count(extras),
)

relative_scope_one_backward_compound = Compound(
    spec="<scope_type> <forward_backward_modifier>",
    name="relative_scope_one_backward",
    extras=[
            scope_type_compound,
            get_ref("forward_backward_modifier"),
        ],
    value_func=lambda node, extras: relative_scope.cursorless_relative_scope_one_backward(extras),
)

relative_scope_compound = Compound(
    spec="<relative_scope_singular> | "
        "<relative_scope_plural> | "
        "<relative_scope_count> | "
        "<relative_scope_one_backward>",
    name="relative_scope",
    extras=[
            relative_scope_singular_compound,
            relative_scope_plural_compound,
            relative_scope_count_compound,
            relative_scope_one_backward_compound,
            # scope_type_compound,
        ],
    # return exact
    # value_func=lambda node, extras: relative_scope.cursorless_relative_scope(extras),
)

# ''' containing_scope ''' # maybe move this near scope_type

# containing_scope_compound = Compound(
#     spec="[every] <scope_type>",
#     name="containing_scope",
#     extras=[
#             scope_type_compound,
#             # scope_type_compound,
#         ],
#     value_func=lambda node, extras: scopes.cursorless_containing_scope(extras),
# )

''' modifier '''

interior_modifier_compound = Compound(
    spec="<interior_modifier>",
    name="interior_modifier",
    extras=[
            get_ref("interior_modifier"),
        ],
    value_func=lambda node, extras: interior.cursorless_interior_modifier(extras),
)

simple_modifier_compound = Compound(
    spec="<simple_modifier>",
    name="simple_modifier",
    extras=[
            get_ref("simple_modifier"),
        ],
    value_func=lambda node, extras: modifiers.cursorless_simple_modifier(extras),
)

simple_scope_modifier_compound = Compound(
    spec="[every] <scope_type>",
    name="simple_scope_modifier",
    extras=[
            get_ref("simple_scope_modifier"),
            scope_type_compound,
        ],
    value_func=lambda node, extras: simple_scope_modifier.cursorless_simple_scope_modifier(extras),
)

head_tail_swallowed_modifier_compound = Compound(
    spec="<simple_modifier> |"
        "<simple_scope_modifier> |"
        "<ordinal_scope> |"
        "<relative_scope> |"
        "<surrounding_pair>",
    # spec="<simple_modifier> |"
    #         "<containing_scope> |"
    #         "<ordinal_scope> |"
    #         "<relative_scope> |"
    #         "<surrounding_pair>",
    name="head_tail_swallowed_modifier",
    extras=[
            simple_modifier_compound,
            simple_scope_modifier_compound,
            # containing_scope_compound,
            ordinal_scope_compound,
            relative_scope_compound,
            surrounding_pair_compound,
        ],
    # returns exact
    # value_func=lambda node, extras: _func(extras),
)

head_tail_modifier_compound = Compound(
    spec="<head_tail_modifier> "
            "[<interior_modifier>] "
            "[<head_tail_swallowed_modifier>]",
    name="head_tail_modifier",
    extras=[
            get_ref("head_tail_modifier"),
            interior_modifier_compound,
            head_tail_swallowed_modifier_compound,
        ],
    value_func=lambda node, extras: head_tail.cursorless_head_tail_modifier(extras),
)

modifier_compound = Compound(
    spec="<interior_modifier> |" 
            "<head_tail_modifier> |"
            "<head_tail_swallowed_modifier>",
    name="modifier",
    extras=[
            interior_modifier_compound,
            head_tail_modifier_compound,
            head_tail_swallowed_modifier_compound,
        ],
    # returns exact
    # value_func=lambda node, extras: _func(extras),
)
modifier_rule = RuleWrap("", modifier_compound).rule

''' any_alphanumeric_key '''

# should be in cursorless/compound.py
symbol_keys = text_punc_dict()

# used to make number output as string, rather than int
number_key_compound = Compound(
    spec="<number_key>",
    name="number_key",
    extras=[
            ShortIntegerRef("number_key", 0, 10),
          ],
    value_func=lambda node, extras: str(extras["number_key"]),
)
    
any_alphanumeric_key_compound = Compound(
    spec="<letter> | <number_key> | <symbol_key>",
    name="any_alphanumeric_key",
    extras=[
            alphabet_support.get_alphabet_choice("letter"),
            number_key_compound,
            Choice("symbol_key", symbol_keys),
        ],
    # returns exact
    # value_func=lambda node, extras: _func(extras),
)

''' range_connective_with_type '''

range_types = get_dict("range_type")
    
range_type_compound = Compound(
    spec="<range_type>",
    name="range_type",
    extras=[
            Choice("range_type", range_types),
        ],
    value_func=lambda node, extras: range_type.cursorless_range_type(extras),
)

# should be in cursorless/compound.py
range_connective_with_type_compound = Compound(
    spec="[<range_type>] <range_connective> | <range_type>",
    name="range_connective_with_type",
    extras=[
            range_type_compound,             
            get_ref("range_connective"),    
        ],
    value_func=lambda node, extras: compound_targets.cursorless_range_connective_with_type(extras),
)

''' position '''

position_compound = Compound(
    spec="<position>",
    name="position",
    extras=[
            get_ref("position"),
        ],
    # returns exact
    # value_func=lambda node, extras: position.cursorless_position(extras),
)