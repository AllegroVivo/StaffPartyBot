from ._Error import ErrorMessage
################################################################################

__all__ = ("GroupTrainingNotCompleteError",)

################################################################################
class GroupTrainingNotCompleteError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Group Training Not Completely Filled Out",
            message=(
                "The group training has not been fully filled out. Please ensure that all "
                "required fields are completed before submitting."
            ),
            solution=(
                "Required fields are as follows:\n"
                "* `Name`\n"
                "* `Description`\n"
                "* `Date & Time`"
            )
        )

################################################################################
