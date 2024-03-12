from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import Interaction, User

from UI.Common import FroggeView, CloseMessageButton, ProfileSectionButton

if TYPE_CHECKING:
    from Classes import ProfilePersonality
################################################################################

__all__ = ("PersonalityStatusView",)

################################################################################        
class PersonalityStatusView(FroggeView):

    def __init__(self, user: User, personality: ProfilePersonality):

        super().__init__(user, timeout=300)

        self.personality: ProfilePersonality = personality

        button_list = [
            LikesButton(self.personality.likes),
            DislikesButton(self.personality.dislikes),
            PersonalityButton(self.personality.personality),
            AboutMeButton(self.personality.aboutme),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)

################################################################################        
class LikesButton(ProfileSectionButton):

    def __init__(self, likes: List[str]) -> None:

        super().__init__(
            label="Likes",
            disabled=False,
            row=0
        )
        
        self.set_style(likes)

    async def callback(self, interaction: Interaction) -> None:
        p = self.view.personality
        
        await p.set_likes(interaction)
        self.set_style(p.likes)
        
        await interaction.edit(embed=p.status(), view=self.view)

################################################################################
class DislikesButton(ProfileSectionButton):

    def __init__(self, dislikes: List[str]) -> None:

        super().__init__(
            label="Dislikes",
            disabled=False,
            row=0
        )

        self.set_style(dislikes)

    async def callback(self, interaction: Interaction) -> None:
        p = self.view.personality

        await p.set_dislikes(interaction)
        self.set_style(p.dislikes)

        await interaction.edit(embed=p.status(), view=self.view)

################################################################################
class PersonalityButton(ProfileSectionButton):
    
    def __init__(self, personality: Optional[str]) -> None:

        super().__init__(
            label="Personality",
            disabled=False,
            row=0
        )

        self.set_style(personality)

    async def callback(self, interaction: Interaction) -> None:
        p = self.view.personality

        await p.set_personality(interaction)
        self.set_style(p.personality)

        await interaction.edit(embed=p.status(), view=self.view)
        
################################################################################
class AboutMeButton(ProfileSectionButton):

    def __init__(self, aboutme: Optional[str]) -> None:

        super().__init__(
            label="About Me/Bio",
            disabled=False,
            row=0
        )

        self.set_style(aboutme)

    async def callback(self, interaction: Interaction) -> None:
        p = self.view.personality

        await p.set_aboutme(interaction)
        self.set_style(p.aboutme)

        await interaction.edit(embed=p.status(), view=self.view)
        
################################################################################
