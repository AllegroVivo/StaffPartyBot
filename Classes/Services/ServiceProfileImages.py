from __future__ import annotations

from typing import TYPE_CHECKING, Optional, List

from .SPAdditionalImage import SPAdditionalImage

if TYPE_CHECKING:
    from Classes import ServiceProfile
################################################################################

__all__ = ("ServiceProfileImages",)

################################################################################
class ServiceProfileImages:
    
    __slots__ = (
        "_parent",
        "_thumbnail",
        "_main_image",
        "_additional",
    )
    
################################################################################
    def __init__(self, parent: ServiceProfile, **kwargs):
        
        self._parent: ServiceProfile = parent
        
        self._thumbnail: Optional[str] = kwargs.get("thumbnail", None)
        self._main_image: Optional[str] = kwargs.get("main_image", None)
        self._additional: List[SPAdditionalImage] = kwargs.get("additional", None) or []
        
################################################################################
    async def load_all(self) -> None:
        
        pass
    
################################################################################
    @property
    def thumbnail(self) -> Optional[str]:
        
        return self._thumbnail
    
################################################################################
    @property
    def main_image(self) -> Optional[str]:
        
        return self._main_image
    
################################################################################
    @property
    def additional(self) -> List[SPAdditionalImage]:
        
        return self._additional
    
################################################################################
