from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List, Optional, Dict, Any

from discord import Interaction, EmbedField, Embed, SelectOption
from discord.ext.pages import Page, PageGroup

from UI.Common import ConfirmCancelView, Frogginator
from UI.Positions import GlobalRequirementsView, GlobalRequirementModal, RemoveRequirementView
from Utilities import Utilities as U, PositionExistsError
from Utilities import log
from .Position import Position
from .Requirement import Requirement

if TYPE_CHECKING:
    from Classes import StaffPartyBot, GuildData
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
    async def _load_all(self, data: Dict[str, Any]) -> None:

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
            self._positions.append(await Position.load(self, pos, reqs))
            
################################################################################    
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._guild.bot
    
################################################################################
    @property
    def guild_data(self) -> GuildData:
        
        return self._guild
    
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
    async def _add_position(self, interaction: Interaction, position_name: str) -> Optional[Position]:
        
        log.info("Positions", f"Adding position {position_name}")
        
        prompt = U.make_embed(
            title="Confirm Position Add",
            description=(
                f"Are you sure you want to add the position `{position_name}` to the database?"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Positions", "Position add cancelled.")
            return

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
        
        log.info("Positions", f"Position {position.name} was added successfully.")
        
        # Also update the currently posted SignUpMessage
        await self._guild.training_manager.signup_message.update_components()
        
        return position
        
################################################################################
    async def add_position(self, interaction: Interaction, position_name: str) -> None:
        
        log.info(
            "Positions",
            f"Adding position {position_name} requested by {interaction.user}"
        )
    
        position = self.get_position_by_name(position_name)
        if position is not None:
            log.warning("Positions", f"Position {position_name} already exists.")
            error = PositionExistsError(position_name)
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        position = await self._add_position(interaction, position_name)
        if position is None:
            return
        
        log.info("Positions", f"Position {position_name} added successfully.")
        
        await asyncio.sleep(2)
        await self.position_status(interaction, position.name)
        
################################################################################
    def get_position_by_name(self, pos_name: str) -> Optional[Position]:
        
        log.debug("Positions", f"Searching for position {pos_name}")
        
        for position in self._positions:
            if position.name.lower() == pos_name.lower():
                log.debug("Positions", f"Position {pos_name} found.")
                return position
            
        log.debug("Positions", f"Position {pos_name} not found.")
            
################################################################################
    async def position_status(self, interaction: Interaction, pos_name: str) -> None:
        
        log.info(
            "Positions",
            f"Displaying status of position {pos_name} for {interaction.user}"
        )

        position = self.get_position_by_name(pos_name)
        if position is None:
            log.info("Positions", f"Position {pos_name} not found. Offering to add.")
            position = await self._add_position(interaction, pos_name)
            if position is None:
                log.debug("Positions", "Position add cancelled.")
                return
            else:
                log.info("Positions", f"Position {pos_name} added successfully.")
                await asyncio.sleep(2)
            
        await position.menu(interaction)

################################################################################
    async def global_requirements_menu(self, interaction: Interaction) -> None:
        
        log.info(
            "Positions",
            f"Displaying global position requirements for {interaction.user}"
        )

        status = self.global_requirements_status()
        view = GlobalRequirementsView(interaction.user, self)

        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    def global_requirements_status(self) -> Embed:

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
        
        log.info(
            "Positions",
            f"Adding global job training requirement requested by {interaction.user}"
        )

        modal = GlobalRequirementModal()

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            log.debug("Positions", "Global requirement add cancelled.")
            return

        requirement = Requirement.new(self, "0", modal.value)
        self._requirements.append(requirement)
        
        log.info("Positions", f"Global requirement '{modal.value}' added successfully.")

################################################################################
    async def remove_global_requirement(self, interaction: Interaction) -> None:
        
        log.info(
            "Positions",
            f"Removing global job training requirement requested by {interaction.user}"
        )

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
            log.debug("Positions", "Global requirement removal cancelled.")
            return

        requirement = self.get_global_requirement(view.value)
        requirement.delete()
        
        log.info("Positions", f"Global requirement '{requirement.description}' removed successfully.")

        self._requirements.remove(requirement)

################################################################################
    def get_global_requirement(self, req_id: str) -> Requirement:
        
        log.debug("Positions", f"Searching for global requirement {req_id}")
        
        for req in self._requirements:
            if req.id == req_id:
                log.debug("Positions", f"Global requirement {req_id} found.")
                return req
            
        log.debug("Positions", f"Global requirement {req_id} not found.")

################################################################################
    def select_options(
        self,
        *,
        exclude: List[Position] = None, 
        include: List[Position] = None
    ) -> List[SelectOption]:
        
        log.debug(
            "Positions",
            f"Building select options for positions (exclude={exclude}, include={include})"
        )

        ret = [p.select_option for p in self.positions]
        
        if exclude:
            ret = [p for p in ret if p.value not in [e.id for e in exclude]]
        elif include:
            ret = [p for p in ret if p.value in [i.id for i in include]]
        
        return ret

################################################################################
    def get_position(self, pos_id: str) -> Optional[Position]:
        
        log.debug("Positions", f"Searching for position {pos_id}")
        
        for position in self._positions:
            if position.id == pos_id:
                log.debug("Positions", f"Position {pos_id} found.")
                return position
            
        log.debug("Positions", f"Position {pos_id} not found.")
            
################################################################################
    async def positions_report(self, interaction: Interaction) -> None:
        
        log.debug("Positions", "Displaying all positions report")
        
        embed = U.make_embed(
            title="All Positions",
            description=("* " + "\n* ".join([f"`{p.name}`" for p in self.positions]))
        )
        await interaction.respond(embed=embed)
        
################################################################################
    async def trainer_pos_report(self, interaction: Interaction) -> None:
        
        log.debug("Positions", "Displaying trainer positions report")
        
        page_groups = [
            PageGroup(label=pos.name, pages=[Page(embeds=[pos.status()])])
            for pos in self.positions
        ]
        
        frogginator = Frogginator(
            pages=page_groups,
            show_menu=True,
            menu_placeholder="Select a position to view details...",
        )
        await frogginator.respond(interaction)
        
################################################################################
    async def trainee_pos_report(self, interaction: Interaction) -> None:
        
        log.debug("Positions", "Displaying trainee positions report")
        
        page_groups = [
            PageGroup(label=pos.name, pages=[Page(embeds=[pos.limited_status()])])
            for pos in self.positions
        ]
        
        frogginator = Frogginator(
            pages=page_groups,
            show_menu=True,
            menu_placeholder="Select a position to view details...",
        )
        await frogginator.respond(interaction)
        
################################################################################
