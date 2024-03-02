from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List, Type, Optional, Tuple

from discord import Embed, Interaction, EmbedField, SelectOption

from UI.Common import ConfirmCancelView
from UI.Positions import (
    PositionStatusView,
    PositionRequirementModal,
    RemoveRequirementView,
    PositionNameModal
)
from Utilities import Utilities as U
from .Requirement import Requirement

if TYPE_CHECKING:
    from Classes import PositionManager, TrainingBot
################################################################################

__all__ = ("Position", )

GUILD_ID = 303742308874977280
P = TypeVar("P", bound="Position")

################################################################################
class Position:
    """A class to represent a workable job position, holdable in an RP establishment.
    
    Attributes:
    -----------
    _manager: :class:`PositionManager`
        The manager instance that holds the position.
    _id: :class:`str`
        The unique identifier for the position.
    _name: :class:`str`
        The name of the position.
    _requirements: List[:class:`Requirement`]
        A list of all the training requirements for the position.
    """

    __slots__ = (
        "_manager",
        "_id",
        "_name",
        "_requirements",
    )
    
################################################################################
    def __init__(
        self, 
        mgr: PositionManager, 
        _id: str,
        name: str, 
        reqs: Optional[List[Requirement]] = None
    ) -> None:

        self._manager: PositionManager = mgr
        
        self._id: str = _id
        self._name: str = name
        self._requirements: List[Requirement] = reqs or []

################################################################################
    @classmethod
    def new(cls: Type[P], mgr: PositionManager, name: str) -> P:
        """Create a new position and insert it into the database.
        
        Parameters:
        -----------
        mgr: :class:`PositionManager`
            The manager instance that holds the position.
        name: :class:`str`
            The name of the position.
            
        Returns:
        --------
        :class:`Position`
            The newly created position.
        """

        new_id = mgr.bot.database.insert.position(mgr.guild_id, name)
        return cls(mgr, new_id, name)

################################################################################
    @classmethod
    def load(
        cls: Type[P], 
        mgr: PositionManager, 
        data: Tuple[str, str],
        requirements: List[Tuple[str, int, str, str]]
    ) -> P:
        """Load database data into a position instance.
        
        Parameters:
        -----------
        mgr: :class:`PositionManager`
            The manager instance that holds the position.
        data: Tuple[:class:`str`, :class:`str`, :class:`int`, :class:`int`]
            The data from the database to load into the position.
            
        Returns:
        --------
        :class:`Position`
            The loaded position instance.
        """

        reqs = [Requirement.load(mgr.bot, r) for r in requirements]
        # (data[1] is the guild_id, which we don't use here.)
        return cls(mgr, data[0], data[2], reqs) 
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.position(self)
        
################################################################################    
    @property
    def bot(self) -> TrainingBot:

        return self._manager.bot

################################################################################
    @property
    def id(self) -> str:

        return self._id

################################################################################
    @property
    def name(self) -> str:

        return self._name
    
################################################################################
    @name.setter
    def name(self, value: str) -> None:
            
        self._name = value
        self.update()
        
################################################################################
    @property
    def requirements(self) -> List[Requirement]:
        
        return self._requirements
    
################################################################################
    @property
    def select_option(self) -> SelectOption:
        """Return the position as a select option where label=name & value=id."""

        return SelectOption(label=self.name, value=self.id)

################################################################################
    def get_requirement(self, req_id: str) -> Requirement:
        
        for r in self._requirements:
            if r.id == req_id:
                return r
            
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        """Open the position's status menu for the user.
        
        Parameters:
        -----------
        interaction: :class:`Interaction`
            The interaction that triggered the menu.
        """

        status = self.status()
        view = PositionStatusView(interaction.user, self)

        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    def status(self) -> Embed:
        """Return the position's current status as an embed.
        
        Returns:
        --------
        :class:`Embed`
            The position's status as an embed.
        """

        reqs_list = [r.description for r in self.requirements]
        reqs_list.extend(
            [f"{r.description} - **(Global)**" for r in self._manager.global_requirements]
        )
        field_value = ("* " + "\n* ".join(reqs_list)) if reqs_list else "`None`"

        return U.make_embed(
            title=f"Position Status for: {self.name}",
            fields=[
                EmbedField(
                    name="Training Requirements",
                    value=field_value,
                    inline=False
                )
            ]
        )
    
################################################################################
    async def add_requirement(self, interaction: Interaction) -> None:
        """Add a new requirement to the position.
        
        Parameters:
        -----------
        interaction: :class:`Interaction`
            The interaction that triggered the menu.
        """
    
        modal = PositionRequirementModal()
    
        await interaction.response.send_modal(modal)
        await modal.wait()
    
        if not modal.complete:
            return
    
        self._requirements.append(Requirement.new(self, self.id, modal.value))

################################################################################
    async def remove_requirement(self, interaction: Interaction) -> None:
        """Remove a requirement from the position.
        
        Parameters:
        -----------
        interaction: :class:`Interaction`
            The interaction that triggered the menu.
        """

        embed = U.make_embed(
            title="Remove Requirement",
            description=(
                "Select the requirement you'd like to remove.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = RemoveRequirementView(interaction.user, [r.select_option() for r in self.requirements])

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return
        
        confirm = U.make_embed(
            title="Confirm Requirement Removal",
            description=(
                f"Are you sure you want to remove the requirement:\n"
                f"`{view.value}`?"
            )
        )
        confirm_view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=confirm, view=confirm_view)
        await confirm_view.wait()

        if not confirm_view.complete or confirm_view.value is False:
            return

        requirement = self.get_requirement(view.value)
        requirement.delete()

        self.requirements.remove(requirement)

################################################################################
    async def edit_name(self, interaction: Interaction) -> None:
        """Edit the position's name.
        
        Parameters:
        -----------
        interaction: :class:`Interaction`
            The interaction that triggered the menu.
        """

        modal = PositionNameModal(self.name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value

################################################################################
