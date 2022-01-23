import json
import re

from talon import actions, app

regex = re.compile(r"\{(\w+):([^}]+)\}")


def process_tutorial_step(raw: str):
    print([(match.group(1), match.group(2)) for match in regex.finditer(raw)])
    content = raw

    return {
        "content": content,
        "restore_callback": print,
        "modes": ["command"],
        "app": "Code",
        "context_hint": "Please open VSCode and enter command mode",
    }


def get_basic_coding_walkthrough():
    with open(
        "/Users/pokey/src/cursorless-vscode/src/test/suite/fixtures/recorded/tutorial/unit-2-basic-coding/script.json"
    ) as f:
        script = json.load(f)

    return [
        actions.user.hud_create_walkthrough_step(**process_tutorial_step(step))
        for step in script
    ]


def on_ready():
    actions.user.hud_add_lazy_walkthrough(
        "Cursorless basic coding", get_basic_coding_walkthrough
    )


app.register("ready", on_ready)
