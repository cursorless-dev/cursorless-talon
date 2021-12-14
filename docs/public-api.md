# Cursorless public API

## Public Talon captures
* `<user.cursorless_target>`    
    Represents a cursorless target. This target can be a single mark, multiple marks or a range.

## Public Talon actions
* `user.cursorless_command(action_id: str, target: cursorless_target)`    
    Perform a Cursorless command on the given target    
    eg: `user.cursorless_command("setSelection", cursorless_target)`
* `user.cursorless_vscode_command(command_id: str, target: cursorless_target)`    
    Performs a VSCode command on the given target    
    eg: `user.cursorless_vscode_command("editor.action.addCommentLine", cursorless_target)`

## Example of combining capture and action
```talon
select <user.cursorless_target>:
    user.cursorless_command("setSelection", cursorless_target)

comment <user.cursorless_target>:
    user.cursorless_vscode_command("editor.action.addCommentLine", cursorless_target)
```