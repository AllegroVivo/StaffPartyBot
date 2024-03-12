from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("InvalidColorError",)

################################################################################
class InvalidColorError(ErrorMessage):

    def __init__(self, invalid_value: str):

        super().__init__(
            title="Invalid Color Value",
            description=f"You entered `{invalid_value}` for your accent color.",
            message="The value you entered in the modal couldn't be parsed into a HEX color.",
            solution=(
                "Ensure you're entering a valid HEX code comprised of 6 characters, "
                "numbers `0 - 9` and letters `A - F`."
            )
        )

################################################################################
