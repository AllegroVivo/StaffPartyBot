from __future__ import annotations

import os

from dotenv import load_dotenv
from typing import TYPE_CHECKING, Dict, Any, Optional

from discord.abc import GuildChannel
from discord import Attachment, Bot, TextChannel, HTTPException

from .Logger import Logger
from .GuildManager import GuildManager
from Utilities.Database import Database

if TYPE_CHECKING:
    from Classes import GuildData
################################################################################

__all__ = ("TrainingBot",)

################################################################################
class TrainingBot(Bot):

    __slots__ = (
        "_img_dump",
        "_db",
        "_guild_mgr",
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._img_dump: TextChannel = None  # type: ignore

        self._db: Database = Database(self)        
        self._guild_mgr: GuildManager = GuildManager(self)

################################################################################
    def __getitem__(self, guild_id: int) -> GuildData:
        
        return self._guild_mgr[guild_id]
    
################################################################################    
    @property
    def database(self) -> Database:
        
        return self._db
    
################################################################################
    @property
    def fguilds(self) -> GuildManager:
        
        return self._guild_mgr
    
################################################################################
    async def load_all(self) -> None:

        print("Fetching image dump...")
        # Image dump can be hard-coded since it's never going to be different.
        self._img_dump = await self.fetch_channel(991902526188302427)
        
        # Generate all GuildDatas to load database info into.
        for g in self.guilds:
            self._guild_mgr.add_guild(g)

        print("Asserting database structure...")
        # Create the database structure if it doesn't exist.
        self._db._assert_structure()

        print("Loading data from database...")
        # Load all the data from the database.
        payload = self._db._load_all()
        data = self._parse_data(payload)
        
        for frogge in self._guild_mgr.fguilds:
            await frogge.load_all(data[frogge.guild_id])

        print("Done!")

################################################################################
    def _parse_data(self, data: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
         
        ret = { g.id : {
            "bot_config": None,
            "tusers": [],
            "availability": [],
            "qualifications": [],
            "positions": [],
            "requirements": [],
            "trainings": [],
            "requirement_overrides": [],
            "profiles": [],
            "venues": {},
        } for g in self.guilds }
        
        load_dotenv()
        
        for cfg in data["bot_config"]:
            if os.getenv("DEBUG") == "True":
                # Skip other servers when running in debug.
                if cfg[0] not in (955933227372122173, 303742308874977280):
                    continue
            ret[cfg[0]]["bot_config"] = cfg
        for u in data["tusers"]:
            ret[u[1]]["tusers"].append(u)
        for a in data["availability"]:
            ret[a[1]]["availability"].append(a)
        for q in data["qualifications"]:
            ret[q[1]]["qualifications"].append(q)
        for p in data["positions"]:
            ret[p[1]]["positions"].append(p)
        for r in data["requirements"]:
            ret[r[1]]["requirements"].append(r)
        for t in data["trainings"]:
            ret[t[1]]["trainings"].append(t)
        for ro in data["requirement_overrides"]:
            ret[ro[1]]["requirement_overrides"].append(ro)
            
        for p in data["profiles"]:
            ret[p[2]]["profiles"].append(
                {
                    "profile": p,
                    "additional_images": [
                        a for a in data["additional_images"] if a[1] == p[0]
                    ]
                }
            )
            
        for v in data["venues"]:
            ret[v[1]]["venues"][v[0]] = {
                "user_ids": v[2],
                "owner_ids": v[4],
                "pending": v[5],
                "positions": v[3],
                "details": None,
                "aag": None,
                "hours": [],
                "location": None,
            }
        for vd in data["venue_details"]:
            ret[vd[1]]["venues"][vd[0]]["details"] = vd
        for vh in data["venue_hours"]:
            ret[vh[1]]["venues"][vh[0]]["hours"].append(vh)
        for vl in data["venue_locations"]:
            ret[vl[1]]["venues"][vl[0]]["location"] = vl
        for aag in data["venue_aag"]:
            ret[aag[1]]["venues"][aag[0]]["aag"] = aag
            
        return ret
    
################################################################################
    async def dump_image(self, image: Attachment) -> str:
        """Dumps an image into the image dump channel and returns the URL.
        
        Parameters:
        -----------
        image : :class:`Attachment`
            The image to dump.
            
        Returns:
        --------
        :class:`str`
            The URL of the dumped image.
        """

        file = await image.to_file()
        post = await self._img_dump.send(file=file)   # type: ignore

        return post.attachments[0].url

################################################################################
    async def get_or_fetch_channel(self, channel_id: int) -> Optional[GuildChannel]:
        
        if not channel_id:
            return

        ret = self.get_channel(channel_id)
        if ret is None:
            try:
                ret = await self.fetch_channel(channel_id)
            except:
                pass
            
        return ret
    
################################################################################
