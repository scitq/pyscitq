from collections import defaultdict
from typing import Dict, List, Optional, Union
from scitq2.grpc_client import Scitq2Client
from scitq2.language import Language, Raw
from scitq2.recruit import WorkerPool
from scitq2.uri import Resource
from scitq2.constants import DEFAULT_TASK_STATUS
import os
import sys

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
    def __init__(self, tag: str, command: str, container: str, outputs: Optional[Dict[str, str]] = None, 
                 resources: Optional[List[Resource]] = None, language: Optional[Language] = None):
        self.tag = tag
        self.command = command
        self.container = container
        self.outputs = outputs or {}
        self.resources = resources or []
        self.language = language or Raw()

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
    def __init__(self, name: str, workflow: "Workflow", worker_pool: Optional[WorkerPool] = None, task_spec: Optional[TaskSpec] = None):
        self.name = name
        self.tasks: List[Task] = []
        self.worker_pool = worker_pool
        self.task_spec = task_spec
        self.step_id: Optional[int] = None
        self.outputs_globs: Dict[str, str] = {}
        self.publish: Optional[dict] = None
        self.workflow = workflow

    def add_task(
        self,
        *,
        tag: str,
        command: str,
        container: str,
        outputs: Optional[Outputs] = None,
        resources: Optional[Union[Resource, List[Resource]]] = None,
        language: Optional[Language] = None,
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

        if isinstance(resources, Resource):
            resources_list = [resources]
        else:
            resources_list = resources or []

        self.tasks.append(Task(tag=tag, command=command, container=container, outputs=output_mapping, resources=resources_list, language=language))

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
            options = pool.build_recruiter(self.task_spec,
                                           default_provider=self.workflow.provider,
                                           default_region=self.workflow.region)
            client.create_recruiter(step_id=self.step_id, options=options)

        for task in self.tasks:
            full_command = task.language.compile_command(task.command)
            client.submit_task(
                step_id=self.step_id,
                command=full_command,
                container=task.container,
                status=DEFAULT_TASK_STATUS,
            )

def underscore_join(*args: str) -> str:
    """
    Joins multiple strings with underscores, ignoring empty strings.
    """
    return "_".join(filter(None, args))

def dot_join(*args: str) -> str:
    """
    Joins multiple strings with dots, ignoring empty strings.
    """
    return ".".join(filter(None, args))

class Workflow:
    def __init__(self, name: str, description: str = "", worker_pool: Optional[WorkerPool] = None, language: Optional[Language] = None, tag: Optional[str] = None,
                 naming_strategy: callable = dot_join, provider: Optional[str] = None, region: Optional[str] = None):
        self.name = name
        self.tag = tag
        self.description = description
        self._steps: Dict[str, Step] = {}
        self.worker_pool = worker_pool
        self.max_recruited = worker_pool.max_recruited if worker_pool else None
        self.language = language or Raw()
        self.naming_strategy = naming_strategy
        self.provider = provider
        self.region = region

    def Step(
        self,
        *,
        name: str,
        tag: str,
        command: str,
        container: str,
        outputs: Optional[Outputs] = None,
        resources: Optional[Union[Resource, List[Resource]]] = None,
        language: Optional[Language] = None,
        worker_pool: Optional[WorkerPool] = None,
        task_spec: Optional[TaskSpec] = None
    ) -> Step:
        new_step = Step(name=name, workflow=self, worker_pool=worker_pool, task_spec=task_spec)
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

        effective_language = language or self.language
        step.add_task(tag=tag, command=command, container=container, outputs=outputs, resources=resources, language=effective_language)
        return step

    def compile(self, client: Scitq2Client) -> int:
        workflow_id = client.create_workflow(
            name=self.naming_strategy(self.name,self.tag),
            description=self.description,
            max_recruited=self.max_recruited,
        )
        template_run_id = os.environ.get("SCITQ_TEMPLATE_RUN_ID")
        if template_run_id:
            try:
                client.update_template_run(template_run_id=int(template_run_id), workflow_id=workflow_id)
            except Exception as e:
                print(f"⚠️ Warning: failed to update template run: {e}", file=sys.stderr)
        for step in self._steps.values():
            step.compile(client, workflow_id, default_worker_pool=self.worker_pool)
        return workflow_id
