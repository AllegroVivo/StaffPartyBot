from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("TooManyImagesError",)

################################################################################
class TooManyImagesError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Image Maximum Reached",
            message="You already have the maximum of 10 additional images on your profile.",
            solution="Sorry, I can't add any more because of formatting restrictions. :("
        )

################################################################################
