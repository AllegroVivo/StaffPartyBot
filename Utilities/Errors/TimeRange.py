from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("TimeRangeError",)

################################################################################
class TimeRangeError(ErrorMessage):

    def __init__(self, min_time: str, max_time: str):

        super().__init__(
            title="Invalid Time Range",
            message="The time range you entered wasn't valid.",
            solution=(
                f"Please enter a time range that is between `{min_time}` "
                f"and `{max_time}` long."
            )
        )

################################################################################
