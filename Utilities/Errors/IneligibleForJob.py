from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("IneligibleForJobError",)

################################################################################
class IneligibleForJobError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Ineligible for Job",
            message="You are not eligible for this job.",
            solution=(
                "Please ensure you have selected the appropriate "
                "pingable role in the server and that your staff profile"
                "has been completed and posted!\n"
            )
        )
        
################################################################################
        