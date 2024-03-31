from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Dict, Optional

from discord import Interaction, ForumChannel, NotFound, ChannelType, ForumTag

from Utilities import (
    Utilities as U,
    VenueDoesntExistError, 
    JobPostingNotFoundError, 
    ChannelTypeError, 
    JobPostingType
)
from .JobPosting import JobPosting

if TYPE_CHECKING:
    from Classes import GuildData, TrainingBot, VenueManager
################################################################################

__all__ = ("JobsManager",)

################################################################################
class JobsManager:
    
    __slots__ = (
        "_guild",
        "_postings",
        "_temp_channel",
        "_perm_channel"
    )
    
################################################################################
    def __init__(self, guild: GuildData):
        
        self._guild: GuildData = guild
        
        self._postings: List[JobPosting] = []
        
        self._temp_channel: Optional[ForumChannel] = None
        self._perm_channel: Optional[ForumChannel] = None
        
################################################################################
    async def _load_all(self, data: Dict[str, Any]) -> None:
        
        temp_channel_id = data["bot_config"][5]
        if temp_channel_id is not None:
            try:
                self._temp_channel = await self._guild.bot.get_or_fetch_channel(temp_channel_id)
            except NotFound:
                self.update()

        perm_channel_id = data["bot_config"][6]
        if perm_channel_id is not None:
            try:
                self._perm_channel = await self._guild.bot.get_or_fetch_channel(perm_channel_id)
            except NotFound:
                self.update()
        
        for _, posting in data["job_postings"].items():
            self._postings.append(await JobPosting.load(self, posting))
            
################################################################################
    def get_posting(self, post_id: str) -> Optional[JobPosting]:
        
        for posting in self._postings:
            if posting.id == post_id:
                return posting
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._guild.bot
    
################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._guild
    
################################################################################
    @property
    def venue_manager(self) -> VenueManager:
        
        return self._guild.venue_manager
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._guild.guild_id
    
################################################################################
    @property
    def all_postings(self) -> List[JobPosting]:
        
        return self._postings
    
################################################################################
    @property
    def temporary_jobs_channel(self) -> Optional[ForumChannel]:
        
        return self._temp_channel
    
    @temporary_jobs_channel.setter
    def temporary_jobs_channel(self, value: Optional[ForumChannel]) -> None:
        
        self._temp_channel = value
        self.update()
        
################################################################################
    @property
    def permanent_jobs_channel(self) -> Optional[ForumChannel]:
        
        return self._perm_channel
    
    @permanent_jobs_channel.setter
    def permanent_jobs_channel(self, value: Optional[ForumChannel]) -> None:
        
        self._perm_channel = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.job_posting_channels(self)
        
################################################################################
    async def create_new(self, interaction: Interaction, venue_name: str) -> None:

        venue = self.venue_manager.get_venue(venue_name)
        if venue is None:
            error = VenueDoesntExistError(venue_name)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        if not await self.venue_manager.authenticate(venue, interaction.user, interaction):
            return
        
        posting = JobPosting.new(self, venue, interaction.user)
        self._postings.append(posting)
        
        await posting.menu(interaction)
    
################################################################################
    async def check_status(self, interaction: Interaction, post_id: str) -> None:
        
        posting = self.get_posting(post_id)
        if posting is None:
            error = JobPostingNotFoundError(post_id)
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await posting.menu(interaction)
        
################################################################################
    async def set_jobs_channel(
        self, 
        interaction: Interaction, 
        channel: ForumChannel,
        post_type: int
    ) -> None:
        
        if channel.type is not ChannelType.forum:
            error = ChannelTypeError(channel, "ForumChannel")
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        post_type = JobPostingType(post_type)
        match post_type:
            case JobPostingType.Temporary:
                self.temporary_jobs_channel = channel
            case JobPostingType.Permanent:
                self.permanent_jobs_channel = channel
            case _:
                raise ValueError(f"Invalid JobPostingType: {post_type}")
        
        confirm = U.make_embed(
            title="Job Posting Channel Set",
            description=(
                f"The jobs posting channel for `{post_type.proper_name}` job "
                f"posts has been set to {channel.mention}."
            )
        )
        
        await interaction.respond(embed=confirm, ephemeral=True)
        
################################################################################
