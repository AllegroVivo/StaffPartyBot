from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, TypeVar, Any, Dict

from discord import User, NotFound, Embed, EmbedField, Interaction, SelectOption

from UI.Common import ConfirmCancelView, Frogginator
from UI.Training import (
    AddTrainingView,
    AddQualificationView,
    TUserNameModal,
    TUserNotesModal,
    WeekdaySelectView,
    TimeSelectView,
    ModifyQualificationView,
    RemoveQualificationView,
    RemoveTrainingView,
    TrainingUpdateView,
)
from Utilities import Utilities as U, TrainingLevel
from .Availability import Availability
from .Qualification import Qualification
from .UserConfig import UserConfiguration
from .Training import Training
from Assets import BotEmojis

if TYPE_CHECKING:
    from Classes import TrainingBot, TrainingManager, PositionManager, GuildData
################################################################################

__all__ = ("TUser",)

TU = TypeVar("TU", bound="TUser")

################################################################################
class TUser:

    __slots__ = (
        "_manager",
        "_user",
        "_name",
        "_notes",
        "_availability",
        "_config",
        "_qualifications"
    )

################################################################################
    def __init__(
        self,
        mgr: TrainingManager,
        user: User,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        availabilities: Optional[List[Availability]] = None,
        configuration: Optional[UserConfiguration] = None,
        qualifications: Optional[List[Qualification]] = None
    ) -> None:

        self._manager: TrainingManager = mgr

        self._user: User = user
        self._name: str = name or user.name
        self._notes: Optional[str] = notes

        self._config: UserConfiguration = configuration or UserConfiguration(self)
        self._availability: List[Availability] = availabilities or []
        self._qualifications: List[Qualification] = qualifications or []

################################################################################
    @classmethod
    def new(cls: Type[TU], manager: TrainingManager, user: User) -> TU:

        manager.bot.database.insert.tuser(manager.guild_id, user.id)

        self: TU = cls.__new__(cls)

        self._manager = manager

        self._user = user
        self._name = user.name
        self._notes = None

        self._config = UserConfiguration(self)
        self._availability = []
        self._qualifications = []

        return self

################################################################################
    @classmethod
    async def load(cls: Type[TU], mgr: TrainingManager, data: Dict[str, Any]) -> Optional[TU]:

        tuser = data["tuser"]
        config = data["tconfig"]
        availability = data["availability"]
        qdata = data["qualifications"]

        try:
            user = await mgr.bot.fetch_user(tuser[0])
        except NotFound:
            return None

        self: TU = cls.__new__(cls)

        self._manager = mgr
        self._user = user

        self._name = tuser[2]
        self._notes = tuser[3]

        self._config = UserConfiguration.load(self, config)
        self._availability = [Availability.load(self, a) for a in availability]
        self._qualifications = [Qualification.load(self, q) for q in qdata]

        return self

################################################################################
    def __eq__(self, other: TUser) -> bool:
        
        if other is None:
            return False
        
        return self.user == other.user
    
################################################################################
    @property
    def bot(self) -> TrainingBot:

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

        return self._name or self.user.display_name

################################################################################
    @name.setter
    def name(self, value: str) -> None:

        self._name = value
        self.update()

################################################################################    
    @property
    def notes(self) -> Optional[str]:

        return self._notes

################################################################################
    @notes.setter
    def notes(self, value: Optional[str]) -> None:

        self._notes = value
        self.update()

################################################################################    
    @property
    def qualifications(self) -> List[Qualification]:

        return self._qualifications

################################################################################
    @property
    def availability(self) -> List[Availability]:

        self._availability.sort(key=lambda a: a.day.value)
        return self._availability

################################################################################
    @property
    def trainings(self) -> List[Training]:

        return [t for t in self.training_manager.all_trainings if t.trainee == self]

################################################################################    
    @property
    def position_manager(self) -> PositionManager:
        
        return self._manager.guild.position_manager
    
################################################################################
    @property
    def training_manager(self) -> TrainingManager:
        
        return self._manager
    
################################################################################
    def update(self) -> None:
        """Update this TUser's information in the database."""

        self.bot.database.update.tuser(self)

################################################################################
    def is_qualified(self, position_id: str) -> bool:
        
        return any(q.position.id == position_id for q in self.qualifications)
    
################################################################################
    def admin_status(self) -> Embed:

        return U.make_embed(
            title=f"User Status for: __{self.name}__",
            description=(
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                self._qualifications_field(),
                self._training_requested_field(),
                self._availability_field(),
                self._notes_field(),
            ]
        )

################################################################################
    def _qualifications_field(self) -> EmbedField:

        return EmbedField(
            name="__Trainer Qualifications__",
            value=(
                (
                    "* " + "\n* ".join(
                        [
                            f"{q.position.name} -- *({q.level.proper_name})*"
                            for q in self.qualifications
                        ]
                    ) if self.qualifications else "`None`"
                )
            ),
            inline=True
        )

################################################################################
    def _training_requested_field(self) -> EmbedField:

        training_str = "`None`" if not self.trainings else ""

        if training_str == "":
            for t in self.trainings:
                training_str += f"* {t.position.name}\n-- Trainer: "
                training_str += f"`{t.trainer.name}`\n" if t.trainer else "None... (Yet!)\n"

        return EmbedField(
            name="__Trainings Requested__",
            value=training_str,
            inline=True
        )

################################################################################
    def _availability_field(self) -> EmbedField:

        return EmbedField(
            name="__Availability__",
            value=Availability.availability_status(self.availability),
            inline=False
        )

################################################################################
    def _notes_field(self) -> EmbedField:

        return EmbedField(
            name="__Internal Notes__",
            value=self.notes if self.notes else "`None`",
            inline=False
        )

################################################################################
    def _bot_pings_field(self) -> EmbedField:
        
        return EmbedField(
            name="__New Trainee Pings__",
            value=(
                str(BotEmojis.Check if self.config.trainee_pings else BotEmojis.Cross)
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

        return U.make_embed(
            title=f"User Status for: __{self.name}__",
            description=(
                f"{U.draw_line(extra=25)}"
            ),
            fields=[
                self._training_requested_field(),
                self._bot_pings_field(),
                self._availability_field(),
            ],
        )

################################################################################    
    async def set_name(self, interaction: Interaction) -> None:

        modal = TUserNameModal(self._name)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.name = modal.value

################################################################################
    async def set_notes(self, interaction: Interaction) -> None:

        modal = TUserNotesModal(self._notes)

        await interaction.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        self.notes = modal.value

################################################################################
    async def set_availability(self, interaction: Interaction) -> None:

        status = U.make_embed(
            title="Set Availability",
            description=(
                "Please select the appropriate day from the initial\n"
                "selector, followed by your available time frame.\n\n"

                "Please note, you can set your timezone\n"
                "by using the `/training config` command.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = WeekdaySelectView(interaction.user)

        await interaction.respond(embed=status, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        weekday = view.value

        prompt = U.make_embed(
            title="Set Availability Start",
            description=(
                f"Please select the beginning of your availability for `{weekday.proper_name}`..."
            )
        )
        view = TimeSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        start_time = view.value if view.value != -1 else None
        end_time = None

        if start_time is not None:
            prompt = U.make_embed(
                title="Set Availability End",
                description=(
                    f"Please select the end of your availability for `{weekday.proper_name}`..."
                )
            )
            view = TimeSelectView(interaction.user)

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete or view.value is False:
                return

            end_time = view.value

        for i, a in enumerate(self.availability):
            if a.day == weekday:
                self._availability.pop(i).delete()

        if start_time is not None:
            availability = Availability.new(self, weekday, start_time, end_time)
            self._availability.append(availability)

################################################################################
    async def add_qualification(self, interaction: Interaction) -> None:

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
            return

        position = self.position_manager.get_position(view.value[0])
        level = TrainingLevel(int(view.value[1]))

        qualification = Qualification.new(self.training_manager, self.user, position, level)
        self._qualifications.append(qualification)

################################################################################
    async def modify_qualification(self, interaction: Interaction) -> None:

        embed = U.make_embed(
            title="Modify Qualification",
            description=(
                "Select the position you would like to modify a qualification\n"
                "for. Subsequently, a second selector will appear to\n"
                "allow you to select the individual qualification to modify.\n"
                f"{U.draw_line(extra=25)}"
            )
        )
        view = ModifyQualificationView(interaction.user, self.qualification_options())

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        pos = self.position_manager.get_position(view.value[0])
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
            return

        qualification = self.get_qualification(view.value)

        confirm = U.make_embed(
            title="Remove Qualification",
            description=(
                f"Are you sure you want to remove the qualification for\n"
                f"the position of {qualification.position.name}?"
            )
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        qualification.delete()
        self._qualifications.remove(qualification)

################################################################################
    async def add_training(self, interaction: Interaction) -> None:
        """Add a new job training for this TUser.
        
        We're doing this inside the TUser class because it's a user-specific
        operation and things get muddy if we do it in the TrainingManager.
        """

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
            if o.value not in [t.position.id for t in self.trainings]
        ]

        view = AddTrainingView(interaction.user, options)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        for pos_id in view.value:
            await self.training_manager.add_training(Training.new(self, pos_id))

################################################################################
    async def remove_training(self, interaction: Interaction) -> None:

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
            return
        
        id_to_remove = view.value

        confirm = U.make_embed(
            title="Confirm Removal",
            description=(
                "Are you sure you want to remove this training?\n"
                f"{U.draw_line(extra=25)}"
            ),
        )
        view = ConfirmCancelView(interaction.user)

        await interaction.respond(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        await self.training_manager.remove_training(id_to_remove)

################################################################################
    def training_select_options(self) -> List[SelectOption]:

        return [
            SelectOption(
                label=t.position.name,
                value=str(t.id),
            )
            for t in self.trainings
        ]

################################################################################
    async def notify_of_training_signup(self, training: Training) -> None:

        notification = U.make_embed(
            title="Training Signup",
            description=(
                f"{training.trainee.name} has signed up for training "
                f"in `{training.position.name}`.\n\n"

                "Please make your way to the server to pick them up if "
                "you're interested.\n"
                f"{U.draw_line(extra=43)}"
            )
        )

        # If the user doesn't exist, isn't accepting DMs, or the bot simply 
        # can't DM them, we'll just skip. Too bad, so sad.
        try:
            await self.user.send(embed=notification)
        except:
            pass

################################################################################
    def toggle_pings(self) -> None:
        
        self._config.toggle_trainee_pings()
        self.update()
        
################################################################################
    def accepting_trainee_pings(self) -> bool:
        
        return self._config.trainee_pings
    
################################################################################
    async def trainer_dashboard(self, interaction: Interaction, cur_page: int = 0) -> None:

        pages = [
            t.status_page(interaction.user) for t in self.training_manager.all_trainings
            if t.trainer == self
        ]
        frogginator = Frogginator(pages)
        
        await frogginator.respond(interaction)
        await frogginator.goto_page(cur_page)
        await frogginator.wait()
    
################################################################################
    async def refresh_dashboard(self, interaction: Interaction, cur_page: int) -> None:

        # await interaction.delete_original_response()
        await self.trainer_dashboard(interaction, cur_page)
        
################################################################################
