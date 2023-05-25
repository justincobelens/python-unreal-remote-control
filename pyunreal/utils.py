import dataclasses
import json
from typing import Any, Union


def dataclass_to_dict(obj: Any) -> Union[dict, Any]:
    """
    If the object is a dataclass, convert it to a dictionary.
    :param obj: Any python object
    :return: If the object is a dataclass, returns a dictionary. Otherwise, returns the object as is.
    """
    if dataclasses.is_dataclass(obj):
        return {k: dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    else:
        return obj



def pretty_print(ugly: Any) -> None:
    """
    Prints dictionary better readable
    :param ugly: Any python object
    :return: None
    """
    try:
        ugly = dataclass_to_dict(ugly)
        print(json.dumps(ugly, sort_keys=True, indent=4))
    except TypeError as e:
        print(ugly)
        print(e)
        print("Couldn't pretty print")
