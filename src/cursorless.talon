app: vscode
-
{self.simple_cursorless_action} <user.cursorless_target>:
    user.cursorless_single_target_command(simple_cursorless_action, cursorless_target)

def show <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("editor.action.revealDefinition")

ref show <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("references-view.find")

hover show <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("editor.action.showHover")

quick fix <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    sleep(300ms)
    user.vscode("editor.action.quickFix")

<user.cursorless_wrapper> wrap <user.cursorless_target>:
    user.cursorless_single_target_command_with_arg_list("wrap", cursorless_target, cursorless_wrapper)

wrap <user.cursorless_target> with funk <user.code_functions>:
    user.cursorless_single_target_command("wrap", cursorless_target, "{code_functions}(", ")")

puff <user.cursorless_target>:
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

<user.cursorless_use>:
    user.cursorless_multiple_target_command("use", cursorless_use)

pour cell <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("jupyter.insertCellBelow")

pour cell:
    user.vscode("jupyter.insertCellBelow")

drink cell <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("jupyter.insertCellAbove")

drink cell:
    user.vscode("jupyter.insertCellAbove")

rename <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("editor.action.rename")
    sleep(100ms)