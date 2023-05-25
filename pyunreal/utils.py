import json


def pretty_print(ugly: dict) -> None:
    """
    Prints dictionary better readable
    :param ugly:
    :return: pretty
    """
    print(json.dumps(ugly, sort_keys=True, indent=4))

