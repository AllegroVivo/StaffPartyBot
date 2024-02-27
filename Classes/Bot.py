from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Attachment, Bot, TextChannel

from Utilities import LogType
from Utilities.Database import Database

if TYPE_CHECKING:
    pass
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
    )

################################################################################
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._img_dump: TextChannel = None  # type: ignore

        self._db: Database = Database(self)
        # self._log: Logger = Logger(self)

################################################################################    
    @property
    def database(self) -> Database:
        
        return self._db
    
################################################################################    
    def log(self, message: str, log_type: LogType) -> None:
        
        return
    
################################################################################
    async def load_all(self) -> None:
        """Loads all the data from the database and sets up the bot."""

        print("Fetching image dump...")
        self._img_dump = await self.fetch_channel(991902526188302427)

        print("Asserting database structure...")
        self._db._assert_structure()

        print("Loading data from database...")
        data = self._db._load_all()

        print("Done!")

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
