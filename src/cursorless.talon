app: vscode
-
tag(): user.cursorless

{self.cursorless_simple_action} <user.cursorless_target>:
    user.cursorless_single_target_command(cursorless_simple_action, cursorless_target)

<user.cursorless_makeshift_action> <user.cursorless_target>:
    user.cursorless_run_makeshift_action(cursorless_makeshift_action, cursorless_target)

<user.cursorless_wrapper> wrap <user.cursorless_target>:
    user.cursorless_single_target_command_with_arg_list("wrap", cursorless_target, cursorless_wrapper)

wrap <user.cursorless_target> with funk <user.code_functions>:
    user.cursorless_single_target_command("wrap", cursorless_target, "{code_functions}(", ")")

line wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "\n", "\n")

extract <user.cursorless_target>:
    user.cursorless_single_target_command("extractVariable", cursorless_target)

extract <user.cursorless_target> as <user.text>:
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
