from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("VenueProfileNotCompleteError",)

################################################################################
class VenueProfileNotCompleteError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Unable to Post Venue Profile",
            message="The venue profile is not complete.",
            solution="Please fully complete the venue profile before posting."
        )
        
################################################################################
        