from __future__ import annotations

import asyncio
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Any, Dict, Tuple

from discord import (
    User,
    Interaction,
    TextChannel,
    NotFound,
    Embed,
    EmbedField,
    Member,
    SelectOption
)
from discord.ext.pages import Page

from .GroupTraining import GroupTraining
from UI.Common import ConfirmCancelView, Frogginator
from UI.Training import (
    TUserAdminStatusView,
    TUserStatusView,
    TraineeStatusView,
    InternshipMatchingView,
    VenueMatchView,
    GroupTrainingMenuView,
    PositionSelectView,
    GroupTrainingSelectView,
)
from Utilities import (
    Utilities as U,
    ChannelTypeError,
    BotUserNotAllowedError,
    NotRegisteredError,
    RPLevel,
    NSFWPreference,
    VenueForumTag,
    log,
    InvalidPositionSelectionError,
)
from .SignUpMessage import SignUpMessage
from .TUser import TUser
from .Training import Training

if TYPE_CHECKING:
    from Classes import StaffPartyBot, GuildData, Position
################################################################################

__all__ = ("TrainingManager",)

################################################################################
class TrainingManager:

    __slots__ = (
        "_guild",
        "_tusers",
        "_trainings",
        "_message",
        "_groups",
    )

################################################################################
    def __init__(self, guild: GuildData) -> None:

        self._guild: GuildData = guild
        
        self._tusers: List[TUser] = []
        self._trainings: List[Training] = []
        self._groups: List[GroupTraining] = []
        
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
        
        self._groups = [
            await GroupTraining.load(self, g) 
            for g in data["group_trainings"]
        ]
        for g in self._groups:
            await g._update_post_components()

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
    def groups(self) -> List[GroupTraining]:
        
        return self._groups
    
################################################################################
    @property
    def unpaid_groups(self) -> List[GroupTraining]:
        
        return [g for g in self._groups if not g.is_paid]
    
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
        
        log.info(
            "Training",
            f"Adding user {user.name} ({user.id}) to the training system."
        )
        
        if user.bot:
            log.warning(
                "Training",
                (
                    f"User {user.name} ({user.id}) is a bot and cannot be "
                    f"added to the training system."
                )
            )
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
        
        log.info(
            "Training",
            f"Requesting admin status for user {user.name} ({user.id})."
        )

        tuser = self[user.id]
        if tuser is None:
            if not await self._add_tuser(interaction, user):
                return
            tuser = self[user.id]

        status = tuser.admin_status()
        view = TUserAdminStatusView(interaction.user, tuser)

        await interaction.respond(embed=status, view=view)
        await view.wait()
    
################################################################################
    async def add_training(self, training: Training) -> None:
        
        log.info(
            "Training",
            f"Adding training {training.id} to the system. (Trainee: {training.trainee.name})"
        )

        self._trainings.append(training)
        
        await self._message.update_components()
        await self._guild.log.training_signup(training)

        for t in self.get_qualified_trainers(training.position.id):
            if t.accepting_trainee_pings():
                await t.notify_of_training_signup(training)
        
################################################################################ 
    @staticmethod
    async def notify_of_availability_change(tuser: TUser) -> None:
        
        log.info(
            "Training",
            f"Notifying trainers of availability change for {tuser.name}."
        )
        
        for training in tuser.trainings_as_trainee:
            if training.is_complete:
                continue
            if training.trainer is not None and training.trainer.accepting_trainee_pings():
                await training.trainer.notify_of_modified_schedule(training)
                
################################################################################
    def get_qualified_trainers(self, position_id: str) -> List[TUser]:
        
        return [t for t in self._tusers if t.is_qualified(position_id)]

################################################################################
    async def remove_training(self, training_id: str) -> None:
        
        log.info(
            "Training",
            f"Removing training {training_id} from the system."
        )

        for t in self._trainings:
            if t.id == training_id:
                await self._guild.log.training_removed(t)
                t.delete()
                break

        await self._message.update_components()

################################################################################
    async def tuser_status(self, interaction: Interaction) -> None:
        
        log.info(
            "Training",
            f"Requesting tuser status for user {interaction.user.name} ({interaction.user.id})."
        )

        tuser = self[interaction.user.id]
        if tuser is None:
            if not await self._add_tuser(interaction, interaction.user):
                return
            tuser = self[interaction.user.id]

        status = tuser.user_status()
        view = TUserStatusView(interaction.user, tuser)

        await interaction.respond(embed=status, view=view)
        await view.wait()

################################################################################
    async def trainee_status(self, interaction: Interaction) -> None:

        log.info(
            "Training",
            f"Requesting trainee status for user {interaction.user.name} ({interaction.user.id})."
        )

        tuser = self[interaction.user.id]
        if tuser is None:
            if not await self._add_tuser(interaction, interaction.user):
                return
            tuser = self[interaction.user.id]

        status = tuser.user_status()
        view = TraineeStatusView(interaction.user, tuser)

        await interaction.respond(embed=status, view=view)
        await view.wait()
        
################################################################################
    async def post_signup_message(self, interaction: Interaction, channel: TextChannel) -> None:
        
        log.info(
            "Training",
            f"Posting signup message to channel {channel.name} ({channel.id})."
        )
        
        if not isinstance(channel, TextChannel):
            log.warning(
                "Training",
                f"Channel {channel.name} ({channel.id}) is not a text channel."
            )
            error = ChannelTypeError(channel, "TextChannel")
            await interaction.respond(embed=error, ephemeral=True)
            return

        await self._message.post(interaction, channel)
        
        log.info("Training", "Signup message posted.")

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
        
        log.info(
            "Training",
            f"Requesting dashboard for user {interaction.user.name} ({interaction.user.id})."
        )
        
        trainer = self[interaction.user.id]
        if trainer is None:
            log.warning(
                "Training",
                f"User {interaction.user.name} ({interaction.user.id}) is not registered."
            )
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
        
        log.info(
            "Training",
            (
                f"Requesting internship matching for user "
                f"{interaction.user.name} ({interaction.user.id})."
            )
        )

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
            log.debug("Training", "User cancelled internship matching.")
            return
        
        main_prompt = self._match_prompt()
        main_prompt.description += (
            f"\n\n{U.draw_line(extra=45)}"
        )
        view = InternshipMatchingView(interaction.user)
        
        await interaction.respond(embed=main_prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "User cancelled internship matching.")
            return
        
        venues = self._matching_routine(*view.value)
        description = ""
        
        v_list = []
        for v_id, score in venues:
            v = self.guild.venue_manager[v_id]
            v_list.append(v)
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
            footer_text=(
                "Click one of the buttons below to express interest in a venue."
            )
        )
        view = VenueMatchView(interaction.user, v_list)

        log.info("Training", "Internship matching complete.")
        
        await interaction.respond(embed=report, view=view)
        await view.wait()

################################################################################
    def _matching_routine(
        self, 
        rp_level: RPLevel, 
        nsfw_pref: NSFWPreference,
        tags: List[VenueForumTag]
    ) -> List[Tuple[str, float]]:

        venue_scores = {}
    
        for venue in self.guild.venue_manager.venues:
            if venue.post_url is None or venue.rp_level is None:
                continue
                
            score = 0
            
            rp_score = 50 - 10 * abs(rp_level.value - venue.rp_level.value)
            score += rp_score
            
            if nsfw_pref == venue.nsfw:
                score += 30
                
            matching_tags = set(
                [t.proper_name.lower() for t in tags]).intersection(
                set([v.tag_text.lower() for v in venue.tags])
            )
            tag_score = (len(matching_tags) / len(tags)) * 20 if tags else 0
            score += tag_score
    
            venue_scores[venue.id] = score
    
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
        
        log.info(
            "Training",
            f"Starting background check for user {interaction.user.name} ({interaction.user.id})."
        )

        tuser = self[interaction.user.id]
        if tuser is None:
            tuser = TUser.new(self, interaction.user)
            self._tusers.append(tuser)

        await tuser.start_bg_check(interaction)

################################################################################
    async def trainee_profile(self, interaction: Interaction, user: User) -> None:
        
        log.info(
            "Training",
            f"Requesting profile for user {user.name} ({user.id})."
        )
        
        tuser = self[user.id]
        if tuser is None:
            log.warning(
                "Training",
                f"User {user.name} ({user.id}) is not registered."
            )
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
            
        await interaction.respond(embed=tuser.user_status(), ephemeral=True)

################################################################################
    async def unpaid_report(self, interaction: Interaction) -> None:
        
        log.info("Training", "Requesting unpaid trainer report.")
        
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
        
        log.info(
            "Training",
            f"Requesting staff experience for user {user.name} ({user.id})."
        )
        
        tuser = self[user.id]
        if tuser is None:
            log.warning(
                "Training",
                f"User {user.name} ({user.id}) is not registered."
            )
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await tuser.staff_experience(interaction)

################################################################################
    async def settle_trainer(self, interaction: Interaction, user: User) -> None:
        
        log.info(
            "Training",
            f"Requesting settlement for user {user.name} ({user.id})."
        )

        tuser = self[user.id]
        if tuser is None:
            log.warning(
                "Training",
                f"User {user.name} ({user.id}) is not registered."
            )
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        await tuser.settle_training_balance(interaction)
        
################################################################################
    async def trainer_management(self, interaction: Interaction, user: User) -> None:
        
        log.info(
            "Training",
            f"Requesting trainer management for user {user.name} ({user.id})."
        )

        tuser = self[user.id]
        if tuser is None:
            log.warning(
                "Training",
                f"User {user.name} ({user.id}) is not registered."
            )
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
    async def group_training_menu(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Group Training Menu",
            description=(
                "Select an option below to manage Group Training events."
            ),
        )
        view = GroupTrainingMenuView(interaction.user, self)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()

################################################################################
    def get_group_trainings_by_trainer(
        self, 
        trainer: TUser, 
        positions: Optional[List[Position]] = None
    ) -> List[GroupTraining]:

        return [
            g for g in self._groups 
            if g.trainer == trainer and (positions is None or g.position in positions)
        ]

################################################################################
    async def add_group_training(self, interaction: Interaction) -> None:
        
        trainer = self[interaction.user.id]
        if trainer is None:
            log.warning(
                "Training",
                f"User {interaction.user.name} ({interaction.user.id}) is not registered."
            )
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return
        
        log.info(
            "Training",
            f"User {interaction.user.name} ({interaction.user.id}) is adding a new Group Training event."
        )
        
        pos_options = [SelectOption(label="General Training", value="general_training")]
        pos_options.extend(self.guild.position_manager.select_options())
        
        prompt = U.make_embed(
            title="Add New Group Training",
            description="Select the Position(s) being trained for in this Group Training."
        )
        view = PositionSelectView(
            user=interaction.user,
            options=pos_options,
            multi_select=True
        )
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "User cancelled Group Training creation.")
            return
        
        if "general_training" in view.value:
            if len(view.value) > 1:
                log.warning(
                    "Training",
                    (
                        f"User {interaction.user.name} ({interaction.user.id}) attempted "
                        f"to create a General Training event with other positions."
                    )
                )
                error = InvalidPositionSelectionError()
                await interaction.respond(embed=error, ephemeral=True)
                return
            else:
                positions = []
                pos_string = "General Training"
        else:
            positions = [self.guild.position_manager.get_position(p) for p in view.value]
            pos_string = ", ".join([p.name for p in positions])
        
        log.info(
            "Training",
            (
                f"User {interaction.user.name} ({interaction.user.id}) is creating "
                f"a new Group Training event for {pos_string}."
            )
        )
        
        group = GroupTraining.new(self, trainer, positions)
        self._groups.append(group)

        await self.guild.log.group_training_created(group)
        await group.menu(interaction)
        
################################################################################
    async def manage_group_trainings(self, interaction: Interaction) -> None:

        trainer = self[interaction.user.id]
        if trainer is None:
            log.warning(
                "Training",
                f"User {interaction.user.name} ({interaction.user.id}) is not registered."
            )
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return

        current_groups = self.get_group_trainings_by_trainer(trainer)
        options = [
            SelectOption(
                label=g.name or "Unnamed Group Training",
                description=U.string_clamp(g.pos_string, 90),
                value=g.id
            ) for g in current_groups
        ]

        prompt = U.make_embed(
            title="Manage Group Trainings",
            description="Select the Group Training you want to modify."
        )
        view = GroupTrainingSelectView(user=interaction.user, options=options)
        
        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "User cancelled Group Training modification.")
            return

        group = self.get_group_training(view.value)

        log.info(
            "Training",
            (
                f"User {interaction.user.name} ({interaction.user.id}) is modifying "
                f"their Group Training event {group.id} - {group.name}."
            )
        )

        await group.menu(interaction)
    
################################################################################
    async def remove_group_training(self, interaction: Interaction) -> None:

        trainer = self[interaction.user.id]
        if trainer is None:
            log.warning(
                "Training",
                f"User {interaction.user.name} ({interaction.user.id}) is not registered."
            )
            error = NotRegisteredError()
            await interaction.respond(embed=error, ephemeral=True)
            return

        current_groups = self.get_group_trainings_by_trainer(trainer)
        options = [
            SelectOption(
                label=g.name or "Unnamed Group Training",
                description=U.string_clamp(g.pos_string, 90),
                value=g.id
            ) for g in current_groups
        ]

        prompt = U.make_embed(
            title="Delete Group Training",
            description="Select the Group Training you want to delete."
        )
        view = GroupTrainingSelectView(user=interaction.user, options=options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            log.debug("Training", "User cancelled Group Training modification.")
            return

        group = self.get_group_training(view.value)

        log.info(
            "Training",
            (
                f"User {interaction.user.name} ({interaction.user.id}) is removing "
                f"their Group Training event {group.id} - {group.name}."
            )
        )

        confirm = U.make_embed(
            title="Delete Group Training",
            description=(
                f"Are you sure you want to delete the following Group Training event:\n\n"
                
                f"__**Name:**__ `{group.name}`\n"
                f"__**Position(s):**__ `{group.pos_string}`\n"
                f"__**Start Time:**__ `{group.start_time}`\n"
                f"__**Description:**__\n{group.description}"
            )
        )
        view = ConfirmCancelView(interaction.user)
        
        await interaction.respond(embed=confirm, view=view)
        await view.wait()
        
        if not view.complete or view.value is False:
            log.debug("Training", "User cancelled Group Training deletion.")
            return
        
        await self._delete_group_training(group)
        
################################################################################
    def get_group_training(self, group_id: str) -> Optional[GroupTraining]:

        for g in self._groups:
            if g.id == group_id:
                return g
            
################################################################################
    async def _delete_group_training(self, group: GroupTraining) -> None:
        
        notification = U.make_embed(
            title="Group Training Canceled",
            description=(
                f"Group Training event `{group.name}` for positions `{group.pos_string}` "
                f"has been canceled. Please check back soon for more group training "
                f"opportunities."
            )
        )
        for signup in group.signups:
            await signup.user.send(embed=notification)

        group.delete()
        
################################################################################
