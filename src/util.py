def flat_dicts(dicts: list[dict]):
    result = {}
    for dict in dicts:
        result.update(dict)
    return result
