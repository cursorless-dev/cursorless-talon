app: vscode
-
{self.simple_cursorless_action} <user.cursorless_target>:
    user.cursorless_single_target_command(simple_cursorless_action, cursorless_target)

drink <user.cursorless_target>:
    user.cursorless_single_target_command("setSelectionBefore", cursorless_target)
    user.new_line_above()

pour <user.cursorless_target>:
    user.cursorless_single_target_command("setSelectionAfter", cursorless_target)
    user.new_line_below()

def show <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("editor.action.revealDefinition")

ref show <user.cursorless_target>:
    user.cursorless_single_target_command("setSelection", cursorless_target)
    user.vscode("references-view.find")

wrap <user.cursorless_target> with funk <user.code_functions>:
    user.cursorless_single_target_command("wrap", cursorless_target, "{code_functions}(", ")")

square wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "[", "]")

round wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "(", ")")

curly wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "{", "}")

(diamond | angle) wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "<", ">")

quad wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "\"", "\"")

twin wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "'", "'")
    
escaped quad wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "\\\"", "\\\"")

escaped twin wrap <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "\\'", "\\'")

puff <user.cursorless_target>:
    user.cursorless_single_target_command("wrap", cursorless_target, "\n", "\n")

extract <user.cursorless_target>:
    user.cursorless_single_target_command("extractVariable", cursorless_target)

extract <user.cursorless_target> as <user.text>:
    user.cursorless_single_target_command("extractVariable", cursorless_target)
    sleep(300ms)
    user.code_public_variable_formatter(text)
    key(enter)

swap <user.cursorless_target> with <user.cursorless_target>:
    user.cursorless_multiple_target_command("swap", cursorless_target_list)

# action(user.dental_click): user.vscode("cursorless.toggleDecorations")