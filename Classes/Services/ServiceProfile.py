from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar, List, Optional

from discord import User, Embed, EmbedField

from .ServiceProfileImages import ServiceProfileImages
from .SAvailability import SAvailability
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import ServicesManager, TrainingBot, HireableService
################################################################################

__all__ = ("ServiceProfile",)

SP = TypeVar("SP", bound="ServiceProfile")

################################################################################
class ServiceProfile:
    
    __slots__ = (
        "_id",
        "_mgr",
        "_user",
        "_service",
        "_schedule",
        "_images",
        "_website",
        "_discord",
        "_nsfw",
        "_rates",
        "_style",
    )
    
################################################################################
    def __init__(self, manager: ServicesManager, user: User, **kwargs):
        
        self._id = kwargs.pop("_id")
        self._mgr: ServicesManager = manager
        self._user: User = user
        
        self._service: HireableService = kwargs.pop("service")
        self._schedule: List[SAvailability] = kwargs.get("schedule", None) or []
        self._images: ServiceProfileImages = kwargs.get("images", None) or ServiceProfileImages(self)
        
        self._website: Optional[str] = kwargs.get("website", None)
        self._discord: Optional[str] = kwargs.get("discord", None)
        self._nsfw: bool = kwargs.get("nsfw", False)
        self._rates: Optional[str] = kwargs.get("rates", None)
        self._style: Optional[str] = kwargs.get("style", None)
    
################################################################################
    @classmethod
    def new(cls: Type[SP], mgr: ServicesManager, user: User, service: HireableService) -> SP:
        
        new_id = mgr.bot.database.insert.service_profile(mgr.guild_id, user.id, service.id)
        return cls(mgr, user, _id=new_id, service=service)
    
################################################################################
    @property
    def bot(self) -> TrainingBot:
        
        return self._mgr.bot
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id 
    
################################################################################
    @property
    def user(self) -> User:
        
        return self._user
    
################################################################################
    @property
    def service(self) -> HireableService:
        
        return self._service
    
################################################################################
    @property
    def schedule(self) -> List[SAvailability]:
        
        return self._schedule
    
################################################################################
    @property
    def thumbnail(self) -> Optional[str]:
        
        return self._images.thumbnail
    
################################################################################
    @property
    def main_image(self) -> Optional[str]:
        
        return self._images.main_image
    
################################################################################
    @property
    def website(self) -> Optional[str]:
        
        return self._website
    
    @website.setter
    def website(self, value: Optional[str]) -> None:
        
        self._website = value
        self.update()
        
################################################################################
    @property
    def discord(self) -> Optional[str]:
        
        return self._discord
    
    @discord.setter
    def discord(self, value: Optional[str]) -> None:
        
        self._discord = value
        self.update()
        
################################################################################
    @property
    def nsfw(self) -> bool:
        
        return self._nsfw
    
    @nsfw.setter
    def nsfw(self, value: bool) -> None:
        
        self._nsfw = value
        self.update()
        
################################################################################
    @property
    def rates(self) -> Optional[str]:
        
        return self._rates
    
    @rates.setter
    def rates(self, value: Optional[str]) -> None:
        
        self._rates = value
        self.update()
        
################################################################################
    @property
    def style(self) -> Optional[str]:
        
        return self._style
    
    @style.setter
    def style(self, value: Optional[str]) -> None:
        
        self._style = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.bot.database.update.service_profile(self)
    
################################################################################
    def status(self) -> Embed:
        
        return U.make_embed(
            color=self.service.color if self.service.color else None,
            title="__Service Profile__",
            description=(
                f"**Service:** {self.service.name}\n"
                
            )
        )
    
################################################################################
    