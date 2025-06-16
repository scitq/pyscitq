class Resource:
    """A resource to be used in a workflow step.

    Attributes:
        path (str): The path to the resource.
        action (str): The action to perform with the resource, e.g., "untar".
    """
    def __init__(self, path: str, action: str):
        self.path = path
        self.action = action

    def __repr__(self):
        return f"Resource(path={self.path}, action={self.action})"
    
    def __str__(self):
        return f"{self.path}|{self.action}"