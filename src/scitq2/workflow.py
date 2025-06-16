from collections import defaultdict
from typing import Dict, List, Optional
from scitq2.grpc_client import Scitq2Client
from recruit import WorkerPool

class Outputs:
    def __init__(self, publish=None, **kwargs):
        self.globs: Dict[str, str] = kwargs
        self.publish = publish

        if publish:
            if not isinstance(publish, dict):
                raise ValueError("publish must be a dictionary")

            required_keys = {"type", "path"}
            if not required_keys.issubset(publish):
                raise ValueError("publish must include 'type' and 'path'")

            if not isinstance(publish["type"], list):
                raise ValueError("'publish[\"type\"]' must be a list of output names")

            for output_key in publish["type"]:
                if output_key not in self.globs:
                    raise ValueError(f"Cannot publish unknown output: '{output_key}'")

            if "mode" in publish and publish["mode"] not in ("copy", "move"):
                raise ValueError("publish['mode'] must be 'copy' or 'move'")



class Task:
    def __init__(self, tag: str, command: str, container: str, outputs: Optional[Dict[str, str]] = None):
        self.tag = tag
        self.command = command
        self.container = container
        self.outputs = outputs or {}

    def output(self, name: str) -> str:
        return self.outputs.get(name)


class TaskSpec:
    def __init__(self, *, cpu=None, mem=None, prefetch=None):
        if cpu is None and mem is None:
            raise ValueError("TaskSpec must define at least one of cpu or mem")
        self.cpu = cpu
        self.mem = mem
        self.prefetch = self._parse_prefetch(prefetch)

    def _parse_prefetch(self, p):
        if p is None:
            return 0
        if isinstance(p, str) and p.endswith("%"):
            return float(p.strip("%")) / 100.0
        return float(p)

    def __eq__(self, other):
        return isinstance(other, TaskSpec) and (
            self.cpu, self.mem, self.prefetch
        ) == (other.cpu, other.mem, other.prefetch)


class Step:
    def __init__(self, name: str, worker_pool: Optional[WorkerPool] = None, task_spec: Optional[TaskSpec] = None):
        self.name = name
        self.tasks: List[Task] = []
        self.worker_pool = worker_pool
        self.task_spec = task_spec
        self.step_id: Optional[int] = None
        self.outputs_globs: Dict[str, str] = {}
        self.publish: Optional[dict] = None

    def add_task(
        self,
        *,
        tag: str,
        command: str,
        container: str,
        outputs: Optional[Outputs] = None,
    ):
        if outputs:
            # Consistency check
            if self.outputs_globs and outputs.globs != self.outputs_globs:
                raise ValueError(f"Inconsistent outputs declared in step '{self.name}'")
            self.outputs_globs = outputs.globs

            if self.publish and outputs.publish != self.publish:
                raise ValueError(f"Inconsistent publish directives in step '{self.name}'")
            self.publish = outputs.publish

            output_mapping = outputs.globs
        else:
            output_mapping = {}

        self.tasks.append(Task(tag=tag, command=command, container=container, outputs=output_mapping))

    def output(self, name: str, grouped: bool = False):
        if not self.tasks:
            raise ValueError(f"No tasks defined for step {self.name}")
        if grouped:
            return [task.output(name) for task in self.tasks]
        return self.tasks[-1].output(name)

    def compile(self, client: Scitq2Client, workflow_id: int, default_worker_pool: Optional[WorkerPool] = None):
        self.step_id = client.create_step(workflow_id, self.name)

        pool = self.worker_pool or default_worker_pool
        if pool:
            options = pool.build_recruiter(self.task_spec)
            client.create_recruiter(step_id=self.step_id, options=options)

        for task in self.tasks:
            client.submit_task(
                step_id=self.step_id,
                command=task.command,
                container=task.container,
            )


class Workflow:
    def __init__(self, name: str, description: str = "", worker_pool: Optional[WorkerPool] = None):
        self.name = name
        self.description = description
        self._steps: Dict[str, Step] = {}
        self.worker_pool = worker_pool
        self.max_recruited = worker_pool.max_recruited if worker_pool else None

    def Step(
        self,
        *,
        name: str,
        tag: str,
        command: str,
        container: str,
        outputs: Optional[Outputs] = None,
        worker_pool: Optional[WorkerPool] = None,
        task_spec: Optional[TaskSpec] = None,
    ) -> Step:
        new_step = Step(name, worker_pool, task_spec)
        if name in self._steps:
            existing = self._steps[name]
            if (existing.worker_pool != new_step.worker_pool or existing.task_spec != new_step.task_spec):
                raise ValueError(
                    f"Step '{name}' was already defined with a different worker_pool or task_spec. "
                    "Steps with different specifications must be given distinct names."
                )
            step = existing
        else:
            self._steps[name] = new_step
            step = new_step

        step.add_task(tag=tag, command=command, container=container, outputs=outputs)
        return step

    def compile(self, client: Scitq2Client) -> int:
        workflow_id = client.create_workflow(
            name=self.name,
            description=self.description,
            max_recruited=self.max_recruited,
        )
        for step in self._steps.values():
            step.compile(client, workflow_id, default_worker_pool=self.worker_pool)
        return workflow_id
