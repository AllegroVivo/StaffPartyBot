from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("TimeRangeError",)

################################################################################
class TimeRangeError(ErrorMessage):

    def __init__(self, min_time: str):

        super().__init__(
            title="Invalid Time Range",
            message="The time range you entered wasn't long enough.",
            solution=f"Please enter a time range that is at least `{min_time}` long."
        )

################################################################################
