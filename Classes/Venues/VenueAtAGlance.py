from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple

from discord import Interaction

from UI.Venues import RPLevelSelectView, RPStyleSelectView, RPSizeSelectView
from Utilities import (
    Utilities as U,
    RPLevel,
    VenueStyle,
    VenueSize,
)

if TYPE_CHECKING:
    from Classes import VenueDetails, TrainingBot
################################################################################

__all__ = ("VenueAtAGlance",)

AAG = TypeVar("AAG", bound="VenueAtAGlance")

################################################################################
class VenueAtAGlance:

    __slots__ = (
        "_parent",
        "_level",
        "_nsfw",
        "_style",
        "_size",
    )

################################################################################
    def __init__(
        self,
        parent: VenueDetails,
        level: Optional[RPLevel] = None,
        nsfw: Optional[bool] = False,
        style: Optional[VenueStyle] = None,
        size: Optional[VenueSize] = None
    ) -> None:

        self._parent: VenueDetails = parent
        
        self._level: Optional[RPLevel] = level
        self._nsfw: bool = nsfw
        self._style: Optional[VenueStyle] = style
        self._size: Optional[VenueSize] = size

################################################################################
    @classmethod
    def load(cls: Type[AAG], parent: VenueDetails, data: Tuple[Any, ...]) -> AAG:
        
        return cls(
            parent,
            RPLevel(data[2]) if data[2] is not None else None,
            data[3],
            VenueStyle(data[4]) if data[4] is not None else None,
            VenueSize(data[5]) if data[5] is not None else None
        )
    
################################################################################
    @property
    def venue_id(self) -> str:
        
        return self._parent.venue_id
    
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
    def style(self) -> Optional[VenueStyle]:
        
        return self._style
    
    @style.setter
    def style(self, value: Optional[VenueStyle]) -> None:
        
        self._style = value
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
        ret += self.level.proper_name if self.level else "`Not Set`"
        
        ret += f"\n__NSFW:__ `{'~Yes~' if self.nsfw else 'No'}`"
        
        ret += f"\n__Venue Style:__ "
        ret += self.style.proper_name if self.style else "`Not Set`"
        
        ret += f"\n__Venue Size:__ "
        ret += self.size.proper_name if self.size else "`Not Set`"
        
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
        view = RPLevelSelectView(interaction.user, self._parent.venue)
        
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
    async def set_style(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Venue Style",
            description=(
                "Please select the style of your venue\n"
                "from the selector below."
            )
        )
        view = RPStyleSelectView(interaction.user, self._parent.venue)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.style = view.value
    
################################################################################
    async def set_size(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Venue Size",
            description=(
                "Please select the size of your venue\n"
                "from the selector below."
            )
        )
        view = RPSizeSelectView(interaction.user, self._parent.venue)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.size = view.value
    
################################################################################
