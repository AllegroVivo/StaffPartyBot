from __future__ import annotations

import asyncio
from enum import Enum
from itertools import islice
from typing import TYPE_CHECKING, List, Optional, Any, Dict, Tuple

from discord import User, Interaction, TextChannel, NotFound, Embed, EmbedField, Member
from discord.ext.pages import Page

from UI.Common import ConfirmCancelView, CloseMessageView, Frogginator
from UI.Training import TUserAdminStatusView, TUserStatusView, InternshipMatchingView
from Utilities import (
    Utilities as U,
    ChannelTypeError,
    BotUserNotAllowedError,
    NotRegisteredError,
    RPLevel,
    NSFWPreference,
    VenueSize,
    VenueForumTag
)
from .SignUpMessage import SignUpMessage
from .TUser import TUser
from .Training import Training

if TYPE_CHECKING:
    from Classes import StaffPartyBot, GuildData, Venue, VenueTag
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

        payload = self._parse_data(data)

        for _, record in payload["tusers"].items():
            try:
                user = await self.bot.fetch_user(record["tuser"][0])
            except NotFound:
                continue
                
            tuser = await TUser.load(self, user, record)
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
        bg_checks = data["bg_checks"]
        
        tusers: Dict[int, Dict[str, Any]] = {}

        for user in tuser_data:
            tusers[user[0]] = {
                "tuser": user,
                "availability": [],
                "qualifications": [],
                "bg_check": None,
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
                
        for bg in bg_checks:
            try:
                tusers[bg[0]]["bg_check"] = bg
            except KeyError:
                pass
        
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
    def bot(self) -> StaffPartyBot:

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

                "3. **Venue Type:**\n"
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
        
        for v_id, score in venues:
            v = self.guild.venue_manager[v_id]
            desc = '\n'.join(v.description)
            if len(desc) > 150:
                desc = desc[:150] + "..."
            description += (
                f"**[{v.name}]({v.post_url}): {score:.0f}% Match!**\n"
                f"*{desc}*\n\n"
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
        tags: List[VenueForumTag]
    ) -> List[Tuple[str, float]]:

        venue_scores = {}
    
        for venue in self.guild.venue_manager.venues:
            if venue.post_url is None or not venue.hiring:
                continue
    
            # Normalize level difference (assuming _calculate_distance returns a non-negative number)
            level_diff = self._calculate_distance(rp_level, venue.rp_level)
            normalized_level_diff = 1 - (level_diff / 10)
    
            # NSFW match (1 for match, 0 for mismatch)
            nsfw_score = 1 if nsfw_pref == venue.nsfw else 0
    
            # Calculate tag similarity as a ratio
            venue_tags = [v.tag_text.lower() for v in venue.tags]
            tags_scalar = sum(1 for tag in tags if tag.proper_name.lower() in venue_tags) / len(tags)
    
            # Calculate the overall score as an average of the three normalized scores, then convert to percentage
            overall_score = ((normalized_level_diff + nsfw_score + tags_scalar) / 3) * 100
    
            venue_scores[venue.id] = overall_score
    
        # Sort venues by score, if more than 5, then slice the first 5
        max_results = 5 if len(venue_scores) >= 5 else len(venue_scores)    
        return sorted(venue_scores.items(), key=lambda x: x[1], reverse=True)[:max_results]
    
################################################################################
    @staticmethod
    def _calculate_distance(user_preference: Enum, venue_attribute: Enum):
        
        if user_preference is None or venue_attribute is None:
            return 0
        
        return abs(user_preference.value - venue_attribute.value)
    
################################################################################
    async def start_bg_check(self, interaction: Interaction) -> None:

        tuser = self[interaction.user.id]
        if tuser is None:
            tuser = TUser.new(self, interaction.user)
            self._tusers.append(tuser)

        await tuser.start_bg_check(interaction)

################################################################################
    async def trainee_profile(self, interaction: Interaction, user: User) -> None:
        
        tuser = self[user.id]
        if tuser is None:
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
            
        await interaction.respond(embed=tuser.user_status(), ephemeral=True)

################################################################################
    async def unpaid_report(self, interaction: Interaction) -> None:
        
        unpaid_trainings = [
            t 
            for t in self._trainings 
            if (
                t.is_complete 
                and not t.trainer_paid 
                and t.trainer is not None
            )
        ]
        unpaid_trainings.sort(key=lambda t: t.trainer.name)
        
        unpaid_trainer_dict = {}
        for t in unpaid_trainings:
            if t.trainer.user_id not in unpaid_trainer_dict:
                unpaid_trainer_dict[t.trainer.user_id] = {}
            try:
                unpaid_trainer_dict[t.trainer.user_id][t.position.name].append(t)
            except KeyError:
                unpaid_trainer_dict[t.trainer.user_id][t.position.name] = [t]

        embed = U.make_embed(
            title="Unpaid Trainer Report",
            description=(
                "The following trainers have unpaid trainings:\n"
                f"{U.draw_line(extra=27)}\n"
            )
        )
                
        pages = []
        fields = []
        
        if not unpaid_trainer_dict:
            embed.description += "`No unpaid trainers found.`"
            pages.append(Page(embeds=[embed]))

        for trainer_id, trainings in unpaid_trainer_dict.items():
            trainer = self[trainer_id]
            value = f"({trainer.user.mention})\n"
            amount = 0
            
            for pos, tlist in trainings.items():
                position = self.guild.position_manager.get_position_by_name(pos)
                x = len(tlist) * position.trainer_pay
                amount += x
                value += f"[{len(tlist)}] **{pos}** = `{x:,}`\n"
                
            fields.append(
                EmbedField(
                    name=f"__{trainer.name}__",
                    value=value + f"__**Total Due:**__\n`{amount:,}`",
                    inline=False
                )
            )
            if len(fields) >= 10:
                embed_copy = embed.copy()
                embed_copy.fields = fields
                pages.append(Page(embeds=[embed_copy]))
                fields = []
                
        if fields:
            embed.fields = fields
            pages.append(Page(embeds=[embed]))
        
        frogginator = Frogginator(pages=pages)
        await frogginator.respond(interaction)

################################################################################
    async def staff_experience(self, interaction: Interaction, user: User) -> None:
        
        tuser = self[user.id]
        if tuser is None:
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await tuser.staff_experience(interaction)

################################################################################
    async def settle_trainer(self, interaction: Interaction, user: User) -> None:

        tuser = self[user.id]
        if tuser is None:
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await tuser.settle_training_balance(interaction)
        
################################################################################
    async def trainer_management(self, interaction: Interaction, user: User) -> None:

        tuser = self[user.id]
        if tuser is None:
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await tuser.manage_trainings(interaction)

################################################################################
    async def on_member_leave(self, member: Member) -> Tuple[int, int]:

        tuser = self[member.id]
        if tuser is None:
            return 0, 0
        
        return await tuser.on_server_leave()

################################################################################
        