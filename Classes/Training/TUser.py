from __future__ import annotations

from datetime import datetime, time
from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Any, Dict, Tuple, Union

import pytz
from discord import User, Embed, EmbedField, Interaction, SelectOption, Member, Forbidden
from discord.ext.pages import Page

from Assets import BotEmojis
from UI.Common import ConfirmCancelView, Frogginator
from UI.Training import (
    AddTrainingView,
    AddQualificationView,
    WeekdayTZSelectView,
    TimeSelectView,
    ModifyQualificationView,
    RemoveQualificationView,
    RemoveTrainingView,
    ManageTrainingsView,
    DecoupleTrainingSelectView,
)
from Utilities import (
    Utilities as U,
    TrainingLevel,
    GlobalDataCenter,
    log,
    Weekday,
    RoleType,
    DTOperations,
    PayAlreadyRequestedError
)
from .BackgroundCheck import BackgroundCheck
from .Qualification import Qualification
from .TAvailability import TAvailability
from .Training import Training
from .UserConfig import UserConfiguration
from .UserDetails import UserDetails

if TYPE_CHECKING:
    from Classes import (
        StaffPartyBot,
        TrainingManager,
        PositionManager,
        GuildData,
        Position,
        JobPosting,
        Profile,
        Venue,
        GroupTraining
    )
################################################################################

__all__ = ("TUser",)

TU = TypeVar("TU", bound="TUser")

################################################################################
class TUser:

    __slots__ = (
        "_manager",
        "_user",
        "_availability",
        "_config",
        "_qualifications",
        "_hiatus",
        "_details",
        "_bg_check",
        "_mutes",
        "_pay_requested",
    )

################################################################################
    def __init__(
        self,
        mgr: TrainingManager,
        user: User,
        details: Optional[UserDetails] = None,
        availabilities: Optional[List[TAvailability]] = None,
        configuration: Optional[UserConfiguration] = None,
        qualifications: Optional[List[Qualification]] = None,
        bg_check: Optional[BackgroundCheck] = None,
        mutes: Optional[List[Venue]] = None
    ) -> None:

        self._manager: TrainingManager = mgr

        self._user: User = user

        self._details: UserDetails = details or UserDetails(self)
        self._config: UserConfiguration = configuration or UserConfiguration(self)
        self._availability: List[TAvailability] = availabilities or []
        self._qualifications: List[Qualification] = qualifications or []
        self._bg_check: BackgroundCheck = bg_check or BackgroundCheck(self)
        self._mutes: List[Venue] = mutes or []
        
        self._pay_requested = False

################################################################################
    @classmethod
    def new(cls: Type[TU], manager: TrainingManager, user: Union[Member, User]) -> TU:
        
        if not isinstance(user, Member):
            user = manager.guild.parent.get_member(user.id)
        is_trainer = manager.guild.role_manager.trainer_pending in user.roles
        manager.bot.database.insert.tuser(manager.guild_id, user.id, is_trainer)

        self: TU = cls.__new__(cls)

        self._manager = manager
        self._user = user

        self._details = UserDetails(self)
        self._config = UserConfiguration(self)
        self._availability = []
        self._qualifications = []
        self._bg_check = BackgroundCheck(self)
        self._mutes = []
        
        self._pay_requested = False

        return self

################################################################################
    @classmethod
    async def load(cls: Type[TU], mgr: TrainingManager, user: User, data: Dict[str, Any]) -> Optional[TU]:

        tuser = data["tuser"]

        self: TU = cls.__new__(cls)

        self._manager = mgr
        self._user = user

        self._details = UserDetails.load(self, tuser[3:8])
        self._config = UserConfiguration.load(self, tuser[8:10])
        self._availability = [TAvailability.load(self, a) for a in data["availability"]]
        self._qualifications = [Qualification.load(self, q) for q in data["qualifications"]]
        
        self._bg_check = await BackgroundCheck.load(self, data["bg_check"])
        self._mutes = [
            mgr.guild.venue_manager.get_venue(venue_id)
            for venue_id in tuser[2]
        ] if tuser[2] is not None else []
        
        self._pay_requested = False

        return self

################################################################################
    def __eq__(self, other: TUser) -> bool:
        
        if other is None:
            return False
        
        return self.user == other.user
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._manager.bot

################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._manager.guild
     
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self.guild.guild_id
    
################################################################################
    @property
    def user(self) -> User:

        return self._user

################################################################################
    @property
    def user_id(self) -> int:

        return self._user.id

################################################################################
    @property
    def image(self) -> Optional[str]:

        return self._config.image

################################################################################
    @property
    def config(self) -> UserConfiguration:

        return self._config

################################################################################
    @property
    def name(self) -> str:

        return self._details.name

################################################################################ 
    @property
    def notes(self) -> Optional[str]:

        return self._details.notes

################################################################################
    @property
    def data_centers(self) -> List[GlobalDataCenter]:
        
        return self._details.data_centers
    
################################################################################    
    @property
    def qualifications(self) -> List[Qualification]:

        self._qualifications.sort(key=lambda q: q.position.name)
        return self._qualifications

################################################################################
    @property
    def is_trainer(self) -> bool:
        
        return len(self.qualifications) > 0
    
################################################################################
    @property
    def qualified_positions(self) -> List[Position]:

        return [q.position for q in self.qualifications if q.level == TrainingLevel.Active]
    
################################################################################
    @property
    def availability(self) -> List[TAvailability]:

        self._availability.sort(key=lambda a: a.day.value)
        return self._availability

################################################################################
    @property
    def trainings_as_trainee(self) -> List[Training]:

        ret = [t for t in self.training_manager.all_trainings if t.trainee == self]
        ret.sort(key=lambda t: t.position.name)
        return ret

################################################################################
    @property
    def trainings_as_trainer(self) -> List[Training]:
        
        ret = [t for t in self.training_manager.all_trainings if t.trainer == self]
        ret.sort(key=lambda t: t.position.name)
        return ret
    
################################################################################
    @property
    def unpaid_trainings(self) -> List[Training]:

        return [
            t for t in self.trainings_as_trainer if (
                t.is_complete and not t.trainer_paid
            )
        ]
    
################################################################################
    @property   
    def unsettled_groups(self) -> List[GroupTraining]:
            
        return [gt for gt in self._manager.unpaid_groups if gt.trainer == self]
    
################################################################################
    @property
    def unmatched_trainings(self) -> List[Training]:
        
        return [t for t in self._manager.unmatched_trainings if t.trainee == self]
    
################################################################################    
    @property
    def position_manager(self) -> PositionManager:
        
        return self._manager.guild.position_manager
    
################################################################################
    @property
    def training_manager(self) -> TrainingManager:
        
        return self._manager
    
################################################################################
    @property
    def on_hiatus(self) -> bool:
        
        return self._details.hiatus
    
################################################################################
    @property
    def bg_check(self) -> BackgroundCheck:
        
        return self._bg_check
    
################################################################################
    @property
    def profile(self) -> Profile:
        
        return self.guild.profile_manager[self.user_id]
    
################################################################################
    @property
    def muted_venues(self) -> List[Venue]:
        
        return self._mutes
    
################################################################################
    def is_qualified(self, position_id: str) -> bool:
        
        return any(q.position.id == position_id for q in self.qualifications)
    
################################################################################
    def admin_status(self) -> Embed:

        return U.make_embed(
            title=f"User Status for: __{self.name}__",
            description=(
                f"{U.draw_line(extra=30)}"
            ),
            fields=[
                self._qualifications_field(),
                self._training_requested_field(),
                self._availability_field(False),
                self._dc_field(),
                self._notes_field(),
                EmbedField(
                    name="__Unsettled Wages__",
                    value=(
                        f"`{self.unsettled_wages():,} gil`"
                        if self.unsettled_wages() > 0
                        else "`None`"
                    ),
                    inline=True
                )
            ]
        )

################################################################################
    def _qualifications_field(self) -> EmbedField:

        value = "`None`" if not self.qualifications else ""
        
        for q in self.qualifications:
            level = "On Hiatus" if self.on_hiatus else q.level.proper_name
            value += f"* {q.position.name} -- *({level})*\n"
        
        return EmbedField(
            name="__Trainer Qualifications__",
            value=value,
            inline=True
        )

################################################################################
    def _training_requested_field(self) -> EmbedField:

        trainings = [t for t in self.trainings_as_trainee if not t.is_complete]
        training_str = "`None`" if not trainings else ""

        if training_str == "":
            for t in trainings:
                training_str += f"* {t.position.name}\n-- Trainer: "
                if t.trainee.on_hiatus:
                    training_str += "On Hiatus\n"
                else:
                    training_str += f"`{t.trainer.name}`\n" if t.trainer else "None... (Yet!)\n"

        return EmbedField(
            name="__Trainings Requested__",
            value=training_str,
            inline=True
        )

################################################################################
    def _availability_field(self, inline: bool) -> EmbedField:

        return EmbedField(
            name="__Availability__",
            value=TAvailability.availability_status(self.availability),
            inline=inline
        )

################################################################################
    def _notes_field(self) -> EmbedField:

        return EmbedField(
            name="__Internal Notes__",
            value=self.notes if self.notes else "`None`",
            inline=False
        )

################################################################################
    def _dc_field(self) -> EmbedField:

        return EmbedField(
            name="__Data Center(s)__",
            value=(
                ( "`" + ", ".join([dc.proper_name for dc in self.data_centers]) + "`")
                if len(self.data_centers) > 0
                else "`Not Set`"
            ),
            inline=False
        )

################################################################################
    def _bot_pings_field(self) -> EmbedField:
        
        return EmbedField(
            name="__New Trainee Pings__",
            value=(
                str(BotEmojis.Check 
                    if (self.config.trainee_pings and not self.on_hiatus) 
                    else BotEmojis.Cross)
                + "\n" +
                "*(If this is enabled, the\n"
                "bot will send you a DM\n"
                "if a new trainee signs up\n"
                "for training in a job you\n"
                "are qualified for.)*"
            ),
            inline=True
        )
    
################################################################################
    def user_status(self) -> Embed:

        fields = [
            self._training_requested_field(),
            EmbedField("** **", "** **", inline=False),
            self._availability_field(True),
            self._dc_field(),
        ]
        
        if len(self.qualifications) > 0:
            fields.insert(1, self._qualifications_field())
            fields.insert(4, self._bot_pings_field())
            fields.append(
                EmbedField(
                    name="__Unsettled Wages__",
                    value=(
                        f"`{self.unsettled_wages():,} gil`" 
                        if self.unsettled_wages() > 0 
                        else "`None`"
                    ),
                    inline=True
                )
            )

        return U.make_embed(
            title=f"User Status for: __{self.name}__",
            description=(
                f"({self.user.display_name})\n"
                f"({self.user.mention})\n"
                f"{U.draw_line(text=str(self.user.mention), extra=3)}"
            ),
            fields=fields,
        )

################################################################################
    def unsettled_wages(self) -> int:

        return sum(
            [
                p.position.trainer_pay
                for p in self.unpaid_trainings
                if p
            ] +
            [
                gt.trainer_pay
                for gt in self._manager.unpaid_groups
                if gt
            ]
        )
    
################################################################################    
    async def set_name(self, interaction: Interaction) -> None:

        await self._details.set_name(interaction)

################################################################################
    async def set_notes(self, interaction: Interaction) -> None:

        await self._details.set_notes(interaction)

################################################################################
    async def set_data_centers(self, interaction: Interaction) -> None:

        await self._details.set_data_centers(interaction)
        
################################################################################
    async def set_availability(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is setting availability."
        )

        result = await DTOperations.collect_availability(interaction)
        if result is None:
            return

        tz, weekday, start_time, end_time = result

        for i, a in enumerate(self.availability):
            if a.day == weekday:
                self._availability.pop(i).delete()

        if start_time is not None:
            availability = TAvailability.new(self, weekday, start_time, end_time)
            self._availability.append(availability)

        await self._manager.notify_of_availability_change(self)
        
        log.info("Training", f"Availability setup complete for {weekday.proper_name}.")

################################################################################
    async def add_qualification(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is adding a qualification."
        )
        
        if not self._details.guidelines_accepted:
            if not await self._details.accept_guidelines(interaction):
                return

        embed = U.make_embed(
            title="Add Qualification",
            description=(
                "Select the position you would like to add a qualification\n"
                "for. Subsequently, a second selector will appear to\n"
                "allow you to select the new qualification level.\n"
                f"{U.draw_line(extra=25)}"
            )
        )

        base_options = self.position_manager.select_options()
        options = [
            o for o in base_options
            if o.value not in [q.position.id for q in self._qualifications]
        ]

        view = AddQualificationView(interaction.user, options)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Qualification setup cancelled.")
            return

        positions = [self.position_manager.get_position(pos_id) for pos_id in view.value[0]]
        level = TrainingLevel(int(view.value[1]))
        
        log.info(
            "Training",
            f"Qualification setup for {', '.join([p.name for p in positions])}."
        )

        for position in positions:
            qualification = Qualification.new(self.training_manager, self.user, position, level)
            self._qualifications.append(qualification)

################################################################################
    async def modify_qualification(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is modifying a qualification."
        )

        embed = U.make_embed(
            title="Modify Qualification",
            description=(
                "Select the position you would like to modify a qualification\n"
                "for. Subsequently, a second selector will appear to\n"
                "allow you to select the individual qualification(s) to modify.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = ModifyQualificationView(interaction.user, self.qualification_options())

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Qualification setup cancelled.")
            return

        positions = [self.position_manager.get_position(pos_id) for pos_id in view.value[0]]
        
        log.info(
            "Training",
            f"Qualification modification for {', '.join([p.name for p in positions])}."
        )
        
        for pos in positions:
            qualification = self.get_qualification(pos.id)
            qualification.update(TrainingLevel(int(view.value[1])))

################################################################################
    def qualification_options(self) -> List[SelectOption]:

        options = []

        for q in self._qualifications:
            options.append(
                SelectOption(
                    label=q.position.name,
                    value=q.position.id
                )
            )

        return options

################################################################################
    def get_qualification(self, position_id: str) -> Optional[Qualification]:

        for q in self._qualifications:
            if q.position.id == position_id:
                return q

################################################################################
    async def remove_qualification(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is removing a qualification."
        )

        embed = U.make_embed(
            title="Remove Qualification",
            description=(
                "Select the position you would like to remove a qualification\n"
                "for. Subsequently, a second selector will appear to\n"
                "allow you to select the individual qualification to remove.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = RemoveQualificationView(interaction.user, self.qualification_options())

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Qualification removal cancelled.")
            return

        qualifications = [self.get_qualification(q_id) for q_id in view.value]
        fields = [
            EmbedField(
                name="__Qualifications Pending Removal__",
                value="\n".join([f"* {q.position.name}" for q in qualifications]),
                inline=False
            )
        ]
        
        log.info(
            "Training",
            f"Qualification removal for {', '.join([q.position.name for q in qualifications])}."
        )

        confirm = U.make_embed(
            title="Remove Qualification(s)",
            description=(
                f"Are you sure you want to remove the following\n"
                f"qualification(s) from {self.name}?\n"
                f"{U.draw_line(extra=25)}"
            ),
            fields=fields
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Qualification removal cancelled.")
            return

        for qualification in qualifications:
            qualification.delete()
            self._qualifications.remove(qualification)
            
        log.info("Training", "Qualification removal complete.")

################################################################################
    async def add_training(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is adding a training."
        )

        embed = U.make_embed(
            title="Add Training",
            description=(
                "Please select a training to add.\n"
                f"{U.draw_line(extra=25)}"
            ),
        )

        base_options = self.position_manager.select_options(
            exclude=[q.position for q in self.qualifications]
        )
        options = [
            o for o in base_options
            if o.value not in [t.position.id for t in self.trainings_as_trainee]
        ]

        view = AddTrainingView(interaction.user, options)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Training setup cancelled.")
            return
        
        msg = await interaction.respond("Adding training(s)... Please Wait...")

        for pos_id in view.value:
            await self.training_manager.add_training(Training.new(self, pos_id))
            
        log.info("Training", "Training setup complete.")
            
        await msg.delete()

################################################################################
    async def remove_training(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is removing a training."
        )

        embed = U.make_embed(
            title="Remove Training",
            description=(
                "Please select a training to remove.\n"
                f"{U.draw_line(extra=25)}"
            ),
        )
        view = RemoveTrainingView(interaction.user, self.training_select_options())

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Training removal cancelled.")
            return
        
        ids_to_remove = view.value
        
        log.info(
            "Training",
            f"Training removal for {', '.join(ids_to_remove)}."
        )

        confirm = U.make_embed(
            title="Confirm Removal",
            description=(
                "Are you sure you want to remove the selected training(s)?\n"
                f"{U.draw_line(extra=28)}"
            ),
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Training removal cancelled.")
            return

        for _id in ids_to_remove:
            await self.training_manager.remove_training(_id)
            
        log.info("Training", "Training removal complete.")

################################################################################
    def training_select_options(self) -> List[SelectOption]:

        return [
            SelectOption(
                label=t.position.name,
                value=str(t.id),
            )
            for t in self.trainings_as_trainee
        ]

################################################################################
    def _notify_check(self, training: Training) -> Optional[Dict[Weekday, List[Tuple[time, time]]]]:

        if self.on_hiatus:
            return

        if not any(dc in training.trainee.data_centers for dc in self.data_centers):
            return

        return TAvailability.combine_availability(training.trainee, self)
        
################################################################################
    async def notify_of_training_signup(self, training: Training) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is being notified of a training signup."
        )

        common_availability = self._notify_check(training)
        if not common_availability:
            return
        
        value = "Your availability matches on the following days:\n\n"
        for a, times in common_availability.items():
            for t in times:
                value += (
                    f"* **{a.proper_name}:** "
                    f"{U.format_dt(U.time_to_datetime(t[0]), 't')} - "
                    f"{U.format_dt(U.time_to_datetime(t[1]), 't')}\n"
                )
                
        url_value = ""
        post_url = self._manager.signup_message.jump_url
        if post_url:
            url_value = (
                f"{BotEmojis.ArrowRight} [Click here to pick up this trainee.]"
                f"({post_url}) {BotEmojis.ArrowLeft}\n"
            )

        notification = U.make_embed(
            title="Training Signup",
            description=(
                f"{training.trainee.name} has signed up for training "
                f"in `{training.position.name}`.\n\n"

                "Please make your way to the server to pick them up if "
                "you're interested.\n"
                f"{url_value}"
                f"{U.draw_line(extra=43)}\n\n"
                
                f"{value}"
            ),
            timestamp=True
        )
        
        await self.send(embed=notification)

################################################################################
    async def notify_of_modified_schedule(self, training: Training) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is being notified of a schedule change."
        )
        
        common_availability = self._notify_check(training)
        if not common_availability:
            return
        
        value = "Your availability matches on the following days:\n\n"
        for a, times in common_availability.items():
            for t in times:
                value += (
                    f"* **{a.proper_name}:** "
                    f"{U.format_dt(U.time_to_datetime(t[0]), 't')} - "
                    f"{U.format_dt(U.time_to_datetime(t[1]), 't')}\n"
                )

        url_value = ""
        post_url = self._manager.signup_message.jump_url
        if post_url:
            url_value = (
                f"{BotEmojis.ArrowRight} [Click here to pick up this trainee.]"
                f"({post_url}) {BotEmojis.ArrowLeft}\n"
            )
        
        notification = U.make_embed(
            title="Trainee Availability Change",
            description=(
                f"{training.trainee.name}'s training schedule has been modified.\n\n"
                f"{url_value}\n"
                f"{U.draw_line(extra=24)}\n\n"
                
                f"{value}"
            ),
            timestamp=True
        )
        
        await self.send(embed=notification)
        
################################################################################
    def toggle_pings(self) -> None:
        
        self._config.toggle_trainee_pings()
        
        log.info(
            "Training",
            (
                f"TUser {self.name} ({self.user_id}) is toggling trainee pings. "
                f"Current status: {self.config.trainee_pings}."
            )
        
        )
        
################################################################################
    def accepting_trainee_pings(self) -> bool:
        
        return self._config.trainee_pings
    
################################################################################
    async def trainer_dashboard(self, interaction: Interaction, cur_page: int = 0) -> None:
        
        log.info(
            "Training",
            (
                f"TUser {self.name} ({self.user_id}) is viewing their trainer "
                f"dashboard. Current page: {cur_page}."
            )
        )

        pages = [
            t.status_page(interaction.user) for t in self.trainings_as_trainer
            if not t.is_complete
        ]
        if not pages:
            error = U.make_embed(
                title="No Trainings Found",
                description=(
                    "No active trainings were found for you to manage.\n\n"
                    "Please check back later or contact the server staff\n"
                    "if you believe this is in error.\n\n"
                    f"{U.draw_line(extra=25)}"
                ),
            )
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        frogginator = Frogginator(pages)
        
        await frogginator.respond(interaction)
        await frogginator.goto_page(cur_page)
        await frogginator.wait()
    
################################################################################
    async def refresh_dashboard(self, interaction: Interaction, cur_page: int) -> None:

        # await interaction.delete_original_response()
        await self.trainer_dashboard(interaction, cur_page)
        
################################################################################
    async def toggle_hiatus(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is toggling their hiatus status."
        )

        if not self.on_hiatus:
            confirm = U.make_embed(
                title="Toggle Hiatus",
                description=(
                    "Are you sure you want to toggle your hiatus status?\n\n"
                    
                    "The following things will happen:\n"
                    "- All currently held trainees will be orphaned or reassigned.\n"
                    "- All training qualifications will be marked 'On Hiatus'.\n"
                    "- You will be unable to pick up new trainees.\n"
                    "- Your name will be (temporarily) removed from the sign-up message (if applicable).\n"
                    "- You will be given a hiatus role, hiding much of the juicy part of the server.\n\n"
                    
                    "**Are you sure you want to do this?**\n"
                    f"{U.draw_line(extra=21)}"
                ),
            )
        else:
            confirm = U.make_embed(
                title="Toggle Hiatus",
                description=(
                    "Are you sure you want to return from hiatus status?\n\n"
                    
                    "The following things will happen:\n"
                    "- All training qualifications will be reverted to their original levels.\n"
                    "- You will be removed from the hiatus role and have your previous role reassigned.\n"
                    "- Your name will be added back to the sign-up message for trainings (if applicable).\n"
                    "- You will be able to pick up trainees again.\n\n"
                    
                    "**Are you sure you want to do this?**\n"
                    f"{U.draw_line(extra=21)}"
                ),
            )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=confirm, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "Hiatus toggle cancelled.")
            return
        
        # Checking current hiatus status before flipping it
        if self.on_hiatus:
            if self.is_trainer:
                await self.guild.role_manager.add_role(interaction.user, RoleType.TrainerMain)
            else:
                await self.guild.role_manager.add_role(interaction.user, RoleType.Trainee)
                
            await self.guild.role_manager.remove_role(interaction.user, RoleType.TrainerHiatus)
            await self.guild.role_manager.remove_role(interaction.user, RoleType.TraineeHiatus)
        else:
            if self.is_trainer:
                await self.guild.role_manager.add_role(interaction.user, RoleType.TrainerHiatus)
            else:
                await self.guild.role_manager.add_role(interaction.user, RoleType.TraineeHiatus)
                
            await self.guild.role_manager.remove_role(interaction.user, RoleType.TrainerMain)
            await self.guild.role_manager.remove_role(interaction.user, RoleType.Trainee)

            for t in self.trainings_as_trainer:
                if t.is_complete:
                    continue
                await t.trainee.notify_of_trainer_hiatus(t)
                t.reset()
                
        self._details.toggle_hiatus()
        
        log.info(
            "Training",
            (
                f"TUser {self.name} ({self.user_id}) has toggled their hiatus status. "
                f"Current status: {self.on_hiatus}."
            )
        )
        
        await self.training_manager.signup_message.update_components()
        await self.guild.log.tuser_hiatus(self)
        
################################################################################
    async def notify_of_trainer_hiatus(self, training: Training) -> None:

        notification = U.make_embed(
            title="Trainer On Hiatus",
            description=(
                f"{training.trainer.name} has gone on hiatus and is\n"
                f"unable to continue training in `{training.position.name}`.\n\n"
                
                "Your name will be re-added to the pool of available\n"
                "trainees and you'll be notified when you're picked up again.\n"
                f"{U.draw_line(extra=43)}"
            )
        )
        await self.send(embed=notification)
        
        log.info(
            "Training",
            (
                f"TUser {self.name} ({self.user_id}) has been notified of a trainer hiatus. "
                f"Trainer: {training.trainer.name} ({training.trainer.user_id})."
            )
        )

################################################################################
    async def is_eligible(
        self, 
        job: JobPosting,
        compare_hiatus: bool = True,
        compare_data_centers: bool = True,
        compare_linked_role: bool = True,
        compare_schedule: bool = True,
        check_profile: bool = True
    ) -> bool:
        
        log.debug(
            "Training",
            f"TUser {self.name} ({self.user_id}) is checking eligibility for job {job.id}."
        )
        
        # Check user and venue mute lists
        if self.user in job.venue.muted_users:
            log.debug("Training", "User is muted for this venue.")
            return False
        if job.venue in self.muted_venues:
            log.debug("Training", "Venue is muted for this user.")
            return False
        
        # Check if on hiatus
        if compare_hiatus:
            if self.on_hiatus:
                log.debug("Training", "User is on hiatus.")
                return False

        if check_profile:
            if not self.profile or self.profile.post_message is None:
                log.debug("Training", "User has no profile or post message.")
                return False
    
        # Check if job's data center is in the user's data centers list
        if compare_data_centers and len(self.profile.data_centers) > 0:
            if not any(dc.contains(job.venue.location.data_center) for dc in self.profile.data_centers):
                log.debug("Training", "User does not have the required data center.")
                return False
    
        # Check if the user has the linked role for the job position, if applicable
        if compare_linked_role:
            if job.position.linked_role is not None:
                try:
                    member = await self.guild.parent.fetch_member(self.user_id)
                except:
                    log.error(
                        "Training",
                        f"Failed to fetch member for TUser {self.name} ({self.user_id})."
                    )
                    return False
                else:
                    if job.position.linked_role not in member.roles:
                        log.debug("Training", "User does not have the required linked role.")
                        return False

        # If comparing schedules, check if the user is available during the job's times
        if compare_schedule and check_profile:
            # Adjust for 0-indexed weekday where 0 is Monday, to match your custom 0-indexed day where 0 is Sunday
            job_day = (job.start_time.weekday() + 1) % 7 
            for availability in self.profile.availability:
                if availability.day.value == job_day:
                    start_time, end_time = job.start_time.time(), job.end_time.time()
                    if availability.contains(start_time, end_time):
                        log.debug("Training", "User is available for the job.")
                        return True
            log.debug("Training", "User is not available for the job.")
            return False  # If no matching availability was found
    
        # If not comparing schedules or none of the above conditions matched, the user is eligible
        log.debug("Training", "User is eligible for the job.")
        return True

################################################################################
    async def start_bg_check(self, interaction: Interaction) -> None:
        
        await self._bg_check.menu(interaction)

################################################################################
    async def send(self, *args, **kwargs) -> None:
        
        try:
            await self.user.send(*args, **kwargs)
        except Forbidden:
            log.warning(
                "Training",
                f"User {self.name} ({self.user_id}) has DMs disabled."
            )
            await self.guild.log.dms_disabled(self.user)
        except Exception as ex:
            log.critical(
                "Training",
                (
                    f"An uncaught exception occurred while attempting to to "
                    f"send message to {self.name} ({self.user_id}).\n{ex}"
                )
            )

################################################################################
    async def mute_venue(self, interaction: Interaction, venue: Venue) -> None:
        
        log.info(
            "Training",
            f"TUser {self.name} ({self.user_id}) is toggling venue mute for {venue.name}."
        )
        
        if venue in self.muted_venues:
            self._mutes.remove(venue)
            flag = False
            log.info("Training", f"Venue mute for {venue.name} has been disabled.")
        else:
            self._mutes.append(venue)
            flag = True
            log.info("Training", f"Venue mute for {venue.name} has been enabled.")
            
        confirm = U.make_embed(
            title="Venue Mute Toggle",
            description=(
                f"Venue pings for {venue.name} have been "
                f"{'enabled' if flag else 'disabled'}.\n\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        await interaction.respond(embed=confirm, ephemeral=True)

################################################################################
    async def staff_experience(self, interaction: Interaction) -> None:
        
        await interaction.respond(embed=self.bg_check.detail_status())

################################################################################
    async def settle_training_balance(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"The training balance for TUser {self.name} ({self.user_id}) is being settled."
        )

        if not self.unpaid_trainings and not self.unsettled_groups:
            log.warning(
                "Training",
                f"No unpaid trainings found for TUser {self.name} ({self.user_id})."
            )
            error = U.make_embed(
                title="No Unpaid Trainings",
                description=(
                    "No unpaid trainings were found to settle.\n"
                    f"{U.draw_line(extra=25)}"
                ),
            )
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        pos_dict = {}
        for t in self.unpaid_trainings:
            if t.position.name not in pos_dict:
                pos_dict[t.position.name] = []
            pos_dict[t.position.name].append(t)

        amount = 0
        training_str = ""
        
        for pos, trainings in pos_dict.items():
            position = self.position_manager.get_position_by_name(pos)
            amount += position.trainer_pay * len(trainings)
            training_str += (
                f"[{len(trainings)}] **{position.name}** = "
                f"`{(position.trainer_pay * len(trainings)):,}`\n"
            )
            
        group_balance = sum([gt.trainer_pay for gt in self.unsettled_groups])
        
        group_str = (
            f"[{len(self.unsettled_groups)}] **Group Trainings** = "
            f"`{group_balance:,}`\n"
        )
        amount += group_balance
            
        embed = U.make_embed(
            title="Settle Training Balance",
            description=(
                "Please confirm you want to settle the\n"
                "following unpaid training balances.\n\n"

                f"{training_str}\n"
                f"{group_str}\n"
                
                "__**Total Amount Due:**__\n"
                f"`{amount:,}`\n"
                f"{U.draw_line(extra=12)}"
            ),
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "Training balance settlement cancelled.")
            return
        
        for t in self.unpaid_trainings:
            t.trainer_paid = True
        for gt in self.unsettled_groups:
            gt.is_paid = True
        self._pay_requested = False
            
        confirm = U.make_embed(
            title="Settle Training Balance",
            description=(
                "All unpaid training balances have been settled.\n"
                f"__**Total Amount Paid:**__ `{amount:,}`\n"
                f"{U.draw_line(extra=25)}"
            ),
        )
        
        await interaction.respond(embed=confirm)
        
        log.info(
            "Training",
            f"Training balance settlement complete for TUser {self.name} ({self.user_id})."
        )

################################################################################
    async def manage_trainings(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"Trainings are being managed for TUser {self.name} ({self.user_id})."
        )
        
        source_trainings = [t for t in self.trainings_as_trainer if not t.is_complete]
        if not source_trainings:
            log.warning(
                "Training",
                f"No active trainings found for TUser {self.name} ({self.user_id})."
            )
            error = U.make_embed(
                title="No Trainings Found",
                description=(
                    "No active trainings were found to manage.\n"
                    f"{U.draw_line(extra=25)}"
                ),
            )
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        training_dict = {}
        for t in source_trainings:
            if t.trainee.user_id not in training_dict:
                training_dict[t.trainee.user_id] = []
            training_dict[t.trainee.user_id].append(t)
            
        pages = []
        for user_id, trainings in training_dict.items():
            tuser = self.training_manager[user_id]
            training_str = ""
            for t in trainings:
                training_str += f"* {t.position.name}\n"
            
            embed = U.make_embed(
                title=f"Trainings for `{self.name}`",
                description=(
                    f"__**Trainee:**__ `{tuser.name}`\n"
                    f"({tuser.user.mention})\n"
                    f"__**Trainings:**__\n"
                    f"{training_str}"
                ),
            )
            view = ManageTrainingsView(interaction.user, tuser, self)
            pages.append(Page(embeds=[embed], custom_view=view))
            
        frogginator = Frogginator(pages)
        await frogginator.respond(interaction)
    
################################################################################
    async def _select_training_to_decouple(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"Trainings are being decoupled for TUser {self.name} ({self.user_id})."
        )
        
        options = [
            SelectOption(
                label=t.position.name,
                value=str(t.id)
            )
            for t in self.trainings_as_trainee
            if (
                t.trainer is not None 
                and t.trainer.user == interaction.user
            )
        ]
        
        prompt = U.make_embed(
            title="Decouple Training",
            description=(
                "Please select the training you would like to decouple the trainer from."
            ),
        )
        view = DecoupleTrainingSelectView(interaction.user, options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "Decouple training cancelled.")
            return
        
        for training_id in view.value:
            log.info(
                "Training",
                f"Decoupling training {training_id} for TUser {self.name} ({self.user_id})."
            )
            await self.training_manager.get_training(training_id).set_trainer(None)

################################################################################
    async def on_server_leave(self) -> Tuple[int, int]:
        
        modified = 0
        deleted = 0
        
        for t in self.trainings_as_trainer:
            await t.set_trainer(None)
            modified += 1
            
        for t in self.trainings_as_trainee:
            await self.training_manager.remove_training(t.id)
            deleted += 1
            
        log.info(
            "Training",
            (
                f"TUser {self.name} ({self.user_id}) has left the server. "
                f"{modified} trainings were modified and {deleted} were deleted."
            )
        )
            
        return modified, deleted

################################################################################
    async def request_pay(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"Pay is being requested for TUser {self.name} ({self.user_id})."
        )
        
        if not self.unpaid_trainings:
            log.warning(
                "Training",
                f"No unpaid trainings found for TUser {self.name} ({self.user_id})."
            )
            # We shouldn't ever reach this, so an inline error is fine
            error = U.make_embed(
                title="No Unpaid Trainings",
                description=(
                    "No unpaid trainings were found to request pay for.\n"
                    f"{U.draw_line(extra=25)}"
                ),
            )
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if self._pay_requested:
            log.warning(
                "Training",
                (
                    f"Pay has already been requested for TUser {self.name} "
                    f"({self.user_id})."
                )
            )
            error = PayAlreadyRequestedError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        pos_dict = {}
        for t in self.unpaid_trainings:
            if t.position.name not in pos_dict:
                pos_dict[t.position.name] = []
            pos_dict[t.position.name].append(t)

        amount = 0
        training_str = ""
        
        for pos, trainings in pos_dict.items():
            position = self.position_manager.get_position_by_name(pos)
            amount += position.trainer_pay * len(trainings)
            training_str += (
                f"[{len(trainings)}] **{position.name}** = "
                f"`{(position.trainer_pay * len(trainings)):,}`\n"
            )
            
        embed = U.make_embed(
            title="Request Pay",
            description=(
                "Please confirm you want to request pay for the\n"
                "following unpaid training balances.\n\n"

                f"{training_str}\n"
                
                "__**Total Amount Due:**__\n"
                f"`{amount:,}`\n"
                f"{U.draw_line(extra=12)}"
            ),
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "Pay request cancelled.")
            return
        
        await self.guild.log.pay_request(self)
        self._pay_requested = True
            
        confirm = U.make_embed(
            title="Request Pay",
            description=(
                "Pay has been requested for all unpaid training balances.\n"
                f"__**Total Amount Requested:**__ `{amount:,}`\n"
                f"{U.draw_line(extra=25)}"
            ),
        )
        
        await interaction.respond(embed=confirm)
        
        log.info(
            "Training",
            f"Pay request complete for TUser {self.name} ({self.user_id})."
        )
        
################################################################################
