from __future__ import annotations
import re
from typing import TYPE_CHECKING, TypeVar, List, Type, Optional, Tuple, Any

from discord import Embed, Interaction, EmbedField, SelectOption, Role

from UI.Common import ConfirmCancelView, CloseMessageView
from UI.Positions import (
    PositionStatusView,
    PositionRequirementModal,
    RemoveRequirementView,
    PositionNameModal,
    PositionTrainerPayModal,
)
from Utilities import Utilities as U, FroggeColor, InvalidSalaryError
from .Requirement import Requirement

if TYPE_CHECKING:
    from Classes import PositionManager, TrainingBot
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
        
################################################################################
    @classmethod
    def new(cls: Type[P], mgr: PositionManager, name: str) -> P:

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

        role = (
            await mgr.guild_data.parent._fetch_role(data[3])
            if data[3] is not None
            else None
        )
        reqs = [Requirement.load(mgr.bot, r) for r in requirements]
        
        return cls(
            mgr=mgr, 
            _id=data[0],
            name=data[2], 
            reqs=reqs,
            role=role,
            trainer_pay=data[4],
            followup=data[5]
        ) 
    
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.position(self)
        
################################################################################    
    @property
    def bot(self) -> TrainingBot:

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
        
        for r in self._requirements:
            if r.id == req_id:
                return r
            
################################################################################
    async def menu(self, interaction: Interaction) -> None:

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
            title=f"Position Status for: {self.name}",
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
    async def add_requirement(self, interaction: Interaction) -> None:

        modal = PositionRequirementModal()
    
        await interaction.response.send_modal(modal)
        await modal.wait()
    
        if not modal.complete:
            return
    
        self._requirements.append(Requirement.new(self._manager, self.id, modal.value))

################################################################################
    async def remove_requirement(self, interaction: Interaction) -> None:

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

        modal = PositionNameModal(self.name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value

################################################################################
    async def edit_role(self, interaction: Interaction) -> None:

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
        
        response = await interaction.respond(embed=prompt)

        def check(m):
            if m.author != interaction.user:
                return False
            if not re.match(r"<@&(\d+)>", m.content):
                if m.content.lower() == "cancel":
                    return True
                return False
            return True

        try:
            message = await self.bot.wait_for("message", check=check, timeout=180)
        except TimeoutError:
            embed = U.make_embed(
                title="Timeout",
                description=(
                    "You took too long to respond. Please try again."
                ),
                color=FroggeColor.brand_red()
            )
            await response.respond(embed=embed)
            return

        error = U.make_embed(
            title="Invalid Role Mention",
            description=(
                "You did not provide a valid role mention. "
                "Please try again."
            ),
            color=FroggeColor.brand_red()
        )

        if message.content.lower() != "cancel":
            results = re.match(r"<@&(\d+)>", message.content)
            if results:
                role_id = int(results.group(1))
                role = await self._manager.guild_data.parent._fetch_role(role_id)
                if role:
                    self.linked_role = role
                else:
                    await interaction.respond(embed=error, ephemeral=True)
                    return
            else:
                await interaction.respond(embed=error, ephemeral=True)
                return

        await message.delete()
        await response.delete_original_response()
    
################################################################################
    async def set_trainer_pay(self, interaction: Interaction) -> None:

        modal = PositionTrainerPayModal(self.trainer_pay)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        trainer_pay = U.parse_salary(modal.value)
        if trainer_pay is None:
            embed = InvalidSalaryError(modal.value)
            await interaction.respond(embed=embed, ephemeral=True)
            return
        
        self.trainer_pay = trainer_pay
    
################################################################################
    def toggle_followup(self) -> None:
        
        self.followup_included = not self.followup_included
        
################################################################################
