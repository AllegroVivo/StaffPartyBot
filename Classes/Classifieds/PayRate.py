from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from Utilities import RateType

if TYPE_CHECKING:
    from Classes import JobPosting
################################################################################

__all__ = ("PayRate",)

################################################################################
class PayRate:
    
    __slots__ = (
        "_parent",
        "_amount",
        "_frequency",
        "_details"
    )
    
################################################################################
    def __init__(self, parent: JobPosting, amount: int, frequency: RateType, details: str) -> None:
        
        self._parent: JobPosting = parent
        
        self._amount: int = amount
        self._frequency: RateType = frequency
        self._details: Optional[str] = details
        
################################################################################
