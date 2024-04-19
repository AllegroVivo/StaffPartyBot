from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Classes import ServiceProfile
################################################################################

__all__ = ("ServiceProfileURLs",)

################################################################################
class ServiceProfileURLs:
    
    __slots__ = (
        "_parent",
        "_webpage",
        "_discord",
        "_twitch",
    )
    
################################################################################
    def __init__(self, parent: ServiceProfile, **kwargs):
        
        self._parent: ServiceProfile = parent
        
        self._webpage: Optional[str] = kwargs.get("webpage", None)
        self._discord: Optional[str] = kwargs.get("discord", None)
        self._twitch: Optional[str] = kwargs.get("twitch", None)
        
################################################################################
    async def load_all(self) -> None:
        
        pass
    
################################################################################
    