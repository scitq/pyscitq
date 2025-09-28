# dsl.py — user-facing DSL surface for scitq2

from .workflow import Workflow, TaskSpec, Outputs
from .param import Param, ParamSpec
from .recruit import WorkerPool, W
from .util import cond
from .language import Shell, Raw
from .uri import Resource, URI, check_if_file
from .runner import run
from .grpc_client import Scitq2Client as Client
from .__version__ import __version__

__all__ = [
    "Workflow",
    "Param", "ParamSpec",
    "WorkerPool", "W",
    "TaskSpec",
    "Shell",
    "Raw",
    "Resource",
    "Outputs",
    "cond",
    "URI",
    "check_if_file",
    "run",
    "Client",
    "__version__",
]

