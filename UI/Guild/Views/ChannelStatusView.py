from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from discord import ButtonStyle, User
from discord.abc import GuildChannel
from discord.ui import Button, View

from UI.Common import CloseMessageButton, FroggeButton, FroggeView
from Utilities import ChannelPurpose

if TYPE_CHECKING:
    from Classes import ChannelManager
################################################################################

__all__ = ("ChannelStatusView",)

################################################################################
class ChannelStatusView(FroggeView):

    def __init__(self, owner: User, channels: ChannelManager):
        
        super().__init__(owner)
        
        self.channels: ChannelManager = channels
        
        button_list = [
            WelcomeChannelButton(self.channels.welcome_channel),
            LogChannelButton(self.channels.log_channel),
            ProfilesChannelButton(self.channels.profiles_channel),
            VenuesChannelButton(self.channels.venues_channel),
            GroupTrainingChannelButton(self.channels.group_training_channel),
            TempJobsChannelButton(self.channels.temp_job_channel),
            PermJobsChannelButton(self.channels.perm_job_channel),
            ServicesButton(self.channels.services_channel),
            BotNotifyChannelsButton(self.channels.notification_channels),
            CloseMessageButton()
        ]
        for btn in button_list:
            self.add_item(btn)
        
################################################################################
class LogChannelButton(FroggeButton):
    
    def __init__(self, channel: Optional[GuildChannel]):
        
        super().__init__(
            label="Log Stream",
            disabled=False,
            row=0
        )
        
        self.set_style(channel)
        
    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.LogStream)
        self.set_style(self.view.channels.log_channel)
        
        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )
        
################################################################################

class ProfilesChannelButton(FroggeButton):

    def __init__(self, channel: Optional[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Staff Profiles",
            disabled=False,
            row=0
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.Profiles)
        self.set_style(self.view.channels.profiles_channel)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )

################################################################################
class VenuesChannelButton(FroggeButton):

    def __init__(self, channel: Optional[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Venue Profiles",
            disabled=False,
            row=0
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.Venues)
        self.set_style(self.view.channels.venues_channel)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )

################################################################################
class TempJobsChannelButton(FroggeButton):

    def __init__(self, channel: Optional[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Temp Jobs",
            disabled=False,
            row=1,
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.TempJobs)
        self.set_style(self.view.channels.temp_job_channel)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )

################################################################################
class PermJobsChannelButton(FroggeButton):

    def __init__(self, channel: Optional[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Permanent Jobs",
            disabled=False,
            row=1,
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.PermJobs)
        self.set_style(self.view.channels.perm_job_channel)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )

################################################################################
class ServicesButton(FroggeButton):

    def __init__(self, channel: Optional[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Hireable Services",
            disabled=False,
            row=1,
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.Services)
        self.set_style(self.view.channels.services_channel)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )
        
################################################################################
class WelcomeChannelButton(FroggeButton):

    def __init__(self, channel: Optional[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Welcome Channel",
            disabled=False,
            row=0,
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.Welcome)
        self.set_style(self.view.channels.welcome_channel)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )
        
################################################################################
class BotNotifyChannelsButton(FroggeButton):

    def __init__(self, channel: List[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Bot Restart Notification",
            disabled=False,
            row=1,
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.BotNotify)
        self.set_style(self.view.channels.notification_channels)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )
        
################################################################################
class GroupTrainingChannelButton(FroggeButton):

    def __init__(self, channel: Optional[GuildChannel]):

        super().__init__(
            style=ButtonStyle.success,
            label="Group Training Channel",
            disabled=False,
            row=0,
        )

        self.set_style(channel)

    async def callback(self, interaction):
        await self.view.channels.set_channel(interaction, ChannelPurpose.GroupTraining)
        self.set_style(self.view.channels.group_training_channel)

        await self.view.edit_message_helper(
            interaction, embed=self.view.channels.status(), view=self.view
        )
        
################################################################################
