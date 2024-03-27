from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar, Optional, Any, Tuple
from discord import Interaction
from .Internship import Internship
from Utilities import Utilities as U
from UI.Venues.Views import PositionSelectView

if TYPE_CHECKING:
    from Classes import Venue, Position
################################################################################

__all__ = ("InternshipManager",)

IM = TypeVar("IM", bound="InternshipManager")

################################################################################
class InternshipManager:
    
    __slots__ = (
        "_parent",
        "_internships",
        "_positions",
    )
    
################################################################################
    def __init__(
        self, 
        parent: Venue,
        internships: Optional[List[Internship]] = None,
        positions: Optional[List[Position]] = None
    ) -> None:
        
        self._parent: Venue = parent
        
        self._internships: List[Internship] = internships or []
        self._positions: List[Position] = positions or []
        
################################################################################
    @classmethod
    def load(cls: Type[IM], parent: Venue, data: Tuple[Any, ...]) -> IM:
        
        position_manager = parent.guild.position_manager
        
        return cls(
            parent=parent,
            internships=[],
            positions=(
                [position_manager.get_position(pos_id) for pos_id in data]
                if data else []
            )
        )
    
################################################################################
    @property
    def sponsored_positions(self) -> List[Position]:
        
        self._positions.sort(key=lambda p: p.name.lower())
        return self._positions

################################################################################
    async def set_sponsored_positions(self, interaction: Interaction) -> None:
        
        options = self._parent.guild.position_manager.select_options()
        for option in options:
            if option.value in [p.id for p in self._positions]:
                option.default = True
        
        prompt = U.make_embed(
            title="Sponsor Positions",
            description="Select the positions you want to sponsor...",
        )
        view = PositionSelectView(interaction.user, options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self._positions = [
            self._parent.guild.position_manager.get_position(pos_id) 
            for pos_id in view.value
        ]
        self._parent.update()

################################################################################
    