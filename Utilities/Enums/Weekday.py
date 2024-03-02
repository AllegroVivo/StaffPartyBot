from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class Weekday(FroggeEnum):

    Null = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:

        return [p.select_option for p in Weekday if p.value != 0]

################################################################################
