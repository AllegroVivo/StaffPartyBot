from ._Error import ErrorMessage
################################################################################

__all__ = ("BotUserNotAllowedError",)

################################################################################
class BotUserNotAllowedError(ErrorMessage):

    def __init__(self):

        super().__init__(
            title="Bot User Not Allowed",
            message="You may not add a bot as a trainer.",
            solution="Try a different user."
        )

################################################################################
