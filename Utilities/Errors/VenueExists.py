from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("VenueExistsError",)

################################################################################
class VenueExistsError(ErrorMessage):

    def __init__(self, venue_name: str):

        super().__init__(
            title="Venue Exists",
            message=f"The venue `{venue_name}` already exists.",
            solution=f"Try a different name for the venue."
        )
        
################################################################################
        