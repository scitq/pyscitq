from typing import Any, Optional, List


class Param:
    def __init__(
        self,
        *,
        typ: type,
        required: bool = False,
        default: Any = None,
        choices: List[Any] = None,
        help: str = ""
    ):
        self.typ = typ
        self.required = required
        self.default = default
        self.choices = choices
        self.help = help
        self.name = None  # to be set by metaclass

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._values.get(self.name, self.default)

    def __set__(self, instance, value):
        raise AttributeError("Parameters are read-only")

    @staticmethod
    def string(**kwargs):
        return Param(typ=str, **kwargs)

    @staticmethod
    def integer(**kwargs):
        return Param(typ=int, **kwargs)

    @staticmethod
    def boolean(**kwargs):
        return Param(typ=bool, **kwargs)

    @staticmethod
    def enum(choices: List[Any], **kwargs):
        return Param(typ=str, choices=choices, **kwargs)


class ParamSpec(type):
    def __new__(mcs, name, bases, namespace):
        declared = {}
        for key, value in namespace.items():
            if isinstance(value, Param):
                declared[key] = value
        cls = super().__new__(mcs, name, bases, namespace)
        cls._declared_params = declared
        return cls

    def parse(cls, values: dict):
        parsed = {}
        for name, param in cls._declared_params.items():
            if name in values:
                raw = values[name]
                try:
                    casted = param.typ(raw)
                except Exception as e:
                    raise ValueError(f"Invalid type for parameter '{name}': {raw}") from e

                if param.choices and casted not in param.choices:
                    raise ValueError(f"Invalid value for parameter '{name}': {casted} not in {param.choices}")

                parsed[name] = casted
            elif param.default is not None:
                parsed[name] = param.default
            elif param.required:
                raise ValueError(f"Missing required parameter: '{name}'")

        obj = cls.__new__(cls)
        obj._values = parsed
        return obj

    def schema(cls):
        return [
            {
                "name": name,
                "type": param.typ.__name__,
                "required": param.required,
                "default": param.default,
                "choices": param.choices,
                "help": param.help,
            }
            for name, param in cls._declared_params.items()
        ]
