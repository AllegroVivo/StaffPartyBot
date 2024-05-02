from __future__ import annotations
import re
from typing import TYPE_CHECKING, TypeVar, List, Type, Optional, Tuple, Any

from discord import Embed, Interaction, EmbedField, SelectOption, Role
from Utilities import log

from UI.Common import ConfirmCancelView
from UI.Positions import (
    PositionStatusView,
    PositionRequirementModal,
    RemoveRequirementView,
    PositionNameModal,
    PositionTrainerPayModal,
    PositionDescriptionModal,
)
from Utilities import Utilities as U, FroggeColor, InvalidSalaryError, MentionableType
from .Requirement import Requirement

if TYPE_CHECKING:
    from Classes import PositionManager, StaffPartyBot
################################################################################

__all__ = ("Position", )

P = TypeVar("P", bound="Position")

################################################################################
class Position:

    __slots__ = (
        "_manager",
        "_id",
        "_name",
        "_requirements",
        "_role",
        "_trainer_pay",
        "_followup",
        "_description",
    )
    
################################################################################
    def __init__(self, mgr: PositionManager, _id: str, name: str, **kwargs) -> None:

        self._manager: PositionManager = mgr
        
        self._id: str = _id
        self._name: str = name
        
        self._requirements: List[Requirement] = kwargs.get("reqs", None) or []
        self._role: Optional[Role] = kwargs.get("role")
        self._trainer_pay: Optional[int] = kwargs.get("trainer_pay")
        self._followup: bool = kwargs.get("followup", False)
        self._description: Optional[str] = kwargs.get("description", None)
        
################################################################################
    @classmethod
    def new(cls: Type[P], mgr: PositionManager, name: str) -> P:

        log.info("Positions", f"Creating new position: {name}")
        
        new_id = mgr.bot.database.insert.position(mgr.guild_id, name)
        return cls(mgr, new_id, name)

################################################################################
    @classmethod
    async def load(
        cls: Type[P], 
        mgr: PositionManager, 
        data: Tuple[Any, ...],
        requirements: List[Tuple[str, int, str, str]]
    ) -> P:

        return cls(
            mgr=mgr, 
            _id=data[0],
            name=data[2], 
            reqs=[Requirement.load(mgr.bot, r) for r in requirements],
            role=await mgr.guild_data.get_or_fetch_role(data[3]),
            trainer_pay=data[4],
            followup=data[5],
            description=data[6]
        ) 
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.position(self)
        
################################################################################    
    @property
    def bot(self) -> StaffPartyBot:

        return self._manager.bot

################################################################################
    @property
    def manager(self) -> PositionManager:
        
        return self._manager
    
################################################################################
    @property
    def id(self) -> str:

        return self._id

################################################################################
    @property
    def name(self) -> str:

        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
            
        self._name = value
        self.update()
        
################################################################################
    @property
    def description(self) -> Optional[str]:
        
        return self._description
    
    @description.setter
    def description(self, value: str) -> None:
        
        self._description = value
        self.update()
        
################################################################################
    @property
    def requirements(self) -> List[Requirement]:
        
        return self._requirements
    
################################################################################
    @property
    def all_requirements(self) -> List[Requirement]:
        
        return self._requirements + self._manager.global_requirements
    
################################################################################
    @property
    def select_option(self) -> SelectOption:
        """Return the position as a select option where label=name & value=id."""

        return SelectOption(label=self.name, value=self.id)

################################################################################
    @property
    def linked_role(self) -> Optional[Role]:
        
        return self._role
    
    @linked_role.setter
    def linked_role(self, role: Role) -> None:
        
        self._role = role
        self.update()
        
################################################################################
    @property
    def trainer_pay(self) -> Optional[int]:
        
        return self._trainer_pay
    
    @trainer_pay.setter
    def trainer_pay(self, value: int) -> None:
        
        self._trainer_pay = value
        self.update()
        
################################################################################
    @property
    def followup_included(self) -> bool:
        
        return self._followup
    
    @followup_included.setter
    def followup_included(self, value: bool) -> None:
        
        self._followup = value
        self.update()
        
################################################################################
    def get_requirement(self, req_id: str) -> Requirement:
        
        log.debug("Positions", f"Getting requirement with ID {req_id}")
        
        for r in self._requirements:
            if r.id == req_id:
                return r
            
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        log.debug("Positions", f"Opening menu for position {self.name}")

        status = self.status()
        view = PositionStatusView(interaction.user, self)

        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    def status(self) -> Embed:

        reqs_list = [r.description for r in self.requirements]
        reqs_list.extend(
            [f"{r.description} - **(Global)**" for r in self._manager.global_requirements]
        )
        field_value = ("* " + "\n* ".join(reqs_list)) if reqs_list else "`Not Set`"
        
        trainer_pay = "`Not Set`"
        if self.trainer_pay is not None:
            trainer_pay = f"{self.trainer_pay:,}"
            if self.followup_included:
                trainer_pay += "\n*(Includes Follow-up/On-Site Assistance)*"

        return U.make_embed(
            title=f"Position Status for: __{self.name}__",
            description=(
                "__**Description**__\n"
                f"{self.description if self.description else '`Not Set`'}\n"
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                EmbedField(
                    name="__Linked Role__",
                    value=(
                        f"{self.linked_role.mention if self.linked_role else '`Not Set`'}"
                    ),
                    inline=True
                ),
                EmbedField(
                    name="__Trainer Pay__",
                    value=trainer_pay,
                    inline=False
                ),
                EmbedField(
                    name="__Training Requirements__",
                    value=field_value,
                    inline=False
                )
            ]
        )
    
################################################################################
    def limited_status(self) -> Embed:
        
        return U.make_embed(
            title=f"Position Description for: __{self.name}__",
            description=self.description if self.description else '`Not Set`'
        )
    
################################################################################
    async def add_requirement(self, interaction: Interaction) -> None:
        
        log.info("Positions", f"Adding requirement to position {self.name}")

        modal = PositionRequirementModal()
    
        await interaction.response.send_modal(modal)
        await modal.wait()
    
        if not modal.complete:
            log.debug("Positions", "Requirement modal was not completed.")
            return
    
        requirement = Requirement.new(self._manager, self.id, modal.value)
        self._requirements.append(requirement)
        
        log.info(
            "Positions",
            f"Requirement {requirement.id} added to position {self.name}"
        )

################################################################################
    async def remove_requirement(self, interaction: Interaction) -> None:
        
        log.info("Positions", f"Removing requirement from position {self.name}")

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
            log.debug("Positions", "Requirement removal was cancelled.")
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
            log.debug("Positions", "Requirement removal was cancelled.")
            return

        requirement = self.get_requirement(view.value)
        requirement.delete()

        self.requirements.remove(requirement)
        
        log.info(
            "Positions",
            f"Requirement {requirement.id} removed from position {self.name}"
        )

################################################################################
    async def edit_name(self, interaction: Interaction) -> None:
        
        log.info("Positions", f"Editing name for position {self.name}")

        modal = PositionNameModal(self.name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            log.debug("Positions", "Name modal was not completed.")
            return

        log.info("Positions", f"Name for position {self.name} updated to {modal.value}")
        
        self.name = modal.value
        
################################################################################
    async def edit_role(self, interaction: Interaction) -> None:
        
        log.info("Positions", f"Editing role for position {self.name}")

        prompt = U.make_embed(
            title="Edit Role",
            description=(
                "**THE BOT IS NOW LISTENING**\n\n"
                
                "Please enter a mention for the role you'd like to link "
                "to this position.\n"
                f"{U.draw_line(extra=25)}\n"
                "*(Type 'Cancel' to cancel this operation.)*"
            )
        )
        
        role = await U.listen_for_mentionable(interaction, prompt, MentionableType.Role)
        if role:
            log.info("Positions", f"Role {role.name} selected for position {self.name}")
            self.linked_role = role
    
################################################################################
    async def set_trainer_pay(self, interaction: Interaction) -> None:
        
        log.info("Positions", f"Setting trainer pay for position {self.name}")

        modal = PositionTrainerPayModal(self.trainer_pay)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            log.debug("Positions", "Trainer pay modal was not completed.")
            return
        
        trainer_pay = U.parse_salary(modal.value)
        if trainer_pay is None:
            log.warning(
                "Positions",
                f"Invalid salary entered for position {self.name}: {modal.value}"
            )
            embed = InvalidSalaryError(modal.value)
            await interaction.respond(embed=embed, ephemeral=True)
            return
        
        self.trainer_pay = trainer_pay
        
        log.info(
            "Positions",
            f"Trainer pay for position {self.name} set to {trainer_pay:,}"
        )
    
################################################################################
    def toggle_followup(self) -> None:
        
        log.info("Positions", f"Toggling follow-up for position {self.name}")
        
        self.followup_included = not self.followup_included
        
################################################################################
    async def set_description(self, interaction: Interaction) -> None:
        
        log.info(
            "Positions",
            f"Setting description for position {self.name}"
        
        )
        
        modal = PositionDescriptionModal(self.description)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            log.debug("Positions", "Description modal was not completed.")
            return
        
        self.description = modal.value
        
        log.info(
            "Positions",
            f"Description for position {self.name} set to {modal.value}"
        )
        
################################################################################
        