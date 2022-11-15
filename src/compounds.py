from dragonfly import Compound, Choice, RuleWrap, RuleRef, Repetition
from .cursorless_lists import get_ref

from .modifiers import compounds as modifier_compounds
from .marks import compounds as mark_compounds
from . import primitive_target
from . import compound_targets
from . import positional_target
from . import paired_delimiter


#''' <action_or_ide_command> <target> '''

''' primitive_target '''

# longest modifier list?
# "its value tail" is it even usefull?
primitive_target_compound = Compound(
    # spec="[<position>] (<mark> | <modifier1> [<modifier2> [<modifier3>] [<modifier4>]] [<mark>])",
    spec="[<position>] (<mark> | <modifier1> [<modifier2> [<modifier3>]] [<mark>])",
    name="primitive_target",
    extras=[
            modifier_compounds.position_compound,
            mark_compounds.mark_compound,
            RuleRef(modifier_compounds.modifier_rule, "modifier1"),
            RuleRef(modifier_compounds.modifier_rule, "modifier2"),
            RuleRef(modifier_compounds.modifier_rule, "modifier3"),
            # RuleRef(modifier_compounds.modifier_rule, "modifier4"),
        ],
    value_func=lambda node, extras: primitive_target.cursorless_primitive_target(extras),
)
primitive_target_rule = RuleWrap("", primitive_target_compound).rule
    
''' range ''' 
   
# list_connective_rule = RuleWrap("", Choice("", 
#     get_dict("list_connective"),
# )).rule 

range_compound = Compound(
    spec="<primitive_target1> [<range_connective_with_type> [<primitive_target2>]]",
    name="range",
    extras=[
            RuleRef(primitive_target_rule, "primitive_target1"),
            modifier_compounds.range_connective_with_type_compound,
            RuleRef(primitive_target_rule, "primitive_target2"),
        ],
    value_func=lambda node, extras: compound_targets.cursorless_range(extras),
)
range_rule = RuleWrap("", range_compound).rule
  
''' target '''  # top level
    
# target_compound = Compound(
#     # spec="<range1> [<list_connective1> <range2>]",
#     spec="<range1> [<list_connective1> <range2> [<list_connective2> <range3>]]",
#     # spec="<range1> [<list_connective1> <range2> [<list_connective2> <range3> [<list_connective3> <range4>]]]",
#     # spec="<range1> [<list_connective1> <range2> [<list_connective2> <range3> [<list_connective3> <range4> [<list_connective4> <range5>]]]]",
#     name="target",
#     extras=[
#             RuleRef(range_rule, "range1"),
#             RuleRef(range_rule, "range2"),
#             RuleRef(range_rule, "range3"),
#             # RuleRef(range_rule, "range4"),
#             # RuleRef(range_rule, "range5"),
#             RuleRef(list_connective_rule, "list_connective1"),
#             RuleRef(list_connective_rule, "list_connective2"),
#             # RuleRef(list_connective_rule, "list_connective3"),
#             # RuleRef(list_connective_rule, "list_connective4"),
#         ],
#     value_func=lambda node, extras: compound_targets.cursorless_target(extras),
# )
# target_rule = RuleWrap("", target_compound).rule

range_repetition = Repetition(
    name="range_repetition",
    child=Compound(
        spec="<list_connective> <range>", 
        name="range_repetition",
        extras=[
            get_ref("list_connective"),
            # RuleRef(list_connective_rule, "list_connective"),
            RuleRef(range_rule, "range"),
        ]
    ),
    min=0,
    max=3,
    optimize=True, 
)

target_compound = Compound(
    spec="<range> [<range_repetition>]",
    name="target",
    extras=[
            RuleRef(range_rule, "range"),
            range_repetition,
        ],
    value_func=lambda node, extras: compound_targets.cursorless_target(extras),
)
target_rule = RuleWrap("", target_compound).rule

    
#''' {positional_action} <positional_target> '''

''' positional target ''' # top level

positional_target_compound = Compound(
    spec="(<position> | <source_destination_connective>) <target>",
    name="positional_target",
    extras=[
            modifier_compounds.position_compound,
            get_ref("source_destination_connective"),
            target_compound,
          ],
    value_func=lambda node, extras: positional_target.cursorless_positional_target(extras),
)

#''' <wrapper> {wrap_action} <target> '''

''' wrapper_paired_delimiter '''

wrapper_paired_delimiter_compound = Compound(
    spec="<wrapper_only_paired_delimiter> |"
        "<wrapper_selectable_paired_delimiter>",
    name="wrapper_paired_delimiter",
    extras=[
            get_ref("wrapper_only_paired_delimiter"),
            get_ref("wrapper_selectable_paired_delimiter"),
          ],
    # returns exact
    # value_func=lambda node, extras: paired_delimiter.cursorless_wrapper_paired_delimiter(extras),
)
