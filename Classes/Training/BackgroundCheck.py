from __future__ import annotations

from typing import TYPE_CHECKING, List, Type, TypeVar, Any, Tuple

from discord import Interaction, Embed, EmbedField

from Assets import BotEmojis
from UI.Common import ConfirmCancelView
from UI.Training import (
    BGCheckNamesModal,
    BGCheckMenuView,
    BGCheckVenueModal,
    BGCheckRemoveVenueView, 
    DataCenterWorldSelectView
)
from Utilities import (
    Utilities as U,
    DataCenter,
    InvalidWorldNameError,
    GameWorld,
    MissingNameError,
    RoleType,
    edit_message_helper,
    ExperienceExistsError,
)
from .BGCheckVenue import BGCheckVenue

if TYPE_CHECKING:
    from Classes import Position, TrainingBot, TUser
################################################################################

__all__ = ("BackgroundCheck",)

BC = TypeVar("BC", bound="BackgroundCheck")

################################################################################
class BackgroundCheck:

    __slots__ = (
        "_parent",
        "_agree",
        "_names",
        "_venues",
        "_positions",
        "_approved",
        "_is_trainer",
        "_prev_exp",
    )

################################################################################
    def __init__(self, parent: TUser, **kwargs) -> None:

        self._parent: TUser = parent
        
        self._agree: bool = kwargs.get("agree", False)
        self._names: List[str] = kwargs.get("names", [])
        self._venues: List[BGCheckVenue] = kwargs.get("venues", [])
        self._positions: List[str] = kwargs.get("positions", [])
        
        self._is_trainer: bool = kwargs.get("is_trainer", False)
        self._prev_exp: bool = kwargs.get("prev_exp", False)
        
        self._approved: bool = kwargs.get("approved", False)

################################################################################
    @classmethod
    def load(cls: Type[BC], parent: TUser, data: Tuple[Any, ...]) -> BC:
        
        return cls(
            parent=parent,
            agree=data[1],
            names=data[2] if data[2] is not None else [],
            venues=(
                [BGCheckVenue.from_db_string(v) for v in data[3]] 
                if data[3] is not None else []
            ),
            positions=data[4] if data[4] is not None else [],
            approved=data[5],
            is_trainer=data[7],
            prev_exp=data[8]
        )
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._parent.bot
    
################################################################################
    @property
    def user_id(self) -> int:
        
        return self._parent.user_id
    
################################################################################
    @property
    def parent(self) -> TUser:
        
        return self._parent
    
################################################################################
    @property
    def agree(self) -> bool:
        
        return self._agree
    
    @agree.setter
    def agree(self, value: bool) -> None:
        
        self._agree = value
        self.update()
        
################################################################################
    @property
    def names(self) -> List[str]:
        
        return self._names
    
    @names.setter
    def names(self, value: List[str]) -> None:
        
        self._names = value
        self.update()
        
################################################################################
    @property
    def venues(self) -> List[BGCheckVenue]:
        
        return self._venues
        
################################################################################
    @property
    def positions(self) -> List[str]:
        
        return self._positions
        
################################################################################
    @property
    def approved(self) -> bool:
        
        return self._approved
    
    @approved.setter
    def approved(self, value: bool) -> None:
        
        self._approved = value
        self.update()
        
################################################################################
    @property
    def is_trainer(self) -> bool:
        
        return self._is_trainer
    
################################################################################
    @property
    def want_to_train(self) -> bool:
        
        return self._prev_exp
    
    @want_to_train.setter
    def want_to_train(self, value: bool) -> None:
            
        self._prev_exp = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.background_check(self)
        
################################################################################
    def status(self) -> Embed:

        fields = [
            EmbedField(
                name="__Character Names__",
                value="* " + (
                    "\n* ".join([f"`{n}`" for n in self.names])
                    if self.names else "`No Names Provided`"
                ),
                inline=True
            ),
            EmbedField(
                name="__Want to Train__",
                value=(
                    str(BotEmojis.Check) if self._prev_exp
                    else str(BotEmojis.Cross)
                ),
                inline=True
            ),
            EmbedField(
                name="__Previous Venues__",
                value="* " + (
                    "\n* ".join([v.format() for v in self.venues])
                    if self.venues else "`No Venue Information Provided`"
                ),
                inline=False
            )
        ]

        return U.make_embed(
            title="Background Check",
            description=(
                "__**Please read, and either agree or disagree to the "
                "following:**__\n"
                "*I confirm that the information I provide in this background\n"
                "check is true and I also provide consent to the employees\n"
                "of the Staff Party Bus to contact and verify my references.*\n\n"
                
                "Please note that it is __**OKAY**__ to disagree with the above\n"
                "statement. If you do, a staff member will contact you shortly."
                
            ) + f"\n{U.draw_line(extra=36)}",
            fields=fields
        )
        
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = BGCheckMenuView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
################################################################################
    async def set_names(self, interaction: Interaction) -> None:
        
        modal = BGCheckNamesModal(self.names)

        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.names = modal.value
        
################################################################################
    async def add_venue_experience(self, interaction: Interaction) -> None:
        
        if len(self.venues) >= 3:
            prompt = U.make_embed(
                title="Maximum Venues Reached",
                description=(
                    "You can only add up to 3 venues to your background check."
                )
            )
            await interaction.respond(embed=prompt, ephemeral=True)
            return

        modal = BGCheckVenueModal()
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        name, jobs = modal.value
        
        prompt = U.make_embed(
            title="Select Data Center & World",
            description=(
                "Please select the data center and world where this venue "
                "was located"
            )
        )
        view = DataCenterWorldSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return

        data_center, world = view.value
        
        matching_venues = [v for v in self.venues if v.name.lower() == name.lower()]
        if matching_venues:
            error = ExperienceExistsError(name)
            await interaction.respond(embed=error, ephemeral=True)
            return

        self._venues.append(BGCheckVenue(name, data_center, world, jobs))
        self.update()
        
################################################################################
    async def remove_venue_experience(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Remove Venue Experience",
            description=(
                "Please select the venue experience you'd like to remove."
            )
        )
        view = BGCheckRemoveVenueView(interaction.user, self)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        for i, venue in enumerate(self._venues):
            if venue.name == view.value:
                self._venues.pop(i)
                
        self.update()
    
################################################################################
    async def submit(self, interaction: Interaction, agreed: bool) -> None:
        
        if not self.names:
            error = MissingNameError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        word = "AGREE" if agreed else "DISAGREE"
        prompt = U.make_embed(
            title="Submit and Agree",
            description=(
                "Are you sure you want to submit your background check\n"
                f"and __**{word}**__ to the above-mentioned terms?"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.agree = agreed
        
        await self.parent.guild.log.bg_check_submitted(self)
        
        if agreed:
            description = (
                "Your background check has been submitted!\n"
                "You will receive a DM from the bot letting you "
                "know when you've been approved."
            )
        else:
            description = (
                "Your background check has been submitted.\n"
                "You will be contacted by a staff member shortly."
            )
        
        confirm = U.make_embed(
            title="Background Check Submitted",
            description=description,
            timestamp=True
        )
        
        await edit_message_helper(interaction, embed=confirm, view=None)
        
################################################################################
    async def approve(self) -> None:
        
        if self.approved:
            return
        
        await self.parent.guild.role_manager.add_role(self.parent.user, RoleType.StaffMain)
        await self.parent.guild.role_manager.remove_role(self.parent.user, RoleType.StaffNotValidated)
        
        self.approved = True
        # 
        # confirm = U.make_embed(
        #     title="User Approved",
        #     description=(
        #         "This user has been approved and can now access the server."
        #     )
        # )
        # await interaction.respond(embed=confirm, ephemeral=True)
        
        user_confirm = U.make_embed(
            title="Approved",
            description=(
                "Your background check has been approved!\n"
                "You now have access to the server."
            )
        )
        try:
            await self.parent.user.send(embed=user_confirm)
        except:
            pass
        
        await self.parent.guild.log.bg_check_approved(self)
        
################################################################################
    def toggle_previously_trained(self) -> None:
        
        self.want_to_train = not self.want_to_train
        
################################################################################
