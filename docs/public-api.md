# Cursorless public API

Cursorless exposes a couple talon actions and captures that you can use to define your own custom command grammar leveraging cursorless targets.

## Public Talon captures
* `<user.cursorless_target>`    
    Represents a cursorless target, such as `"air"`, `"this"`, `"air past bat"`, `"air and bat"`, `"funk air past token bat and class cap"`, etc

## Public Talon actions
* `user.cursorless_command(action_id: str, target: cursorless_target)`    
    Perform a Cursorless command on the given target    
    eg: `user.cursorless_command("setSelection", cursorless_target)`
* `user.cursorless_vscode_command(command_id: str, target: cursorless_target)`    
    Performs a VSCode command on the given target    
    eg: `user.cursorless_vscode_command("editor.action.addCommentLine", cursorless_target)`

## Example of combining capture and action
```talon
add dock string <user.cursorless_target>:
    user.cursorless_command("editNewLineAfter", cursorless_target)
    "\"\"\"\"\"\""
    key(left:3)

comment <user.cursorless_target>:
    user.cursorless_vscode_command("editor.action.addCommentLine", cursorless_target)
```