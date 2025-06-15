from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional
from scitq2.grpc_client import Scitq2Client
from recruit import WorkerPool


@dataclass
class Task:
    tag: str
    command: str
    container: str
    outputs: Dict[str, str]  # Named output globs

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
        if not isinstance(other, TaskSpec):
            return False
        return (self.cpu, self.mem, self.prefetch) == (other.cpu, other.mem, other.prefetch)


class Step:
    def __init__(self, name: str, worker_pool: Optional[WorkerPool] = None, task_spec: Optional[TaskSpec] = None):
        self.name = name
        self.tasks: List[Task] = []
        self.outputs_globs: Dict[str, str] = {}  # e.g., {"fastqs": "*.fastq.gz"}
        self.worker_pool: Optional["WorkerPool"] = worker_pool
        self.task_spec: Optional[TaskSpec] = task_spec
        self.step_id: Optional[int] = None

    def add_task(
        self,
        *,
        tag: str,
        command: str,
        container: str,
        outputs: Optional[Dict[str, str]] = None,
    ):
        if outputs:
            for key, pattern in outputs.items():
                if key in self.outputs_globs:
                    if self.outputs_globs[key] != pattern:
                        raise ValueError(f"Output '{key}' in step '{self.name}' is declared with conflicting glob patterns.")
                else:
                    print(f"[WARNING] Output '{key}' is newly introduced in task '{tag}' of step '{self.name}' — inconsistent output keys.")

            for expected_key in self.outputs_globs:
                if expected_key not in outputs:
                    print(f"[WARNING] Task '{tag}' in step '{self.name}' is missing declared output '{expected_key}'.")

            for key in outputs:
                if key not in self.outputs_globs:
                    self.outputs_globs[key] = outputs[key]

        self.tasks.append(Task(tag=tag, command=command, container=container, outputs=outputs or {}))

    def output(self, name: str, grouped: bool = False):
        if name not in self.outputs_globs:
            raise ValueError(f"Output '{name}' not declared in step '{self.name}'")
        if not self.tasks:
            raise ValueError(f"No tasks defined for step {self.name}")
        if grouped:
            return [task.output(name) for task in self.tasks]
        return self.tasks[-1].output(name)

    def compile(self, client: Scitq2Client, workflow_id: int, default_worker_pool: Optional[WorkerPool] = None):
        self.step_id = client.create_step(workflow_id, self.name)

        pool = self.worker_pool or default_worker_pool
        if pool:
            strategy, options = pool.build_recruiter(self.task_spec)
            client.create_recruiter(step_id=self.step_id, strategy=strategy, options=options)

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
        outputs: Optional[Dict[str, str]] = None,
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