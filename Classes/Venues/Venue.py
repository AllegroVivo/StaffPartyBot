from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Any, Dict, Type, TypeVar

from discord import (
    User,
    Embed,
    EmbedField,
    Interaction,
    Message,
    SelectOption,   
    TextChannel,
)

from Assets import BotEmojis
from UI.Venues import (
    VenueNameModal,
    VenueDescriptionModal,
    PositionSelectView,
    RemoveUserView,
    ScheduleOpenSelectView,
    ScheduleCloseSelectView,
    VenueWeekdaySelectView,
)
from Utilities import (
    Utilities as U,
    RPLevel,
    VenueSize,
    Weekday,
)
from .VenueAtAGlance import VenueAtAGlance
from .VenueHours import VenueHours
from .VenueLocation import VenueLocation
from .VenueTag import VenueTag
from .VenueURLs import VenueURLs

if TYPE_CHECKING:
    from Classes import TrainingBot, VenueManager, Position, GuildData, XIVVenue
################################################################################

__all__ = ("Venue",)

V = TypeVar("V", bound="Venue")

################################################################################
class Venue:

    __slots__ = (
        "_id",
        "_mgr",
        "_name",
        "_description",
        "_hiring",
        "_users",
        "_location",
        "_urls",
        "_pending",
        "_schedule",
        "_aag",
        "_positions",
        "_post_msg",
        "_mare_id",
        "_mare_pass",
    )

################################################################################
    def __init__(self, mgr: VenueManager,  venue_id: str, name: str, **kwargs) -> None:
        
        self._mgr: VenueManager = mgr
        self._id: str = venue_id
        
        self._name: str = name
        self._description: List[str] = kwargs.get("description", [])
        
        self._mare_id: Optional[str] = kwargs.get("mare_id", None)
        self._mare_pass: Optional[str] = kwargs.get("mare_password", None)
        
        self._hiring: bool = kwargs.get("hiring", True)
        self._pending: bool = kwargs.get("pending", True)
        
        self._location: VenueLocation = kwargs.get("location", VenueLocation(self))
        self._aag: VenueAtAGlance = kwargs.get("ataglance", VenueAtAGlance(self))
        
        self._users: List[User] = kwargs.get("users", [])
        self._schedule: List[VenueHours] = kwargs.get("schedule", [])
        self._positions: List[Position] = kwargs.get("positions", [])
        
        self._urls: VenueURLs = VenueURLs.load(
            self,
            {
                "discord": kwargs.get("discord", None),
                "website": kwargs.get("website", None),
                "banner": kwargs.get("banner", None),
                "logo": kwargs.get("logo", None),
            }
        )
        
        self._post_msg: Optional[Message] = kwargs.get("post_message", None)
    
################################################################################
    @classmethod
    def new(cls: Type[V], mgr: VenueManager, name: str) -> V:
        
        new_id = mgr.bot.database.insert.venue(mgr.guild_id, name)
        return cls(mgr, new_id, name)
        
################################################################################    
    @classmethod
    async def load(cls: Type[V], mgr: VenueManager, data: Dict[str, Any]) -> V:
        
        venue = data["venue"]
        hours = data["hours"]
        
        self: V = cls.__new__(cls)

        self._mgr = mgr
        self._id = venue[0]

        self._name = venue[6]
        self._description = venue[7]

        self._mare_id = venue[9]
        self._mare_pass = venue[10]

        self._hiring = venue[8]
        self._pending = venue[4]

        self._location = VenueLocation.load(self, venue[11:19])
        self._aag = VenueAtAGlance.load(self, venue[19:23])

        self._users = [
            u for u in
            [await mgr.bot.get_or_fetch_user(user_id) for user_id in venue[2]]
            if u is not None
        ]
        self._schedule = [VenueHours.load(self, h) for h in hours]
        self._positions = [mgr.guild.position_manager.get_position(p) for p in venue[3]]

        self._urls = VenueURLs.load(
            self,
            {
                "discord": venue[23],
                "website": venue[24],
                "banner": venue[25],
                "logo": venue[26],
            }
        )
        
        self._post_msg = None
        post_url_parts = (venue[5].split("/")) if venue[5] else None
        if post_url_parts:
            channel = await mgr.bot.get_or_fetch_channel(post_url_parts[-2])
            if channel:
                self._post_msg = await channel.fetch_message(post_url_parts[-1])  # type: ignore
        
        return self
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._mgr.bot
    
################################################################################
    @property
    def guild(self) -> GuildData:
        
        return self._mgr.guild 
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._mgr.guild_id
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################

    @property
    def name(self) -> str:

        return self._name

    @name.setter
    def name(self, value: str) -> None:

        self._name = value
        self.update()

################################################################################
    @property
    def description(self) -> List[str]:

        return self._description

    @description.setter
    def description(self, value: List[str]) -> None:

        self._description = value
        self.update()

################################################################################

    @property
    def mare_id(self) -> Optional[str]:

        return self._mare_id

    @mare_id.setter
    def mare_id(self, value: Optional[str]) -> None:

        self._mare_id = value
        self.update()

################################################################################
    @property
    def mare_password(self) -> Optional[str]:

        return self._mare_pass

    @mare_password.setter
    def mare_password(self, value: Optional[str]) -> None:

        self._mare_pass = value
        self.update()

################################################################################

    @property
    def hiring(self) -> bool:

        return self._hiring

    @hiring.setter
    def hiring(self, value: bool) -> None:

        self._hiring = value
        self.update()

################################################################################
    @property
    def pending(self) -> bool:

        return self._pending

    @pending.setter
    def pending(self, value: bool) -> None:

        self._pending = value
        self.update()

################################################################################
    @property
    def location(self) -> VenueLocation:
        
        return self._location
    
################################################################################
    @property
    def rp_level(self) -> Optional[RPLevel]:

        return self._aag.level

################################################################################
    @property
    def nsfw(self) -> bool:
        
        return self._aag.nsfw
    
################################################################################
    @property
    def size(self) -> Optional[VenueSize]:
        
        return self._aag.size
    
################################################################################
    @property
    def tags(self) -> List[VenueTag]:
        
        return self._aag.tags
    
################################################################################    
    @property
    def schedule(self) -> List[VenueHours]:

        self._schedule.sort(key=lambda x: x.day.value)
        return self._schedule

################################################################################
    @property
    def authorized_users(self) -> List[User]:

        return self._users
    
    @authorized_users.setter
    def authorized_users(self, value: List[User]) -> None:
        
        self._users = value
        self.update()
        
################################################################################
    @property
    def positions(self) -> List[Position]:

        return self._positions

    @positions.setter
    def positions(self, value: List[Position]) -> None:
        
        self._positions = value
        self.update()
        
################################################################################
    @property
    def discord_url(self) -> Optional[str]:
            
        return self._urls["discord"]
    
    @discord_url.setter
    def discord_url(self, value: Optional[str]) -> None:
        
        self._urls["discord"] = value
        
################################################################################
    @property
    def website_url(self) -> Optional[str]:
        
        return self._urls["website"]
    
    @website_url.setter
    def website_url(self, value: Optional[str]) -> None:
        
        self._urls["website"] = value

################################################################################
    @property
    def banner_url(self) -> Optional[str]:
        
        return self._urls["banner"]
    
    @banner_url.setter
    def banner_url(self, value: Optional[str]) -> None:
        
        self._urls["banner"] = value
        
################################################################################
    @property
    def logo_url(self) -> Optional[str]:
        
        return self._urls["logo"]
    
    @logo_url.setter
    def logo_url(self, value: Optional[str]) -> None:
        
        self._urls["logo"] = value
        
################################################################################
    @property
    def post_url(self) -> Optional[str]:

        if not self._post_msg:
            return

        return self._post_msg.jump_url

################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            title=f"Venue Profile: __{self.name}__",
            description=(
                (
                    "\n\n".join(self.description) if self.description
                    else "`No description provided.`"
                )
                + f"\n{U.draw_line(extra=33)}"
            ),
            thumbnail_url=self.logo_url,
            fields=[
                self._authorized_users_field(),
                self._venue_hours_field(),
                self._accepting_field(),
                self._venue_location_field(),
                self._ataglance_field(),
                self._urls_status_field(),
                self._positions_field(),
            ]
        )
    
################################################################################
    def _authorized_users_field(self, inline: bool = False) -> EmbedField:

        auth_user_value = (
            ("\n".join([f"• {user.mention}" for user in self._users]))
            if self._users
            else "`No Users Specified`"
        )
        
        return EmbedField(
            name="__Owners/Managers__",
            value=(
                f"{auth_user_value}\n"
                + U.draw_line(extra=15)
            ),
            inline=inline,
        )
    
################################################################################
    def _venue_location_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Location__",
            value=f"`{self._location.format()}`\n{U.draw_line(extra=15)}",
            inline=False,
        )
    
################################################################################
    def _venue_hours_field(self) -> EmbedField:
        
        value = "`Not Implemented Yet`"
        if self.schedule:
            value = "* " + "\n* ".join([h.format() for h in self.schedule])
        
        return EmbedField(
            name="__Open Hours__",
            value=value + f"\n{U.draw_line(extra=15)}",
            inline=True,
        )

################################################################################
    def _ataglance_field(self) -> EmbedField:
        
        return EmbedField(
            name=f"{BotEmojis.Eyes} __At a Glance__ {BotEmojis.Eyes}",
            value=self._aag.compile(),
            inline=True,
        )
    
################################################################################
    def _accepting_field(self) -> EmbedField:
        
        return EmbedField(
            name="__Accepting Applications__",
            value=(
                f"{BotEmojis.Check}" if self.hiring else f"{BotEmojis.Cross}"
            ),
            inline=True,
        )
    
################################################################################
    def _positions_field(self) -> EmbedField:

        if self.hiring:
            if self.positions:
                positions_list = [f"`{pos.name}`" for pos in self.positions]
                positions_formatted = [
                    ', '.join(positions_list[i:i+5]) 
                    for i in range(0, len(positions_list), 5)
                ]
                value = '\n'.join(positions_formatted)
            else:
                value = "`No sponsored positions.`"
        else:
            value = "`Not accepting applications at this time`"
        
        return EmbedField(
            name="__We Employ the Following Jobs__",
            value=value + "\n" + U.draw_line(extra=15),
            inline=False,
        )
    
################################################################################
    def _urls_status_field(self) -> EmbedField:
        
        value = (self.discord_url or '`Not Set`') + "\n\n"
        value += "__**Webpage**__\n"
        value += (self.website_url or '`Not Set`')
                
        return EmbedField(
            name="__Discord Server__",
            value=value,
            inline=True,
        )

################################################################################
    def add_user(self, user: User) -> None:

        self._users.append(user)
        self.update()

################################################################################
    def update(self) -> None:
        
        self.bot.database.update.venue(self)
        
################################################################################
    def delete(self) -> None:
    
        self.bot.database.delete.venue(self)
        
################################################################################
    def update_from_xiv_venue(self, interaction: Interaction, venue: XIVVenue) -> None:

        self._name: str = venue.name
        self._description: List[str] = venue.description.copy() if venue.description else []

        self._mare_id: Optional[str] = venue.mare_id
        self._mare_pass: Optional[str] = venue.mare_pass
        self._hiring: bool = venue.hiring

        self._location.update_from_xiv_venue(venue.location)
        self._aag.update_from_xiv_venue(venue)
        self._urls.update_from_xiv_venue(venue)

        managers = venue.managers.copy()
        if interaction.user not in managers:
            managers.append(interaction.user)
        self._users: List[User] = managers
        
        for s in self._schedule:
            s.delete()
        self._schedule = [VenueHours.from_xiv_schedule(self, h) for h in venue.schedule]
        
        self.update()
    
################################################################################
    async def approve(self, interaction: Interaction) -> None:
        
        if self.pending:
            self.pending = False
            embed = U.make_embed(
                title=f"Venue Approved: __{self.name}__",
                description=(
                    f"The venue has been approved by {interaction.user.mention}!\n"
                    "They can now begin accepting applications."
                )
            )
            await interaction.respond(embed=embed, ephemeral=True)
        
################################################################################
    async def set_name(self, interaction: Interaction) -> None:
        
        modal = VenueNameModal(self.name)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.name = modal.value
        
################################################################################
    async def set_description(self, interaction: Interaction) -> None:
        
        modal = VenueDescriptionModal(self.description)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.description = modal.value
        
################################################################################
    async def toggle_hiring(self, interaction: Interaction) -> None:
        
        self.hiring = not self.hiring
        await interaction.respond("** **", delete_after=0.1)
        
################################################################################
    async def set_positions(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Venue Positions",
            description=(
                "Please select the positions you currently employ for\n"
                "from the selector below."
            )
        )
        
        pos_options = self._mgr.guild.position_manager.select_options()
        for opt in pos_options:
            if opt.value in [p.id for p in self.positions]:
                opt.default = True
                
        view = PositionSelectView(interaction.user, pos_options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.positions = [
            self._mgr.guild.position_manager.get_position(p) 
            for p in view.value
        ]
    
################################################################################
    async def remove_authorized_user(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Remove Authorized User",
            description=(
                "Please select the user you would like to remove\n"
                "from the authorized users list."
            )
        )
        
        user_options = [
            SelectOption(label=user.display_name, value=str(user.id)) 
            for user in self._users if user.id != interaction.user.id
        ]
        if not user_options:
            user_options.append(
                SelectOption(label="No users to remove", value="-1")
            )
        
        view = RemoveUserView(interaction.user, user_options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        self.authorized_users = [
            u for u in self._users if u.id not in view.value
        ]
        
################################################################################
    async def set_discord_url(self, interaction: Interaction) -> None:
        
        await self._urls.set_discord_url(interaction)
        
################################################################################
    async def set_website_url(self, interaction: Interaction) -> None:
        
        await self._urls.set_website_url(interaction)
        
################################################################################
    async def set_logo(self, interaction: Interaction) -> None:
        
        await self._urls.set_logo(interaction)
        
################################################################################
    async def set_rp_level(self, interaction: Interaction) -> None:
        
        await self._aag.set_level(interaction)
        
################################################################################
    async def toggle_nsfw(self, interaction: Interaction) -> None:
        
        await self._aag.toggle_nsfw(interaction)
        
################################################################################
    async def set_size(self, interaction: Interaction) -> None:
        
        await self._aag.set_size(interaction)
        
################################################################################
    async def set_location(self, interaction: Interaction) -> None:
        
        await self._location.menu(interaction)
        
################################################################################
    def _full_schedule(self) -> str:
        
        ret = ""
        for day in [w for w in Weekday if w.value != 0]:
            ret += f"\n* {day.proper_name}: "
            
            present = False
            for s in self.schedule:
                if s.day == day:
                    ret += f"{s.open_ts} - {s.close_ts}"
                    present = True
                    break
                    
            if not present:
                ret += "`Closed`"
                   
        return ret
        
################################################################################
    async def set_schedule(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Venue Schedule",
            description=(
                "The following is your venue's current schedule.\n\n"
                
                f"{self._full_schedule()}\n\n"
                
                f"{U.draw_line(extra=26)}\n"
                "Please select the day you would like to edit."
            )
        )
        view = VenueWeekdaySelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        weekday = view.value
        
        prompt = U.make_embed(
            title=f"Set {weekday.proper_name} Schedule",
            description=(
                "Please select the open time for the venue on this day."
            )
        )
        view = ScheduleOpenSelectView(interaction.user)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        timezone = view.timezone
        open_time = view.value
        
        prompt = U.make_embed(
            title=f"Set {weekday.proper_name} Schedule",
            description=(
                "Please select the close time for the venue on this day."
            )
        )
        view = ScheduleCloseSelectView(interaction.user, timezone)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        close_time = view.value
        
        for s in self.schedule:
            if s.day == weekday:
                s.delete()
                
        self._schedule.append(VenueHours.new(self, weekday, open_time, close_time))

################################################################################
    def post(self, interaction: Interaction, _channel: TextChannel) -> None:
        pass

################################################################################
