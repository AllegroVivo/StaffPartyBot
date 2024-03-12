from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("CharNameNotSetError",)

################################################################################
class CharNameNotSetError(ErrorMessage):

    def __init__(self):
        super().__init__(
            title="Character Name Not Set",
            message="You haven't set a character name for your profile!",
            solution=(
                "You can't post your profile until you complete at least that much.\n"
                "Use `/profile details` to change it."
            )
        )

################################################################################
