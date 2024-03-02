from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Any

from discord import Attachment, Bot, TextChannel

from .GuildManager import GuildManager
from Utilities.Database import Database

if TYPE_CHECKING:
    from Classes import GuildData
################################################################################

__all__ = ("TrainingBot",)

################################################################################
class TrainingBot(Bot):
    """The main bot instance.
    
    This class is a subclass of discord.Bot, and is the main bot instance for 
    the Training Server. It contains all the managers and utilities required 
    to run the server's operations.
    
    Attributes:
    -----------
    _img_dump : :class:`TextChannel`
        The internal channel for dumping/storing user images long-term.
    _db : :class:`Database`
        The utility database class for the bot.
    _log : :class:`Logger`
        The utility logger class for the bot.
    _pos_mgr : :class:`PositionManager`
        The position manager for the bot.
    _training_mgr : :class:`TrainingManager`
        The training manager for the bot.
        
    Methods:
    --------
    load_all() -> None
        Loads all the data from the database and sets up the bot.
    dump_image(image: :class:`Attachment`) -> :class:`str`
        Dumps an image into the image dump channel and returns the URL.
    """

    __slots__ = (
        "_img_dump",
        "_db",
        "_log",
        "_guild_mgr",
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._img_dump: TextChannel = None  # type: ignore

        self._db: Database = Database(self)
        # self._log: Logger = Logger(self)
        
        self._guild_mgr: GuildManager = GuildManager(self)

################################################################################
    def __getitem__(self, guild_id: int) -> GuildData:
        
        return self._guild_mgr[guild_id]
    
################################################################################    
    @property
    def database(self) -> Database:
        
        return self._db
    
################################################################################
    async def load_all(self) -> None:
        """Loads all the data from the database and sets up the bot."""

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
            "tconfig": [],
            "availability": [],
            "qualifications": [],
            "positions": [],
            "requirements": [],
            "trainings": [],
            "requirement_overrides": [],
        } for g in self.guilds }
        
        for cfg in data["bot_config"]:
            ret[cfg[0]]["bot_config"] = cfg
        for u in data["tusers"]:
            ret[u[1]]["tusers"].append(u)
        for tcfg in data["tconfig"]:
            ret[tcfg[1]]["tconfig"].append(tcfg)
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
