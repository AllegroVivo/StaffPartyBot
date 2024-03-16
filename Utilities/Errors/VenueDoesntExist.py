from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("VenueDoesntExistError",)

################################################################################
class VenueDoesntExistError(ErrorMessage):

    def __init__(self, venue_name: str):

        super().__init__(
            title="Venue Doesn't Exist",
            message=f"The venue `{venue_name}` hasn't been created yet.",
            solution=f"Use the `/admin add_venue` command to create the venue."
        )
        
################################################################################
        