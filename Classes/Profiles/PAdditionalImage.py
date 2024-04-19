from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from discord import Interaction
from discord.ext.pages import Page

from Classes.Common import AdditionalImage
from UI.Profiles import AdditionalImageView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import ProfileImages
################################################################################

__all__ = ("PAdditionalImage",)

################################################################################
class PAdditionalImage(AdditionalImage):
    
    @classmethod
    def new(cls, parent: ProfileImages, url: str, caption: Optional[str]) -> PAdditionalImage:
        
        new_id = parent.parent.bot.database.insert.addl_image(parent.parent.id, url, caption)
        return cls(parent=parent, _id=new_id, url=url, caption=caption)
    
################################################################################
    def update(self) -> None:
        
        self._parent.parent.bot.database.update.profile_addl_image(self)
    
################################################################################
    def delete(self) -> None:
        
        self._parent.parent.bot.database.delete.profile_addl_image(self)
        
################################################################################
    def page(self, interaction: Interaction, parent: ProfileImages) -> Page:

        return Page(
            embeds=[
                U.make_embed(
                    title="Additional Images",
                    image_url=self.url,
                    footer_text=f"Caption: {str(self.caption)}",
                    timestamp=False
                )
            ],
            custom_view=AdditionalImageView(interaction.user, parent, self.id)
        )

################################################################################
