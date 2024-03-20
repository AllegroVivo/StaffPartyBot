from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("NoTrainingsError",)

################################################################################
class NoTrainingsError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="No Trainings Available",
            message="You have not picked up any trainees yet.",
            solution="Pick up trainees by checking the `#handshake` channel."
        )

################################################################################
