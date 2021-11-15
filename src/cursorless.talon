app: vscode
-

<user.cursorless_simple_action> <user.cursorless_target>:
    user.cursorless_simple_action(cursorless_simple_action, cursorless_target)

{user.cursorless_swap_action} <user.cursorless_swap_targets>:
    user.cursorless_multiple_target_command(cursorless_swap_action, cursorless_swap_targets)

{user.cursorless_move_bring_action} <user.cursorless_move_bring_targets>:
    user.cursorless_multiple_target_command(cursorless_move_bring_action, cursorless_move_bring_targets)

{user.cursorless_reformat_action} <user.formatters> at <user.cursorless_target>:
    user.cursorless_reformat(cursorless_target, formatters)

<user.cursorless_wrapper> <user.cursorless_target>:
    user.cursorless_wrap(cursorless_wrapper, cursorless_target)

cursorless help:           user.cursorless_cheat_sheet_toggle()
cursorless instructions:   user.cursorless_open_instructions()