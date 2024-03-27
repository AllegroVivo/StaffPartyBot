from ._Error import ErrorMessage
################################################################################

__all__ = ("PostingNotCompleteError",)

################################################################################
class PostingNotCompleteError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Job Posting Not Complete",
            message=(
                "The job posting is not complete. Please ensure that all "
                "required fields are filled out before submitting."
            ),
            solution=(
                "Required fields are as follows:\n"
                "* `Position`\n"
                "* `Salary`\n"
                "* `Posting Type`\n"
                "* `Description`\n"
                "* `Schedule`"
            )
        )

################################################################################
