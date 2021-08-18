from talon import actions, fs, app
import os
from datetime import datetime
from pathlib import Path

directory_name = "cursorless-settings"


def init_csv_and_watch_changes(
    filename: str, default_values: list[dict], callback: callable
):
    dir_path, file_path = get_file_paths(filename)
    super_default_values = join_dicts(default_values)

    if not dir_path.is_dir():
        os.mkdir(dir_path)

    def on_watch(path, flags):
        if file_path.match(path):
            current_values = read_file(file_path, super_default_values.values())
            update_dicts(default_values, current_values, callback)

    fs.watch(dir_path, on_watch)

    if file_path.is_file():
        current_values = update_file(file_path, super_default_values)
        update_dicts(default_values, current_values, callback)
    else:
        create_file(file_path, super_default_values)
        update_dicts(default_values, super_default_values, callback)


def update_dicts(default_values: list[dict], current_values: dict, callback: callable):
    # Create map with all default values
    results_map = {}
    for i in range(len(default_values)):
        for key, value in default_values[i].items():
            results_map[value] = {"key": key, "value": value, "index": i}

    # Update result with current values
    for key, value in current_values.items():
        results_map[value]["key"] = key

    # Convert result map back to result list
    results = [{} for _ in default_values]
    for obj in results_map.values():
        results[obj["index"]][obj["key"]] = obj["value"]

    callback(results)


def update_file(path, default_values: dict):
    current_values = read_file(path, default_values.values())
    current_identifiers = current_values.values()

    missing = {}
    for key, value in default_values.items():
        if value not in current_identifiers:
            missing[key] = value

    if missing:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "\n",
            f"# {timestamp} - Added new commands\n",
            *[create_line(key, missing[key]) for key in sorted(missing)],
        ]
        write_file(path, lines, "a")

        message = f"Cursorless added new commands to {path.name}"
        print(message)
        for key in sorted(missing):
            print(f"{key}: {missing[key]}")
        app.notify(message)

    return current_values


def create_file(path, default_values: dict):
    lines = [create_line(key, default_values[key]) for key in sorted(default_values)]
    lines.insert(0, create_line("# Spoken words", "Identifier"))
    write_file(path, lines, "w")


def write_file(path, lines, mode):
    with open(path, mode) as f:
        f.writelines(lines)


def read_file(path, default_identifiers: list[str]) -> dict:
    with open(path, "r") as f:
        lines = f.read().splitlines()

    result = {}
    for i in range(len(lines)):
        line = lines[i].strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        key, value = read_line(line, path, i)
        assert value in default_identifiers, f"Unknown identifier {value}"
        result[key] = value
    return result


def create_line(key: str, value: str):
    return f"{key}, {value}\n"


def read_line(line: str, path, index: int):
    parts = line.split(",")
    assert len(parts) == 2, f"Malformed {path.name}:{index+1} | {line}"
    key = parts[0].strip()
    value = parts[1].strip()
    return key, value


def join_dicts(dicts: list[dict]):
    result = {}
    for dict in dicts:
        result.update(dict)
    return result


def get_file_paths(filename: str):
    if not filename.endswith(".csv"):
        filename = f"{filename}.csv"
    user_dir = actions.path.talon_user()
    dir_path = Path(user_dir, directory_name)
    csv_path = Path(dir_path, filename)
    return dir_path, csv_path
