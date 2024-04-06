from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from discord import Guild, User, Interaction, Role, Embed, EmbedField
from discord.abc import GuildChannel

from Classes.Jobs.JobsManager import JobsManager
from Classes.Logger import Logger
from Classes.Positions.PositionManager import PositionManager
from Classes.Profiles.ProfileManager import ProfileManager
from Classes.Training.TrainingManager import TrainingManager
from Classes.Venues.VenueManager import VenueManager
from Classes.RoleManager import RoleManager
from UI.Guild import ReportMenuView
from Utilities import Utilities as U
from Classes.ChannelManager import ChannelManager

if TYPE_CHECKING:
    from Classes import TrainingBot, Profile
################################################################################

__all__ = ("GuildData",)

################################################################################
class GuildData:
    """A container for bot-specific guild data and settings."""

    __slots__ = (
        "_state",
        "_parent",
        "_pos_mgr",
        "_training_mgr",
        "_logger",
        "_profile_mgr",
        "_venue_mgr",
        "_job_mgr",
        "_role_mgr",
        "_channel_mgr",
    )

################################################################################
    def __init__(self, bot: TrainingBot, parent: Guild):

        self._state: TrainingBot = bot
        self._parent: Guild = parent
        
        self._logger: Logger = Logger(self)
        
        self._pos_mgr: PositionManager = PositionManager(self)
        self._training_mgr: TrainingManager = TrainingManager(self)
        self._profile_mgr: ProfileManager = ProfileManager(self)
        self._venue_mgr: VenueManager = VenueManager(self)
        self._job_mgr: JobsManager = JobsManager(self)
        
        self._role_mgr: RoleManager = RoleManager(self)
        self._channel_mgr: ChannelManager = ChannelManager(self)

################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        await self._logger.load()
        
        await self._pos_mgr._load_all(data)
        await self._training_mgr._load_all(data)
        await self._profile_mgr._load_all(data)
        await self._venue_mgr._load_all(data)
        await self._job_mgr._load_all(data)
        await self._role_mgr._load_all(data["roles"])
        await self._channel_mgr._load_all(data["channels"])
        
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._state
    
################################################################################
    @property
    def parent(self) -> Guild:
        
        return self._parent
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._parent.id
    
################################################################################
    @property
    def log(self) -> Logger:
        
        return self._logger
    
################################################################################
    @property
    def position_manager(self) -> PositionManager:

        return self._pos_mgr

################################################################################
    @property
    def training_manager(self) -> TrainingManager:

        return self._training_mgr

################################################################################
    @property
    def profile_manager(self) -> ProfileManager:

        return self._profile_mgr
    
################################################################################
    @property
    def venue_manager(self) -> VenueManager:
        
        return self._venue_mgr
    
################################################################################
    @property
    def jobs_manager(self) -> JobsManager:
        
        return self._job_mgr
    
################################################################################
    @property
    def role_manager(self) -> RoleManager:
        
        return self._role_mgr
    
################################################################################
    @property
    def channel_manager(self) -> ChannelManager:
        
        return self._channel_mgr
         
################################################################################
    def get_profile(self, user: User) -> Profile:

        profile = self._profile_mgr[user.id]
        if profile is None:
            profile = self._profile_mgr.create_profile(user)
            
        return profile
    
################################################################################
    async def report_menu(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="TrainerBot Report Menu",
            description="Please select a report to generate."
        )
        view = ReportMenuView(interaction.user, self)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
    
################################################################################
    async def get_or_fetch_channel(self, channel_id: int) -> Optional[GuildChannel]:
        
        if channel_id is None:
            return
        
        channel = self._parent.get_channel(channel_id)
        if channel is not None:
            try:
                channel = await self._parent.fetch_channel(channel_id)
            except:
                pass
            else:
                return channel
    
################################################################################
