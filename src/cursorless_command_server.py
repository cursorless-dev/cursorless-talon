from typing import Any

from .command_client.command_client import Actions as client_actions
# from .command_client.vscode import Actions as vscode_actions


def run_rpc_command_no_wait(command_id: str, *args):
    """Execute command via rpc."""
    client_actions.run_rpc_command(command_id, *args)
    # try:
    #     client_actions.run_rpc_command(command_id, *args)
    # except KeyError:
    #     print(KeyError)
    #     vscode_actions.vscode_with_plugin(command_id, *args)


def run_rpc_command_and_wait(command_id: str, *args):
    """Execute command via rpc and wait for command to finish."""
    client_actions.run_rpc_command_and_wait(command_id, *args)
    # try:
    #     client_actions.run_rpc_command_and_wait(command_id, *args)
    # except KeyError:
    #     print(KeyError)
    #     vscode_actions.vscode_with_plugin_and_wait(command_id, *args)


def run_rpc_command_get(command_id: str, *args) -> Any:
    """Execute command via rpc and return command output."""
    return client_actions.run_rpc_command_get(command_id, *args)
    # try:
    #     return client_actions.run_rpc_command_get(command_id, *args)
    # except KeyError:
    #     print(KeyError)
    #     return vscode_actions.vscode_get(command_id, *args)
