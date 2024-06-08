from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional, List, Any, Type, TypeVar, Dict

from discord import Interaction, Embed, EmbedField, Message, NotFound, SelectOption

from Assets import BotEmojis
from Classes.Training.GroupTrainingSignup import GroupTrainingSignup
from UI.Common import TimezoneSelectView, ConfirmCancelView
from UI.Training import (
    GroupTrainingStatusView,
    GroupTrainingTitleModal,
    GroupTrainingDescriptionModal,
    GroupTrainingScheduleModal,
    GroupTrainingPickupView,
    GroupTrainingNoShowView
)
from Utilities import Utilities as U, log, SignupLevel, RoleType
from Utilities.Errors import (
    DateTimeFormatError,
    DateTimeMismatchError,
    TimeRangeError,
    DateTimeBeforeNowError,
    GroupTrainingNotCompleteError,
    NotRegisteredError,
)

if TYPE_CHECKING:
    from Classes import TrainingManager, Position, TUser, StaffPartyBot
################################################################################

__all__ = ("GroupTraining",)

GT = TypeVar("GT", bound="GroupTraining")

################################################################################
class GroupTraining:
    
    __slots__ = (
        "_mgr",
        "_id",
        "_name",
        "_description",
        "_start",
        "_end",
        "_positions",
        "_signups",
        "_trainer",
        "_msg",
        "_schedule_updated",
        "_reminder_sent",
        "_completed",
        "_paid",
        "_attended",
    )
    
    REMINDER_THRESHOLD = 30
    
################################################################################
    def __init__(
        self, 
        mgr: TrainingManager, 
        _id: str,
        trainer: TUser, 
        positions: List[Position], 
        **kwargs
    ):
        
        self._id: str = _id
        self._mgr: TrainingManager = mgr
        
        self._trainer: TUser = trainer
        self._positions: List[Position] = positions
        
        self._name: Optional[str] = kwargs.get("name")
        self._description: Optional[str] = kwargs.get("description")
        
        self._schedule_updated: bool = False
        self._reminder_sent: bool = False
        
        self._completed: bool = kwargs.get("completed", False)
        self._paid: bool = kwargs.get("paid", False)
        
        self._start: Optional[datetime] = kwargs.get("start_time")
        self._end: Optional[datetime] = kwargs.get("end_time")
        
        self._signups: List[GroupTrainingSignup] = kwargs.get("signups") or []
        self._msg: Optional[Message] = kwargs.get("post_message")
        self._attended: List[TUser] = kwargs.get("attended") or []
        
################################################################################
    @classmethod
    def new(
        cls: Type[GT], 
        mgr: TrainingManager, 
        trainer: TUser, 
        positions: List[Position],
        **kwargs
    ) -> GT:
        
        new_id = mgr.bot.database.insert.group_training(
            mgr.guild_id, trainer.user_id, [pos.id for pos in positions]
        )
        return cls(mgr, new_id, trainer, positions, **kwargs)
    
################################################################################
    @classmethod
    async def load(cls: Type[GT], mgr: TrainingManager, data: Dict[str, Any]) -> GT:
        
        self: GT = cls.__new__(cls)
        
        self._mgr = mgr
        
        self._id = data["training"][0]
        self._name = data["training"][2]
        self._description = data["training"][3]
        
        self._start = data["training"][4]
        self._end = data["training"][5]
        
        self._schedule_updated = False
        self._reminder_sent = False
        
        self._positions = [
            mgr.guild.position_manager.get_position(pos)
            for pos in data["training"][6]
        ]
        self._trainer = mgr[data["training"][7]]
        self._msg = await mgr.guild.get_or_fetch_message(data["training"][8])
        
        self._signups = [
            GroupTrainingSignup(
                parent=self,
                _id=s[0],
                user=mgr[s[2]],
                level=SignupLevel(s[3])
            )
            for s in data["signups"]
        ]
        
        self._completed = data["training"][9]
        self._paid = data["training"][10]
        
        self._attended = [await mgr.guild.get_or_fetch_user(user) for user in data["training"][11]]
        
        return self
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._mgr.bot
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def name(self) -> Optional[str]:
        
        return self._name
    
    @name.setter
    def name(self, value: Optional[str]) -> None:
        
        self._name = value
        self.update()
        
################################################################################
    @property
    def description(self) -> Optional[str]:
        
        return self._description
    
    @description.setter
    def description(self, value: Optional[str]) -> None:
        
        self._description = value
        self.update()
        
################################################################################
    @property
    def start_time(self) -> Optional[datetime]:
        
        return self._start
    
    @start_time.setter
    def start_time(self, value: Optional[datetime]) -> None:
        
        self._start = value
        self.update()
        
################################################################################
    @property
    def end_time(self) -> Optional[datetime]:
        
        return self._end
    
    @end_time.setter
    def end_time(self, value: Optional[datetime]) -> None:
        
        self._end = value
        self.update()
       
################################################################################
    @property
    def post_message(self) -> Optional[Message]:
        
        return self._msg
    
    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:
        
        self._msg = value
        self.update()
        
################################################################################
    @property
    def is_paid(self) -> bool:
        
        return self._paid
    
    @is_paid.setter
    def is_paid(self, value: bool) -> None:
        
        self._paid = value
        self.update()
        
################################################################################
    @property
    def is_completed(self) -> bool:
        
        return self._completed
    
    @is_completed.setter
    def is_completed(self, value: bool) -> None:
            
        self._completed = value
        self.update()
        
################################################################################
    @property
    def positions(self) -> List[Position]:
        
        if self._positions:
            self._positions.sort(key=lambda x: x.name)
        return self._positions
    
################################################################################
    @property
    def trainer(self) -> TUser:
        
        return self._trainer
    
################################################################################
    @property
    def confirmed_signups(self) -> List[GroupTrainingSignup]:
            
        return [s for s in self._signups if s.level == SignupLevel.Accepted]
    
################################################################################
    @property
    def tentative_signups(self) -> List[GroupTrainingSignup]:
        
        return [s for s in self._signups if s.level == SignupLevel.Tentative]
    
################################################################################
    @property
    def signups(self) -> List[GroupTrainingSignup]:
        
        return self._signups
    
################################################################################
    @property
    def attended_users(self) -> List[TUser]:
        
        return self._attended
    
################################################################################
    @property
    def pos_string(self) -> str:
        
        return (
            ", ".join(f"{pos.name}" for pos in self.positions)
            if self.positions
            else "General Training"
        )
    
################################################################################
    @property
    def is_complete(self) -> bool:
        
        return all([
            self.name is not None,
            self.description is not None,
            self.start_time is not None,
            self.end_time is not None
        ]) 
    
################################################################################
    @property
    def trainer_pay(self) -> int:
        
        return (
            sum((pos.trainer_pay or 0) for pos in self.positions)
            if self.positions
            else 250000
        ) * len(self.attended_users)
    
################################################################################
    def update(self) -> None:
        
        self._mgr.bot.database.update.group_training(self)
        
################################################################################
    def delete(self) -> None:
        
        self._mgr.bot.database.delete.group_training(self)
        self._mgr.groups.remove(self)
        
################################################################################
    def get_signup_by_user(self, user: TUser) -> Optional[GroupTrainingSignup]:
        
        return next((s for s in self._signups if s.user == user), None)
    
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        log.info("Training", f"Opening group training menu for {self.name}")
        
        embed = self.status()
        view = GroupTrainingStatusView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            title=self.name or "Name Not Set",
            description=self.description or "`Description Not Set`",
            fields=[
                EmbedField(
                    name="__Positions__",
                    value=self.pos_string,
                    inline=False
                ),
                EmbedField(
                    name="__Trainer__",
                    value=(
                        f"{self.trainer.user.mention}\n"
                        f"({self.trainer.user.display_name})"
                    ),
                    inline=False
                ),
                EmbedField(
                    name="__Date & Time__",
                    value=(
                        f"{U.format_dt(self.start_time, 'd')}: "
                        f"{U.format_dt(self.start_time, 't')} - "
                        f"{U.format_dt(self.end_time, 't')}\n"
                        f"⏱️({U.format_dt(self.start_time, 'R')})"
                    ) if self.start_time else "`Not Set`",
                    inline=False
                ),
                EmbedField(
                    name=f"{str(BotEmojis.Check)} __Confirmed__",
                    value="* " + "\n* ".join(
                        f"{s.user.user.mention} ({s.user.name})"
                        for s in self.confirmed_signups
                    ) if self.confirmed_signups else "`None`",
                    inline=True
                ),
                EmbedField(
                    name=f"{str(BotEmojis.Goose)}  __Tentative__",
                    value="* " + "\n* ".join(
                        f"{s.user.user.mention} ({s.user.name})"
                        for s in self.tentative_signups
                    ) if self.tentative_signups else "`None`",
                    inline=True
                )
            ]
        )
    
################################################################################
    async def set_title(self, interaction: Interaction) -> None:
        
        log.info("Training", f"Setting group training title for {self.name}")
        
        modal = GroupTrainingTitleModal(self.name)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            log.debug("Training", "Title modal was not completed")
            return
        
        self.name = modal.value
        
        log.info("Training", f"Title set to {self.name}")
    
################################################################################
    async def set_description(self, interaction: Interaction) -> None:
        
        log.info("Training", f"Setting group training description for {self.name}")
        
        modal = GroupTrainingDescriptionModal(self.description)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            log.debug("Training", "Description modal was not completed")
            return
        
        self.description = modal.value
        
        log.info("Training", f"Description set to {self.name}")
    
################################################################################
    async def set_times(self, interaction: Interaction) -> None:

        log.info(
            "Training",
            f"Setting group training schedule for GroupTraining {self.id} "
            f"(Title: {self.name}, Position: {self.pos_string}, "
            f"User: {self.trainer.user.name})"
        )

        prompt = U.make_embed(
            title="Set Group Training Schedule",
            description=(
                "You'll now be given an opportunity to enter the start and end "
                "times for this group training.\n\n"

                "You can begin this process by selecting the timezone that will "
                "correspond to your entries from the selector below."
            ),
        )
        view = TimezoneSelectView(interaction.user)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Group training schedule selection canceled")
            return

        timezone, inter = view.value
        py_timezone = U.TIMEZONE_OFFSETS[timezone]
        
        start_time = (
            self.start_time.astimezone(py_timezone)
            if self.start_time else None
        )
        end_time = (
            self.end_time.astimezone(py_timezone)
            if self.end_time else None
        )
        
        modal = GroupTrainingScheduleModal(start_time, end_time)

        await inter.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            log.debug("Training", "Group training schedule entry canceled")
            return

        raw_start, raw_end = modal.value

        try:
            start_temp = datetime.strptime(raw_start, "%m/%d/%Y %I:%M %p")
        except ValueError:
            log.warning(
                "Training",
                (
                    f"Failed to parse start time: '{raw_start}' for group training {self.id} "
                    f"(Title: {self.name}, Position: {self.pos_string}, "
                    f"User: {self.trainer.user.name})"
                )
            )
            error = DateTimeFormatError(raw_start)
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            start_time: datetime = U.TIMEZONE_OFFSETS[timezone].localize(
                datetime(
                    year=start_temp.year,
                    month=start_temp.month,
                    day=start_temp.day,
                    hour=start_temp.hour,
                    minute=start_temp.minute
                )
            )

        try:
            end_temp = datetime.strptime(raw_end, "%m/%d/%Y %I:%M %p")
        except ValueError:
            log.warning(
                "Training",
                (
                    f"Failed to parse end time: '{raw_end}' for group training {self.id} "
                    f"(Title: {self.name}, Position: {self.pos_string}, "
                    f"User: {self.trainer.user.name})"
                )
            )
            error = DateTimeFormatError(raw_end)
            await interaction.respond(embed=error, ephemeral=True)
            return
        else:
            end_time: datetime = U.TIMEZONE_OFFSETS[timezone].localize(
                datetime(
                    year=end_temp.year,
                    month=end_temp.month,
                    day=end_temp.day,
                    hour=end_temp.hour,
                    minute=end_temp.minute
                )
            )

        if end_time <= start_time:
            log.warning(
                "Training",
                (
                    f"End time '{end_time}' is before start time '{start_time}' "
                    f"for group training {self.id} (Title: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name})"
                )
            )
            error = DateTimeMismatchError(start_time, end_time)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if datetime.now().timestamp() > end_time.timestamp():
            log.warning(
                "Training",
                (
                    f"End time '{end_time}' is before current time for group training "
                    f"{self.id} (Title: {self.name}, Position: {self.pos_string}, "
                    f"User: {self.trainer.user.name})"
                )
            )
            error = DateTimeBeforeNowError(start_time)
            await interaction.respond(embed=error, ephemeral=True)
            return

        if (end_time - start_time).total_seconds() < 900 or (end_time - start_time).total_seconds() > 10800:
            log.warning(
                "Training",
                (
                    f"Time range '{start_time} - {end_time}' is outside of the acceptable "
                    f"length for group training {self.id} (Title: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name})"
                )
            )
            error = TimeRangeError("15 Minutes", "3 Hours")
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        prev_start = self.start_time
        prev_end = self.end_time

        self._start = start_time
        self._end = end_time
        self.update()
        
        if prev_start is not None:
            notification = U.make_embed(
                title="Group Training Schedule Updated",
                description=(
                    f"The group training schedule for **{self.name}** has been updated.\n\n"
                    
                    "__**PREVIOUS SCHEDULE**__\n"
                    f"**Date & Time:** {U.format_dt(prev_start, 'd')} "
                    f"{U.format_dt(prev_start, 't')} - {U.format_dt(prev_end, 't')}\n\n"
                    
                    "__**NEW SCHEDULE**__\n"
                    f"**Date & Time:** {U.format_dt(self.start_time, 'd')} "
                    f"{U.format_dt(self.start_time, 't')} - {U.format_dt(self.end_time, 't')}\n\n"
                    
                    f"[Click here to view the updated posting.]({self.post_message.jump_url})"
                )
            )
            await self.notify_enrolled_applicants(notification)

        log.info(
            "Training",
            (
                f"Group training schedule for {self.id} (Title: {self.name}, "
                f"Position: {self.pos_string}, User: {self.trainer.user.name}) "
                f"set to {start_time} - {end_time}"
            )
        )
    
################################################################################
    async def post(self, interaction: Interaction) -> None:

        log.info(
            "Training",
            f"Creating group training post for {self._id} (Name: {self.name}, "
            f"Position: {self.pos_string}, User: {self.trainer.user.name})"
        )

        if not self.is_complete:
            log.warning(
                "Training",
                (
                    f"Group training {self._id} (Name: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name})"
                    f" is incomplete. Aborting post."
                )
            )
            error = GroupTrainingNotCompleteError()
            await interaction.respond(embed=error, ephemeral=True)
            return

        if self.post_message is not None and await self._update_post_components():
            confirm = U.make_embed(
                title="Group Training Updated",
                description="The group training has been updated."
            )
            await interaction.respond(embed=confirm, ephemeral=True)

            log.info(
                "Training",
                (
                    f"Group training {self._id} (Name: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name}) "
                    f"post updated successfully"
                )
            )

            if self._schedule_updated:
                await self.notify_enrolled_applicants()
                log.info("Training", "Notified group training signups of schedule update")
                self._schedule_updated = False
            return

        confirm = U.make_embed(
            title="Group Training Post Confirmation",
            description="Are you sure you want to post this group training?"
        )
        view = ConfirmCancelView(interaction.user)
        await interaction.respond(embed=confirm, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "Group training post creation canceled")
            return

        post_view = GroupTrainingPickupView(self)
        self.bot.add_view(post_view)

        channel = self._mgr.guild.channel_manager.group_training_channel

        try:
            self.post_message = await channel.send(embed=self.status(), view=post_view)

            log.debug(
                "Training",
                (
                    f"Created group training posting {self._id} (Name: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name})"
                )
            )

            confirm = U.make_embed(
                title="Group Training Created",
                description=f"The group training post has been created."
            )

            await interaction.respond(embed=confirm, ephemeral=True)
        except Exception as ex:
            log.error(
                "Training",
                (
                    f"Failed to create group training post {self._id} (Name: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name}):\n{ex}"
                )
            )
            error = U.make_embed(
                title="Posting Error",
                description="There was an error posting the group training."
            )
            await interaction.respond(embed=error, ephemeral=True)
        else:
            await self.notify_eligible_trainees()
            log.info("Training", "Notified eligible applicants of group training")
    
################################################################################
    async def _update_post_components(self) -> bool:

        if self.post_message is None:
            return False

        log.info(
            "Training",
            (
                f"Updating group training components for {self._id} (Name: {self.name}, "
                f"Position: {self.pos_string}, User: {self.trainer.user.name})"
            )
        )

        try:
            view = GroupTrainingPickupView(self)
            self.bot.add_view(view, message_id=self.post_message.id)
            await self.post_message.edit(embed=self.status(), view=view)
        except NotFound as ex:
            log.error(
                "Training",
                (
                    f"Failed to update group training {self._id} (Name: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name}):\n{ex}"
                )
            )
            self.post_message = None
            return False
        except Exception as ex:
            log.warning(
                "Training",
                (
                    f"Failed to update group training {self._id} (Name: {self.name}, "
                    f"Position: {self.pos_string}, User: {self.trainer.user.name}):\n{ex}"
                )
            )
            return False
        else:
            log.info(
                "Training",
                "Group training post components updated successfully"
            )
            return True
        
################################################################################
    async def notify_eligible_trainees(self) -> None:
        
        if self.post_message is None:
            return
        
        notification = U.make_embed(
            title="Group Training Notification",
            description=(
                f"**{self.name}** has been scheduled for `{self.pos_string}` "
                f"and will be hosted by `{self.trainer.name}`.\n\n"
                f"[Please sign up here]({self.post_message.jump_url}) if you're "
                f"interested in attending!"
            )
        )
        
        trainees = [
            t.trainee 
            for t in self._mgr.unmatched_trainings 
            if t.position in self.positions
        ]
        for trainee in trainees:
            await trainee.send(embed=notification)
            
################################################################################
    async def notify_enrolled_applicants(self, message: Embed) -> None:
        
        for signup in self.signups:
            await signup.user.send(embed=message)
    
################################################################################
    async def signup(self, interaction: Interaction) -> None:
        
        trainee = self._mgr[interaction.user.id]
        if trainee is None:
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        current = self.get_signup_by_user(trainee)
        if current is not None:
            if current.level == SignupLevel.Accepted:
                current.delete()
                confirm_str = "Your signup has been removed."
            else:
                current.level = SignupLevel.Accepted
                confirm_str = "Your signup has been changed to confirmed."
        else:
            self._signups.append(GroupTrainingSignup.new(self, trainee, SignupLevel.Accepted))
            confirm_str = "You have successfully signed up for this group training."
            
        confirm = U.make_embed(
            title="Signup Confirmation",
            description=confirm_str
        )
        await interaction.respond(embed=confirm, ephemeral=True)
    
################################################################################
    async def tentative_signup(self, interaction: Interaction) -> None:

        trainee = self._mgr[interaction.user.id]
        if trainee is None:
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return

        current = self.get_signup_by_user(trainee)
        if current is not None:
            if current.level == SignupLevel.Tentative:
                current.delete()
                confirm_str = "Your signup has been removed."
            else:
                current.level = SignupLevel.Tentative
                confirm_str = "Your signup has been changed to tentative."
        else:
            self._signups.append(GroupTrainingSignup.new(self, trainee, SignupLevel.Tentative))
            confirm_str = "You have tentatively signed up for this group training."

        confirm = U.make_embed(
            title="Signup Confirmation",
            description=confirm_str
        )
        await interaction.respond(embed=confirm, ephemeral=True)
    
################################################################################
    async def reminder(self) -> None:
        
        if self.is_completed or self.start_time is None or self._reminder_sent:
            return
    
        if U.compare_datetimes(
            self.start_time - timedelta(minutes=self.REMINDER_THRESHOLD),
            datetime.now()
        ) == 1:
            notification = U.make_embed(
                title="Group Training Reminder",
                description=(
                    f"[**{self.name}**]({self.post_message.jump_url}) is scheduled "
                    f"to begin in roughly 30 minutes.\n\n"
                    
                    f"Please make sure you're ready to attend!"
                )
            )
            for signup in self.signups:
                await signup.user.send(embed=notification)
    
            self._reminder_sent = True
            
################################################################################
    async def complete(self, interaction: Interaction) -> bool:
        
        prompt = U.make_embed(
            title="Complete Group Training",
            description="Are you sure you want to complete this group training?"
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return False
        
        options = [
            SelectOption(
                label=f"{s.user.name} ({s.user.user.name})",
                value=str(s.user.user_id)
            ) for s in self.signups
        ]
        
        prompt = U.make_embed(
            title="Select No-Shows",
            description="Please select all trainees who did not show up for this training."
        )
        view = GroupTrainingNoShowView(interaction.user, options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return False
        
        no_shows = [self._mgr[int(user_id)] for user_id in view.value]
        self._attended = [s.user for s in self.signups if s.user not in no_shows]
        
        prompt = U.make_embed(
            title="Complete Group Training",
            description=f"Please confirm the following users completed this group training.",
            fields=[
                EmbedField(
                    name="__Attendees__",
                    value=(
                        "* " + "\n* ".join([f"{a.name} ({a.user.name})" for a in self.attended_users])
                    ) if self.attended_users else "`None`",
                    inline=False
                ),
                EmbedField(
                    name="__No-Shows__",
                    value=(
                        "* " + "\n* ".join([f"{n.name} ({n.user.name})" for n in no_shows])
                    ) if no_shows else "`None`",
                    inline=False
                )
            ]
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return False
        
        prompt = U.make_embed(
            title="Please Wait...",
            description="Completing group training. This will take a moment..."
        )
        please_wait = await interaction.respond(embed=prompt)
    
        if self.positions:
            completion_embed = U.make_embed(
                title="Training Complete",
                description=(
                    f"Congratulations! You have completed your training for\n"
                    f"the position(s) of `{self.pos_string}`!\n\n"
        
                    "__**You are now ready to take on your new role(s)!**__\n\n"
        
                    "Visit the server and use the `/trainee match` command to find venues "
                    "who can offer you a temporary internship! (The goal of these is to give "
                    "you on-site training without any risk or obligation on your part.)\n\n"
        
                    "Additionally, you need to run the `/staffing profile` "
                    "command to set up your profile! (Follow the instructions "
                    "at https://discord.com/channels/1104515062187708525/1219788797223374938 "
                    "to get started!)"
                ),
            )
        else:
            completion_embed = U.make_embed(
                title="Training Complete",
                description=(
                    f"Congratulations! You have completed your general skill training!\n\n"
                    
                    "We hope you found the training helpful and informative!"
                ),
            )
        role_list = [pos.linked_role for pos in self.positions]
        
        for trainee in self.attended_users:
            await trainee.send(embed=completion_embed)
            self.trainer._pay_requested = False
            
            if self.positions:
                await self._mgr.guild.role_manager.add_role(trainee.user, RoleType.StaffMain)
                if trainee.profile and trainee.profile.post_message is not None:
                    for role in role_list:
                        await self._mgr.guild.role_manager.add_role_manual(trainee.user, role)
                        
                for training in trainee.trainings_as_trainee:
                    if training.position in self.positions and not training.is_complete:
                        await training.group_override()
        
        await self._mgr.guild.log.group_training_no_show_report(self, no_shows)
        await self._mgr.guild.log.group_training_complete_report(self, self._attended)
        
        self.is_completed = True
        
        try:
            await please_wait.delete()
        except NotFound:
            pass
        except Exception as ex:
            log.error("Training", f"Failed to delete 'Please Wait' message: {ex}")
            pass
        
        congrats = U.make_embed(
            title="Group Training Complete",
            description=f"The group training has been completed. {str(BotEmojis.Party)}"
        )
        await interaction.respond(embed=congrats)
        
        log.info("Training", "Group training completed successfully, scheduling deletion.")
        await self.post_message.delete()

        log.info("Training", "Group training post deleted successfully.")
        
        return True
    
################################################################################
        