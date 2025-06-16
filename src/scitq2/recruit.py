from typing import Any, List, Optional


class FieldExpr:
    def __init__(self, field: str, op: str, value: Any):
        self.field = field
        self.op = op
        self.value = value

    def to_dict(self):
        return {
            "field": self.field,
            "op": self.op,
            "value": self.value,
        }

    def to_protofilter(self):
        val = str(self.value)
        if self.op == "is":
            return f"{self.field} is {val}"
        return f"{self.field}{self.op}{val}"


class WorkerSymbol:
    def __getattr__(self, field):
        return FieldBuilder(field)


class FieldBuilder:
    def __init__(self, field):
        self.field = field

    def __eq__(self, value): return FieldExpr(self.field, "==", value)
    def __ne__(self, value): raise NotImplementedError("'!=' is not supported in protofilter expressions")

class NumberFieldBuilder(FieldBuilder):
    def __ge__(self, value): return FieldExpr(self.field, ">=", value)
    def __gt__(self, value):  return FieldExpr(self.field, ">", value)
    def __le__(self, value): return FieldExpr(self.field, "<=", value)
    def __lt__(self, value):  return FieldExpr(self.field, "<", value)


class StringFieldBuilder(FieldBuilder):

    def like(self, pattern: str):
        return FieldExpr(self.field, "~", pattern)

class StringWithDefaultFieldBuilder(StringFieldBuilder):
    def is_default(self):
        return FieldExpr(self.field, "is", "default")


class W:
    """
    Static filter interface for worker recruitment.
    This class provides a set of fields that can be used to filter workers
    based on their attributes such as cpu, mem (memory), region, provider, flavor, and disk.
    Usage:
    worker_pool=WorkerPool(
        W.provider.like("azure%"),
        W.region.is_default(),
        W.cpu == 32,
        W.mem >= 120,
        W.disk >= 400,
        max_recruited=10,
        task_batches=2
    )
    """
    cpu = NumberFieldBuilder("cpu")
    mem = NumberFieldBuilder("mem")
    region = StringWithDefaultFieldBuilder("region")
    provider = StringFieldBuilder("provider")
    flavor = StringFieldBuilder("flavor")
    disk = NumberFieldBuilder("disk")


class WorkerPool:
    """
    Defines a strategy for recruiting workers based on hardware or metadata constraints.

    A WorkerPool specifies:
    - A list of filter expressions (e.g., W.cpu >= 32) that determine worker compatibility.
    - Optional recruiter-level parameters such as `max_recruited`.
    - Arbitrary extra options (e.g., container image, zone) passed to the backend.

    This class also supports estimating task concurrency based on a TaskSpec (cpu/mem needs).

    Parameters:
        *match: FieldExpr
            Filter expressions to select eligible workers.
        max_recruited: int, optional
            Maximum number of workers this pool can recruit (per step).
        **extra_options: Any
            Additional backend-specific parameters (e.g., image="...", zone="...").

    Example:
        WorkerPool(
            W.cpu >= 32,
            W.region.is_default(),
            max_recruited=10,
            image="ubuntu:22.04"
        )
    """
    
    def __init__(self, *match: FieldExpr, max_recruited: Optional[int] = None, **extra_options):
        self.match = list(match)
        self.max_recruited = max_recruited
        self.extra_options = extra_options

    def compile_filter(self) -> str:
        return compile_protofilter(self.match)

    def build_recruiter(self, task_spec) -> tuple[str, dict]:
        options = dict(self.extra_options)
        options["filter"] = self.compile_filter()

        if task_spec is None:
            options["concurrency"] = 1
            options["prefetch"] = 0
        else:
            if not any(e.field == "cpu" for e in self.match) and not any(e.field == "mem" for e in self.match):
                raise ValueError("To use a TaskSpec, WorkerPool must include a cpu and/or mem requirement")

            candidates = []
            for e in self.match:
                if e.field == "cpu" and task_spec.cpu is not None:
                    candidates.append(float(e.value) / task_spec.cpu)
                if e.field == "mem" and task_spec.mem is not None:
                    candidates.append(float(e.value) / task_spec.mem)

            concurrency = int(max(1, min(candidates)))
            prefetch = round(concurrency * task_spec.prefetch)

            options["concurrency"] = concurrency
            if prefetch > 0:
                options["prefetch"] = prefetch

        return options
    
    def clone_with(self, *match: FieldExpr, max_recruited: Optional[int] = None, **extra_options) -> "WorkerPool":
        """
        Returns a copy of the current WorkerPool with optionally overridden fields.
        Any provided arguments override the corresponding fields in the original pool.
        """
        new_match = list(match) if match else self.match
        new_max = max_recruited if max_recruited is not None else self.max_recruited
        new_options = dict(self.extra_options)
        new_options.update(extra_options)
        return WorkerPool(*new_match, max_recruited=new_max, **new_options)


def compile_protofilter(match: List[FieldExpr]) -> str:
    return ":".join(expr.to_protofilter() for expr in match)
