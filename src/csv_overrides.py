from talon import Context, actions, fs, app
import os
from datetime import datetime
from pathlib import Path

directory_name = "cursorless-settings"

ctx = Context()


def init_csv_and_watch_changes(filename: str, default_values: dict[str, dict]):
    dir_path, file_path = get_file_paths(filename)
    super_default_values = get_super_values(default_values)

    dir_path.mkdir(parents=True, exist_ok=True)

    def on_watch(path, flags):
        if file_path.match(path):
            current_values, has_errors = read_file(
                file_path, super_default_values.values()
            )
            update_dicts(default_values, current_values)

    fs.watch(dir_path, on_watch)

    if file_path.is_file():
        current_values = update_file(file_path, super_default_values)
        update_dicts(default_values, current_values)
    else:
        create_file(file_path, super_default_values)
        update_dicts(default_values, super_default_values)


def update_dicts(default_values: dict[str, dict], current_values: dict):
    # Create map with all default values
    results_map = {}
    for list_name, dict in default_values.items():
        for key, value in dict.items():
            results_map[value] = {"key": key, "value": value, "list": list_name}

    # Update result with current values
    for key, value in current_values.items():
        results_map[value]["key"] = key

    # Convert result map back to result list
    results = {key: {} for key in default_values}
    for obj in results_map.values():
        results[obj["list"]][obj["key"]] = obj["value"]

    # Assign result to talon context list
    for list_name, dict in results.items():
        ctx.lists[f"user.cursorless_{list_name}"] = dict


def update_file(path: Path, default_values: dict):
    current_values, has_errors = read_file(path, default_values.values())
    current_identifiers = current_values.values()

    missing = {}
    for key, value in default_values.items():
        if value not in current_identifiers:
            missing[key] = value

    if missing and not has_errors:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lines = [
            "\n",
            f"# {timestamp} - New entries automatically added by cursorless\n",
            *[create_line(key, missing[key]) for key in sorted(missing)],
        ]
        write_file(path, lines, "a")

        message = f"🎉🎉 New cursorless features in {path.name}"
        print(message)
        for key in sorted(missing):
            print(f"{key}: {missing[key]}")
        app.notify(message)

    return current_values


def create_file(path: Path, default_values: dict):
    lines = [create_line(key, default_values[key]) for key in sorted(default_values)]
    lines.insert(0, create_line("# Spoken form", "Cursorless identifier"))
    path.write_text("\n".join(lines))


def write_file(path, lines, mode):
    with open(path, mode) as f:
        f.writelines(lines)


def csv_assertion(condition: bool, path: Path, index: int, message: str, value: str):
    """Check that an expected condition is true

    Note that we try to continue reading in this case so cursorless doesn't get bricked

    Args:
        condition (bool): The condition that should be true.
        path (Path): The path of the CSV (for error reporting)
        index (int): The index into the file (for error reporting)
        text (str): The text of the error message to report if condition is false
    """
    if condition:
        return True
    error_message = (
        f"Cursorless settings csv error {path.name}:{index+1} | {message} | {value}"
    )
    app.notify(error_message)
    print(error_message)

    return False


def read_file(path: Path, default_identifiers: list[str]):
    with open(path) as f:
        lines = list(f)

    print(path)
    result = {}
    used_identifiers = []
    has_errors = False
    for i, raw_line in enumerate(lines):
        line = raw_line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue

        parts = line.split(",")
        has_errors = has_errors or not csv_assertion(
            len(parts) == 2, path, i, "Malformed csv", line
        )
        key = parts[0].strip()
        value = parts[1].strip()

        has_errors = has_errors or not csv_assertion(
            value in default_identifiers, path, i, "Unknown identifier", value
        )
        has_errors = has_errors or not csv_assertion(
            value not in used_identifiers, path, i, "Duplicate identifier", value
        )

        result[key] = value
        used_identifiers.append(value)
    return result, has_errors


def create_line(key: str, value: str):
    return f"{key}, {value}\n"


def get_file_paths(filename: str):
    if not filename.endswith(".csv"):
        filename = f"{filename}.csv"
    user_dir = actions.path.talon_user()
    dir_path = Path(user_dir, directory_name)
    csv_path = Path(dir_path, filename)
    return dir_path, csv_path


def get_super_values(values: dict[str, dict]):
    result = {}
    for dict in values.values():
        result.update(dict)
    return result
