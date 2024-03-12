from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("ExceedsMaxLengthError",)

################################################################################
class ExceedsMaxLengthError(ErrorMessage):

    def __init__(self, embed_length: int):
        super().__init__(
            title="Profile Too Large!",
            description=f"Current Character Count: `{embed_length}`.",
            message=(
                "Your profile is larger than Discord's mandatory 6,000-character "
                "limit for embedded messages."
            ),
            solution=(
                "The total number of characters in all your profile's sections "
                "must not exceed 6,000."
            )
        )

################################################################################
