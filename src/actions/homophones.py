# from talon import actions, app

from .get_text import get_text
from .replace import Actions as replace_actions


def run_homophones_action(targets: dict):
    raise NotImplementedError
    """Replaced target with next homophone"""
    texts = get_text(targets, show_decorations=False)
    try:
        updated_texts = list(map(get_next_homophone, texts))
    except LookupError as e:
        # app.notify(str(e))
        return
    replace_actions.cursorless_replace(targets, updated_texts)


def get_next_homophone(word: str):
    # homophones = actions.user.homophones_get(word)
    homophones = None
    if not homophones:
        raise LookupError(f"Found no homophones for '{word}'")
    index = (homophones.index(word.lower()) + 1) % len(homophones)
    homophone = homophones[index]
    return format_homophone(word, homophone)


def format_homophone(word: str, homophone: str):
    if word.isupper():
        return homophone.upper()
    if word == word.capitalize():
        return homophone.capitalize()
    return homophone
