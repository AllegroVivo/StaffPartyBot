from __future__ import annotations

from discord    import Interaction, Member, User
from discord.ui import View
from typing     import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    pass
################################################################################

__all__ = (
    "FroggeView",
)

################################################################################
class FroggeView(View):

    def __init__(
        self,
        owner: Union[Member, User],
        *args,
        close_on_complete: bool = False,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.owner: Union[Member, User] = owner
        self.value: Optional[Any] = None
        self.complete: bool = False

        self._interaction: Optional[Interaction] = None
        self._close_on_complete: bool = close_on_complete

################################################################################
    async def interaction_check(self, interaction: Interaction) -> bool:

        if interaction.user == self.owner:
            self._interaction = interaction
            return True

        return False

################################################################################
    async def on_timeout(self) -> None:

        if self.disable_on_timeout:
            self.disable_all_items()
        else:
            self.clear_items()

        await self._edit_message_helper()

################################################################################
    async def _edit_message_helper(self) -> None:

        try:
            await self._interaction.edit(view=self)
        except:
            pass

################################################################################
    async def stop(self) -> None:

        super().stop()

        if self._close_on_complete:
            if self._interaction is not None:
                try:
                    await self._interaction.message.delete()
                except:
                    try:
                        await self._interaction.delete_original_response()
                    except:
                        pass

################################################################################
    def close_on_complete(self, value: bool) -> None:

        self._close_on_complete = value

################################################################################
