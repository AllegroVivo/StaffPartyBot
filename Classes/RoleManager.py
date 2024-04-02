from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

from discord import Interaction, Role, Embed, EmbedField, User, Member, Forbidden

from UI.Guild import RolesStatusView
from Utilities import Utilities as U, RoleType, FroggeColor

if TYPE_CHECKING:
    from Classes import GuildData, TrainingBot
################################################################################

__all__ = ("RoleManager",)

################################################################################
class RoleManager:

    __slots__ = (
        "_guild",
        "_trainer_main",
        "_trainer_pending",
        "_trainer_hiatus",
        "_staff_main",
        "_staff_unvalidated"
    )

################################################################################
    def __init__(self, guild: GuildData):

        self._guild: GuildData = guild
        
        self._trainer_main: Optional[Role] = None
        self._trainer_pending: Optional[Role] = None
        self._trainer_hiatus: Optional[Role] = None
        self._staff_main: Optional[Role] = None
        self._staff_unvalidated: Optional[Role] = None
    
################################################################################
    async def _load_all(self, data: Tuple[Any, ...]) -> None:
        
        guild = self._guild._parent
        
        self._trainer_main = guild.get_role(data[1]) if data[1] else None
        self._trainer_pending = guild.get_role(data[2]) if data[2] else None
        self._trainer_hiatus = guild.get_role(data[3]) if data[3] else None
        self._staff_main = guild.get_role(data[4]) if data[4] else None
        self._staff_unvalidated = guild.get_role(data[5]) if data[5] else None
        
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._guild.bot
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._guild._parent.id
    
################################################################################
    @property
    def trainer_main(self) -> Optional[Role]:
        
        return self._trainer_main
    
    @trainer_main.setter
    def trainer_main(self, role: Optional[Role]) -> None:
        
        self._trainer_main = role
        self.update()
      
################################################################################
    @property
    def trainer_pending(self) -> Optional[Role]:
        
        return self._trainer_pending
    
    @trainer_pending.setter
    def trainer_pending(self, role: Optional[Role]) -> None:
        
        self._trainer_pending = role
        self.update()
        
################################################################################
    @property
    def trainer_hiatus(self) -> Optional[Role]:
        
        return self._trainer_hiatus
    
    @trainer_hiatus.setter
    def trainer_hiatus(self, role: Optional[Role]) -> None:
        
        self._trainer_hiatus = role
        self.update()
        
################################################################################
    @property
    def staff_main(self) -> Optional[Role]:
        
        return self._staff_main
    
    @staff_main.setter
    def staff_main(self, role: Optional[Role]) -> None:
        
        self._staff_main = role
        self.update()
        
################################################################################
    @property
    def staff_unvalidated(self) -> Optional[Role]:
        
        return self._staff_unvalidated
    
    @staff_unvalidated.setter
    def staff_unvalidated(self, role: Optional[Role]) -> None:
        
        self._staff_unvalidated = role
        self.update()
        
################################################################################
    def update(self) -> None:
    
        self.bot.database.update.roles(self)
        
################################################################################
    def status(self) -> Embed:

        fields = [
            EmbedField(
                name="__Trainer__",
                value=self._trainer_main.mention if self._trainer_main else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Trainer Pending__",
                value=self._trainer_pending.mention if self._trainer_pending else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Trainer Hiatus__",
                value=self._trainer_hiatus.mention if self._trainer_hiatus else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Staff__",
                value=self._staff_main.mention if self._staff_main else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Staff Unvalidated__",
                value=self._staff_unvalidated.mention if self._staff_unvalidated else "`Not Set`",
                inline=False
            )
        ]

        return U.make_embed(
            title="TrainerBot Roles Status",
            description=U.draw_line(extra=25),
            fields=fields
        )
        
################################################################################
    async def roles_menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = RolesStatusView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
################################################################################
    async def set_role(self, interaction: Interaction, _type: RoleType) -> None:

        prompt = U.make_embed(
            title="Edit Role",
            description=(
                "**THE BOT IS NOW LISTENING**\n\n"

                "Please enter a mention for the role you'd like to link.\n"
                f"{U.draw_line(extra=25)}\n"
                "*(Type 'Cancel' to cancel this operation.)*"
            )
        )

        response = await interaction.respond(embed=prompt)

        def check(m):
            return m.author == interaction.user

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
            if not results:
                await interaction.respond(embed=error)
                return
            
            role_id = int(results.group(1))
            role = await self._guild.parent._fetch_role(role_id)
            if not role:
                await interaction.respond(embed=error)
                return                

            match _type:
                case RoleType.TrainerMain:
                    self.trainer_main = role
                case RoleType.TrainerPending:
                    self.trainer_pending = role
                case RoleType.TrainerHiatus:
                    self.trainer_hiatus = role
                case RoleType.StaffMain:
                    self.staff_main = role
                case RoleType.StaffNotValidated:
                    self.staff_unvalidated = role

        await message.delete()
        await response.delete_original_response()
        
################################################################################
    async def add_role(self, user: Union[Member, User], _type: RoleType) -> None:
        
        if isinstance(user, User):
            user = await self._guild.parent.fetch_member(user.id)

        match _type:
            case RoleType.TrainerMain:
                role = self.trainer_main
            case RoleType.TrainerPending:
                role = self.trainer_pending
            case RoleType.TrainerHiatus:
                role = self.trainer_hiatus
            case RoleType.StaffMain:
                role = self.staff_main
            case RoleType.StaffNotValidated:
                role = self.staff_unvalidated
            case _:
                raise ValueError(f"Invalid RoleType: {_type}")

        if role not in user.roles:
            try:
                await user.add_roles(role)
            except:
                pass
            
################################################################################
    async def remove_role(self, user: Union[Member, User], _type: RoleType) -> None:

        if isinstance(user, User):
            user = await self._guild.parent.fetch_member(user.id)
            
        match _type:
            case RoleType.TrainerMain:
                role = self.trainer_main
            case RoleType.TrainerPending:
                role = self.trainer_pending
            case RoleType.TrainerHiatus:
                role = self.trainer_hiatus
            case RoleType.StaffMain:
                role = self.staff_main
            case RoleType.StaffNotValidated:
                role = self.staff_unvalidated
            case _:
                raise ValueError(f"Invalid RoleType: {_type}")

        if role in user.roles:
            try:
                await user.remove_roles(role)
            except:
                pass
            
################################################################################