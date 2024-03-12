from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class ImageType(FroggeEnum):

    Thumbnail = 1
    MainImage = 2
    AdditionalImage = 3

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 2:
            return "Main Image"
        elif self.value == 3:
            return "Additional Image"

        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [g.select_option for g in ImageType]
    
################################################################################
    