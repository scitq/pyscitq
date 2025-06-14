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
    def __ge__(self, value): return FieldExpr(self.field, ">=", value)
    def __gt__(self, value):  return FieldExpr(self.field, ">", value)
    def __le__(self, value): return FieldExpr(self.field, "<=", value)
    def __lt__(self, value):  return FieldExpr(self.field, "<", value)

    def like(self, pattern: str):
        return FieldExpr(self.field, "~", pattern)

    def is_default(self):
        return FieldExpr(self.field, "is", "default")


W = WorkerSymbol()


class WorkerPool:
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

        return "simple", options


def compile_protofilter(match: List[FieldExpr]) -> str:
    return ":".join(expr.to_protofilter() for expr in match)
