from .conventions import get_cursorless_list_name
from talon import Context, Module, actions, fs, app, settings
from datetime import datetime
from pathlib import Path


mod = Module()
ctx = Context()
cursorless_settings_directory = mod.setting(
    "cursorless_settings_directory",
    type=str,
    default="cursorless-settings",
    desc="The directory to use for cursorless settings csvs relative to talon user directory",
)


def init_csv_and_watch_changes(filename: str, default_values: dict[str, dict]):
    """
    Initialize a cursorless settings csv, creating it if necessary, and watch
    for changes to the csv.  Talon lists will be generated based on the keys of
    `default_values`.  For example, if there is a key `foo`, there will be a
    list created called `user.cursorless_foo` that will contain entries from
    the original dict at the key `foo`, updated according to customization in
    the csv at

        actions.path.talon_user() / "cursorless-settings" / filename

    Args:
        filename (str): The name of the csv file to be placed in
        `cursorles-settings` dir
        default_values (dict[str, dict]): The default values for the lists to
        be customized in the given csv
    """
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


def is_removed(value: str):
    return value == "-"


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
        value = obj["value"]
        if is_removed(value):
            del results[obj["list"]][obj["key"]]
        else:
            results[obj["list"]][obj["key"]] = value

    # Assign result to talon context list
    for list_name, dict in results.items():
        ctx.lists[get_cursorless_list_name(list_name)] = dict


def update_file(path: Path, default_values: dict):
    current_values, has_errors = read_file(path, default_values.values())
    current_identifiers = current_values.values()

    missing = {}
    for key, value in default_values.items():
        if value not in current_identifiers:
            missing[key] = value

    if missing:
        if has_errors:
            print(
                "NOTICE: New cursorless features detected, but refusing to update "
                "csv due to errors.  Please fix csv errors above and restart talon"
            )
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lines = [
                f"# {timestamp} - New entries automatically added by cursorless",
                *[create_line(key, missing[key]) for key in sorted(missing)],
            ]
            with open(path, "a") as f:
                f.write("\n\n" + "\n".join(lines))

            print(f"New cursorless features added to {path.name}")
            for key in sorted(missing):
                print(f"{key}: {missing[key]}")
            print(
                "See release notes for more info: "
                "https://github.com/pokey/cursorless-vscode/blob/master/CHANGELOG.md"
            )
            app.notify(f"🎉🎉 New cursorless features; see log")

    return current_values


def create_line(key: str, value: str):
    return f"{key}, {value}"


SPOKEN_FORM_HEADER = "Spoken form"
CURSORLESS_IDENTIFIER_HEADER = "Cursorless identifier"
header_row = create_line(SPOKEN_FORM_HEADER, CURSORLESS_IDENTIFIER_HEADER)


def create_file(path: Path, default_values: dict):
    lines = [create_line(key, default_values[key]) for key in sorted(default_values)]
    lines.insert(0, header_row)
    path.write_text("\n".join(lines))


def csv_error(path: Path, index: int, message: str, value: str):
    """Check that an expected condition is true

    Note that we try to continue reading in this case so cursorless doesn't get bricked

    Args:
        condition (bool): The condition that should be true.
        path (Path): The path of the CSV (for error reporting)
        index (int): The index into the file (for error reporting)
        text (str): The text of the error message to report if condition is false
    """
    print(f"ERROR: {path}:{index+1}: {message} '{value}'")


def read_file(path: Path, default_identifiers: list[str]):
    with open(path) as f:
        lines = list(f)

    result = {}
    used_identifiers = []
    has_errors = False
    seen_header = False
    for i, raw_line in enumerate(lines):
        line = raw_line.strip()
        if len(line) == 0 or line.startswith("#"):
            continue

        parts = line.split(",")

        if len(parts) != 2:
            has_errors = True
            csv_error(path, i, "Malformed csv entry", line)
            continue

        key = parts[0].strip()
        value = parts[1].strip()

        if not seen_header:
            if key != SPOKEN_FORM_HEADER or value != CURSORLESS_IDENTIFIER_HEADER:
                has_errors = True
                csv_error(path, i, "Malformed header", line)
                print(f"Expected '{header_row}'")
            seen_header = True
            continue

        if value not in default_identifiers:
            has_errors = True
            csv_error(path, i, "Unknown identifier", value)
            continue

        if value in used_identifiers:
            has_errors = True
            csv_error(path, i, "Duplicate identifier", value)
            continue

        result[key] = value
        used_identifiers.append(value)

    if has_errors:
        app.notify("Cursorless settings error; see log")

    return result, has_errors


def get_file_paths(filename: str):
    if not filename.endswith(".csv"):
        filename = f"{filename}.csv"
    user_dir = actions.path.talon_user()
    settings_directory = Path(cursorless_settings_directory.get())

    if not settings_directory.is_absolute():
        settings_directory = user_dir / settings_directory

    csv_path = Path(settings_directory, filename)
    return settings_directory, csv_path


def get_super_values(values: dict[str, dict]):
    result = {}
    for dict in values.values():
        result.update(dict)
    return result
