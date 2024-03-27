from typing import List, Optional

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class DataCenter(FroggeEnum):
    
    Aether = 1
    Crystal = 2
    Dynamis = 3
    Primal = 4
    Light = 5
    Chaos = 6
    Materia = 7

################################################################################
    @classmethod
    def from_xiv(cls, xiv_name: Optional[str]) -> Optional["DataCenter"]:
        
        if xiv_name is None:
            return 
        
        for dc in cls:
            if dc.proper_name == xiv_name:
                return dc
            
        raise ValueError(f"Invalid XIV data center name: {xiv_name}")
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [dc.select_option for dc in DataCenter]
    
################################################################################
