from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("DateTimeFormatError",)

################################################################################
class DateTimeFormatError(ErrorMessage):

    def __init__(self, entry: str):

        super().__init__(
            title="Invalid Datetime Entry",
            message=f"The value `{entry}` couldn't be parsed into a datetime.",
            solution=(
                "Please ensure that the datetime is in the format "
                "`MM/DD/YYYY HH:MM AM/PM`."
            )
        )

################################################################################
