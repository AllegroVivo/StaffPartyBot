from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List, Optional, Dict, Any

from discord import Interaction, EmbedField, Embed, SelectOption

from UI.Positions import GlobalRequirementsView, GlobalRequirementModal, RemoveRequirementView
from Utilities import Utilities as U, PositionExistsError
from .Position import Position
from .Requirement import Requirement

if TYPE_CHECKING:
    from Classes import TrainingBot, GuildData
################################################################################

__all__ = ("PositionManager", )

################################################################################
class PositionManager:

    __slots__ = (
        "_guild",
        "_positions",
        "_requirements",
    )
    
################################################################################
    def __init__(self, guild: GuildData) -> None:
    
        self._guild: GuildData = guild
    
        self._positions: List[Position] = []
        self._requirements: List[Requirement] = []

################################################################################
    def _load_all(self, data: Dict[str, Any]) -> None:
        """Loads all the positions and requirements from the database.
        
        Parameters:
        -----------
        data : Dict[:class:`str`, :class:`Any`]
            The data retrieved from the database.
        """

        position_data = data["positions"]
        requirement_data = data["requirements"]

        requirements = {"0": []}
        for req in requirement_data:
            if req[2] not in requirements.keys():
                requirements[req[2]] = []
            requirements[req[2]].append(req)

        global_reqs = requirements.get("0")
        # Global requirements
        self._requirements.extend(
            [Requirement.load(self.bot, r) for r in global_reqs]
        )

        for pos in position_data:
            reqs = requirements.get(pos[0], [])
            self._positions.append(Position.load(self, pos, reqs))
            
################################################################################    
    @property
    def bot(self) -> TrainingBot:
        
        return self._guild.bot
    
################################################################################
    @property
    def global_requirements(self) -> List[Requirement]:
        
        return self._requirements
    
################################################################################
    @property
    def positions(self) -> List[Position]:
        
        self._positions.sort(key=lambda p: p.name)
        return self._positions
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._guild.guild_id
    
################################################################################    
    async def _add_position(self, interaction: Interaction, position_name: str) -> Position:

        position = Position.new(self, position_name)
        self._positions.append(position)

        description = f"The position `{position.name}` has been added to the database."
        confirm = U.make_embed(
            title="Position Added",
            description=(
                f"{description}\n"
                f"{U.draw_line(text=description)}"
            )
        )
        await interaction.respond(embed=confirm, ephemeral=True)
        
        # Also update the currently posted SignUpMessage
        await self._guild.training_manager.signup_message.update_components()
        
        return position
        
################################################################################
    async def add_position(self, interaction: Interaction, position_name: str) -> None:
        """Adds a new position to the database.
        
        This method is a coroutine.
        
        Parameters:
        -----------
        interaction : :class:`Interaction`
            The interaction that triggered the command.
        position_name : :class:`str`
            The name of the position to add.
        """
    
        position = self.get_position_by_name(position_name)
        if position is not None:
            error = PositionExistsError(position_name)
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        position = await self._add_position(interaction, position_name)
        
        await asyncio.sleep(2)
        await self.position_status(interaction, position.name)
        
################################################################################
    def get_position_by_name(self, pos_name: str) -> Optional[Position]:
        """Get a position by its name.
        
        Parameters:
        -----------
        pos_name : :class:`str`
            The name of the position to retrieve.
            
        Returns:
        --------
        Optional[:class:`Position`]
            The position with the given name, if it exists.
        """
        
        for position in self._positions:
            if position.name.lower() == pos_name.lower():
                return position
            
################################################################################
    async def position_status(self, interaction: Interaction, pos_name: str) -> None:
        """Displays the status of a specific position.
        
        Parameters:
        -----------
        interaction : :class:`Interaction`
            The interaction that triggered the command.
        pos_name : Optional[:class:`str`]
            The name of the position to display the status of.
        """

        position = self.get_position_by_name(pos_name)
        if position is None:
            position = await self._add_position(interaction, pos_name)
            await asyncio.sleep(2)
            
        await position.menu(interaction)

################################################################################
    async def global_requirements_menu(self, interaction: Interaction) -> None:
        """Displays the global job training requirements.
        
        Parameters:
        -----------
        interaction : :class:`Interaction`
            The interaction that triggered the command.
        """

        status = self.global_requirements_status()
        view = GlobalRequirementsView(interaction.user, self)

        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    def global_requirements_status(self) -> Embed:
        """Returns an embed displaying the status of all global requirements.
        
        Returns:
        --------
        :class:`Embed`
            An embed displaying the status of all global requirements.
        """

        return U.make_embed(
            title="Global Job Training Requirements",
            description=(
                "These requirements are applied to all jobs.\n"
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                EmbedField(
                    name="__Current Global Requirements__",
                    value=(
                        ("* " + "\n* ".join([r.description for r in self.global_requirements]))
                        if self.global_requirements else "`None`"
                    ),
                    inline=False
                )
            ]
        )

################################################################################
    async def add_global_requirement(self, interaction: Interaction) -> None:
        """Adds a new global job training requirement.
        
        Parameters:
        -----------
        interaction : :class:`Interaction`
            The interaction that triggered the command.
        """

        modal = GlobalRequirementModal()

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        requirement = Requirement.new(self, "0", modal.value)
        self._requirements.append(requirement)

################################################################################
    async def remove_global_requirement(self, interaction: Interaction) -> None:
        """Removes a global job training requirement.
        
        Parameters:
        -----------
        interaction : :class:`Interaction`
            The interaction that triggered the command.
        """

        embed = U.make_embed(
            title="Remove Requirement",
            description=(
                "Select the global job requirement you'd like to remove.\n"
                f"{U.draw_line(extra=30)}"
            )
        )
        view = RemoveRequirementView(interaction.user, [r.select_option() for r in self._requirements])

        await interaction.response.send_message(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        requirement = self.get_global_requirement(view.value)
        requirement.delete()

        self._requirements.remove(requirement)

################################################################################
    def get_global_requirement(self, req_id: str) -> Requirement:
        """Get a global requirement by its ID.
        
        Parameters:
        -----------
        req_id : :class:`str`
            The ID of the requirement to retrieve.
            
        Returns:
        --------
        :class:`Requirement`
            The requirement with the given ID.
        """
        
        for req in self._requirements:
            if req.id == req_id:
                return req

################################################################################
    def select_options(
        self,
        *,
        exclude: List[Position] = None, 
        include: List[Position] = None
    ) -> List[SelectOption]:

        ret = [p.select_option for p in self.positions]
        
        if exclude:
            ret = [p for p in ret if p.value not in [e.id for e in exclude]]
        elif include:
            ret = [p for p in ret if p.value in [i.id for i in include]]
        
        return ret

################################################################################
    def get_position(self, pos_id: str) -> Optional[Position]:
        """Get a position by its ID.
        
        Parameters:
        -----------
        pos_id : :class:`str`
            The ID of the position to retrieve.
        """
        
        for position in self._positions:
            if position.id == pos_id:
                return position
            
################################################################################
            