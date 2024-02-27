from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from .Builder import DatabaseBuilder
from .Deleter import DatabaseDeleter
from .Inserter import DatabaseInserter
from .Loader import DatabaseLoader
from .Updater import DatabaseUpdater

if TYPE_CHECKING:
    from Classes import PartyBusBot
################################################################################

__all__ = ("DatabaseWorker", )

################################################################################
class DatabaseWorker:
    """The main container for all database utility classes.

    This class is ultimately responsible for creating, inserting, updating,
    and deleting, loading data from the database. Should be pretty
    self-explanatory."""

    __slots__ = (
        "_state",
        "_inserter",
        "_updater",
        "_deleter",
        "_builder",
        "_loader",
    )

################################################################################
    def __init__(self, bot: PartyBusBot):

        self._state: PartyBusBot = bot

        self._builder: DatabaseBuilder = DatabaseBuilder(bot)
        self._inserter: DatabaseInserter = DatabaseInserter(bot)
        self._updater: DatabaseUpdater = DatabaseUpdater(bot)
        self._deleter: DatabaseDeleter = DatabaseDeleter(bot)
        self._loader: DatabaseLoader = DatabaseLoader(bot)

################################################################################
    def build_all(self) -> None:

        self._builder.build_all()

################################################################################
    def load_all(self) -> Dict[str, Any]:

        return self._loader.load_all()

################################################################################
