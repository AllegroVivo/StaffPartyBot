from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Interaction, Embed, NotFound
from discord.ext.pages import Paginator, Page

if TYPE_CHECKING:
    from Classes import ProfileImages
################################################################################

__all__ = ("ImageFrogginator",)

################################################################################
class ImageFrogginator(Paginator):

    def __init__(
        self,
        pages: List[Page],
        images: ProfileImages,
        close_on_complete: bool = False,
        **kwargs
    ):

        super().__init__(pages=pages, author_check=True, **kwargs)

        self.images: ProfileImages = images
        
        self._interaction: Optional[Interaction] = None
        self._close_on_complete: bool = close_on_complete

################################################################################
    async def interaction_check(self, interaction: Interaction) -> bool:

        self._interaction = interaction
        return await super().interaction_check(interaction)

################################################################################
    async def on_timeout(self) -> None:

        try:
            await super().on_timeout()
        except NotFound:
            pass
        except:
            raise

################################################################################
    async def cancel(
        self,
        include_custom: bool = False,
        page: Optional[str, Page, List[Embed], Embed] = None,
    ) -> None:

        if self._close_on_complete:
            if self._interaction is not None:
                try:
                    await self.message.delete()
                except:
                    print("Error in Frogginator Cancel")
        else:
            await super().cancel(include_custom, page)

################################################################################
