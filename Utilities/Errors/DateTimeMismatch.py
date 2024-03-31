from __future__ import annotations

from datetime import datetime

from ..Utilities import Utilities as U
from ._Error import ErrorMessage
################################################################################

__all__ = ("DateTimeMismatchError",)

################################################################################
class DateTimeMismatchError(ErrorMessage):

    def __init__(self, start_time: datetime, end_time: datetime):

        super().__init__(
            title="Datetime Mismatch Error",
            message=(
                f"The start time {U.format_dt(start_time, 'f')} is "
                f"after the end time {U.format_dt(end_time, 'f')}."
            ),
            solution="Please ensure that the start time is before the end time."
        )

################################################################################
