from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Interaction, User

from UI.Common import FroggeView, CloseMessageButton, FroggeButton

if TYPE_CHECKING:
    from Classes import ProfileImages, PAdditionalImage
################################################################################

__all__ = ("ProfileImageStatusView",)

################################################################################        
class ProfileImageStatusView(FroggeView):

    def __init__(self, user: User, images: ProfileImages):

        super().__init__(user, timeout=300)

        self.images: ProfileImages = images

        button_list = [
            RemoveThumbnailButton(self.images._thumbnail),
            RemoveMainImageButton(self.images._main_image),
            PaginateAdditionalImagesButton(self.images.additional),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################        
class RemoveThumbnailButton(FroggeButton):

    def __init__(self, thumbnail: Optional[str]) -> None:

        super().__init__(
            label="Remove Thumbnail",
            disabled=False,
            row=0
        )
        
        self.set_style(thumbnail)
        self.disabled = thumbnail is None

    async def callback(self, interaction: Interaction) -> None:
        images: ProfileImages = self.view.images
        await images.remove_thumbnail(interaction)

        self.set_style(images.thumbnail)
        self.disabled = images.thumbnail is None

        await self.view.edit_message_helper(
            interaction=interaction,
            embed=images.status(),
            view=self.view
        )

################################################################################
class RemoveMainImageButton(FroggeButton):
    
    def __init__(self, main_img: Optional[str]) -> None:
        
        super().__init__(
            label="Remove Main Image",
            disabled=False,
            row=0
        )
        
        self.set_style(main_img)
        self.disabled = main_img is None
        
    async def callback(self, interaction: Interaction) -> None:
        images: ProfileImages = self.view.images
        await images.remove_main_image(interaction)

        self.set_style(images.thumbnail)
        self.disabled = images.main_image is None

        await self.view.edit_message_helper(
            interaction=interaction,
            embed=images.status(),
            view=self.view
        )
        
################################################################################
class PaginateAdditionalImagesButton(FroggeButton):
    
    def __init__(self, images: List[PAdditionalImage]) -> None:
        
        super().__init__(
            label="Manage Additional Images",
            disabled=False,
            row=0
        )
        
        self.set_style(images)
        self.disabled = len(images) == 0
        
    async def callback(self, interaction: Interaction) -> None:
        images: ProfileImages = self.view.images
        await images.manage_additional(interaction)

        self.disabled = len(images.additional) == 0

        await self.view.edit_message_helper(
            interaction=interaction,
            embed=images.status(),
            view=self.view
        )
        
################################################################################
