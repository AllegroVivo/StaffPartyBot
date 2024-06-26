from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
################################################################################
class VenueForumTag(FroggeEnum):

    TwitchDJ = 1
    Nightclub = 2
    Bards = 3
    Lounge = 4
    Cafe = 5
    Tavern = 6
    Gambling = 7
    BathHouse = 8
    Restaurant = 9
    Casino = 10
    Den = 11
    Inn = 12
    Shop = 13
    Fightclub = 14
    Courtesans = 15
    AuctionHouse = 16
    Artists = 17
    LGBTQIA = 18
    VIP = 19
    
################################################################################
    @property
    def proper_name(self) -> str:
        
        if self.value == 1:
            return "Twitch DJ"
        elif self.value == 8:
            return "Bath House"
        elif self.value == 16:
            return "Auction House"
        elif self.value == 18:
            return "LGBTQIA+"
        
        return self.name
    
################################################################################
    @staticmethod
    def select_options() -> List[SelectOption]:
        
        return [vs.select_option for vs in VenueForumTag]
    
################################################################################
    