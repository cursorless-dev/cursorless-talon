app: vscode
-
tag(): user.cursorless

{user.cursorless_simple_action} <user.cursorless_target>:
    user.cursorless_simple_action(cursorless_simple_action, cursorless_target)

<user.cursorless_wrapper> wrap <user.cursorless_target>:
    user.cursorless_single_target_command_with_arg_list("wrap", cursorless_target, cursorless_wrapper)

wrap <user.cursorless_target> with funk <user.code_functions>:
    user.cursorless_single_target_command("wrap", cursorless_target, "{code_functions}(", ")")

replace <user.cursorless_target> with <user.cursorless_replace_value>$:
    user.cursorless_replace(cursorless_target, cursorless_replace_value)

# TODO Enable when support is in community repository
# reformat <user.cursorless_target> as <user.formatters>:
    # user.cursorless_reformat(cursorless_target, formatters)

extract <user.cursorless_target> as <user.text>$:
    user.cursorless_single_target_command("extractVariable", cursorless_target)
    sleep(300ms)
    user.code_public_variable_formatter(text)
    key(enter)

<user.cursorless_swap>:
    user.cursorless_multiple_target_command("swap", cursorless_swap)

{user.cursorless_move_bring_action} <user.cursorless_move_bring_targets>:
    user.cursorless_multiple_target_command(cursorless_move_bring_action, cursorless_move_bring_targets)

pour cell:
    user.vscode("jupyter.insertCellBelow")

drink cell:
    user.vscode("jupyter.insertCellAbove")

cursorless help:           user.cursorless_cheat_sheet_toggle()
cursorless instructions:   user.cursorless_open_instructions()