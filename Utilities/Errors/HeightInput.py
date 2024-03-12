from __future__ import annotations

from ._Error import ErrorMessage
################################################################################

__all__ = ("HeightInputError",)

################################################################################
class HeightInputError(ErrorMessage):

    def __init__(self, entry: str):

        super().__init__(
            title="Invalid Height Input",
            message=f"The value `{entry}` couldn't be interpreted.",
            solution=(
                "The following are acceptable input styles:\n"
                "- `X feet X inches`\n"
                "- `X ft. X in.`\n"
                "- `X in.`\n"
                "- `X cm.`"
            )
        )

################################################################################
