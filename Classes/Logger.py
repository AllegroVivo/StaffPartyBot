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
    User,
    EmbedField,
    Message
)
from Assets import BotEmojis
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
    async def _log(self, message: Embed, action: LogType, **kwargs) -> Optional[Message]:

        if self.log_channel is None:
            return

        try:
            message.colour = LOG_COLORS[action]
        except KeyError:
            print(f"Invalid action passed to LOG_COLORS: '{action}'")
            message.colour = Colour.embed_background()

        return await self.log_channel.send(embed=message, **kwargs)
       
################################################################################
    async def member_join(self, member: Member) -> None:

        tuser = self._guild.bot[member.guild.id].training_manager[member.id]

        qualifications = trainings = "`None`"
        if tuser is not None:
            qualifications = "* " + "\n* ".join(
                [f"{q.position.name}" for q in tuser.qualifications]
            )
            trainings = "* " + "\n* ".join(
                [f"{t.position.name}" for t in tuser.trainings_as_trainee]
            )

        embed = U.make_embed(
            title=f"Member Joined!",
            description=f"{member.mention} has joined the server!",
            fields=[
                ("__Owned Qualifications__", qualifications, True),
                ("__Requested Trainings__", trainings, True)
            ],
            thumbnail_url=member.display_avatar.url,
            timestamp=True
        )

        await self._log(embed, LogType.MemberJoin)

################################################################################
    async def member_left(
        self,
        member: Member,
        venue_deleted: bool,
        profile_deleted: bool,
        trainings_modified: int,
        trainings_deleted: int,
        jobs_deleted: int,
        jobs_canceled: int,
    ) -> None:

        tuser = self._guild.bot[member.guild.id].training_manager[member.id]

        qualifications = trainings = "`None`"
        if tuser is not None:
            qualifications = "* " + "\n* ".join(
                [f"{q.position.name}" for q in tuser.qualifications]
            )
            trainings = "* " + "\n* ".join(
                [f"{t.position.name}" for t in tuser.trainings_as_trainee]
            )

        venue_emoji = BotEmojis.Check if venue_deleted else BotEmojis.Cross
        profile_emoji = BotEmojis.Check if profile_deleted else BotEmojis.Cross

        embed = U.make_embed(
            title=f"Member Left!",
            description=f"{member.mention} has left the server!",
            fields=[
                ("__Owned Qualifications__", qualifications, True),
                ("__Requested Trainings__", trainings, True),
                ("** **", "** **", False),
                ("__Trainings Reassigned__", f"`{trainings_modified}`", True),
                ("__Trainings Deleted__", f"`{trainings_deleted}`", True),
                ("** **", "** **", False),
                ("__Jobs Deleted__", f"`{jobs_deleted}`", True),
                ("__Jobs Re-Opened__", f"`{jobs_canceled}`", True),
                ("** **", "** **", False),
                ("__Venue Deleted__", str(venue_emoji), True),
                ("__Profile Deleted__", str(profile_emoji), True)
            ],
            thumbnail_url=member.display_avatar.url,
            timestamp=True
        )

        await self._log(embed, LogType.MemberLeave)

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
                
                f"__Managers:__\n"
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
    async def bg_check_submitted(self, bg_check: BackgroundCheck) -> Message:
        
        embed = U.make_embed(
            title="Background Check Submitted!",
            fields=[
                EmbedField(
                    name="__Names__",
                    value="* " + ("\n* ".join(bg_check.names)),
                    inline=True
                ),
                EmbedField(
                    name="__Want to Train__",
                    value=(
                        str(BotEmojis.Check) if bg_check._prev_exp
                        else str(BotEmojis.Cross)
                    ),
                    inline=True
                ),
                EmbedField(
                    name="__Venue Experience__",
                    value="\n".join([f'* {v.format()}' for v in bg_check.venues]),
                    inline=False
                )
            ],
            timestamp=True
        )
        view = BGCheckApprovalView(bg_check)

        return await self._log(embed, LogType.BGCheckSubmitted, view=view)

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
