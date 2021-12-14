# Cursorless custom VSCode actions

You can use Cursorless to run any built-in VSCode command on a specific target.

Just add your custom commands to: `actions_custom.csv`

```csv
Spoken form, VSCode command
custom, editor.action.addCommentLine
```

You can now use the command: `custom blue air` to comment the line containing the token with the `blue a` hat. 