import json
import re

regex = re.compile(r"\{(\w+):([^}]+)\}")

def process_tutorial_step(raw: str):
    print([(match.group(1), match.group(2)) for match in regex.finditer(raw)])
    content = "whatever"

    return {
        "content": content,
		"modes": ["command"],
		"app": "vscode",		
		"context_hint": "Please open VSCode",
    }

with open("/Users/pokey/src/cursorless-vscode/src/test/suite/fixtures/recorded/tutorial/unit-2-basic-coding/script.json") as f:
    script = json.load(f)

print([process_tutorial_step(step) for step in script])