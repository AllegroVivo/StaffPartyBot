from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction, User, ButtonStyle
from discord.ui import Button

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import ProfileImages
################################################################################

__all__ = ("AdditionalImageView",)

################################################################################        
class AdditionalImageView(FroggeView):

    def __init__(self, owner: User, images: ProfileImages, image_id: str = None):

        super().__init__(owner, close_on_complete=True)
    
        self.images: ProfileImages = images
    
        if image_id is not None:
            self.add_item(EditCaptionButton(image_id))
            self.add_item(RemoveImageButton(image_id))
    
        self.add_item(ViewImagesStatusButton())
        self.add_item(CloseMessageButton())

################################################################################
class EditCaptionButton(Button):

    def __init__(self, image_id: str):
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Caption",
            disabled=False,
            row=0
        )

        self.image_id: str = image_id

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images
        addl = images.get_additional(self.image_id)

        await addl.set_caption(interaction)

        await images.paginate_additional(interaction)
        await self.view.cancel()

################################################################################
class RemoveImageButton(Button):

    def __init__(self, image_id: str):
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Image",
            disabled=False,
            row=0
        )

        self.image_id: str = image_id

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images
        await images.remove_additional(interaction, self.image_id)

        await images.paginate_additional(interaction)
        await self.view.cancel()

################################################################################
class ViewImagesStatusButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="View Images Status",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        images: ProfileImages = self.view.images

        self.view._close_on_complete = True
        await self.view.cancel()  # type: ignore

        await images.set(interaction)

################################################################################
