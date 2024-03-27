from typing import List, Optional

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class HousingZone(FroggeEnum):

    Mist = 1
    LavenderBeds = 2
    Goblet = 3
    Shirogane = 4
    Empyreum = 5

################################################################################
    @classmethod
    def from_xiv(cls, xiv_district: Optional[str]) -> Optional["HousingZone"]:
        
        if xiv_district is None:
            return
        
        if xiv_district == "Lavender Beds":
            return cls.LavenderBeds
        
        return cls[xiv_district]
        
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [o.select_option for o in HousingZone]
    
################################################################################    
    @property
    def proper_name(self) -> str:
        
        if self.value == 2:
            return "Lavender Beds"
        
        return self.name
        
################################################################################
        