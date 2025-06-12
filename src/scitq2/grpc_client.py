# src/scitq2/grpc_client.py

import grpc
import os
from scitq2.pb import taskqueue_pb2, taskqueue_pb2_grpc


class BearerAuth(grpc.AuthMetadataPlugin):
    """Adds a Bearer token to the gRPC metadata for authorization."""
    def __init__(self, token: str):
        self.token = token

    def __call__(self, context, callback):
        callback((("authorization", f"Bearer {self.token}"),), None)


class Scitq2Client:
    """
    Client for interacting with the scitq2 gRPC backend.

    This client handles:
    - Secure connection setup (TLS, with InsecureSkipVerify)
    - Bearer token authentication (via SCITQ_TOKEN environment variable)
    - Submission of workflows, steps, tasks, and recruiters
    """
    def __init__(self, server: str = None, token: str = None):
        """
        Initializes a gRPC connection with authentication.

        Parameters:
        - server (str): server address (host:port). Defaults to SCITQ_SERVER or 'localhost:50051'.
        - token (str): Bearer token for authentication. Defaults to SCITQ_TOKEN environment variable.
        """
        server = server or os.environ.get("SCITQ_SERVER", "localhost:50051")
        token = token or os.environ.get("SCITQ_TOKEN")
        if not token:
            raise RuntimeError("Missing SCITQ_TOKEN environment variable")

        credentials = grpc.ssl_channel_credentials()
        call_credentials = grpc.metadata_call_credentials(BearerAuth(token))
        composite_credentials = grpc.composite_channel_credentials(credentials, call_credentials)

        self.channel = grpc.secure_channel(server, composite_credentials)
        self.stub = taskqueue_pb2_grpc.TaskQueueStub(self.channel)

    def create_workflow(self, name: str, description: str = "") -> int:
        """
        Creates a new workflow on the server.

        Parameters:
        - name (str): Name of the workflow
        - description (str): Optional description

        Returns:
        - int: The workflow ID
        """
        request = taskqueue_pb2.WorkflowRequest(name=name, description=description)
        response = self.stub.CreateWorkflow(request)
        return response.workflow_id

    def create_step(self, workflow_id: int, name: str) -> int:
        """
        Creates a new step associated with a given workflow.

        Parameters:
        - workflow_id (int): The parent workflow's ID
        - name (str): Name of the step

        Returns:
        - int: The step ID
        """
        request = taskqueue_pb2.StepRequest(workflow_id=workflow_id, name=name)
        response = self.stub.CreateStep(request)
        return response.step_id

    def submit_task(self, step_id: int, command: str, container: str) -> int:
        """
        Submits a task to a specific step.

        Parameters:
        - step_id (int): ID of the step the task belongs to
        - command (str): Shell command to run
        - container (str): Docker/Singularity container to use

        Returns:
        - int: The task ID
        """
        request = taskqueue_pb2.TaskRequest(step_id=step_id, command=command, container=container)
        response = self.stub.SubmitTask(request)
        return response.task_id

    def create_recruiter(self, step_id: int, strategy: str, options: dict) -> int:
        """
        Creates a recruiter for a given step.

        Parameters:
        - step_id (int): ID of the step the recruiter belongs to
        - strategy (str): Recruitment strategy identifier
        - options (dict): Strategy-specific options as key-value pairs

        Returns:
        - int: The recruiter ID
        """
        request = taskqueue_pb2.RecruiterRequest(
            step_id=step_id,
            strategy=strategy,
            options=options
        )
        response = self.stub.CreateRecruiter(request)
        return response.recruiter_id
