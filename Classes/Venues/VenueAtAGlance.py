from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple, List

from discord import Interaction

from .VenueTag import VenueTag
from UI.Venues import RPLevelSelectView, VenueTagSelectView, RPSizeSelectView
from Utilities import (
    Utilities as U,
    RPLevel,
    VenueSize,
)

if TYPE_CHECKING:
    from Classes import Venue, TrainingBot, XIVVenue
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
        "_size",
    )

################################################################################
    def __init__(
        self,
        parent: Venue,
        level: Optional[RPLevel] = None,
        nsfw: Optional[bool] = False,
        tags: Optional[VenueTag] = None,
        size: Optional[VenueSize] = None
    ) -> None:

        self._parent: Venue = parent
        
        self._level: Optional[RPLevel] = level
        self._nsfw: bool = nsfw
        self._tags: List[VenueTag] = tags or []
        self._size: Optional[VenueSize] = size

################################################################################
    @classmethod
    def load(cls: Type[AAG], parent: Venue, data: Tuple[Any, ...]) -> AAG:
        
        return cls(
            parent,
            level=RPLevel(data[0]) if data[0] is not None else None,
            nsfw=data[1],
            size=VenueSize(data[2]) if data[2] is not None else None,
            tags=[VenueTag(t) for t in data[3]] if data[3] is not None else None,
        )
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.id
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
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
    @property
    def size(self) -> Optional[VenueSize]:
        
        return self._size
    
    @size.setter
    def size(self, value: Optional[VenueSize]) -> None:
        
        self._size = value
        self.update()
        
################################################################################
    def compile(self) -> str:
        
        ret = f"__RP Level:__ "
        ret += f"`{self.level.proper_name}`" if self.level else "`Not Set`"
        
        ret += f"\n__NSFW:__ `{'~Yes~' if self.nsfw else 'No'}`"
        
        ret += f"\n__Venue Size:__ "
        ret += f"`{self.size.proper_name}`" if self.size else "`Not Set`"
        
        ret += f"\n__Venue Tags:__\n"
        if self.tags:
            tags_list = [f"`{t.tag_text}`" for t in self.tags]
            tags_formatted = [', '.join(tags_list[i:i+3]) for i in range(0, len(tags_list), 3)]
            ret += '\n'.join(tags_formatted)
        else:
            ret += "`Not Set`"
        
        ret += f"\n{U.draw_line(extra=15)}"
            
        return ret
        
################################################################################
    async def set_level(self, interaction: Interaction) -> None:
        
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
            return
        
        self.level = view.value
        
################################################################################
    async def toggle_nsfw(self, interaction: Interaction) -> None:
        
        self.nsfw = not self.nsfw
        await interaction.respond("** **", delete_after=0.1)
        
################################################################################
    async def set_size(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Venue Size",
            description=(
                "Please select the size of your venue\n"
                "from the selector below."
            )
        )
        view = RPSizeSelectView(interaction.user, self._parent)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.size = view.value

################################################################################
    def update_from_xiv_venue(self, venue: XIVVenue) -> None:
        
        self._nsfw = not venue.sfw
        self._tags = [VenueTag(t) for t in venue.tags]
        
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
