from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class Minutes(FroggeEnum):

    Unavailable = 0
    Zero = 1
    Fifteen = 2
    Thirty = 3
    FortyFive = 4

################################################################################
    @property
    def proper_name(self) -> str:

        if self.value == 1:
            return "xx:00"
        elif self.value == 2:
            return "xx:15"
        elif self.value == 3:
            return "xx:30"
        elif self.value == 4:
            return "xx:45"
        else:
            return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in Minutes if p.value != 0]

################################################################################
