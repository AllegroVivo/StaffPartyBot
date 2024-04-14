from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Dict, List

from discord import User, Interaction, Embed, EmbedField, Message, NotFound

from Assets import BotEmojis
from UI.Common import ConfirmCancelView
from UI.Jobs import (
    JobDescriptionModal,
    PositionSelectView,
    JobPostingStatusView,
    SalaryFrequencySelectView,
    SalaryModal,
    JobPostingTypeView,
    TimezoneSelectView,
    JobPostingTimesModal,
    JobPostingPickupView,
)
from Utilities import (
    Utilities as U,
    JobPostingType,
    RateType,
    PostingNotCompleteError,
    DateTimeFormatError,
    DateTimeMismatchError,
    TimeRangeError,
    DateTimeBeforeNowError,
    IneligibleForJobError,
    CannotEditPostingError,
)
from .PayRate import PayRate

if TYPE_CHECKING:
    from Classes import JobsManager, Position, Venue, TrainingBot, TUser
################################################################################

__all__ = ("JobPosting",)

JP = TypeVar("JP", bound="JobPosting")

################################################################################
class JobPosting:
    
    __slots__ = (
        "_id",
        "_mgr",
        "_venue",
        "_user",
        "_type",
        "_position",
        "_salary",
        "_start",
        "_end",
        "_description",
        "_post_msg",
        "_candidate",
        "_rejections",
    )
    
################################################################################
    def __init__(self, mgr: JobsManager, **kwargs) -> None:
        
        self._mgr: JobsManager = mgr
        
        self._id: str = kwargs.pop("_id")
        self._venue: Venue = kwargs.pop("venue")
        self._user: User = kwargs.pop("user")
        self._candidate: Optional[TUser] = kwargs.pop("tuser", None)
        self._rejections: List[TUser] = []
        
        self._description: Optional[str] = kwargs.pop("description", None)
        self._type: Optional[JobPostingType] = JobPostingType.Temporary
        self._position: Optional[Position] = kwargs.pop("position", None)
        self._post_msg: Optional[Message] = kwargs.pop("post_msg", None)
        
        self._salary: PayRate = kwargs.pop("salary", None) or PayRate(self)
        self._start: Optional[datetime] = kwargs.pop("start", None)
        self._end: Optional[datetime] = kwargs.pop("end", None)
        
################################################################################
    @classmethod
    def new(cls: Type[JP], mgr: JobsManager, venue: Venue, user: User) -> JP:
        
        new_id = mgr.bot.database.insert.job_posting(mgr.guild_id, venue.id, user.id)
        return cls(mgr, _id=new_id, venue=venue, user=user)
    
################################################################################
    @classmethod
    async def load(cls: Type[JP], mgr: JobsManager, record: Dict[str, Any]) -> JP:
        
        data = record["data"]
        
        self: JP = cls.__new__(cls)
        
        self._mgr = mgr
        
        self._id = data[0]
        self._venue = mgr.guild.venue_manager[data[2]]
        self._user = await mgr.bot.get_or_fetch_user(data[3])
        self._candidate = mgr.guild.training_manager[data[13]] if data[13] else None
        self._rejections = [mgr.guild.training_manager[r] for r in data[14]] if data[14] else []
        
        self._description = data[6]
        self._type = JobPostingType.Temporary
        self._position = mgr.guild.position_manager.get_position(data[5]) if data[5] else None

        self._post_msg = None
        if data[10] is not None:
            url_parts = data[10].split("/")
            channel = await mgr.bot.get_or_fetch_channel(int(url_parts[-2]))
            if channel is not None:
                try:
                    self._post_msg = await channel.fetch_message(int(url_parts[-1]))  # type: ignore
                except:
                    pass

        self._salary = PayRate(self, data[7], RateType(data[8]) if data[8] else None, data[9])
        self._start = data[11]
        self._end = data[12]
        
        try:
            await self._update_posting()
        except:
            pass
        
        return self
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._mgr.bot
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._mgr.guild_id
    
################################################################################
    @property
    def user(self) -> User:
        
        return self._user
    
################################################################################
    @property
    def venue(self) -> Venue:
        
        return self._venue
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def post_type(self) -> Optional[JobPostingType]:
        
        return self._type
    
    @post_type.setter
    def post_type(self, value: JobPostingType) -> None:
        
        self._type = value
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
    def position(self) -> Optional[Position]:
        
        return self._position
    
    @position.setter
    def position(self, value: Position) -> None:
        
        self._position = value
        self.update()
    
################################################################################    
    @property
    def post_message(self) -> Optional[Message]:
        
        return self._post_msg
    
    @post_message.setter
    def post_message(self, value: Optional[Message]) -> None:
        
        self._post_msg = value
        self.update()
        
################################################################################
    @property
    def candidate(self) -> Optional[TUser]:
        
        return self._candidate
    
    @candidate.setter
    def candidate(self, value: Optional[TUser]) -> None:
        
        self._candidate = value
        self.update()
        
################################################################################
    @property
    def salary(self) -> Optional[int]:
        
        return self._salary.amount
    
################################################################################    
    @property
    def frequency(self) -> Optional[RateType]:
        
        return self._salary.frequency
    
################################################################################    
    @property
    def pay_details(self) -> Optional[str]:
        
        return self._salary.details
    
################################################################################
    @property
    def start_time(self) -> Optional[datetime]:
        
        return self._start
        
################################################################################
    @property
    def end_time(self) -> Optional[datetime]:
        
        return self._end
        
################################################################################
    @property
    def complete(self) -> bool:
        
        return all(
            [self._position, self._salary, self._description, self.end_time]
        )
    
################################################################################
    @property
    def rejections(self) -> List[TUser]:
        
        return self._rejections
    
################################################################################
    @property
    def has_passed(self) -> bool:
        
        return (
            self._candidate is not None or 
            (
                self.end_time is not None and
                self.end_time.timestamp() <= datetime.now().timestamp()
            )
        )
    
################################################################################
    def update(self) -> None:

        self.bot.database.update.job_posting(self)
        
################################################################################
    async def delete(self) -> None:
        
        if self.post_message is not None:
            try:
                await self.post_message.delete()
            except:
                pass
            
        if self.candidate is not None:
            embed = U.make_embed(
                title="Job Posting Canceled",
                description=(
                    "The job posting you've accepted has been canceled by the venue.\n\n"
                    
                    "__**Position**__\n"
                    f"`{self.position.name}`\n"
                    f"*`({self.venue.name})`*\n\n"
                    
                    "If you have any questions or concerns, please reach out to the venue "
                )
            )
            await self.candidate.send(embed=embed)
        
        self._mgr._postings.remove(self)
        self.bot.database.delete.job_posting(self)
        
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        if self.has_passed:
            error = CannotEditPostingError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        embed = self.status()
        view = JobPostingStatusView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
    
################################################################################
    def status(self) -> Embed:

        job_desc = "`No description provided.`"
        if self.description:
            job_desc = U.wrap_text(self.description, 50)

        description = (
            "__**Venue Name:**__\n"
            f"`{self._venue.name}`\n\n"
            
            "__**Venue Contact:**__\n"
            f"`{self._user.name}`\n"
            f"({self._user.mention})\n\n"

            "__**Job Description:**__\n"
            f"{job_desc}\n\n"
            
            f"{U.draw_line(extra=30)}\n"
        )
        
        return U.make_embed(
            title=f"Job Posting Status",
            description=description,
            fields=[
                self._position_field(),
                self._salary_field(),
                self._hours_field(),
                self._total_time_field(),
                self._post_url_field(),
            ],
            footer_text=f"Posting ID: {self._id}",
        )
    
################################################################################
    def compile(self) -> Embed:
        
        job_desc = "`No description provided.`"
        if self.description is not None:
            job_desc = U.wrap_text(self.description, 50)

        description = (
            "__**Venue Contact:**__\n"
            f"`{self._user.name}`\n"
            f"({self._user.mention})\n\n"

            "__**Job Description:**__\n"
            f"{job_desc}\n"

            f"{U.draw_line(extra=30)}\n"
        )
        
        return U.make_embed(
            title=f"`{self.position.name}` needed at `{self._venue.name}`",
            description=description,
            fields=[
                self._position_field(),
                self._salary_field(),
                self._hours_field(),
            ],
            footer_text=f"Posting ID: {self._id}",
        )
    
################################################################################
    def _post_url_field(self) -> EmbedField:
        
        description = (
            f"{BotEmojis.ArrowRight}{BotEmojis.ArrowRight}{BotEmojis.ArrowRight} "
            f"[Click here to view the posting]({self.post_message.jump_url}) "
            f"{BotEmojis.ArrowLeft}{BotEmojis.ArrowLeft}{BotEmojis.ArrowLeft}"
        ) if self.post_message is not None else "`Not Posted`"

        return EmbedField(
            name="__Posting URL__",
            value=description,
            inline=False
        )

################################################################################
    def _position_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Position__",
            value=f"{self._position.name if self._position is not None else '`Not Set`'}",
            inline=True
        )
    
################################################################################
    def _salary_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Salary__",
            value=self._salary.format(),
            inline=False
        )
    
################################################################################
    def _hours_field(self) -> EmbedField:
        
        start_ts = (
            U.format_dt(self.start_time, "F") if self.start_time is not None
            else "`Not Set`"
        )
        end_ts = (
            U.format_dt(self.end_time, "F") if self.end_time is not None
            else "`Not Set`"
        )
        
        return EmbedField(
            name="__Start Time__",
            value=(
                f"{start_ts}\n\n"
                
                f"__**End Time**__\n"
                f"{end_ts}\n"
                f"{U.draw_line(extra=12)}"
            ),
            inline=True
        )
    
################################################################################
    def _total_time_field(self) -> EmbedField:
        
        if self.start_time is not None and self.end_time is not None:
            delta = self.end_time - self.start_time
            hours = delta.total_seconds() / 3600
            field_value = f"`{hours:.2f} hours`"
        else:
            field_value = "`Invalid Time Range`"
        
        return EmbedField(
            name="__Total Time__",
            value=field_value,
            inline=True
        )
    
################################################################################
    async def set_description(self, interaction: Interaction) -> None:
        
        modal = JobDescriptionModal(self.description)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.description = modal.value
    
################################################################################
    async def set_position(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Job Posting Position",
            description="Please select a position for this job posting.",
        )
        view = PositionSelectView(
            interaction.user, self._mgr.guild.position_manager.select_options()
        )
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.position = self._mgr.guild.position_manager.get_position(view.value)
    
################################################################################
    async def set_salary(self, interaction: Interaction) -> None:
        
        explanation = U.make_embed(
            title="Set Job Posting Salary",
            description=(
                "__**READ THIS CAREFULLY**__\n\n"
            
                "Please provide the salary for this job posting.\n\n"
                "For the purposes of data collection and display, the salary will be "
                "collected as three different values in this order:\n\n"
                
                "1. The frequency at which the salary is paid.\n"
                "2. The amount of the salary.\n"
                "3. Any additional details about the salary.\n\n"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=explanation, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        freq_prompt = U.make_embed(
            title="Set Salary Frequency",
            description="Please select the frequency at which the salary is paid.",
        )
        view = SalaryFrequencySelectView(interaction.user)
        
        await interaction.respond(embed=freq_prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        frequency, inter = view.value
        
        modal = SalaryModal(self.salary, self.pay_details)
        
        await inter.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        rate, details, inter = modal.value
        
        self._salary = PayRate(self, rate, frequency, details)
        self.update()
    
################################################################################
    async def set_posting_type(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Job Posting Type",
            description="Please select a type for this job posting.",
        )
        view = JobPostingTypeView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.post_type = view.value
    
################################################################################
    async def set_schedule(self, interaction: Interaction) -> None:
    
        prompt = U.make_embed(
            title="Set Job Posting Schedule",
            description=(
                "You'll now be given an opportunity to enter the start and end "
                "times for this job posting.\n\n"
                
                "You can begin this process by selecting the timezone that will "
                "correspond to your entries from the selector below."
            ),
        )
        view = TimezoneSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        timezone, inter = view.value
        modal = JobPostingTimesModal(self.start_time, self.end_time)
        
        await inter.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        raw_start, raw_end = modal.value
        
        try:
            start_temp = datetime.strptime(raw_start, "%m/%d/%Y %I:%M %p")
        except ValueError:
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
            error = DateTimeMismatchError(start_time, end_time)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if datetime.now().timestamp() > end_time.timestamp():
            error = DateTimeBeforeNowError(start_time)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if (end_time - start_time).total_seconds() < 7200:
            error = TimeRangeError("2 Hours")
            await interaction.respond(embed=error, ephemeral=True)
            return
            
        self._start = start_time
        self._end = end_time
        
        self.update()
        
################################################################################
    async def create_post(self, interaction: Interaction) -> None:

        if not self.complete:
            error = PostingNotCompleteError()
            await interaction.respond(embed=error, ephemeral=True)
            return
    
        if self.post_message is not None and await self._update_posting():
            confirm = U.make_embed(
                title="Job Posting Updated",
                description="The job posting has been updated."
            )
            await interaction.respond(embed=confirm, ephemeral=True)
            return
    
        confirm = U.make_embed(
            title="Post Job Listing",
            description="Are you sure you want to post this job listing?"
        )
        view = ConfirmCancelView(interaction.user)
        await interaction.respond(embed=confirm, view=view)
        await view.wait()
    
        if not view.complete or view.value is False:
            return
    
        post_view = JobPostingPickupView(self)
        self.bot.add_view(post_view)
        
        channel = (
            self._mgr.temporary_jobs_channel 
            if self.post_type == JobPostingType.Temporary 
            else self._mgr.permanent_jobs_channel
        )
        pos_thread = next(
            (t for t in channel.threads if t.name == self.position.name), None
        ) if channel is not None else None
    
        try:
            if pos_thread:
                self.post_message = await pos_thread.send(embed=self.compile(), view=post_view)
            else:
                pos_thread = await channel.create_thread(name=self.position.name, embed=self.compile(), view=post_view)
                self.post_message = pos_thread.last_message
            
            confirm = U.make_embed(
                title="Job Posting Created/Updated",
                description=(
                    f"The job posting has been created/updated. "
                    f"`ID: {self._id}`"
                )
            )
            
            await interaction.respond(embed=confirm, ephemeral=True)
        except:
            error = U.make_embed(
                title="Posting Error",
                description="There was an error posting the job listing."
            )
            await interaction.respond(embed=error, ephemeral=True)
        else:
            await self._mgr.guild.log.temp_job_posted(self)
            await self.notify_eligible_applicants()

################################################################################
    async def _update_posting(self) -> bool:
        
        try:
            view = JobPostingPickupView(self)
            self.bot.add_view(view, message_id=self._post_msg.id)
            await self._post_msg.edit(embed=self.compile(), view=view)
        except:
            self.post_message = None
            return False
        else:
            return True
        
################################################################################
    async def notify_eligible_applicants(self) -> None:
        
        eligible = [
            tuser for tuser in self._mgr.guild.training_manager.tusers 
            if await tuser.is_eligible(self)
        ]
        if not eligible:
            return
        
        embed = U.make_embed(
            title="Job Posting Alert",
            description=(
                f"An opportunity has been posted for a `{self.position.name}` position at "
                f"`{self._venue.name}`. If you're interested, you can [view the posting "
                f"here]({self.post_message.jump_url})."
            )
        )
        
        for tuser in eligible:
            try:
                await tuser.user.send(embed=embed)
            except:
                continue
            
################################################################################
    async def candidate_accept(self, interaction: Interaction) -> None:
        
        tuser = self._mgr.guild.training_manager[interaction.user.id]
        if not tuser or not await tuser.is_eligible(
            self, 
            compare_hiatus=False, 
            compare_data_centers=False,
            compare_linked_role=True, 
            compare_schedule=False, 
            check_profile=True
        ):
            error = IneligibleForJobError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        self.candidate = tuser
        await self._update_posting()
        await interaction.edit()
        
        notify = U.make_embed(
            title="Job Accepted",
            description=(
                f"__**Position**__\n\n"
                f"`{self.position.name}`\n"
                f"*({self.venue.name})*\n\n"
                
                f"__**Picked Up By**__\n\n"
                f"`{self.candidate.name}`\n"
                f"{self.candidate.user.mention}\n"
            )
        )
        
        try:
            await self._user.send(embed=notify)
        except:
            pass
        
        await self._mgr.guild.log.temp_job_accepted(self)
    
################################################################################
    async def cancel(self, interaction: Optional[Interaction] = None) -> None:
        
        if self.candidate is None:
            return
        
        # Log before removing the candidate
        await self._mgr.guild.log.temp_job_canceled(self)
        
        self.candidate = None
        await self._update_posting()
        
        if interaction is not None:
            await interaction.edit()
            
        notify = U.make_embed(
            title="Job Canceled",
            description=(
                f"__**Position**__\n\n"
                f"`{self.position.name}`\n"
                f"*({self.venue.name})*\n\n"
                
                "The previous candidate has removed themself from this job posting.\n\n"
                
                "For your convenience, the posting has been re-activated and "
                "is now available for other applicants to accept."
            )
        )
        
        try:
            await self._user.send(embed=notify)
        except:
            pass
        
################################################################################
    async def reject(self, interaction: Interaction) -> None:
        
        tuser = self._mgr.guild.training_manager[interaction.user.id]
        if not tuser or not await tuser.is_eligible(
            self, False, False, True, False
        ):
            error = IneligibleForJobError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if tuser == self.candidate:
            await self.cancel(interaction)
        
        self._rejections.append(tuser)
        self.update()
        
        confirm = U.make_embed(
            title="Rejection Recorded",
            description="Thanks for helping us keep our statistics up to date!"
        )
        
        await interaction.respond(embed=confirm, ephemeral=True)

################################################################################
    async def expiration_check(self) -> None:
        
        if self.end_time is not None and self.end_time.timestamp() <= datetime.now().timestamp():
            await self.delete()

################################################################################
