app: vscode
-
tag(): user.cursorless

{user.cursorless_simple_action} <user.cursorless_target>:
    user.cursorless_simple_action(cursorless_simple_action, cursorless_target)

{user.cursorless_multiple_target_action} <user.cursorless_multiple_targets>:
    user.cursorless_multiple_target_command(cursorless_multiple_target_action, cursorless_multiple_targets)

<user.cursorless_wrapper> wrap <user.cursorless_target>:
    user.cursorless_single_target_command_with_arg_list("wrap", cursorless_target, cursorless_wrapper)

# disabling for now until we can figure out dfa compilation
# See https://github.com/pokey/cursorless-talon/issues/58
# replace <user.cursorless_target> with <user.cursorless_replace_value>$:
#     user.cursorless_replace(cursorless_target, cursorless_replace_value)

format <user.formatters> at <user.cursorless_target>:
    user.cursorless_reformat(cursorless_target, formatters)

pour cell:                 user.vscode("jupyter.insertCellBelow")
drink cell:                user.vscode("jupyter.insertCellAbove")

cursorless help:           user.cursorless_cheat_sheet_toggle()
cursorless instructions:   user.cursorless_open_instructions()