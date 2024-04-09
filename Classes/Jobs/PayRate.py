from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from Utilities import Utilities as U, RateType

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
    def __init__(
        self, 
        parent: JobPosting,
        amount: Optional[int] = None, 
        frequency: Optional[RateType] = None, 
        details: Optional[str] = None
    ) -> None:
        
        self._parent: JobPosting = parent
        
        self._amount: Optional[int] = amount
        self._frequency: Optional[RateType] = frequency
        self._details: Optional[str] = details
        
################################################################################
    def __bool__(self) -> bool:
        
        if self._amount is None:
            return False
        
        return self._amount > -1
    
################################################################################
    @property
    def amount(self) -> Optional[int]:

        return self._amount

    @amount.setter
    def amount(self, value: int) -> None:
        
        self._amount = value
        self.update()
        
################################################################################
    @property
    def frequency(self) -> RateType:
        
        return self._frequency

    @frequency.setter
    def frequency(self, value: RateType) -> None:
        
        self._frequency = value
        self.update()
        
################################################################################
    @property
    def details(self) -> Optional[str]:
        
        return self._details

    @details.setter
    def details(self, value: str) -> None:
        
        self._details = value
        self.update()
        
################################################################################
    def update(self) -> None:
        
        self._parent.update()
        
################################################################################
    def format(self) -> str:
        
        if not self.amount:
            return "`Not Set`"
        
        return (
            f"> `{self.amount:,} gil {self.frequency.proper_name}`\n" +
            (f"*({U.wrap_text(self.details, 40)})*" if self.details else "")
        )
    
################################################################################
