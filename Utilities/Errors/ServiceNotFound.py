from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("ServiceNotFoundError",)

################################################################################
class ServiceNotFoundError(ErrorMessage):

    def __init__(self, service_name: str):

        super().__init__(
            title="Service Type Not Found",
            message=f"The hireable service `{service_name}` was not found.",
            solution=f"Try a different name for the service."
        )

################################################################################
