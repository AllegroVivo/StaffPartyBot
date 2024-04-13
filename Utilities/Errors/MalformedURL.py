from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("MalformedURLError",)

################################################################################
class MalformedURLError(ErrorMessage):

    def __init__(self, url: str):

        super().__init__(
            title="Malformed URL",
            message=f"The URL '{url}' is malformed and could not be accepted.",
            solution="Please ensure it is of schema '`https://`'."
        )

################################################################################
