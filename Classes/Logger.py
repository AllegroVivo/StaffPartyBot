from __future__ import annotations

import os

from dotenv import load_dotenv
from typing import TYPE_CHECKING, Optional

from UI.Guild import BGCheckApprovalView
from discord import (
    Interaction,
    TextChannel,
    Embed,
    Colour,
    Member,
    NotFound,
    Forbidden,
    User
)

from Utilities import Utilities as U, ChannelTypeError, LOG_COLORS, LogType

if TYPE_CHECKING:
    from Classes import *
################################################################################

__all__ = ("Logger",)

################################################################################
class Logger:

    __slots__ = (
        "_guild",
        "_alyah",
    )
    
    ALYAH = 334530475479531520

################################################################################
    def __init__(self, state: GuildData) -> None:

        self._guild: GuildData = state
        self._alyah: User = None  # type: ignore

################################################################################
    async def load(self) -> None:

        self._alyah = await self._guild.bot.fetch_user(self.ALYAH)
        
################################################################################
    @property
    def log_channel(self) -> Optional[TextChannel]:

        return self._guild.channel_manager.log_channel

################################################################################
    async def _log(self, message: Embed, action: LogType, **kwargs) -> None:

        if self.log_channel is None:
            return

        try:
            message.colour = LOG_COLORS[action]
        except KeyError:
            print(f"Invalid action passed to LOG_COLORS: '{action}'")
            message.colour = Colour.embed_background()

        await self.log_channel.send(embed=message, **kwargs)
       
################################################################################
    async def _member_event(self, member: Member, _type: LogType) -> None:

        tuser = self._guild.bot[member.guild.id].training_manager[member.id]
        
        qualifications = trainings = "`None`"
        if tuser is not None:
            qualifications = "* " + "\n* ".join(
                [f"{q.position.name}" for q in tuser.qualifications]
            )
            trainings = "* " + "\n* ".join(
                [f"{t.position.name}" for t in tuser.trainings_as_trainee]
            )

        word = "joined" if _type == LogType.MemberJoin else "left"
        embed = U.make_embed(
            title=f"Member {word.title()}!",
            description=f"{member.mention} has {word} the server!",
            fields=[
                ("__Owned Qualifications__", qualifications, True),
                ("__Requested Trainings__", trainings, True)
            ],
            thumbnail_url=member.display_avatar.url,
            timestamp=True
        )

        await self._log(embed, _type)

################################################################################
    async def member_join(self, member: Member) -> None:

        await self._member_event(member, LogType.MemberJoin)

################################################################################
    async def member_left(self, member: Member) -> None:

        await self._member_event(member, LogType.MemberLeave)

################################################################################
    async def training_signup(self, training: Training) -> None:

        embed = U.make_embed(
            title="Training Signup!",
            description=(
                f"{training.trainee.user.mention} has signed up for "
                f"`{training.position.name}` training!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.TrainingSignup)
        
################################################################################
    async def training_removed(self, training: Training) -> None:

        embed = U.make_embed(
            title="Training Removed!",
            description=(
                f"{training.trainee.user.mention} has canceled their request for "
                f"`{training.position.name}` training!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.TrainingRemoved)
        
################################################################################
    async def training_matched(self, training: Training) -> None:

        embed = U.make_embed(
            title="Trainer Assigned!",
            description=(
                f"{training.position.name} training for `{training.trainee.name}` has been\n"
                f"matched to `{training.trainer.name}` ({training.trainer.user.mention})!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.TrainerAssigned)
        
################################################################################
    async def training_completed(self, training: Training) -> None:

        embed = U.make_embed(
            title="Training Completed!",
            description=(
                f"{training.position.name} training for `{training.trainee.name}` has been\n"
                f"completed by `{training.trainer.name}`!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.TrainingCompleted)

################################################################################
    async def tuser_hiatus(self, tuser: TUser) -> None:
        
        embed = U.make_embed(
            title="TUser Hiatus!",
            description=(
                f"{tuser.name} has __{'entered' if tuser.on_hiatus else 'exited'}__ "
                f"hiatus status!"
            ),
            timestamp=True
        )
        
        await self._log(embed, LogType.UserHiatus)
        
################################################################################
    async def venue_user_added(self, venue: Venue, user: User) -> None:

        embed = U.make_embed(
            title="Venue User Added!",
            description=(
                f"{user.mention} is now authorized to access `{venue.name}`!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.VenueUserAdded)
        
################################################################################
    async def venue_user_removed(self, venue: Venue, user: User) -> None:

        embed = U.make_embed(
            title="Venue User Removed!",
            description=(
                f"{user.mention} has been removed from the authorized "
                f"list for `{venue.name}`!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.VenueUserRemoved)
        
################################################################################
    async def venue_created(self, venue: Venue) -> None:

        users = "\n".join(
            [f"* {u.mention}" for u in venue.authorized_users]
        )

        embed = U.make_embed(
            title="Venue Created!",
            description=(
                f"New venue `{venue.name}` has been created!\n\n"
                
                f"__Proposed Users:__\n"
                f"{users}"
                
            ),
            timestamp=True
        )

        await self._log(embed, LogType.VenueCreated)
        if os.getenv("DEBUG") == "False":
            await self._alyah.send(embed=embed)
        
################################################################################
    async def venue_removed(self, venue: Venue) -> None:

        embed = U.make_embed(
            title="Venue Removed!",
            description=(
                f"Venue `{venue.name}` has been removed from the system!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.VenueRemoved)
            
################################################################################
    async def temp_job_posted(self, job: JobPosting) -> None:

        embed = U.make_embed(
            title="Temporary Job Posted!",
            description=(
                f"New temporary job posting for `{job.position.name}` has "
                f"been posted by `{job.venue.name}`!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.TempJobPosted)
        
################################################################################
    async def temp_job_accepted(self, job: JobPosting) -> None:

        embed = U.make_embed(
            title="Temporary Job Accepted!",
            description=(
                f"Temporary job posting for `{job.position.name}` at "
                f"`{job.venue.name}` has been accepted by `{job.candidate.name}`!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.TempJobAccepted)
        
################################################################################
    async def temp_job_canceled(self, job: JobPosting) -> None:

        embed = U.make_embed(
            title="Temporary Job Rejected!",
            description=(
                f"Temporary job posting for `{job.position.name}` at "
                f"`{job.venue.name}` has been canceled by `{job.candidate.name}`!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.TempJobCanceled)

################################################################################
    async def bg_check_submitted(self, bg_check: BackgroundCheck) -> None:
        
        venue_string = "\n".join([f'* {v.format()}' for v in bg_check.venues])
        embed = U.make_embed(
            title="Background Check Submitted!",
            description=(
                f"A background check for `{bg_check.names[0]}` has been submitted!\n"
                f"{U.draw_line(extra=25)}\n"
                f"__Venues:__\n"
                f"{venue_string}"
            ),
            timestamp=True
        )
        view = BGCheckApprovalView(bg_check)

        await self._log(embed, LogType.BGCheckSubmitted, view=view)

################################################################################
    async def bg_check_approved(self, bg_check: BackgroundCheck) -> None:

        embed = U.make_embed(
            title="Background Check Approved!",
            description=(
                f"Background check for `{bg_check.names[0]}` has been approved!"
            ),
            timestamp=True
        )

        await self._log(embed, LogType.BGCheckApproved)
        
################################################################################
