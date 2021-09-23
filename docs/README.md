# Cursorless - Instructions

You may find it helpful to start with the [tutorial video](https://www.youtube.com/watch?v=JxcNW0hnfTk).

Once you understand the concepts, you can pull up a cheatsheet for reference using the command `"cursorless help"`.

You can get back to these docs by saying `"cursorless docs"`.

Note: If you'd like to customize any of the spoken forms, please see the [documentation](customization.md).

## Table of contents

- [Table of contents](#table-of-contents)
- [Overview](#overview)
- [Targets](#targets)
  - [Primitive targets](#primitive-targets)
    - [Marks](#marks)
      - [Decorated symbol](#decorated-symbol)
        - [Colors](#colors)
        - [Shapes](#shapes)
      - [`"this"`](#this)
      - [`"that"`](#that)
    - [Modifiers](#modifiers)
      - [Syntactic scopes](#syntactic-scopes)
      - [`"every"`](#every)
      - [Sub-token modifiers](#sub-token-modifiers)
        - [`"word"`](#word)
        - [`"char"`](#char)
      - [`"line"`](#line)
      - [`"file"`](#file)
  - [Compound targets](#compound-targets)
    - [Range targets](#range-targets)
    - [List targets](#list-targets)
- [Actions](#actions)
  - [Cursor movement](#cursor-movement)
  - [Delete](#delete)
  - [Changing a target](#changing-a-target)
  - [Cut / copy](#cut--copy)
  - [Swap](#swap)
  - [Insert empty lines](#insert-empty-lines)
  - [Rename](#rename)
  - [Scroll](#scroll)
  - [Insert/Use/Repeat](#insertuserepeat)
  - [Wrap](#wrap)
  - [Show definition/reference/quick fix](#show-definitionreferencequick-fix)
  - [Fold/unfold](#foldunfold)
  - [Extract](#extract)

## Overview

Every cursorless command consists of an action performed on a target. For example, the command `"chuck blue air"` deletes the token with a blue hat over the `"a"`. In this command, the action is `"chuck"` (delete), and the target is `"blue air"`.

## Targets

There are two types of targets: primitive targets and compound targets. Compound targets are constructed from primitive targets, so let's begin with primitive targets.

### Primitive targets

A primitive target consists of a mark and one or more optional modifiers. The simplest primitive targets just consist of a mark without any modifiers, so let's begin with those

#### Marks

There are several types of marks:

##### Decorated symbol

This is the first type of mark you'll notice when you start using cursorless. You'll see that for every token on the screen, one of its characters will have a hat on top of it. We can refer to the given token by saying the name of the character that has a hat, along with the color if the hat is not gray, and the shape of the hat if the hat is not the default dot:

- `"air"` (if the color is gray)
- `"blue bat"`
- `"blue dash"`
- `"blue five"`
- `"fox bat"`
- `"blue fox bat"`

The general form of this type of mark is:

`"[<color>] [<shape>] (<letter> | <symbol> | <number>)"`

Combining this with an action, we might say `"take blue air"` to select the token containing letter `'a'` with a blue hat over it.

###### Colors

The following colors are supported:

| Spoken form | Visible color |
| ----------- | ------------- |
| `"blue"`    | Blue          |
| `"green"`   | Green         |
| `"rose"`    | Red           |
| `"squash"`  | Yellow        |
| `"plum"`    | Pink          |

###### Shapes

The following shapes are supported:

| Spoken form | Shape                                                                                          | Enabled by default? |
| ----------- | ---------------------------------------------------------------------------------------------- | ------------------- |
| `"ex"`      | ![Ex](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/ex.svg)       | ❌                  |
| `"fox"`     | ![Fox](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/fox.svg)     | ❌                  |
| `"wing"`    | ![Wing](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/wing.svg)   | ❌                  |
| `"hole"`    | ![Hole](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/hole.svg)   | ❌                  |
| `"frame"`   | ![Frame](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/frame.svg) | ❌                  |
| `"curve"`   | ![Curve](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/curve.svg) | ❌                  |
| `"eye"`     | ![Eye](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/eye.svg)     | ❌                  |
| `"play"`    | ![Play](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/play.svg)   | ❌                  |
| `"star"`    | ![Star](https://raw.githubusercontent.com/pokey/cursorless-vscode/main/images/hats/star.svg)   | ❌                  |

To enable or disable shapes requires the following two steps:

1. Check the box corresponding to the given shape in the `cursorless.hatEnablement.shapes` field of the cursorless vscode settings
2. Enable the corresponding spoken form in the [spoken form customization csvs](customization.md) for cursorless talon

##### `"this"`

The word `"this"` can be used as a mark to refer to the current cursor(s) or selection(s). Note that when combined with a modifier, the `"this"` mark can be omitted, and it will be implied.

- `chuck this`
- `take this funk`
- `pre funk`
- `chuck line`

##### `"that"`

The word `"that"` can be used as a mark to refer to the target of the previous cursorless command.

- `"pre that"`
- `"round wrap that"`

#### Modifiers

Modifiers can be applied to any mark to modify its extent. This is commonly used to refer to larger syntactic elements within a source code document.

Note that if the mark is `"this"`, and you have multiple cursors, the modifiers will be applied to each cursor individually.

##### Syntactic scopes

| Term           | Syntactic element                            |
| -------------- | -------------------------------------------- |
| `"arg"`        | function parameter or function call argument |
| `"arrow"`      | anonymous lambda function                    |
| `"call"`       | function call, eg `foo(1, 2)`                |
| `"class"`      | class definition                             |
| `"class name"` | the name in a class declaration              |
| `"comment"`    | comment                                      |
| `"element"`    | list element                                 |
| `"funk"`       | function definition                          |
| `"funk name"`  | the name in a function declaration           |
| `"if"`         | if statement                                 |
| `"key"`        | key in a map / object                        |
| `"lambda"`     | equivalent to `"arrow"`                      |
| `"list"`       | list                                         |
| `"map"`        | map / object                                 |
| `"name"`       | the name in a declaration (eg function name) |
| `"pair"`       | an entry in a map / object                   |
| `"state"`      | a statement, eg `let foo;`                   |
| `"string"`     | string                                       |
| `"type"`       | a type annotation or declaration             |
| `"value"`      | a value in a map / object                    |

For example, `"take funk blue air"` selects the function containing the token with a blue hat over the letter `'a'`.

##### `"every"`

The command `"every"` can be used to select a syntactic element and all of its matching siblings.

- `"take every key air"`
- `"take every funk air"`
- `"take every key"` (if cursor is currently within a key)

For example, the command `take every key [blue] air` will select every key in the map/object/dict including the token with a blue hat over the letter 'a'.

##### Sub-token modifiers

###### `"word"`

If you need to refer to the individual words within a `camelCase`/`kebab-case`/`snake_case` token, you can use the `"word"` modifier. For example,

- `"second word air"`
- `"second through fourth word air"`
- `"last word air"`

For example, the following command:

    "take second through fourth word blue air"

Selects the second, third and fourth word in the token containing letter 'a' with a blue hat.

###### `"char"`

You can also refer to individual characters within a token:

- `"second char air"`
- `"second through fourth char air"`
- `"last char air"`

##### `"line"`

The word `"line"` can be used to expand a target to refer to entire lines rather than individual tokens:

eg:  
`take line [blue] air`  
Selects the line including the token containing letter 'a' with a blue hat.

##### `"file"`

The word file can be used to expand the target to refer to the entire file.

- `"copy file"`
- `"take file"`
- `"take file blue air"`

For example, `"take file [blue] air"` selects the file including the token containing letter 'a' with a blue hat.

### Compound targets

Individual targets can be combined into compound targets to make bigger targets or refer to multiple selections at the same time.

#### Range targets

A range target uses one primitive target as its start and another as its end to form a range from the start to the end. For example, `"air past bat"` refers to the range from the token with a hat over its 'a' to a token with a hat over its 'b'.

Note that if the first target is omitted, the start of the range will be the current selection(s).

- `"take [blue] air past [green] bat"`
- `"take past [blue] air"`
- `"take funk [blue] air past [blue] bat"` (note end of range inherits `"funk"`)
- `"take funk [blue] air past token [blue] bat"`
- `"take past before [blue] air"`
- `"take after [blue] air past before [blue] bat"`
- `"take past end of line"`
- `"take past start of line"`
- `"take [blue] air past end of line"` (but see [pokey/cursorless-vscode#4](https://github.com/pokey/cursorless-vscode/issues/4))

eg:  
`take blue air past green bat`  
Selects the range from the token containing letter 'a' with a blue hat past the token containing letter 'b' with a green hat.

#### List targets

In addition to range targets, cursorless supports list targets, which allow you to refer to multiple targets at the same time. When combined with the `"take"` action, this will result in multiple cursors, for other actions, such as `"chuck"` the action will be applied to all the different targets at once.

- `"take [blue] air and [green] bat"`
- `"take funk [blue] air and [green] bat"` (note second target inherits `"funk"`)
- `"take funk [blue] air and token [green] bat"` [blue] air and [green] bat
- `"take air and bat past cap"`

eg:  
`take blue air and green bat`  
Selects both the token containing letter 'a' with a blue hat AND the token containing 'b' with a green hat.

## Actions

In any cursorless command the action defines what happens to the given target, for example deleting the target (`"chuck"`) or moving the cursor to select the target (`"take"`).

### Cursor movement

Despite the name cursorless, some of the most basic commands in cursorless are for moving the cursor.

Note that when combined with list targets, these commands will result in multiple cursors

- `"take"`: Selects the given target
- `"pre"`: Places the cursor before the given target
- `"post"`: Places the cursor after the given target

eg:  
`pre blue air`  
Moves the cursor to before the token containing letter 'a' with a blue hat.

### Delete

This command can be used to delete a target without moving the cursor

- `"chuck"`

eg:  
`chuck blue air`  
Deletes the token containing letter 'a' with a blue hat.

### Changing a target

This command will delete a target and leave the cursor where the target used to be, making it easy to change a target

- `"clear"`

### Cut / copy

- `"cut"`
- `"copy"`

eg:  
`copy blue air`  
Copies the token containing letter 'a' with a blue hat.

### Swap

Swaps two targets. If the first target is omitted, it will refer to the current selection. If the targets are list targets they will be zipped together.

- `"swap <TARGET 1> with <TARGET 2>"`
- `"swap with <TARGET>"`

eg:  
`swap blue air with green bat`

Swaps the given tokens.

### Insert empty lines

- `"drink"`: Inserts a new line above the current line, and moves the cursor to the newly created line
- `"pour"`: Inserts a new line below the current line, and moves the cursor to the newly created line

eg:  
`pour blue air`  
Insert empty line below the token containing letter 'a' with a blue hat.

### Rename

Executes vscode rename action on the given target

- `"rename"`

eg:  
`rename blue air`  
Rename the token containing letter 'a' with a blue hat.

### Scroll

Scrolls a given target to the top, center or bottom of the screen.

- `"top"`
- `"center"`
- `"bottom"`

eg `top blue air` scrolls the line containing the letter 'a' with a blue hat to the top of the screen.

### Insert/Use/Repeat

The `"bring"` command can be used to replace one target with another, or to use a target at the current cursor position.

- `"bring <TARGET>"`: Inserts the given target at the cursor position
- `"bring <TARGET 1> to <TARGET 2>"`

eg:  
`bring blue air to green bat`  
Replaces the token containing letter 'b' with a green hat using the token containing letter 'a' with a blue hat.

### Wrap

The wrap commands can be used to wrap a given target with a pair of symbols

| Term                                        | Symbol inserted before target | Symbol inserted after target |
| ------------------------------------------- | ----------------------------- | ---------------------------- |
| `"square wrap"`                             | `[`                           | `]`                          |
| `"round wrap"`                              | `(`                           | `)`                          |
| `"curly wrap"`                              | `{`                           | `}`                          |
| `"(diamond \| angle) wrap"`                 | `<`                           | `>`                          |
| `"quad wrap"`                               | `"`                           | `"`                          |
| `"twin wrap"`                               | `'`                           | `'`                          |
| `"escaped quad wrap"`                       | `\"`                          | `\"`                         |
| `"escaped twin wrap"`                       | `\'`                          | `\'`                         |
| `"line wrap"`                               | `\n`                          | `\n`                         |
| `"wrap <TARGET> with funk <FUNCTION_NAME>"` | `<FUNCTION_NAME>(`            | `)`                          |

eg:  
`square wrap blue air`  
Wraps the token containing letter 'a' with a blue hat in square brackets.

### Show definition/reference/quick fix

- `"def show"`
- `"ref show"`
- `"hover show"`
- `"quick fix"`

eg:  
`def show blue air`  
Shows definition for the token containing letter 'a' with a blue hat.

### Fold/unfold

Note that these actions will only work if referring to the entire target, not just the first line (see [#72](https://github.com/pokey/cursorless-vscode/issues/72)).

- `"fold"`
- `"unfold"`

eg:  
`fold funk blue air`  
Fold the function with the token containing letter 'a' with a blue hat.

### Extract

Extracts a target as a variable using the VSCode refactor action

- `"extract"`
- `"extract {TARGET} as hello world"`

eg:  
`extract call air`

Extracts the function call containing the decorated 'a' into its own variable.
