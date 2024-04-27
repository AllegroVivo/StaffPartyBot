from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple, Dict

from discord import Role, Embed, EmbedField, Interaction, ForumChannel

from Assets import BotEmojis
from UI.Common import ColorPickerModal
from UI.Services import (
    HireableServiceStatusView,
    ServiceNameModal,
)
from Utilities import Utilities as U, FroggeColor, MentionableType
from .ServiceConfiguration import ServiceConfiguration

if TYPE_CHECKING:
    from Classes import ServicesManager, StaffPartyBot
################################################################################

__all__ = ("HireableService",)

HS = TypeVar("HS", bound="HireableService")

################################################################################
class HireableService:
    
    __slots__ = (
        "_id",
        "_mgr",
        "_name",
        "_role",
        "_color",
        "_config",
    )
    
################################################################################
    def __init__(self, manager: ServicesManager, **kwargs):
        
        self._mgr: ServicesManager = manager
        self._config: ServiceConfiguration = (
            kwargs.get("config", None)
            or ServiceConfiguration(self)
        )
        
        self._id: str = kwargs.pop("_id")
        self._name: str = kwargs.pop("name")
        self._role: Optional[Role] = kwargs.get("role", None)
        self._color: Optional[FroggeColor] = kwargs.get("color", None)
        
################################################################################
    @classmethod
    def new(cls: Type[HS], manager: ServicesManager, name: str) -> HS:
        
        new_id = manager.bot.database.insert.service(manager.guild_id, name)
        return cls(manager, _id=new_id, name=name)
    
################################################################################
    @classmethod
    async def load(cls: Type[HS], manager: ServicesManager, data: Dict[str, Any]) -> HS:
        
        sdata = data["service"]
        
        self: HS = cls.__new__(cls)
        
        self._mgr = manager
        self._config = ServiceConfiguration.load(self, data["config"])
        
        self._id = sdata[0]
        self._name = sdata[2]
        
        self._role = await manager.guild.get_or_fetch_role(sdata[3])
        self._color = FroggeColor(sdata[4]) if sdata[4] else None
        
        return self
    
################################################################################
    @property
    def bot(self) -> StaffPartyBot:
        
        return self._mgr.bot
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def configuration(self) -> ServiceConfiguration:
        
        return self._config
    
################################################################################
    @property
    def post_channel(self) -> Optional[ForumChannel]:
        
        return self._mgr.guild.channel_manager.services_channel
    
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
    def role(self) -> Optional[Role]:
        
        return self._role
    
    @role.setter
    def role(self, value: Optional[Role]) -> None:
        
        self._role = value
        self.update()
    
################################################################################
    @property
    def color(self) -> Optional[FroggeColor]:
        
        return self._color
    
    @color.setter
    def color(self, value: Optional[FroggeColor]) -> None:
        
        self._color = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.service(self)
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            color=self.color or FroggeColor.embed_background(),
            title=f"__Hireable Service: `{self.name}`__",
            description=U.draw_line(extra=45),
            fields=[
                EmbedField(
                    name="__Accent Color__",
                    value=(
                        f"{str(BotEmojis.ArrowLeft)} -- (__{str(self.color).upper()}__)"
                        if self.color
                        else "`Not Set`"
                    ) + f"\n{U.draw_line(extra=17)}",
                    inline=True
                ),
                EmbedField(
                    name="__Linked Role__",
                    value=self.role.mention if self.role else "`Not Set`",
                    inline=True
                ),
                EmbedField(
                    name="__Profile Setup Configuration__", 
                    value=(
                        "*(A value of `True` indicates that the corresponding "
                        "section is enabled and will be required to complete "
                        "a service profile for the given Service.)*"
                    ), 
                    inline=False
                ),
            ] + self._config.fields()
        )
    
################################################################################    
    async def menu(self, interaction: Interaction) -> None:
        
        embed = self.status()
        view = HireableServiceStatusView(interaction.user, self)
        
        await interaction.respond(embed=embed, view=view)
        await view.wait()
        
################################################################################
    async def set_name(self, interaction: Interaction) -> None:
        
        modal = ServiceNameModal(self.name)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.name = modal.value
        
################################################################################
    async def set_color(self, interaction: Interaction) -> None:
        
        modal = ColorPickerModal(self.color)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.color = modal.value
        
################################################################################
    async def set_role(self, interaction: Interaction) -> None:
        
        prompt = U.make_embed(
            title="Set Role",
            description=(
                "Please mention the role you would like to link to this service."
            )
        )
        
        role = await U.listen_for_mentionable(interaction, prompt, MentionableType.Role)
        if role is None:
            return
        
        self.role = role
    
################################################################################
    def toggle_nsfw(self) -> None:
        
        self.configuration.nsfw = not self.configuration.nsfw
        
################################################################################
    def toggle_rates(self) -> None:
        
        self.configuration.rates = not self.configuration.rates
        
################################################################################
    def toggle_style(self) -> None:
        
        self.configuration.style = not self.configuration.style
        
################################################################################
    def toggle_urls(self) -> None:
        
        self.configuration.urls = not self.configuration.urls
        
################################################################################
    def toggle_images(self) -> None:
        
        self.configuration.images = not self.configuration.images
        
################################################################################
    def toggle_schedule(self) -> None:
        
        self.configuration.schedule = not self.configuration.schedule
        
################################################################################
