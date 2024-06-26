from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple, List

from discord import Interaction

from UI.Venues import RPLevelSelectView, VenueTagSelectView
from Utilities import (
    Utilities as U,
    RPLevel,
    VenueForumTag,
    log,
)
from .VenueTag import VenueTag

if TYPE_CHECKING:
    from Classes import Venue, StaffPartyBot, XIVVenue
################################################################################

__all__ = ("VenueAtAGlance",)

AAG = TypeVar("AAG", bound="VenueAtAGlance")

################################################################################
class VenueAtAGlance:

    __slots__ = (
        "_parent",
        "_level",
        "_nsfw",
        "_tags",
    )

################################################################################
    def __init__(
        self,
        parent: Venue,
        level: Optional[RPLevel] = None,
        nsfw: Optional[bool] = False,
        tags: Optional[VenueTag] = None,
    ) -> None:

        self._parent: Venue = parent
        
        self._level: Optional[RPLevel] = level
        self._nsfw: bool = nsfw
        self._tags: List[VenueTag] = tags or []

################################################################################
    @classmethod
    def load(cls: Type[AAG], parent: Venue, data: Tuple[Any, ...]) -> AAG:
        
        raw_tags = [VenueTag(t) for t in data[3]] if data[3] is not None else []
        tags = [
            t for t in raw_tags 
            if t.tag_text.lower() in [tag.proper_name.lower() for tag in VenueForumTag]
        ]
        
        return cls(
            parent,
            level=RPLevel(data[0]) if data[0] is not None else None,
            nsfw=data[1],
            tags=tags,
        )
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.id
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._parent.bot

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue_aag(self)
        
################################################################################
    @property
    def level(self) -> Optional[RPLevel]:
        
        return self._level
    
    @level.setter
    def level(self, value: Optional[RPLevel]) -> None:
        
        self._level = value
        self.update()
        
################################################################################
    @property
    def nsfw(self) -> bool:
        
        return self._nsfw
    
    @nsfw.setter
    def nsfw(self, value: bool) -> None:
        
        self._nsfw = value
        self.update()
        
################################################################################
    @property
    def tags(self) -> List[VenueTag]:
        
        return self._tags
    
    @tags.setter
    def tags(self, value: List[VenueTag]) -> None:
        
        self._tags = value
        self.update()
        
################################################################################
    def compile(self) -> str:
        
        ret = f"__RP Level:__ "
        ret += f"`{self.level.proper_name}`" if self.level else "`Not Set`"
        
        ret += f"\n__NSFW:__ `{'~Yes~' if self.nsfw else 'No'}`"
        
        ret += f"\n__Venue Tags:__\n"
        if self.tags:
            tags_list = [f"`{t.tag_text}`" for t in self.tags]
            tags_formatted = [', '.join(tags_list[i:i+3]) for i in range(0, len(tags_list), 3)]
            ret += '\n'.join(tags_formatted)
        else:
            ret += "`Not Set`"
            
        return ret
        
################################################################################
    async def set_level(self, interaction: Interaction) -> None:
        
        log.info(
            "Venues",
            f"Setting RP level for {self._parent.name} ({self._parent.id})..."
        )
        
        prompt = U.make_embed(
            title="Set RP Level",
            description=(
                "Please select the RP level for your venue\n"
                "from the selector below."
            )
        )
        view = RPLevelSelectView(interaction.user, self._parent)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Venues", "User cancelled RP level selection.")
            return
        
        self.level = view.value
        
        log.info(
            "Venues",
            (
                f"RP level for {self._parent.name} ({self._parent.id}) has been "
                f"set to {self.level.proper_name}."
            )
        )
        
################################################################################
    async def toggle_nsfw(self, interaction: Interaction) -> None:
        
        self.nsfw = not self.nsfw
        await interaction.respond("** **", delete_after=0.1)
        
        log.info(
            "Venues",
            (
                f"NSFW status for {self._parent.name} ({self._parent.id}) has been "
                f"set to {self.nsfw}."
            )
        )
        
################################################################################
    def update_from_xiv_venue(self, venue: XIVVenue) -> None:
        
        self._nsfw = not venue.sfw
        self._tags = [
            VenueTag(t) for t in venue.tags
            if t.lower() in [tag.proper_name.lower() for tag in VenueForumTag]
        ]
        
        self.update()

################################################################################
    async def set_tags(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Venue Tags",
            description=(
                "Please select the tags for your venue\n"
                "from the selector below."
            )
        )
        view = VenueTagSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.tags = [VenueTag(t.proper_name) for t in view.value]
    
################################################################################
