from talon import Context, Module
import copy

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.cursorless
"""

containing_scope_type_map = {
    "arg": "argumentOrParameter",
    "arrow": "arrowFunction",
    "call": "functionCall",
    "class name": "className",
    "class": "class",
    "comment": "comment",
    "funk name": "functionName",
    "funk": "namedFunction",
    "if": "ifStatement",
    "item": "collectionItem",
    "key": "collectionKey",
    "lambda": "arrowFunction",
    "list": "list",
    "map": "dictionary",
    "name": "name",
    "regex": "regex",
    "state": "statement",
    "string": "string",
    "type": "type",
    "value": "value",
    #  XML, JSX
    "attribute": "xmlAttribute",
    "element": "xmlElement",
    "tags": "xmlBothTags",
    "start tag": "xmlStartTag",
    "end tag": "xmlEndTag",
}

containing_scope_types = {
    term: {
        "modifier": {
            "type": "containingScope",
            "scopeType": containing_scope_type,
        }
    }
    for term, containing_scope_type in containing_scope_type_map.items()
}

mod.list("cursorless_containing_scope_type", desc="Supported containing scope types")
ctx.lists["self.cursorless_containing_scope_type"] = containing_scope_types.keys()


@mod.capture(rule="{user.cursorless_containing_scope_type}")
def cursorless_containing_scope_type(m) -> str:
    return containing_scope_types[m.cursorless_containing_scope_type]


@mod.capture(rule=("[every] <user.cursorless_containing_scope_type>"))
def cursorless_containing_scope(m) -> str:
    """Supported containing scope types"""
    if m[0] == "every":
        current_target = copy.deepcopy(m.cursorless_containing_scope_type)
        current_target["modifier"]["includeSiblings"] = True
        return current_target
    return m.cursorless_containing_scope_type
