from __future__ import annotations

import asyncio
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Any, Dict

from discord import User, Interaction, TextChannel, NotFound, Embed, EmbedField

from UI.Common import ConfirmCancelView, CloseMessageView
from UI.Training import TUserAdminStatusView, TUserStatusView, InternshipMatchingView
from Utilities import (
    Utilities as U,
    ChannelTypeError,
    BotUserNotAllowedError,
    NotRegisteredError,
    RPLevel,
    NSFWPreference,
    VenueSize
)
from .SignUpMessage import SignUpMessage
from .TUser import TUser
from .Training import Training

if TYPE_CHECKING:
    from Classes import TrainingBot, GuildData, Venue
################################################################################

__all__ = ("TrainingManager",)

################################################################################
class TrainingManager:
    """A class performing management operations for all TUsers in the system.
    
    Attributes:
    -----------
    _state: :class:`TrainingBot`
        The bot instance.
    _tusers: List[:class:`TUser`]
        A list of all TUsers in the system.
    """

    __slots__ = (
        "_guild",
        "_tusers",
        "_trainings",
        "_message",
    )

################################################################################
    def __init__(self, guild: GuildData) -> None:

        self._guild: GuildData = guild
        
        self._tusers: List[TUser] = []
        self._trainings: List[Training] = []
        
        self._message: SignUpMessage = SignUpMessage(self)

################################################################################
    async def _load_all(self, data: Dict[str, Any]) -> None:
        """Load all TUsers from the database records provided.
        
        Parameters:
        -----------
        data : Dict[:class:`str`, Any]
            The data to load from.
        """

        payload = self._parse_data(data)

        for _, record in payload["tusers"].items():
            try:
                user = await self.bot.fetch_user(record["tuser"][0])
            except NotFound:
                continue
                
            tuser = TUser.load(self, user, record)
            self._tusers.append(tuser)
                
        overrides = payload["overrides"]
        trainings = data["trainings"]
        for t in trainings:
            training = Training.load(self[t[2]], t, overrides.get(t[0], []))
            if training is not None:
                self._trainings.append(training)
                
        await self._message.load(payload["signup_message"])
        
################################################################################
    @staticmethod    
    def _parse_data(data: Dict[str, Any]) -> Dict[str, Any]:

        bot_config = data["bot_config"]
        tuser_data = data["tusers"]
        availability_data = data["availability"]
        qdata = data["qualifications"]
        
        tusers: Dict[int, Dict[str, Any]] = {}

        for user in tuser_data:
            tusers[user[0]] = {
                "tuser": user,
                "availability": [],
                "qualifications": [],
            }

        for a in availability_data:
            try:
                tusers[a[0]]["availability"].append(a)
            except KeyError:  # Should only happen if there's no primary TUser record
                pass
        for q in qdata:
            try:
                tusers[q[2]]["qualifications"].append(q)
            except KeyError:
                pass
            
        overrides = {}
        for o in data["requirement_overrides"]:
            try:
                overrides[o[2]].append((o[3], o[4]))
            except KeyError:
                overrides[o[2]] = [(o[3], o[4])]
        
        return {
            "tusers": tusers,
            "overrides": overrides,
            "signup_message": (bot_config[0], bot_config[2], bot_config[3]),
        }
        
################################################################################    
    def __getitem__(self, user_id: int) -> Optional[TUser]:

        for t in self._tusers:
            if t.user_id == user_id:
                return t
    
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
    def tusers(self) -> List[TUser]:
        
        return self._tusers
    
################################################################################
    @property
    def signup_message(self) -> SignUpMessage:
        
        return self._message
    
################################################################################
    @property
    def all_trainings(self) -> List[Training]:
        
        return self._trainings
    
################################################################################
    @property
    def unmatched_trainings(self) -> List[Training]:
        
        return [t for t in self._trainings if t.trainer is None]
    
################################################################################
    @property
    def guild_id(self) -> int:
        
        return self._guild.guild_id
    
################################################################################
    async def _add_tuser(self, interaction: Interaction, user: User) -> bool:
        
        if user.bot:
            error = BotUserNotAllowedError()
            await interaction.respond(embed=error, ephemeral=True)
            return False

        tuser = TUser.new(self, user)
        self._tusers.append(tuser)
        
        confirm = U.make_embed(
            title="User Added",
            description=f"User {tuser.name} added to the system.",
        )
        await interaction.respond(embed=confirm, ephemeral=True)
        await asyncio.sleep(2)
        
        return True
        
################################################################################
    async def tuser_admin_status(self, interaction: Interaction, user: User) -> None:

        tuser = self[user.id]
        if tuser is None:
            if not await self._add_tuser(interaction, user):
                return
            else:
                tuser = self[user.id]

        status = tuser.admin_status()
        view = TUserAdminStatusView(interaction.user, tuser)

        await interaction.respond(embed=status, view=view)
        await view.wait()
    
################################################################################
    async def add_training(self, training: Training) -> None:

        self._trainings.append(training)
        
        await self._message.update_components()
        await self._guild.log.training_signup(training)

        for t in self.get_qualified_trainers(training.position.id):
            if t.accepting_trainee_pings():
                await t.notify_of_training_signup(training)
        
################################################################################        
    async def notify_of_availability_change(self, tuser: TUser) -> None:
        
        for training in tuser.trainings_as_trainee:
            for t in self.get_qualified_trainers(training.position.id):
                if t.accepting_trainee_pings():
                    await t.notify_of_modified_schedule(training)
                
################################################################################
    def get_qualified_trainers(self, position_id: str) -> List[TUser]:
        
        return [t for t in self._tusers if t.is_qualified(position_id)]

################################################################################
    async def remove_training(self, training_id: str) -> None:

        for t in self._trainings:
            if t.id == training_id:
                self._trainings.remove(t)
                await self._guild.log.training_removed(t)
                t.delete()
                break

        await self._message.update_components()

################################################################################
    async def tuser_status(self, interaction: Interaction) -> None:

        tuser = self[interaction.user.id]
        if tuser is None:
            if not await self._add_tuser(interaction, interaction.user):
                return
            else:
                tuser = self[interaction.user.id]

        status = tuser.user_status()
        view = TUserStatusView(interaction.user, tuser)

        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    async def post_signup_message(self, interaction: Interaction, channel: TextChannel) -> None:
        
        if not isinstance(channel, TextChannel):
            error = ChannelTypeError(channel, "TextChannel")
            await interaction.respond(embed=error, ephemeral=True)
            return

        await self._message.post(interaction, channel)

################################################################################
    def get_trainings_for_position(self, position_id: str) -> List[Training]:

        return [t for t in self._trainings if t.position.id == position_id]
    
################################################################################
    def get_training(self, training_id: str) -> Optional[Training]:

        for t in self._trainings:
            if t.id == training_id:
                return t
            
################################################################################
    async def trainer_dashboard(self, interaction: Interaction) -> None:
        
        trainer = self[interaction.user.id]
        if trainer is None:
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await trainer.trainer_dashboard(interaction)

################################################################################
    @staticmethod
    def _match_prompt() -> Embed:
        
        return U.make_embed(
            title="Internship Matching",
            description=(
                "This feature will help try to match you to a foster venue "
                "for your internship.\n\n"

                "You'll be asked your preference on the following four criteria:\n"
                "1. **RP Level:**\n"
                "*(The amount of roleplay used within the venue.)*\n\n"

                "2. **NSFW Preference:**\n"
                "*(Whether or not the venue is NSFW-safe.)*\n\n"

                "3. **Venue Size:**\n"
                "*(The size of the space the venue is located in.)*\n\n"

                "4. **Venue Type:**\n"
                "*(You can select up to three tags for the style of venue you "
                "want to intern at.)*"
            ),
        )
    
################################################################################
    async def match(self, interaction: Interaction) -> None:

        initial_prompt = self._match_prompt()
        initial_prompt.description += (
            "\n\nSelect '`Continue`' below to proceed.\n"
            f"{U.draw_line(extra=22)}"
        )
        
        view = ConfirmCancelView(interaction.user)
        view.children[0].label = "Continue"  # type: ignore
        
        await interaction.respond(embed=initial_prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            return
        
        main_prompt = self._match_prompt()
        main_prompt.description += (
            f"\n\n{U.draw_line(extra=45)}"
        )
        view = InternshipMatchingView(interaction.user)
        
        await interaction.respond(embed=main_prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return
        
        venues = self._matching_routine(*view.value)
        description = ""
        
        for v in venues:
            description += (
                f"**{v.name}:**\n"
                f"*({v.description})*\n\n"
            )
        
        report = U.make_embed(
            title="Internship Matching Results",
            description=description or "`No venues found.`",
        )
        
        await interaction.respond(embed=report)

################################################################################
    def _matching_routine(
        self, 
        rp_level: RPLevel, 
        nsfw_pref: NSFWPreference,
        size: VenueSize, 
        styles: List[VenueTag]
    ) -> List[Venue]:
        
        ret = {}
        
        for venue in self.guild.venue_manager.venues:
            if not venue.ataglance_complete or not venue.accepting_interns:
                continue
    
            level_diff = self._calculate_distance(rp_level, venue.rp_level)
            size_diff = self._calculate_distance(size, venue.size)
            style_scalar = 0.5 if venue.style.value in [s.value for s in styles] else 1
            nsfw_match = nsfw_pref == venue.nsfw
    
            overall_score = (level_diff + size_diff) * style_scalar - nsfw_match
    
            ret[venue] = overall_score
            
        return [venue for venue, score in sorted(ret.items(), key=lambda x: x[1])]
    
################################################################################
    @staticmethod
    def _calculate_distance(user_preference: Enum, venue_attribute: Enum):
        
        return abs(user_preference.value - venue_attribute.value)
    
################################################################################
    async def unpaid_report(self, interaction: Interaction) -> None:

        positions = {
            p.name: {}
            for p in self.guild.position_manager.positions
        }
        
        for training in [
            t for t in self._trainings if t.trainer is not None and not t.trainer_paid
        ]:
            try:
                positions[training.position.name][training.trainer.user_id].append(training)
            except KeyError:
                positions[training.position.name][training.trainer.user_id] = [training]
                
        fields = []
        for pos_name, records in positions.items():
            if not records: 
                continue
                
            value = ""
            for trainer_id, trainings in records.items():
                trainer = self[trainer_id]
                value += f"{trainer.name} - {trainer.user.mention} - `{len(trainings)} unpaid`\n"

            fields.append(
                EmbedField(
                    name=f"__{pos_name}__",
                    value=value,
                    inline=False
                )
            )
            
        if not fields:
            fields.append(
                EmbedField(
                    name="__No Unpaid Trainings__",
                    value="`All trainers have been paid.`",
                    inline=False
                )
            )
                
        report = U.make_embed(
            title="Unpaid Trainer Report",
            description=(
                "The following trainers have unpaid trainings:\n"
                f"{U.draw_line(extra=27)}\n"
            ),
            fields=fields,
        )
        view = CloseMessageView(interaction.user)
        
        await interaction.respond(embed=report, view=view)
        await view.wait()
    
################################################################################
