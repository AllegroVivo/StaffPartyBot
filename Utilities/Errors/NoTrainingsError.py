from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("NoTrainingsError",)

################################################################################
class NoTrainingsError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="No Trainings Registered",
            message="The provided trainee has no available trainings.",
            solution="Ensure the trainee has registered for training before trying to acquire them."
        )

################################################################################
