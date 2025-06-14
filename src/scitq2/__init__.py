# dsl.py — user-facing DSL surface for scitq2

from .workflow import Workflow, TaskSpec
from .param import Param, ParamSpec
from .recruit import WorkerPool, W
from .filters import S, SampleFilter
from .conditions import cond
from .shell import Shell
from .resources import Container, Resource
from .outputs import Outputs
from .runner import run

__all__ = [
    "Workflow",
    "Param", "ParamSpec",
    "WorkerPool", "W", "S", "SampleFilter",
    "TaskSpec",
    "Shell",
    "Container", "Resource",
    "Outputs",
    "cond",
    "run",
]
