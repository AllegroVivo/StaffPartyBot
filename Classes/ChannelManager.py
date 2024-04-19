from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Tuple

from discord import (
    Interaction,
    Embed,
    EmbedField,
    TextChannel,
    ForumChannel,
)

from UI.Guild import ChannelStatusView
from Utilities import Utilities as U, MentionableType, ChannelPurpose

if TYPE_CHECKING:
    from Classes import GuildData, TrainingBot
################################################################################

__all__ = ("ChannelManager",)

################################################################################
class ChannelManager:

    __slots__ = (
        "_guild",
        "_temp_job",
        "_perm_job",
        "_venues",
        "_profiles",
        "_log",
        "_services",
    )

################################################################################
    def __init__(self, guild: GuildData):

        self._guild: GuildData = guild

        self._temp_job: Optional[ForumChannel] = None
        self._perm_job: Optional[ForumChannel] = None
        self._venues: Optional[ForumChannel] = None
        self._profiles: Optional[ForumChannel] = None
        self._log: Optional[TextChannel] = None
        self._services: Optional[ForumChannel] = None
    
################################################################################
    async def _load_all(self, data: Tuple[Any, ...]) -> None:
        
        self._temp_job = await self._guild.get_or_fetch_channel(data[1])
        self._perm_job = await self._guild.get_or_fetch_channel(data[2])
        self._venues = await self._guild.get_or_fetch_channel(data[3])
        self._profiles = await self._guild.get_or_fetch_channel(data[4])
        self._log = await self._guild.get_or_fetch_channel(data[5])
        self._services = await self._guild.get_or_fetch_channel(data[6])
        
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
    def temp_job_channel(self) -> Optional[ForumChannel]:
        
        return self._temp_job
    
    @temp_job_channel.setter
    def temp_job_channel(self, channel: Optional[ForumChannel]) -> None:
        
        self._temp_job = channel
        self.update()
        
################################################################################
    @property
    def perm_job_channel(self) -> Optional[ForumChannel]:
        
        return self._perm_job
    
    @perm_job_channel.setter
    def perm_job_channel(self, channel: Optional[ForumChannel]) -> None:
        
        self._perm_job = channel
        self.update()
        
################################################################################
    @property
    def venues_channel(self) -> Optional[ForumChannel]:
        
        return self._venues
    
    @venues_channel.setter
    def venues_channel(self, channel: Optional[ForumChannel]) -> None:
        
        self._venues = channel
        self.update()
        
################################################################################
    @property
    def profiles_channel(self) -> Optional[ForumChannel]:
        
        return self._profiles
    
    @profiles_channel.setter
    def profiles_channel(self, channel: Optional[ForumChannel]) -> None:
        
        self._profiles = channel
        self.update()
        
################################################################################
    @property
    def log_channel(self) -> Optional[TextChannel]:
        
        return self._log
    
    @log_channel.setter
    def log_channel(self, channel: Optional[TextChannel]) -> None:
        
        self._log = channel
        self.update()
        
################################################################################
    @property
    def services_channel(self) -> Optional[ForumChannel]:
        
        return self._services
    
    @services_channel.setter
    def services_channel(self, channel: Optional[ForumChannel]) -> None:
        
        self._services = channel
        self.update()
        
################################################################################
    def update(self) -> None:
    
        self.bot.database.update.channels(self)
        
################################################################################
    def status(self) -> Embed:

        fields = [
            EmbedField(
                name="__Log Stream__",
                value=self.log_channel.mention if self.log_channel else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Staff Profiles__",
                value=self.profiles_channel.mention if self.profiles_channel else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Venue Profiles__",
                value=self.venues_channel.mention if self.venues_channel else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Temporary Jobs__",
                value=self.temp_job_channel.mention if self.temp_job_channel else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Permanent Jobs__",
                value=self.perm_job_channel.mention if self.perm_job_channel else "`Not Set`",
                inline=False
            ),
            EmbedField(
                name="__Hireable Services__",
                value=self.services_channel.mention if self.services_channel else "`Not Set`",
                inline=False
            ),
        ]

        return U.make_embed(
            title="__Channels Status__",
            description=U.draw_line(extra=25),
            fields=fields
        )
        
################################################################################
    async def menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = ChannelStatusView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
################################################################################
    async def set_channel(self, interaction: Interaction, _type: ChannelPurpose) -> None:

        prompt = U.make_embed(
            title="Edit Channel",
            description=(
                "**THE BOT IS NOW LISTENING**\n\n"

                "Please enter a mention for the channel you'd like to link.\n"
                f"{U.draw_line(extra=33)}\n"
                "*(Type 'Cancel' to cancel this operation.)*"
            )
        )

        channel = await U.listen_for_mentionable(interaction, prompt, MentionableType.Channel)
        if channel is None:
            return

        match _type:
            case ChannelPurpose.Venues:
                self.venues_channel = channel
            case ChannelPurpose.Profiles:
                self.profiles_channel = channel
            case ChannelPurpose.LogStream:
                self.log_channel = channel
            case ChannelPurpose.TempJobs:
                self.temp_job_channel = channel
            case ChannelPurpose.PermJobs:
                self.perm_job_channel = channel
            case ChannelPurpose.Services:
                self.services_channel = channel
            case _:
                raise ValueError(f"Invalid ChannelPurpose: {_type}")
        
        embed = U.make_embed(
            title="Channel Set!",
            description=f"The channel has been set to {channel.mention}!"  # type: ignore
        )
        await interaction.respond(embed=embed, ephemeral=True)
        
################################################################################
