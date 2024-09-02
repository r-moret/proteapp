class UnsavedDataError(Exception):
    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(message)

        self.field = field


class TokenDecodificationError(Exception): ...
