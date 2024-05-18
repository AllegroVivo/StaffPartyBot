from typing import List

from discord import SelectOption

from .DataCenter import DataCenter
from ._Enum import FroggeEnum
################################################################################
class GlobalDataCenter(FroggeEnum):
    
    Americas = 1
    Europe = 2
    Oceania = 3
    Japanese = 4

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [dc.select_option for dc in GlobalDataCenter]
    
################################################################################
    @property
    def abbreviation(self) -> str:
        
        if self.value == 1:
            return "AM"
        elif self.value == 2:
            return "EU"
        elif self.value == 3:
            return "OC"
        elif self.value == 4:
            return "JP"
    
################################################################################
    def contains(self, dc: DataCenter) -> bool:
        
        if dc is None:
            return False
        
        if self.value == 1:
            return dc.value in [1, 2, 3, 4]
        elif self.value == 2:
            return dc.value in [5, 6]
        elif self.value == 3:
            return dc.value in [7]
        elif self.value == 4:
            return dc.value in [8, 9, 10, 11]
        
################################################################################
    @staticmethod
    def data_centers_by_region(region: str) -> List[DataCenter]:
        
        if region == "NA":
            return [DataCenter.Aether, DataCenter.Crystal, DataCenter.Dynamis, DataCenter.Primal]
        elif region == "EU":
            return [DataCenter.Light, DataCenter.Chaos]
        elif region == "OC":
            return [DataCenter.Materia]
        elif region == "JP":
            return [DataCenter.Elemental, DataCenter.Gaia, DataCenter.Mana, DataCenter.Meteor]
        
################################################################################
