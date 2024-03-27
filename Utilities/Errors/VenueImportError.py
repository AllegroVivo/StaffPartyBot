from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("VenueImportError",)

################################################################################
class VenueImportError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Unable to Import Venue",
            message=(
                "An unexpected error occurred while attempting to import the venue."
            ),
            solution="Please contact the bot owner for assistance."
        )
        
################################################################################
        