import os
from talon import Context, Module, actions
from pathlib import Path
from ..vendor.jstyleson import loads

mod = Module()

windows_ctx = Context()
mac_ctx = Context()
linux_ctx = Context()

windows_ctx.matches = r"""
os: windows
"""
mac_ctx.matches = r"""
os: mac
"""
linux_ctx.matches = r"""
os: linux
"""


@mod.action_class
class Actions:
    def vscode_settings_path() -> Path:
        """Get path of vscode settings json file"""
        pass

    def vscode_get_setting(key: str, default_value: any = None):
        """Get the value of vscode setting at the given key"""
        path: Path = actions.user.vscode_settings_path()
        settings: dict = loads(path.read_text())

        if default_value is not None:
            return settings.get(key, default_value)
        else:
            return settings[key]


def pick_path(paths: list[Path]):
    existing_paths = [path for path in paths if path.exists()]
    return max(existing_paths, key=lambda path: path.stat().st_mtime)


@mac_ctx.action_class("user")
class MacUserActions:
    def vscode_settings_path() -> Path:
        return pick_path(
            [
                Path(
                    f"{os.environ['HOME']}/Library/Application Support/Code/User/settings.json"
                ),
                Path(
                    f"{os.environ['HOME']}/Library/Application Support/VSCodium/User/settings.json"
                ),
            ]
        )


@linux_ctx.action_class("user")
class LinuxUserActions:
    def vscode_settings_path() -> Path:
        return pick_path(
            [
                Path(f"{os.environ['HOME']}/.config/Code/User/settings.json"),
                Path(f"{os.environ['HOME']}/.config/VSCodium/User/settings.json"),
            ]
        )


@windows_ctx.action_class("user")
class WindowsUserActions:
    def vscode_settings_path() -> Path:
        return pick_path(
            [
                Path(f"{os.environ['APPDATA']}/Code/User/settings.json"),
                Path(f"{os.environ['APPDATA']}/VSCodium/User/settings.json"),
            ]
        )
