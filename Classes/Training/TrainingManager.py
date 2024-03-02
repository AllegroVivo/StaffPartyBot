from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, List, Optional, Any, Dict

from discord import User, Interaction, TextChannel

from UI.Training import TUserAdminStatusView, TUserStatusView
from Utilities import Utilities as U, ChannelTypeError, BotUserNotAllowedError
from .SignUpMessage import SignUpMessage
from .TUser import TUser
from .Training import Training

if TYPE_CHECKING:
    from Classes import TrainingBot, GuildData
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
            tuser = await TUser.load(self, record)
            if tuser is not None:
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
        config_data = data["tconfig"]
        availability_data = data["availability"]
        qdata = data["qualifications"]
        
        tusers: Dict[int, Dict[str, Any]] = {}

        for user in tuser_data:
            tusers[user[0]] = {
                "tuser": user,
                "availability": [],
                "qualifications": [],
            }

        for config in config_data:
            tusers[config[0]]["tconfig"] = config
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
                overrides[o[1]].append((o[2], o[3]))
            except KeyError:
                overrides[o[1]] = [(o[2], o[3])]
        
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

        status = tuser.admin_status()
        view = TUserAdminStatusView(interaction.user, tuser)

        await interaction.respond(embed=status, view=view)
        await view.wait()
    
################################################################################
    async def add_training(self, training: Training) -> None:

        self._trainings.append(training)
        
        await self._message.update_components()

        for t in self.get_qualified_trainers(training.position.id):
            await t.notify_of_training_signup(training)

################################################################################
    def get_qualified_trainers(self, position_id: str) -> List[TUser]:
        
        return [t for t in self._tusers if t.is_qualified(position_id)]

################################################################################
    async def remove_training(self, training_id: str) -> None:

        for t in self._trainings:
            if t.id == training_id:
                self._trainings.remove(t)
                t.delete()
                return

        await self._message.update_components()

################################################################################
    async def tuser_status(self, interaction: Interaction) -> None:

        tuser = self[interaction.user.id]
        if tuser is None:
            if not await self._add_tuser(interaction, interaction.user):
                return

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
            