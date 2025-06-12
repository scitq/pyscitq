import argparse
import json
import inspect
import sys
from types import ModuleType
from typing import Callable, Type

from scitq2.param import ParamSpec


def find_param_class_from_func(func: Callable) -> Type[ParamSpec]:
    """
    Inspect the signature of the given function to determine if it takes a ParamSpec subclass.

    Returns:
        - The ParamSpec subclass if found.
        - None if the function takes no parameters.

    Raises:
        - ValueError if the function takes more than one argument or if the argument is not a ParamSpec subclass.
    """
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    if len(params) == 0:
        return None
    if len(params) != 1:
        raise ValueError("Pipeline function must take zero or exactly one argument (the Params class instance)")

    param_class = params[0].annotation
    if not isinstance(param_class, type) or not issubclass(param_class, ParamSpec):
        raise ValueError("The parameter must be a subclass of ParamSpec")

    return param_class


def run(func: Callable):
    """
    Run a workflow function that may optionally take a Params class instance.

    Behavior:
    - If --params is passed: outputs the parameter schema as JSON.
    - If --values is passed: parses the values and calls the workflow function.
    - If neither is passed and the function takes no arguments: just runs the function.
    - Otherwise: prints error and exits.

    Args:
        func: A function representing the pipeline entry point.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", action="store_true", help="Print the parameter schema as JSON")
    parser.add_argument("--values", type=str, help="JSON dictionary of parameter values")
    args = parser.parse_args()

    param_class = find_param_class_from_func(func)

    if args.params:
        if param_class is None:
            print("[]")
        else:
            print(json.dumps(param_class.schema(), indent=2))
        return

    if args.values:
        if param_class is None:
            raise ValueError("--values was provided but the workflow function does not take any parameters")
        values = json.loads(args.values)
        param_instance = param_class.parse(values)
        func(param_instance)
        return

    if param_class is None:
        func()
        return

    print("Either --params or --values must be provided", file=sys.stderr)
    sys.exit(1)
