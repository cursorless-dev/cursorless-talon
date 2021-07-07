from talon import Context, Module

mod = Module()
ctx = Context()

ctx.matches = r"""
app: vscode
"""

containing_scope_type_map = {
    "arg": "argumentOrParameter",
    "arrow": "arrowFunction",
    "call": "functionCall",
    "class": "class",
    "comment": "comment",
    "element": "listElement",
    "funk": "namedFunction",
    "if": "ifStatement",
    "key": "pairKey",
    "lambda": "arrowFunction",
    "list": "list",
    "map": "dictionary",
    "pair": "pair",
    "state": "statement",
    "string": "string",
    "value": "value",
    "type": "type",
    "name": "name"
}

containing_scope_types = {
    term: {
        "transformation": {
            "type": "containingScope",
            "scopeType": containing_scope_type,
        }
    }
    for term, containing_scope_type in containing_scope_type_map.items()
}

mod.list("cursorless_containing_scope_type", desc="Supported symbol extent types")
ctx.lists["self.cursorless_containing_scope_type"] = containing_scope_types.keys()

@mod.capture(rule="{user.cursorless_containing_scope_type}")
def cursorless_containing_scope_type(m) -> str:
    return containing_scope_types[m.cursorless_containing_scope_type]


@mod.capture(rule=("[every] <user.cursorless_containing_scope_type>"))
def cursorless_containing_scope(m) -> str:
    """Supported extents for cursorless navigation"""
    if m[0] in ["every"]:
        current_target = m.cursorless_containing_scope_type
        current_target["transformation"]["includeSiblings"] = True
        return current_target
    return m.cursorless_containing_scope_type
