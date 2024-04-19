from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, Any, Tuple, List

from discord import Role, EmbedField, Embed

from Assets import BotEmojis
from Utilities import FroggeColor

if TYPE_CHECKING:
    from Classes import HireableService
################################################################################

__all__ = ("ServiceConfiguration",)

SC = TypeVar("SC", bound="ServiceConfiguration")

################################################################################
class ServiceConfiguration:
    
    __slots__ = (
        "_parent",
        "_nsfw",
        "_rates",
        "_style",
        "_urls",
        "_images",
        "_schedule"
    )
    
################################################################################
    def __init__(self, parent: HireableService, **kwargs):
        
        self._parent: HireableService = parent
        
        self._nsfw: bool = kwargs.get("nsfw", True)
        self._rates: bool = kwargs.get("rates", True)
        self._style: bool = kwargs.get("style", True)
        self._urls: bool = kwargs.get("urls", True)
        self._images: bool = kwargs.get("images", True)
        self._schedule: bool = kwargs.get("schedule", True)
        
################################################################################
    @classmethod
    def load(cls: Type[SC], parent: HireableService, data: Tuple[bool, ...]) -> SC:
        
        return cls(
            parent=parent,
            nsfw=data[1],
            rates=data[2],
            style=data[3],
            urls=data[4],
            images=data[5],
            schedule=data[6]
        )
    
################################################################################
    @property
    def parent(self) -> HireableService:
        
        return self._parent
    
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
    def rates(self) -> bool:
        
        return self._rates
    
    @rates.setter
    def rates(self, value: bool) -> None:
        
        self._rates = value
        self.update()
        
################################################################################
    @property
    def style(self) -> bool:
        
        return self._style
    
    @style.setter
    def style(self, value: bool) -> None:
        
        self._style = value
        self.update()
################################################################################
    @property
    def urls(self) -> bool:
        
        return self._urls
    
    @urls.setter
    def urls(self, value: bool) -> None:
        
        self._urls = value
        self.update()
        
################################################################################
    @property
    def images(self) -> bool:
        
        return self._images
    
    @images.setter
    def images(self, value: bool) -> None:
        
        self._images = value
        self.update()
        
################################################################################
    @property
    def schedule(self) -> bool:
        
        return self._schedule
    
    @schedule.setter
    def schedule(self, value: bool) -> None:
        
        self._schedule = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self.parent.update()
        
################################################################################
    def fields(self) -> List[EmbedField]:
        
        return [
            EmbedField(
                name="__Accepts NSFW__",
                value=str(BotEmojis.Check) if self._nsfw else str(BotEmojis.Cross),
                inline=True
            ),
            EmbedField(
                name="__Rates Section__",
                value=str(BotEmojis.Check) if self._rates else str(BotEmojis.Cross),
                inline=True
            ),
            EmbedField(
                name="__Style Descriptor__",
                value=str(BotEmojis.Check) if self._style else str(BotEmojis.Cross),
                inline=True
            ),
            EmbedField(
                name="__Webpage/Discord URLs__",
                value=str(BotEmojis.Check) if self._urls else str(BotEmojis.Cross),
                inline=True
            ),
            EmbedField(
                name="__Display Images__",
                value=str(BotEmojis.Check) if self._images else str(BotEmojis.Cross),
                inline=True
            ),
            EmbedField(
                name="__Schedule Active__",
                value=str(BotEmojis.Check) if self._schedule else str(BotEmojis.Cross),
                inline=True
            )
        ]
    
################################################################################
        