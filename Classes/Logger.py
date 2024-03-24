from __future__ import annotations

import os

from dotenv import load_dotenv
from typing import TYPE_CHECKING, Optional

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
    from Classes import Training, TUser, GuildData, Venue
################################################################################

__all__ = ("Logger",)

################################################################################
class Logger:

    __slots__ = (
        "_guild",
        "_channel",
        "_alyah",
    )
    
    ALYAH = 334530475479531520

################################################################################
    def __init__(self, state: GuildData) -> None:

        self._guild: GuildData = state
        
        self._channel: Optional[TextChannel] = None
        self._alyah: User = None  # type: ignore

################################################################################
    async def load(self, data: Optional[int]) -> None:

        if data is None:
            self._channel = None
        else:
            try:
                self._channel = await self._guild.bot.fetch_channel(data)
            except (NotFound, Forbidden):
                self._channel = None

        self._alyah = await self._guild.bot.fetch_user(self.ALYAH)
        
################################################################################
    @property
    def log_channel(self) -> Optional[TextChannel]:

        return self._channel

################################################################################
    async def set_log_channel(self, interaction: Interaction, channel: TextChannel) -> None:

        if not isinstance(channel, TextChannel):
            embed = ChannelTypeError(channel, "TextChannel")
        else:
            self._channel = channel
            self.update(interaction.guild_id)
            embed = U.make_embed(
                title="Log Channel Set!",
                description=f"Log channel has been set to {channel.mention}!"
            )

        await interaction.respond(embed=embed)

################################################################################
    def update(self, guild_id: int) -> None:

        self._guild.bot.database.update.log_channel(
            guild_id, self.log_channel.id if self.log_channel else None
        )

################################################################################
    async def _log(self, message: Embed, action: LogType) -> None:

        if self.log_channel is None:
            return

        try:
            message.colour = LOG_COLORS[action]
        except KeyError:
            print(f"Invalid action passed to LOG_COLORS: '{action}'")
            message.colour = Colour.embed_background()

        await self.log_channel.send(embed=message)
       
################################################################################
    async def _member_event(self, member: Member, _type: LogType) -> None:

        tuser = self._guild.bot[member.guild.id].training_manager[member.id]
        
        qualifications = trainings = "`None`"
        if tuser is not None:
            qualifications = "* " + "\n* ".join([f"{q.position.name}" for q in tuser.qualifications])
            trainings = "* " + "\n* ".join([f"{t.position.name}" for t in tuser.trainings_as_trainee])

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
            [f"* {u.mention}" for u in venue.owners] +
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
    async def owner_removal_flagged(self, venue: Venue, user: User, instigator: User) -> None:

        embed = U.make_embed(
            title="Owner Removal Flagged!",
            description=(
                f"{user.mention} has been flagged for removal as an "
                f"owner of `{venue.name}` by {instigator.mention}!\n\n"
                
                "Please head to the server and review the request."
            ),
            timestamp=True
        )

        await self._log(embed, LogType.OwnerRemovalFlagged)
        if os.getenv("DEBUG") == "False":
            await self._alyah.send(embed=embed)
        
################################################################################
