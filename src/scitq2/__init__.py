# dsl.py — user-facing DSL surface for scitq2

from .workflow import Workflow
from .param import Param, ParamSpec
from .filters import W, S, WorkerPool, SampleFilter
from .task import TaskSpec
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
