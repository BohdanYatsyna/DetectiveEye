class FileDeleteError(Exception):
    """
    Exception raised when an error occurs during
    the deletion of a file.
    """
    def __init__(self, path: str, error: Exception) -> None:
        self.message = (
            f"Unexpected error occurred during "
            f"deleting processed file '{path}': {error}"
        )
        super().__init__(self.message)
