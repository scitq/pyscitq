from scitq2 import *

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

class Params(metaclass=ParamSpec):
    name = Param.string(required=True, help="State your name here")
    how_many = Param.integer(default=1, help="How many times to say hello")
    failure_rate = Param. float(default=10, help="% of failure for the steps")

def hellogoodbye(params: Params):

    workflow = Workflow(
        name="hellogoodbye-failures",
        description="Mini workflow example, with parallel steps, dependencies and failures",
        version="1.0.0",
        tag=f"{params.name}",
        language=Shell("sh", options=(Shell.HELPERS, Shell.ERREXIT)),
        worker_pool=WorkerPool(W.provider=="local.local", W.region=="local")
    )

    for i in range(params.how_many):
        step = workflow.Step(
            name="hello",
            tag=str(i),
            command=fr"for i in Hello, {params.name} did you know that {LOREM_IPSUM}; do echo $i; sleep 1; done && if [ $((RANDOM % 100)) -lt {params.failure_rate} ]; then echo fail; exit 1; fi",
            container="alpine",
            retry=2,
            task_spec=TaskSpec(concurrency=params.how_many)
        )
        other_step = workflow.Step(
            name="goodbye",
            tag=str(i),
            dependencies=[step],
            command=fr"for i in Goodbye, {params.name} did you know that {LOREM_IPSUM}; do echo $i; sleep 1; done && if [ $((RANDOM % 100)) -lt {params.failure_rate} ]; then echo fail; exit 1; fi",
            container="alpine",
            retry=2,
            task_spec=TaskSpec(concurrency=params.how_many)
        )

    
run(hellogoodbye)