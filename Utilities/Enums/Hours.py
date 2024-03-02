from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class Hours(FroggeEnum):

    Unavailable = 0
    TwelveAM = 1
    OneAM = 2
    TwoAM = 3
    ThreeAM = 4
    FourAM = 5
    FiveAM = 6
    SixAM = 7
    SevenAM = 8
    EightAM = 9
    NineAM = 10
    TenAM = 11
    ElevenAM = 12
    TwelvePM = 13
    OnePM = 14
    TwoPM = 15
    ThreePM = 16
    FourPM = 17
    FivePM = 18
    SixPM = 19
    SevenPM = 20
    EightPM = 21
    NinePM = 22
    TenPM = 23
    ElevenPM = 24

################################################################################
    @property
    def proper_name(self) -> str:
        # Still missing 12:00 AM at the start. Will need to correct for that.

        # if self.value == 0:
        #     return "Unavailable"
        # 
        # # Correcting the mapping for 12:00 PM
        # if self.value == 24:
        #     return "12:00 AM"
        # 
        # # Correct mapping for AM and PM times
        # hour = self.value if self.value <= 12 else self.value - 12
        # period = "AM" if self.value < 12 else "PM"
        # 
        # # Special handling for 12 AM
        # if self.value == 12:
        #     period = "PM"
        # elif self.value == 24:
        #     hour = 12  # Handling for 12 PM at the end of the cycle
        # 
        # return f"{hour}:00 {period}"

        if self.value == 1:
            return "12:xx AM"
        elif self.value == 2:
            return "1:xx AM"
        elif self.value == 3:
            return "2:xx AM"
        elif self.value == 4:
            return "3:xx AM"
        elif self.value == 5:
            return "4:xx AM"
        elif self.value == 6:
            return "5:xx AM"
        elif self.value == 7:
            return "6:xx AM"
        elif self.value == 8:
            return "7:xx AM"
        elif self.value == 9:
            return "8:xx AM"
        elif self.value == 10:
            return "9:xx AM"
        elif self.value == 11:
            return "10:xx AM"
        elif self.value == 12:
            return "11:xx AM"
        elif self.value == 13:
            return "12:xx PM"
        elif self.value == 14:
            return "1:xx PM"
        elif self.value == 15:
            return "2:xx PM"
        elif self.value == 16:
            return "3:xx PM"
        elif self.value == 17:
            return "4:xx PM"
        elif self.value == 18:
            return "5:xx PM"
        elif self.value == 19:
            return "6:xx PM"
        elif self.value == 20:
            return "7:xx PM"
        elif self.value == 21:
            return "8:xx PM"
        elif self.value == 22:
            return "9:xx PM"
        elif self.value == 23:
            return "10:xx PM"
        elif self.value == 24:
            return "11:xx PM"
        else:
            return self.name

################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        """Returns a list of SelectOptions for the Hours enum. Includes all 
        hours of the day and the "Unavailable" option."""

        return [p.select_option for p in Hours]

################################################################################
    @staticmethod
    def adjusted_select_options(start: int) -> List[SelectOption]:
        """Returns a list of SelectOptions for the Hours enum. Includes all
        hours starting at the given hour and going to the end of the day."""

        ret = [o for o in Hours.select_options() if int(o.value) > start]
        ret.append(Hours(1).select_option)

        return ret

################################################################################
    @staticmethod
    def limited_select_options() -> List[SelectOption]:
        """Returns a list of SelectOptions for the Hours enum. Does not include
        the "Unavailable" option."""

        return [o for o in Hours.select_options() if o.value != "0"]

################################################################################
