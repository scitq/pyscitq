from typing import Dict, List, Optional, Union
from scitq2.grpc_client import Scitq2Client
from scitq2.language import Language, Raw
from scitq2.recruit import WorkerPool
from scitq2.uri import Resource
from scitq2.constants import DEFAULT_TASK_STATUS, ACTIONS
import os
import sys

class Outputs:
    """Represents the declarative outputs of a Step, which can be used in other Steps."""
    def __init__(self, publish: Optional[str]=None, **kwargs):
        self.globs: Dict[str, str] = kwargs
        self.publish = publish

        if publish:
            if not isinstance(publish, str):
                raise ValueError("publish must be a string (for now)")

class Output:
    """Represents a single output of a task, which can be used in other tasks at runtime."""
    def __init__(self, step: "Step", grouped: bool = False, globs: Optional[str]=None,
                 publish: Optional[str] = None, action: Optional[str] = "", move: Optional[str] = None):
        self.step = step
        self.grouped = grouped
        self.globs = globs
        self.publish = publish
        self.action = ""
        if action:
            if action not in ACTIONS:
                if action.startswith('mv'):
                    raise ValueError(f"Use move attribute and not action='mv:...' in output")
                raise ValueError(f"Unsupported action {action} (supported actions are: {','.join(ACTIONS)}).")
            self.action += f"|{action}"
        if move:
            self.action += f"|mv:{move}"

    def __str__(self):
        try:
            return self.resolve_path()
        except ValueError as e:
            return f"Output({self.step.name}, grouped={self.grouped}, globs={self.globs}, publish={self.publish}), action={self.action}: {e}" 

    def resolve_path(self) -> Union[str, List[str]]:
        """Resolve the output path for this output, based on the workflow and step."""
        if self.publish:
            return self.publish
        
        wf = self.step.workflow
        
        def one(task: "Task") -> str:
            return f"{wf.workspace_root}/{wf.full_name}/{task.full_name}/" + (self.globs or "") + self.action

        if self.grouped:
            return [one(task) for task in self.step.tasks]
        if not self.step.tasks:
            raise ValueError(f"Step {self.step.name} has no tasks to get output from")
        return one(self.step.tasks[-1])

    def resolve_task_id(self) -> List[int]:
        """Resolve the task ID for this output, if available."""
        if not self.step.tasks:
            if self.grouped:
                return []
            else:
                raise ValueError(f"Step {self.step.name} has no tasks compiled yet")
        if self.step.tasks[-1].task_id is None:
            raise ValueError(f"Step {self.step.name} has no tasks compiled yet")
        if self.grouped:
            ids = [t.task_id for t in self.step.tasks]
            if any(tid is None for tid in ids):
                raise ValueError(f"Step {self.step.name} has some tasks uncompiled yet")
            return ids
        return [self.step.tasks[-1].task_id]
    
class GroupedStep:
    """A Step that groups multiple tasks together, allowing for collective task_id resolution."""
    def __init__(self, step: "Step"):
        self.step = step
        
    def task_ids(self) -> List[int]:
        """Return a list of task IDs for all tasks in this grouped step."""
        for task in self.step.tasks:
            if task.task_id is None:
                raise ValueError(f"Step {self.step.name} has some tasks uncompiled yet")
        return [task.task_id for task in self.step.tasks]
    
    def output(self, name: Optional[str] = None, move: Optional[str] = None, action: Optional[str] = "") -> Output:
        """Create an Output object for this grouped step."""
        output_glob = self.step.outputs_globs.get(name, "")

        return Output(step=self.step, grouped=True, globs=output_glob, publish=self.step.publish, action=action, move=move)

class Task:
    def __init__(self, tag: str, command: str, container: str, 
                 step: "Step",
                 inputs: Optional[Union[str, Output, List[str], List[Output]]] = None,
                 outputs: Optional[Dict[str, str]] = None, 
                 resources: Optional[List[Resource]] = None, 
                 language: Optional[Language] = None,
                 depends: Optional[List["Task"]] = None):
        self.tag = tag
        self.command = command
        self.container = container
        self.step = step  # backref to the Step this task belongs to
        self.full_name = self.step.naming_strategy(self.step.name, self.tag) if self.tag else self.step.name
        self.outputs = outputs or {}
        self.depends = depends
        if inputs is None:
            self.inputs = []
        elif isinstance(inputs, list):
            self.inputs = inputs
        elif isinstance(inputs, (str, Output)):
            self.inputs = [inputs]
        else:
            raise ValueError(f"Invalid type for inputs: {type(inputs)}. Expected str, Output, or list of these.")

        self.resources = resources or []
        self.language = language or Raw()
    
    def compile(self, client: Scitq2Client):
        # Resolve command using the language's compile_command method
        resolved_command = self.language.compile_command(self.command)

        # Resolve dependencies
        resolved_depends = set()
        if self.depends is None and self.inputs:
            # Step 1: if no explicit dependencies, infer from inputs
            for input_item in self.inputs:
                if isinstance(input_item, Output):
                    for task_id in input_item.resolve_task_id():
                        resolved_depends.add(task_id)
        elif self.depends is not None:
            # Step 2: if explicit dependencies are given, resolve them
            for dep in self.depends:
                if isinstance(dep, Step):
                    # If a Step is given, use its last task as the dependency
                    if dep.tasks:
                        task_id = dep.tasks[-1].task_id
                        if task_id is None:
                            raise ValueError(f"Step {dep.name} has no tasks compiled yet")
                        resolved_depends.add(task_id)
                    else:
                        raise ValueError(f"Step {dep.name} has no tasks to depend on")
                elif isinstance(dep, GroupedStep):
                    for task_id in dep.task_ids():
                        resolved_depends.add(task_id)
        # check that there is no None in the dependencies
        if None in resolved_depends:
            raise ValueError("Task dependencies cannot contain None. Ensure all steps are compiled before compiling tasks.")

        # Resolve inputs to Output objects
        resolved_inputs = []
        for input_item in self.inputs:
            if isinstance(input_item, Output):
                # If it's an Output, resolve its path
                resolved_path = input_item.resolve_path()
                if isinstance(resolved_path, list):
                    resolved_inputs.extend(resolved_path)
                else:
                    resolved_inputs.append(resolved_path)
            elif isinstance(input_item, str):
                # If it's a string, treat it as a file path
                resolved_inputs.append(input_item)
            else:
                raise ValueError(f"Invalid input type: {type(input_item)}. Expected str or Output.")
        
        resolved_output = Output(step=self.step, grouped=False).resolve_path()

        # Resolve resources
        resolved_resources = list(map(str, self.resources))

        self.task_id = client.submit_task(
                step_id=self.step.step_id,
                command=resolved_command,
                container=self.container,
                depends=resolved_depends,
                inputs=resolved_inputs,
                output=resolved_output,
                resources=resolved_resources,
                status=DEFAULT_TASK_STATUS,
                task_name=self.full_name
            )



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
    
    def __str__(self):
        return f"TaskSpec(cpu={self.cpu}, mem={self.mem}, prefetch={self.prefetch})"


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


class Step:
    def __init__(self, name: str, workflow: "Workflow", worker_pool: Optional[WorkerPool] = None, task_spec: Optional[TaskSpec] = None,
                 naming_strategy: callable = dot_join, depends: Optional[Union["Step",List["Step"]]] = None):
        self.name = name
        self.tasks: List[Task] = []
        self.worker_pool = worker_pool
        self.task_spec = task_spec
        self.step_id: Optional[int] = None
        self.outputs_globs: Dict[str, str] = {}
        self.publish: Optional[str] = None
        self.workflow = workflow
        self.naming_strategy = naming_strategy
        if depends is None:
            self.depends = None
        elif isinstance(depends, Step):
            self.depends = [depends]
        elif isinstance(depends, list) and all(isinstance(d, Step) for d in depends):
            self.depends = depends

    def add_task(
        self,
        *,
        tag: str,
        command: str,
        container: str,
        outputs: Optional[Outputs] = None,
        inputs: Optional[Union[str, Output, List[str], List[Output]]] = None,
        resources: Optional[Union[Resource, List[Resource]]] = None,
        language: Optional[Language] = None,
    ):
        if outputs:
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

        task = Task(tag=tag, step=self, command=command, container=container, outputs=output_mapping, 
                    inputs=inputs, resources=resources_list, language=language, depends=self.depends)
        self.tasks.append(task)

    def output(self, name: str, grouped: bool = False, move: Optional[str] = None, action: Optional[str] = ""):
        """Create an Output object for this step."""
        output_glob = self.outputs_globs.get(name, "")
        return Output(step=self, grouped=grouped, globs=output_glob, publish=self.publish, move=move, action=action)

    def compile(self, client: Scitq2Client):
        self.step_id = client.create_step(self.workflow.workflow_id, self.name)

        pool = self.worker_pool or self.workflow.worker_pool
        if pool:
            options = pool.build_recruiter(self.task_spec,
                                           default_provider=self.workflow.provider,
                                           default_region=self.workflow.region)
            client.create_recruiter(step_id=self.step_id, **options)

        for task in self.tasks:
            task.compile(client)
    
    def grouped(self) -> GroupedStep:
        """Create a grouped step with a specific tag."""
        return GroupedStep(step=self)
    
    @property
    def container(self) -> str:
        """Return the container for the last task in this step."""
        if not self.tasks:
            raise ValueError(f"Step {self.name} has no tasks defined")
        return self.tasks[-1].container


class Workflow:
    last_created = None

    def __init__(self, name: str, version:str, description: str = "", worker_pool: Optional[WorkerPool] = None, language: Optional[Language] = None, tag: Optional[str] = None,
                 naming_strategy: callable = dot_join, task_naming_strategy: callable = dot_join, provider: Optional[str] = None, region: Optional[str] = None):
        self.name = name
        self.tag = tag
        self.description = description
        self._steps: Dict[str, Step] = {}
        self.worker_pool = worker_pool
        self.max_recruited = worker_pool.max_recruited if worker_pool else None
        self.language = language or Raw()
        self.naming_strategy = naming_strategy
        self.task_naming_strategy = task_naming_strategy
        self.provider = provider
        self.region = region
        self.workflow_id: Optional[int] = None
        self.full_name: Optional[str] = None
        self.workspace_root: Optional[str] = None
        self.version = version
        if Workflow.last_created is not None:
            print(f"⚠️ Warning: it is highly unrecommanded to declare several Workflow in a code, you have previously declared {Workflow.last_created.name} and you redeclare {self.name}", file=sys.stderr)
        Workflow.last_created = self

    def Step(
        self,
        *,
        name: str,
        command: str,
        container: str,
        tag: Optional[str] = None,
        inputs: Optional[Union[str, Output, List[str], List[Output]]] = None,
        outputs: Optional[Outputs] = None,
        resources: Optional[Union[Resource, List[Resource]]] = None,
        language: Optional[Language] = None,
        worker_pool: Optional[WorkerPool] = None,
        task_spec: Optional[TaskSpec] = None,
        naming_strategy: Optional[callable] = None,
        depends: Optional[Union["Step", List["Step"]]] = None,
    ) -> Step:
        if naming_strategy is None:
            naming_strategy = self.task_naming_strategy
        new_step = Step(name=name, workflow=self, worker_pool=worker_pool, task_spec=task_spec, naming_strategy=naming_strategy,
                        depends=depends)
        if name in self._steps:
            existing = self._steps[name]
            if (existing.worker_pool != new_step.worker_pool or existing.task_spec != new_step.task_spec):
                print("worker_pool", existing.worker_pool, new_step.worker_pool)
                print("task_spec", existing.task_spec, new_step.task_spec)
                raise ValueError(
                    f"Step '{name}' was already defined with a different worker_pool or task_spec. "
                    "Steps with different specifications must be given distinct names."
                )
            step = existing
        else:
            self._steps[name] = new_step
            step = new_step

        effective_language = language or self.language
        if tag is None and step.tasks:
            raise RuntimeError(f"Step '{name}' has no tag specified and has several iterations which is forbidden")
        step.add_task(tag=tag, command=command, container=container, outputs=outputs, inputs=inputs, resources=resources, language=effective_language)
        return step

    def compile(self, client: Scitq2Client) -> int:
        self.workspace_root = client.get_workspace_root(
            provider=self.provider,
            region=self.region,
        )
        self.full_name = self.naming_strategy(self.name, self.tag) if self.tag else self.name

        self.workflow_id = client.create_workflow(
            name=self.full_name,
            maximum_workers=self.max_recruited,
        )
        template_run_id = os.environ.get("SCITQ_TEMPLATE_RUN_ID")
        if template_run_id:
            try:
                client.update_template_run(template_run_id=int(template_run_id), workflow_id=self.workflow_id)
            except Exception as e:
                print(f"⚠️ Warning: failed to update template run: {e}", file=sys.stderr)
        for step in self._steps.values():
            step.compile(client)
        return self.workflow_id
