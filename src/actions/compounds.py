from dragonfly import Compound, Choice, RuleRef
from ..cursorless_lists import get_ref
from . import actions
from . import swap
from . import move_bring
from . import wrap
from .. import compounds as base_compounds

#''' <action_or_ide_command> <target> '''

''' action_or_ide_command ''' # top level

action_or_ide_command_compound = Compound(
    spec="<simple_action> | <callback_action> | <custom_action>",
    name="action_or_ide_command",
    extras=[
            get_ref("simple_action"),
            get_ref("callback_action"),
            get_ref("custom_action"),
        ],
    value_func=lambda node, extras: actions.cursorless_action_or_ide_command(extras),     
)

#''' {swap_action} <swap_targets> '''

''' swap_targets ''' # top level

swap_targets_compound = Compound(
    spec="[<target1>] <swap_connective> <target2>",
    name="swap_targets",
    extras=[
            RuleRef(base_compounds.target_rule, "target1"),
            get_ref("swap_connective"),
            RuleRef(base_compounds.target_rule, "target2"),
          ],
    value_func=lambda node, extras: swap.cursorless_swap_targets(extras),
)

#''' {move_bring_action} <move_bring_targets> '''

''' move_bring_targets ''' # top level

move_bring_targets_compound = Compound(
    spec="<target> [<positional_target>]",
    name="move_bring_targets",
    extras=[
            base_compounds.target_compound,
            base_compounds.positional_target_compound,
          ],
    value_func=lambda node, extras: move_bring.cursorless_move_bring_targets(extras),
)

#''' <wrapper> {wrap_action} <target> '''

''' wrapper ''' # top level

wrapper_compound = Compound(
    spec="<wrapper_paired_delimiter> | <wrapper_snippet>",
    name="wrapper",
    extras=[
            base_compounds.wrapper_paired_delimiter_compound,
            get_ref("wrapper_snippet"),
          ],
    value_func=lambda node, extras: wrap.cursorless_wrapper(extras),
)
