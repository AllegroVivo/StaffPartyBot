from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("ExperienceExistsError",)

################################################################################
class ExperienceExistsError(ErrorMessage):

    def __init__(self, venue_name: str):

        super().__init__(
            title="Job Experience Already Exists",
            message=f"Experience for {venue_name} already exists.",
            solution="Please remove the existing experience before adding a new one."
        )

################################################################################
