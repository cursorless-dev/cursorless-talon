# Cursorless custom VSCode actions

You can use Cursorless to run any built-in VSCode command on a specific target.

Just add your custom commands to: `experimental/actions_custom.csv`.  For example, if you wanted to be able to say `"push down <T>"` to move the line(s) containing target `<T>` downwards, you could do the following:

```csv
Spoken form, VSCode command
custom, editor.action.addCommentLine
```

You can now use the command: `custom blue air` to comment the line containing the token with the `blue a` hat. 