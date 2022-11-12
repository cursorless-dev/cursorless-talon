from ..primitive_target import IMPLICIT_TARGET

def cursorless_move_bring_targets(m) -> list[dict]:
    target_list = [m["target"]]

    try:
        target_list += [m["positional_target"]]
    except KeyError:
        target_list += [IMPLICIT_TARGET.copy()]

    return target_list
