from talon import actions, fs, app

# import csv
import os
from datetime import datetime
from pathlib import Path

# from typing import Dict, List, Tuple
# from talon import resource

directory_name = "cursorless-settings"

# def update_lists_from_csv(filename: str, *args: [dict]):
# print()


def get_file_path(filename: str) -> str:
    if not filename.endswith(".csv"):
        filename = f"{filename}.csv"
    user_dir = actions.path.talon_user()
    dir_path = Path(user_dir, directory_name)
    csv_path = Path(dir_path, filename)
    return dir_path, csv_path


def watch_csv(filename: str, default_values: dict, callback: callable):
    dir_path, file_path = get_file_path(filename)
    # print(file_path)
    # print(default_values)

    if not dir_path.is_dir():
        os.mkdir(dir_path)

    if file_path.is_file():
        update_file(file_path, default_values)

    else:
        create_file(file_path, default_values)
    #   callback()
    on_watch = lambda path, flags: callback()
    fs.watch(file_path, on_watch)


def update_file(path, default_values: dict):
    current_values = read_file(path).values()

    missing = {}
    for key, value in default_values.items():
        if value not in current_values:
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


def create_line(key: str, value: str):
    return f"{key}, {value}\n"


def create_file(path, default_values: dict):
    lines = [create_line(key, default_values[key]) for key in sorted(default_values)]
    lines.insert(0, create_line("# Spoken words", "Identifier"))
    write_file(path, lines, "w")


def write_file(path, lines, mode):
    with open(path, mode) as f:
        f.writelines(lines)


def read_file(path) -> dict:
    with open(path, "r") as f:
        lines = f.read().splitlines()

    result = {}
    for i in range(len(lines)):
        line = lines[i].strip()
        if len(line) == 0 or line.startswith("#"):
            continue
        parts = line.split(",")
        assert len(parts) == 2, f"Malformed {path.name}:{i+1} | {line}"
        key = parts[0].strip()
        value = parts[1].strip()
        result[key] = value
    return result


# NOTE: This method requires this module to be one folder below the top-level
#   knausj folder.
# SETTINGS_DIR = Path(__file__).parents[1] / "settings"

# if not SETTINGS_DIR.is_dir():
#     os.mkdir(SETTINGS_DIR)


# def get_list_from_csv(
#     filename: str, headers: Tuple[str, str], default: Dict[str, str] = {}
# ):
#     """Retrieves list from CSV"""
#     path = SETTINGS_DIR / filename
#     assert filename.endswith(".csv")

#     if not path.is_file():
#         with open(path, "w", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow(headers)
#             for key, value in default.items():
#                 writer.writerow([key] if key == value else [value, key])

#     # Now read via resource to take advantage of talon's
#     # ability to reload this script for us when the resource changes
#     with resource.open(str(path), "r") as f:
#         rows = list(csv.reader(f))

#     # print(str(rows))
#     mapping = {}
#     if len(rows) >= 2:
#         actual_headers = rows[0]
#         if not actual_headers == list(headers):
#             print(
#                 f'"{filename}": Malformed headers - {actual_headers}.'
#                 + f" Should be {list(headers)}. Ignoring row."
#             )
#         for row in rows[1:]:
#             if len(row) == 0:
#                 # Windows newlines are sometimes read as empty rows. :champagne:
#                 continue
#             if len(row) == 1:
#                 output = spoken_form = row[0]
#             else:
#                 output, spoken_form = row[:2]
#                 if len(row) > 2:
#                     print(
#                         f'"{filename}": More than two values in row: {row}.'
#                         + " Ignoring the extras."
#                     )
#             # Leading/trailing whitespace in spoken form can prevent recognition.
#             spoken_form = spoken_form.strip()
#             mapping[spoken_form] = output

#     return mapping
