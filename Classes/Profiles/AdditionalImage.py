from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Dict

from discord import Interaction
from discord.ext.pages import Page

from UI.Profiles import AdditionalImageView, AdditionalImageCaptionModal
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import ProfileImages
################################################################################

__all__ = ("AdditionalImage",)

################################################################################
class AdditionalImage:
    
    __slots__ = (
        "_parent",
        "_id",
        "_url",
        "_caption"
    )
    
################################################################################
    def __init__(self, **kwargs) -> None:
        
        self._parent: ProfileImages = kwargs.pop("parent")
        
        self._id: str = kwargs.pop("_id")
        self._url: str = kwargs.pop("url")
        self._caption: Optional[str] = kwargs.pop("caption", None)
    
################################################################################
    @classmethod
    def new(cls, parent: ProfileImages, url: str, caption: Optional[str]) -> AdditionalImage:
        
        new_id = parent.parent.bot.database.insert.addl_image(parent.parent.id, url, caption)
        return cls(parent=parent, _id=new_id, url=url, caption=caption)
    
################################################################################
    def __eq__(self, other: AdditionalImage) -> bool:
        
        return self.id == other.id
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def url(self) -> str:
        
        return self._url
    
################################################################################
    @property
    def caption(self) -> Optional[str]:
        
        return self._caption
    
################################################################################
    @caption.setter
    def caption(self, value: Optional[str]) -> None:
        
        self._caption = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.parent.bot.database.update.profile_addl_image(self)
    
################################################################################
    def delete(self) -> None:
        
        self._parent.parent.bot.database.delete.profile_addl_image(self)
        
################################################################################
    def compile(self) -> str:

        if self.caption is None:
            return self.url

        return f"[{self.caption}]({self.url})"

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
    async def set_caption(self, interaction: Interaction) -> None:

        modal = AdditionalImageCaptionModal(self.caption)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.caption = modal.value
        
################################################################################
    def _to_dict(self) -> Dict[str, Any]:
        
        return {
            "id": self.id,
            "url": self.url,
            "caption": self.caption
        }
    
################################################################################
