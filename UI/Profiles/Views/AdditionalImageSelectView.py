from __future__ import annotations

from typing import TYPE_CHECKING, List

from discord import Interaction, User, ButtonStyle, SelectOption
from discord.ui import Select, Button

from UI.Common import FroggeView, CloseMessageButton

if TYPE_CHECKING:
    from Classes import ProfileImages, PAdditionalImage
################################################################################

__all__ = ("AdditionalImageSelectView",)

################################################################################        
class AdditionalImageSelectView(FroggeView):

    def __init__(self, owner: User, images: ProfileImages, img: PAdditionalImage):

        super().__init__(owner, close_on_complete=True)
    
        self.images: ProfileImages = images
        self.image: PAdditionalImage = img
    
        item_list = [
            EditCaptionButton(),
            RemoveImageButton(),
            AdditionalImageSelect(images._additional_image_options()),
            CloseMessageButton()
        ]
        for item in item_list:
            self.add_item(item)

################################################################################
class AdditionalImageSelect(Select):

    def __init__(self, options: List[SelectOption]):
        
        super().__init__(
            placeholder="Select an image to edit",
            disabled=False,
            options=options,
            min_values=1,
            max_values=1,
            row=3
        )

    async def callback(self, interaction: Interaction):
        self.view.value = self.values[0]
        self.view.complete = True
        
        await self.view.edit_message_helper(interaction)
        await self.view.stop()  # type: ignore

################################################################################
class EditCaptionButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.primary,
            label="Edit Caption",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.image.set_caption(interaction)
        
        await self.view.edit_message_helper(
            interaction,
            embed=self.view.images._manage_additional_embed(self.view.image),
            view=self.view
        )

################################################################################
class RemoveImageButton(Button):

    def __init__(self):
        super().__init__(
            style=ButtonStyle.danger,
            label="Remove Image",
            disabled=False,
            row=0
        )

    async def callback(self, interaction: Interaction):
        await self.view.images.remove_additional(interaction, self.view.image)
        
        self.view.complete = True
        await self.view.stop()  # type: ignore
        
        if len(self.view.images.additional) == 0:
            return
        
        await self.view.images.manage_additional(interaction)

################################################################################
