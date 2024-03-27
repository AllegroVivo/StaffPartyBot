from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("VenueImportNotFoundError",)

################################################################################
class VenueImportNotFoundError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Unable to Import Venue",
            message=(
                "An error occurred while attempting to import the venue.\n\n"
                
                "Either there are no venues with you listed as a manager on "
                "the XIV Venues API, **or** there is no venue that you manage "
                "that has the name you provided."
            ),
            solution=(
                "If you are not listed as a manager for any venues on the XIV "
                "Venues API, you will need to contact them to have yourself "
                "added as a manager.\n\n"
                
                "If you are listed as a manager for a venue, but the venue "
                "was not found, please ensure that you have entered the name "
                "of the venue correctly."
            )
        )
        
################################################################################
        