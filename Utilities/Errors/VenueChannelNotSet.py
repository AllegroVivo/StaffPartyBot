from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("VenueChannelNotSetError",)

################################################################################
class VenueChannelNotSetError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Venue Posting Channel Not Set",
            message=(
                "The venue internship posting channel for this server hasn't "
                "been set yet."
            ),
            solution="Have a bot administrator use `/admin venue_channel` to set it."
        )

################################################################################
