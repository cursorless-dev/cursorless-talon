from dragonfly import MappingRule, Function, Choice
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.state.short import R

from .actions.actions import Actions as action_actions
from .command import Actions as command_actions
from .apps.cursorless_vscode import Actions as vscode_actions
from .actions.wrap import Actions as wrap_actions
# from .actions.reformat import Actions as reformat_actions
from .actions.compounds import action_or_ide_command_compound, swap_targets_compound, move_bring_targets_compound, wrapper_compound
from .compounds import target_compound, positional_target_compound
from .cheatsheet import cheat_sheet as file_cheat_sheet     

from .cursorless_lists import get_ref
    
class Cursorless(MappingRule):
    mapping = {
        "<action_or_ide_command> <target>":
            R(Function(lambda target, action_or_ide_command: action_actions.cursorless_action_or_ide_command(action_or_ide_command, target))),
            
        "<positional_action> <positional_target>":
            R(Function(lambda positional_action, positional_target: command_actions.cursorless_single_target_command(positional_action, positional_target))),
        
        "<swap_action> <swap_targets>":
            R(Function(lambda swap_action, swap_targets: command_actions.cursorless_multiple_target_command(swap_action, swap_targets))),
    
        # memory hungry to cache
        # "<move_bring_action> <move_bring_targets>":
        #     R(Function(lambda move_bring_action, move_bring_targets: command_actions.cursorless_multiple_target_command(move_bring_action, move_bring_targets))),

        # not implemented
        # "<reformat_action> <formatters> at <target>": 
        #     R(Function(lambda formatters, target: reformat_actions.cursorless_reformat(target, formatters))),

        "<wrapper> <wrap_action> <target>":
            R(Function(lambda wrap_action, target, wrapper: wrap_actions.cursorless_wrap(wrap_action, target, wrapper))),

        "cursor less settings":
            R(Function(vscode_actions.cursorless_show_settings_in_ide)),
    
        "cursor less cheat sheet":
            R(Function(file_cheat_sheet.Actions.cursorless_cheat_sheet_show_html)),
        "cursor less help":
            R(Function(file_cheat_sheet.Actions.cursorless_open_instructions)),
    }
    extras = [ 
        action_or_ide_command_compound,
        target_compound,
        get_ref("positional_action"),
        positional_target_compound,
        get_ref("swap_action"),
        swap_targets_compound,
        get_ref("move_bring_action"),
        move_bring_targets_compound,
        # get_ref("reformat_action"),
        get_ref("wrap_action"),
        wrapper_compound,
    ]
    
def get_rule():
    details = RuleDetails(name="cursor less",
                          executable=["code", "VSCodium"],
                          title=["Visual Studio Code", "VSCodium"])
    return Cursorless, details