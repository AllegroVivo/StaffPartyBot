from __future__ import annotations
from datetime import datetime
from ._Error import ErrorMessage
################################################################################

__all__ = ("DateTimeBeforeNowError",)

################################################################################
class DateTimeBeforeNowError(ErrorMessage):

    def __init__(self, dt: datetime):

        super().__init__(
            title="Invalid Datetime Entry",
            message=(
                f"The datetime `{dt.isoformat()}` is before the current time."
            ),
            solution=(
                "Please enter a datetime that is after the current time."
            )
        )

################################################################################
