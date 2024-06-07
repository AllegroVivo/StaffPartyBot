from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("InvalidPositionSelectionError",)

################################################################################
class InvalidPositionSelectionError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Invalid Position Selection",
            message=(
                "You cannot select the General Training position along with "
                "other positions."
            ),
            solution="Please select only the General Training position or other positions.",
        )

################################################################################
        