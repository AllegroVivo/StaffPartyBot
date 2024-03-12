from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Tuple, Any

from discord import Interaction, Embed, EmbedField

from Assets import BotEmojis
from UI.Profiles import (
    PersonalityStatusView,
    ProfileLikesModal,
    ProfilePersonalityModal,
    ProfileAboutMeModal
)
from Utilities import Utilities as U, NS
from .ProfileSection import ProfileSection

if TYPE_CHECKING:
    from Classes import Profile
################################################################################

__all__ = ("ProfilePersonality",)

PP = TypeVar("PP", bound="ProfilePersonality")

################################################################################
class ProfilePersonality(ProfileSection):
    
    __slots__ = (
        "_likes",
        "_dislikes",
        "_personality",
        "_aboutme"
    )

################################################################################
    def __init__(self, parent: Profile, **kwargs) -> None:
        
        super().__init__(parent)

        self._likes: List[str] = kwargs.pop("likes", None) or []
        self._dislikes: List[str] = kwargs.pop("dislikes", None) or []
        self._personality: Optional[str] = kwargs.pop("personality", None)
        self._aboutme: Optional[str] = kwargs.pop("aboutme", None)
        
################################################################################    
    @classmethod
    def load(cls: Type[PP], parent: Profile, data: Tuple[Any, ...]) -> PP:

        return cls(
            parent=parent,
            likes=data[0],
            dislikes=data[1],
            personality=data[2],
            aboutme=data[3]
        )
    
################################################################################
    @property
    def likes(self) -> List[str]:
        
        return self._likes
    
################################################################################
    @likes.setter
    def likes(self, value: List[str]) -> None:
        
        self._likes = value
        self.update()
        
################################################################################
    @property
    def dislikes(self) -> List[str]:
        
        return self._dislikes
    
################################################################################
    @dislikes.setter
    def dislikes(self, value: List[str]) -> None:
        
        self._dislikes = value
        self.update()
        
################################################################################
    @property
    def personality(self) -> Optional[str]:
        
        return self._personality
    
################################################################################
    @personality.setter
    def personality(self, value: Optional[str]) -> None:
        
        self._personality = value
        self.update()
        
################################################################################
    @property
    def aboutme(self) -> Optional[str]:
        
        return self._aboutme
    
################################################################################    
    @aboutme.setter
    def aboutme(self, value: Optional[str]) -> None:
        
        self._aboutme = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.parent.bot.database.update.profile_personality(self)
        
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = PersonalityStatusView(interaction.user, self)
        
        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            color=self.parent.color,
            title=f"Personality Attributes for __{self.parent.char_name}__",
            description=U.draw_line(extra=40),
            timestamp=False,
            fields=[
                self._likes_field(True),
                self._likes_field(False),
                self._personality_field(),
                self._preview_aboutme()
            ]
        )

################################################################################
    def _likes_field(self, is_likes: bool) -> EmbedField:

        if is_likes:
            section_name = f"{BotEmojis.Check}  __Likes__"
            field_value = ("- " + "\n- ".join(self._likes)) if self.likes else str(NS)
            field_value += f"\n{U.draw_line(extra=15)}"
        else:
            section_name = f"{BotEmojis.Cross}  __Dislikes__"
            field_value = ("- " + "\n- ".join(self._dislikes)) if self.dislikes else str(NS)

        return EmbedField(
            name=section_name,
            value=field_value,
            inline=True
        )

################################################################################
    def _personality_field(self) -> EmbedField:

        value = self.personality if self.personality is not None else str(NS)

        return EmbedField(
            name=f"{BotEmojis.Goose}  __Personality__  {BotEmojis.Goose}",
            value=f"{value}\n{U.draw_line(extra=15)}",
            inline=False
        )

################################################################################
    def _preview_aboutme(self) -> EmbedField:

        if self.aboutme is None:
            value = str(NS)
        elif len(self.aboutme) < 250:
            value = self.aboutme
        else:
            value = self.aboutme[:251] + "...\n*(Preview Only -- Click below to see the whole thing!)*"

        return EmbedField(
            name=f"{BotEmojis.Scroll}  __About Me / Biography__  {BotEmojis.Scroll}",
            value=f"{value}\n{U.draw_line(extra=15)}",
            inline=False
        )

################################################################################
    async def set_likes(self, interaction: Interaction) -> None:
        
        modal = ProfileLikesModal(self.likes, True)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.likes = modal.value
        
################################################################################
    async def set_dislikes(self, interaction: Interaction) -> None:

        modal = ProfileLikesModal(self.dislikes, False)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.dislikes = modal.value
        
################################################################################
    async def set_personality(self, interaction: Interaction) -> None:

        modal = ProfilePersonalityModal(self.personality)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.personality = modal.value
        
################################################################################
    async def set_aboutme(self, interaction: Interaction) -> None:

        modal = ProfileAboutMeModal(self.aboutme)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.aboutme = modal.value
        
################################################################################
    def progress(self) -> str:

        em_likes = self.progress_emoji(self._likes)
        em_dislikes = self.progress_emoji(self._dislikes)
        em_personality = self.progress_emoji(self._personality)
        em_aboutme = self.progress_emoji(self._aboutme)

        return (
            f"{U.draw_line(extra=15)}\n"
            "__**Personality**__\n"
            f"{em_likes} -- Likes\n"
            f"{em_dislikes} -- Dislikes\n"
            f"{em_personality} -- Personality\n"
            f"{em_aboutme} -- About Me\n"
        )

################################################################################
    def compile(
            self
    ) -> Tuple[
        Optional[EmbedField],
        Optional[EmbedField],
        Optional[EmbedField],
        Optional[Embed]
    ]:

        return (
            self._likes_field(True) if self.likes else None,
            self._likes_field(False) if self.dislikes else None,
            self._personality_field() if self.personality else None,
            self._compile_aboutme()
        )

################################################################################
    def _compile_aboutme(self) -> Optional[Embed]:

        if not self.aboutme:
            return

        return U.make_embed(
            color=self.parent.color,
            title=f"About {self.parent.char_name}",
            description=self.aboutme,
            footer_text=(
                self.parent._details.url
                if self.parent._details.url is not NS
                else None
            )
        )

################################################################################
