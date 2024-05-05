from __future__ import annotations

from datetime import datetime, timedelta
from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

import discord.utils
from discord import Guild, User, Interaction, Message, NotFound, Member, Role
from discord.abc import GuildChannel
from discord.ext import tasks

from Classes.Itinerary.ItineraryManager import ItineraryManager
from Classes.ChannelManager import ChannelManager
from Classes.Jobs.JobsManager import JobsManager
from Classes.Logger import Logger
from Classes.Positions.PositionManager import PositionManager
from Classes.Profiles.ProfileManager import ProfileManager
from Classes.RoleManager import RoleManager
from Classes.Services.ServicesManager import ServicesManager
from Classes.Training.TrainingManager import TrainingManager
from Classes.Venues.VenueManager import VenueManager
from UI.Guild import ReportMenuView, BulkUpdateView
from Utilities import Utilities as U, log

if TYPE_CHECKING:
    from Classes import StaffPartyBot, Profile
################################################################################

__all__ = ("GuildData",)

################################################################################
class GuildData:
    """A container for bot-specific guild data and settings."""

    # Can't have slots if we're going to do the member_welcome task as 
    # the presence of __slots__ will prevent writing to this class.
    
    # __slots__ = (
    #     "_state",
    #     "_parent",
    #     "_pos_mgr",
    #     "_training_mgr",
    #     "_logger",
    #     "_profile_mgr",
    #     "_venue_mgr",
    #     "_job_mgr",
    #     "_role_mgr",
    #     "_channel_mgr",
    #     "_service_mgr",
    #     "_itinerary_mgr",
    # )

################################################################################
    def __init__(self, bot: StaffPartyBot, parent: Guild):

        self._state: StaffPartyBot = bot
        self._parent: Guild = parent
        
        self._logger: Logger = Logger(self)
        
        self._pos_mgr: PositionManager = PositionManager(self)
        self._training_mgr: TrainingManager = TrainingManager(self)
        self._profile_mgr: ProfileManager = ProfileManager(self)
        self._venue_mgr: VenueManager = VenueManager(self)
        self._job_mgr: JobsManager = JobsManager(self)
        
        self._role_mgr: RoleManager = RoleManager(self)
        self._channel_mgr: ChannelManager = ChannelManager(self)
        self._service_mgr: ServicesManager = ServicesManager(self)
        self._itinerary_mgr: ItineraryManager = ItineraryManager(self)

################################################################################
    async def load_all(self, data: Dict[str, Any]) -> None:
        
        await self._logger.load()
        
        await self._channel_mgr._load_all(data["channels"])
        await self.begin_notify_of_bot_restart()
        await self._role_mgr._load_all(data["roles"])
        
        await self._pos_mgr._load_all(data)
        await self._venue_mgr._load_all(data)
        await self._training_mgr._load_all(data)
        await self._profile_mgr._load_all(data)
        
        await self._job_mgr._load_all(data)
        await self._service_mgr._load_all(data)
        
        await self.end_notify_of_bot_restart()
        
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
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
    @property
    def service_manager(self) -> ServicesManager:
        
        return self._service_mgr
    
################################################################################
    @property
    def itinerary_manager(self) -> ItineraryManager:
        
        return self._itinerary_mgr
    
################################################################################
    def get_or_create_profile(self, user: User) -> Profile:
        
        log.info(
            "Core",
            f"Getting or creating profile for {user.name} ({user.id})..."
        )

        profile = self._profile_mgr[user.id]
        if profile is None:
            profile = self._profile_mgr.create_profile(user)
            
        return profile
    
################################################################################
    async def report_menu(self, interaction: Interaction) -> None:
        
        log.info(
            "Core",
            f"Opening report menu for guild ({self.guild_id})..."
        )
        
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
        
        log.info(
            "Core",
            f"Getting or fetching channel {channel_id}..."
        )
        
        if channel := self._parent.get_channel(channel_id):
            log.info("Core", "Channel found in cache.")
            return channel
        
        try:
            ret = await self._parent.fetch_channel(channel_id)
        except NotFound:
            log.warning("Core", f"Channel {channel_id} not found.")
            return
        except Exception as ex:
            log.critical(
                "Core",
                f"Error fetching channel {channel_id}: {ex}"
            )
            return
        else:
            log.info("Core", "Channel fetched from Discord.")
            return ret

################################################################################
    async def get_or_fetch_message(self, message_url: Optional[str]) -> Optional[Message]:
        
        if message_url is None:
            return
        
        log.info(
            "Core",
            f"Getting or fetching message {message_url}..."
        )
        
        url_parts = message_url.split("/")
        
        if msg := self.bot.get_message(int(url_parts[-1])):
            log.info("Core", "Message found in cache.")
            return msg
        
        channel = await self.get_or_fetch_channel(int(url_parts[-2]))
        if channel is None:
            log.info("Core", "Message channel not found.")
            return
        
        try:
            ret = await channel.fetch_message(int(url_parts[-1]))  # type: ignore
        except NotFound:
            log.warning("Core", f"Message {message_url} not found.")
            return
        except Exception as ex:
            log.critical(
                "Core",
                f"Error fetching message {message_url}: {ex}"
            )
            return
        else:
            log.info("Core", "Message fetched from Discord.")
            return ret

################################################################################
    async def get_or_fetch_user(self, user_id: Optional[int]) -> Optional[Union[Member, User]]:
        
        if user_id is None:
            return
        
        log.info(
            "Core",
            f"Getting or fetching user/member {user_id}..."
        )
        
        if user := self._parent.get_member(user_id):
            log.info("Core", "Member found in cache.")
            return user
        
        if member := await self._parent.fetch_member(user_id):
            log.info("Core", "Member fetched from Discord.")
            return member
        
        try:
            ret = await self.bot.get_or_fetch_user(user_id)
        except NotFound:
            log.warning("Core", f"User {user_id} not found.")
            return
        except Exception as ex:
            log.critical(
                "Core",
                f"Error fetching user {user_id}: {ex}"
            )
            return
        else:
            log.info("Core", "User fetched from Discord.")
            return ret
            
################################################################################
    async def get_or_fetch_role(self, role_id: Optional[int]) -> Optional[Role]:
        
        if role_id is None:
            return
        
        log.info("Core", f"Getting or fetching role {role_id}...")
        
        if role := self._parent.get_role(role_id):
            log.info("Core", "Role found in cache.")
            return role
        
        try:
            ret = await self._parent._fetch_role(role_id)
        except NotFound:
            log.warning("Core", f"Role {role_id} not found.")
            return
        except Exception as ex:
            log.critical(
                "Core",
                f"Error fetching role {role_id}: {ex}"
            )
            return
        else:
            log.info("Core", "Role fetched from Discord.")
            return ret
    
################################################################################
    async def on_member_leave(self, member: Member) -> None:
        
        venue_deleted = await self.venue_manager.on_member_leave(member)
        profile_deleted = await self.profile_manager.on_member_leave(member)
        num_modified, num_deleted = await self.training_manager.on_member_leave(member)
        jobs_deleted, jobs_canceled = await self.jobs_manager.on_member_leave(member)
        
        await self.log.member_left(
            member=member,
            venue_deleted=venue_deleted,
            profile_deleted=profile_deleted,
            trainings_modified=num_modified,
            trainings_deleted=num_deleted,
            jobs_deleted=jobs_deleted,
            jobs_canceled=jobs_canceled
        )        
        
################################################################################
    async def on_member_join(self, member: Member) -> None:
        
        log.info("Core", f"Member joined! Sending welcome message in t-minus 60 seconds...")
        
        await self.log.member_join(member)
        self.member_welcome.start(member)
        
################################################################################
    @tasks.loop(count=1)
    async def member_welcome(self, member: Member) -> None:
        
        if not self.channel_manager.welcome_channel:
            return
        
        # One minute for role selection
        await discord.utils.sleep_until(member.joined_at + timedelta(minutes=1))
        
        # Get updated member object
        if get_member := self.parent.get_member(member.id):
            member = get_member
        
        welcome_message = (
            "# __Welcome to the <a:party_bus:1225557207836393645> "
            "Staff Party Bus!! <a:party_bus:1225557207836393645>__\n\n"
            
            f"Hiya, {member.mention}! I'm the Staff Party Bot, and I'm going to be "
            f"your best friend throughout your time here at the Staff Party Bus!\n\n"
        )
        
        flag = False
        if self.role_manager.venue_management in member.roles:
            welcome_message += (
                "It looks like you've selected the Venue Management role!\n"
                "You can follow the instructions <#1220087653815291954> to set up "
                "your venue profile \\o/ <a:bartender:1168135253387378748> \n\n"
            )
            flag = True
        if self.role_manager.staff_unvalidated in member.roles:
            welcome_message += (
                "I see you've picked the Staff Pending role!\n"
                "You can follow the instructions here <#1104515062636478643> to do "
                "your staff validation and you'll be able to create your staff "
                "profile afterwards! <a:dancer:1168134583158575175>\n\n"
            )
            flag = True
        if "trainee" in [r.name.lower() for r in member.roles]:
            welcome_message += (
                "I see you've selected the Trainee role!\n"
                "You can follow the instructions here <#1219488746664230974> to "
                "set up your profile and receive training! <a:greeter:1168134573926912071>"
            )
            flag = True
            
        if not flag:
            welcome_message += (
                "It looks like you haven't selected any roles yet! You can do so "
                "in <#1104515062636478638> to get started! <a:host:1168134582000943124>"
            )
            
        await self.channel_manager.welcome_channel.send(welcome_message)
    
################################################################################
    async def bulk_update_menu(self, interaction: Interaction) -> None:
        
        log.info(
            "Core",
            f"Opening bulk update menu for guild ({self.guild_id})..."
        )
        
        prompt = U.make_embed(
            title="TrainerBot Bulk Update Menu",
            description="Please select a category to update."
        )
        view = BulkUpdateView(interaction.user, self)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()

################################################################################
    async def begin_notify_of_bot_restart(self) -> None:
        
        log.info("Core", "Notifying of bot restart...")
        
        ready_time = datetime.now() + timedelta(minutes=2)
        notification = U.make_embed(
            title="__Staff Party Bot Restarting!__",
            description=(
                "The Staff Party Bot is currently restarting and some "
                "features may be temporarily unavailable. <a:DJ:1115502710914035722>\n\n"
                
                f"**Current estimated ready-to-go time: {U.format_dt(ready_time)}**\n\n"
                
                "This channel will receive a notification when the bot is back online. "
                "<a:host:1168134582000943124>"
            )
        )
        
        for ch in self._channel_mgr.notification_channels:
            try:
                await ch.send(embed=notification)
            except NotFound:
                log.warning("Core", f"Notification channel '{ch.id}' not found.")
                pass
            except Exception as ex:
                log.critical(
                    "Core",
                    f"Error sending bot restart notification to {ch.id}: {ex}"
                )
            else:
                log.info("Core", f"Bot restart notification sent to {ch.id}.")

################################################################################
    async def end_notify_of_bot_restart(self) -> None:
        
        notification = U.make_embed(
            title="__Staff Party Bot Restarted!__",
            description=(
                "<a:security:1168134596815224873> The Staff Party Bot has "
                "finished restarting and all features should now be available. "
                "<a:security:1168134596815224873>\n\n"
                
                "Thank you for your patience! <a:dancer:1168134583158575175>"
            )
        )
        
        for ch in self._channel_mgr.notification_channels:
            try:
                await ch.send(embed=notification)
            except NotFound:
                log.warning("Core", f"Notification channel '{ch.id}' not found.")
                pass
            except Exception as ex:
                log.critical(
                    "Core",
                    f"Error sending bot restart notification to {ch.id}: {ex}"
                )
            else:
                log.info("Core", f"Bot restart notification sent to {ch.id}.")

################################################################################
        