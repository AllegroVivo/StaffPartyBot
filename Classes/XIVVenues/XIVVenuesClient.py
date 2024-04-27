from __future__ import annotations

import os

import requests
from typing import TYPE_CHECKING, Optional, Any, Dict, List
from dotenv import load_dotenv
from .XIVVenue import XIVVenue
from Utilities.Errors.WTFException import WTFException
if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("XIVVenuesClient",)

################################################################################
class XIVVenuesClient:

    __slots__ = (
        "_state",
    )
    
    load_dotenv()
    
    if os.getenv("DEBUG") == "True":
        URL_BASE = "https://api.ffxivvenues.dev/venue?"
    else:
        URL_BASE = "https://api.ffxivvenues.com/venue?"
    
################################################################################
    def __init__(self, state: StaffPartyBot):
        
        self._state: StaffPartyBot = state
        
################################################################################
    async def get_venues_by_manager(self, manager_id: int) -> List[XIVVenue]:
        
        query = self.URL_BASE + "manager=" + str(manager_id)
        
        load_dotenv()
        if os.getenv("DEBUG") == "True":
            print("Executing XIVClient query: " + query)
            
        response = requests.get(query)
        
        if response.status_code != 200:
            raise WTFException(
                "Failed to get venue by manager - response status code: " + 
                str(response.status_code)
            )
        
        if os.getenv("DEBUG") == "True":
            print("Response: " + str(response.json()))
        
        ret = []
        
        for venue in response.json():
            ret.append(await XIVVenue.from_data(self._state, venue))
            
        return ret
    
################################################################################
    async def get_venues_by_name(self, name: str) -> List[XIVVenue]:

        query = self.URL_BASE + "search=" + str(name)
        
        load_dotenv()
        if os.getenv("DEBUG") == "True":
            print("Executing XIVClient query: " + query)
            
        response = requests.get(query)

        if response.status_code != 200:
            raise WTFException(
                "Failed to get venue by name - response status code: " +
                str(response.status_code)
            )

        if os.getenv("DEBUG") == "True":
            print("Response: " + str(response.json()))

        ret = []

        for venue in response.json():
            ret.append(await XIVVenue.from_data(self._state, venue))

        return ret
    
################################################################################
    