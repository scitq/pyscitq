import argparse
import json
import inspect
import sys
import ast
from typing import Callable, Type, Optional, Dict, get_type_hints
from scitq2.param import ParamSpec
import tokenize
import io
import os

class WorkflowDefinitionError(Exception):
    pass


def find_param_class_from_func(func: Callable) -> Optional[Type]:
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    if len(params) == 0:
        return None
    if len(params) != 1:
        raise ValueError("Workflow function must take zero or one parameter")

    param = params[0]
    annotation = param.annotation

    if annotation is inspect.Parameter.empty:
        raise ValueError("Workflow parameter must have a type annotation")

    if isinstance(annotation, str):
        annotation = get_type_hints(func).get(param.name)

    if not isinstance(annotation, type):
        raise ValueError("Workflow parameter must be a class")

    if annotation.__class__ is not ParamSpec:
        raise ValueError("Workflow parameter class must use ParamSpec as metaclass")

    return annotation


def extract_workflow_metadata(source_code: str) -> Dict[str, str]:
    """
    Extracts name, description, and version from the first Workflow(...) call.
    Raises WorkflowDefinitionError if values are missing or non-literals.
    """
    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "Workflow":
            result = {}
            for field in {"name", "description", "version"}:
                value = next((kw.value for kw in node.keywords if kw.arg == field), None)
                if value is None:
                    continue
                if isinstance(value, ast.Str):
                    result[field] = value.s
                else:
                    raise WorkflowDefinitionError(
                        f"The workflow metadata field '{field}' must be a plain string literal, "
                        f"not an expression or f-string (got AST node: {type(value).__name__})"
                    )

            missing = {"name", "description", "version"} - result.keys()
            if missing:
                raise WorkflowDefinitionError(
                    f"Missing required workflow metadata field(s): {', '.join(sorted(missing))}."
                )

            return result

    raise WorkflowDefinitionError("No Workflow(...) declaration found in the script.")

def warn_if_non_raw_command_strings(source_code: str, filename: str = "<string>"):
    """
    Emits warnings if 'command=' values are f-strings or triple-quoted strings
    that should be marked as raw (r or fr).
    """
    tokens = list(tokenize.generate_tokens(io.StringIO(source_code).readline))
    for i, tok in enumerate(tokens):
        if tok.type == tokenize.NAME and tok.string == "command":
            # Look ahead for "="
            if i + 2 < len(tokens) and tokens[i + 1].string == "=":
                string_token = tokens[i + 2]
                if string_token.type == tokenize.STRING:
                    raw_str = string_token.string
                    lineno = string_token.start[0]
                    if raw_str.startswith(('f"', "f'", 'f"""', "f'''")):
                        print(f"⚠️ Warning: line {lineno} in {filename} uses a non-raw f-string for `command=`. Use fr\"...\" instead.", file=sys.stderr)
                    elif raw_str.startswith(('"', "'")):
                        if "\\" in raw_str:
                            print(f"⚠️ Warning: line {lineno} in {filename} uses triple-quoted string with backslashes. Use raw string (r\"\"\"...\") to avoid escape issues.", file=sys.stderr)
                        elif "{" in raw_str or "}" in raw_str:
                            print(f"⚠️ Warning: line {lineno} in {filename} uses a non-raw string with curly braces. Use fr\"...\" instead.", file=sys.stderr)
                    elif raw_str.startswith(('r"', "r'", 'r"""', "r'''")) and ("{" in raw_str or "}" in raw_str):
                        print(f"⚠️ Warning: line {lineno} in {filename} uses a raw string with curly braces. Use fr\"...\" instead.", file=sys.stderr)
                    elif raw_str.startswith(('"""', "'''")) and "\\" in raw_str:
                        print(f"⚠️ Warning: line {lineno} in {filename} uses triple-quoted string with backslashes. Use raw string (r\"\"\"...\") to avoid escape issues.", file=sys.stderr)


def run(func: Callable):
    """
    Run a workflow function that may optionally take a Params class instance.

    Behavior:
    - --params: Outputs the parameter schema as JSON.
    - --values: Parses values and runs the workflow.
    - --metadata: Extracts workflow metadata (static AST inspection).
    - No args:
        - If function takes no parameter, calls directly.
        - Otherwise, prints usage error.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--params", action="store_true", help="Print the parameter schema as JSON.")
    parser.add_argument("--values", type=str, help="JSON dictionary of parameter values.")
    parser.add_argument("--metadata", action="store_true", help="Print workflow metadata (name, version, description).")
    args = parser.parse_args()

    try:
        param_class = find_param_class_from_func(func)
    except Exception as e:
        print(f"❌ Invalid workflow function signature: {e}", file=sys.stderr)
        sys.exit(1)

    if args.metadata:
        # Load the source code of the function to extract metadata
        source_file = inspect.getsourcefile(func)
        source_code = inspect.getsource(func)

        metadata = extract_workflow_metadata(source_code)
        if metadata is None:
            print("No metadata found in the workflow function", file=sys.stderr)
            sys.exit(1)
        if not metadata.get("name"):
            print("No name found in the workflow function metadata", file=sys.stderr)
            sys.exit(1)
        if not metadata.get("version"):
            print("No version found in the workflow function metadata", file=sys.stderr)
            sys.exit(1)
        if not metadata.get("description"):
            print("No description found in the workflow function metadata", file=sys.stderr)
            sys.exit(1)

        # Emit warnings on possibly misquoted command strings
        warn_if_non_raw_command_strings(source_code, filename=source_file)

        print(json.dumps(metadata, indent=2))
        return

    if args.params:
        if param_class is None:
            print("[]")
        else:
            print(json.dumps(param_class.schema(), indent=2))
        return

    if args.values:
        if param_class is None:
            print("❌ --values was provided but the workflow function does not accept parameters.", file=sys.stderr)
            sys.exit(1)
        try:
            values = json.loads(args.values)
            param_instance = param_class.parse(values)
            func(param_instance)
        except Exception as e:
            print(f"❌ Failed to parse values or execute workflow: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if param_class is None:
        func()
        return

    print("❌ Either --params or --values must be provided.", file=sys.stderr)
    sys.exit(1)
