from talon import Module, actions

mod = Module()


@mod.capture(rule="count [from <number_small>]")
def cursorless_count(m) -> str:
    try:
        start = m.number_small
    except AttributeError:
        start = 0
    return {"start": start}


@mod.capture(rule="[<user.formatters>] <user.text> (and <user.text>)*")
def cursorless_texts(m) -> str:
    texts = m.text_list
    try:
        formatters = m.formatters
        texts = list(
            map(lambda text: actions.user.formatted_text(text, formatters), texts)
        )
    except AttributeError:
        pass
    return texts


@mod.capture(rule="<user.cursorless_texts> | <user.cursorless_count>")
def cursorless_replace_value(m) -> str:
    return m[0]


@mod.action_class
class Actions:
    def cursorless_replace(targets: dict, texts: list[str] or dict):
        """Replaced targets with texts"""
        actions.user.cursorless_single_target_command("replace", targets, texts)
