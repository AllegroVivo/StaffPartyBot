from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional, Any, Dict, Union

from discord import Interaction

from UI.Profiles import AdditionalImageCaptionModal

if TYPE_CHECKING:
    from Classes import ProfileImages, ServiceProfileImages
################################################################################

__all__ = ("AdditionalImage",)

################################################################################
class AdditionalImage(ABC):
    
    __slots__ = (
        "_parent",
        "_id",
        "_url",
        "_caption"
    )
    
################################################################################
    def __init__(self, **kwargs) -> None:
        
        self._parent: Union[ProfileImages, ServiceProfileImages] = kwargs.pop("parent")
        
        self._id: str = kwargs.pop("_id")
        self._url: str = kwargs.pop("url")
        self._caption: Optional[str] = kwargs.get("caption", None)
    
################################################################################
    @classmethod
    @abstractmethod
    def new(cls, parent: Any, url: str, caption: Optional[str]) -> AdditionalImage:
        
        raise NotImplementedError
    
################################################################################
    def __eq__(self, other: AdditionalImage) -> bool:
        
        return self.id == other.id
    
################################################################################
    @property
    def id(self) -> str:
        
        return self._id
    
################################################################################
    @property
    def url(self) -> str:
        
        return self._url
    
################################################################################
    @property
    def caption(self) -> Optional[str]:
        
        return self._caption
    
    @caption.setter
    def caption(self, value: Optional[str]) -> None:
        
        self._caption = value
        self.update()
        
################################################################################
    @abstractmethod
    def update(self) -> None:
        
        raise NotImplementedError
    
################################################################################
    @abstractmethod
    def delete(self) -> None:

        raise NotImplementedError
        
################################################################################
    def compile(self) -> str:

        if self.caption is None:
            return self.url

        return f"[{self.caption}]({self.url})"

################################################################################
    async def set_caption(self, interaction: Interaction) -> None:

        modal = AdditionalImageCaptionModal(self.caption)
        
        await interaction.response.send_modal(modal)
        await modal.wait()
        
        if not modal.complete:
            return
        
        self.caption = modal.value
        
################################################################################
    def _to_dict(self) -> Dict[str, Any]:
        
        return {
            "id": self.id,
            "url": self.url,
            "caption": self.caption
        }
    
################################################################################
