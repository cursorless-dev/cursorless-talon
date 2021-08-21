# Customization

Many of the words used in cursorless can be easily customized without needing
to fork cursorless or modify the talon / python files contained therein. If you
find that your customization needs cannot be met without making changes to
cursorless files, please [file an issue](https://github.com/pokey/cursorless-talon/issues/new) so we can try to improve customization.

## Cursorless settings csvs

The words for actions, scope types, colors, etc can be customized using the
csvs found in the `cursorless-settings` subdirectory of your user folder. On
Linux and Mac, the directory is `~/.talon/user/cursorless-settings`. On
Windows, it is `%AppData%\Talon\user\cursorless-settings`.

Note that these csv's have no header column, and support empty lines, as well as comment lines beginning with `#`. All spoken forms and cursorless identifiers will automatically be stripped of leading and trailing whitespace.

### Changing a word

Simply modify the spoken form in the first column of any of the csvs above to
change the word you'd like to use.

### New features

When new actions, scope types, etc are added, Cursorless will detect that they're missing from your csvs and append the default term to the end. You can then feel free to modify the spoken form if you'd like to change it.

### Removing a term

If you'd like to remove an action, scope type, etc, you can simply set the
spoken form in the first column to `-`. Please don't delete any lines, as that
will trigger cursorless to automatically add the spoken form back on talon
restart.
