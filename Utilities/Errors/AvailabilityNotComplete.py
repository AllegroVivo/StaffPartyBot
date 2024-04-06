from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("AvailabilityNotCompleteError",)

################################################################################
class AvailabilityNotCompleteError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Availability Not Complete",
            message="Before posting your profile, you must complete your availability!",
            solution="Please set your availability by using the `/profile details` command.",
        )
        
################################################################################
        