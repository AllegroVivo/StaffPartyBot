from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("TooManyUsersError",)

################################################################################
class TooManyUsersError(ErrorMessage):

    def __init__(self, venue_name: str):

        super().__init__(
            title="Too Many Authorized Users",
            message=(
                f"You're trying to add too many authorized users to `{venue_name}`."
            ),
            solution=(
                "The maximum number of authorized owners is 2 and additional "
                "authorized users is 3. For a total of 5. If you need to add"
                "more users, please contact a server administrator."
            )
        )

################################################################################
