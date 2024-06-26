from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Dict, Tuple

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

from .Worker import DatabaseWorker

if TYPE_CHECKING:
    from psycopg2.extensions import connection, cursor

    from .Inserter import DatabaseInserter
    from .Updater import DatabaseUpdater
    from .Deleter import DatabaseDeleter
    from Classes import StaffPartyBot
################################################################################

__all__ = ("Database", )

################################################################################
class Database:
    """Database class for handling all database interactions."""

    __slots__ = (
        "_state",
        "_connection",
        "_cursor",
        "_worker",
    )

################################################################################
    def __init__(self, bot: StaffPartyBot):

        self._state: StaffPartyBot = bot

        self._connection: connection = None  # type: ignore
        self._cursor: cursor = None  # type: ignore
        self._worker: DatabaseWorker = DatabaseWorker(bot)
        
################################################################################        
    def _connect(self) -> None:

        load_dotenv()

        self._reset_connection()
        
        if os.getenv("DEBUG") == "True":
            self._connection = psycopg2.connect(os.getenv("DATABASE_URL"))
        else:
            self._connection = psycopg2.connect(os.getenv("HEROKU_POSTGRESQL_NAVY_URL"), sslmode="require")
            
        self._cursor = self._connection.cursor()

        print("Connecting to database")

################################################################################
    def _assert_structure(self) -> None:

        self._worker.build_all()

################################################################################
    def _load_all(self) -> Dict[str, Any]:

        return self._worker.load_all()
    
################################################################################
    def _reset_connection(self) -> None:

        try:
            self._cursor.close()
            self._connection.close()
        except (OperationalError, AttributeError):
            pass
        finally:
            self._connection = None
            self._cursor = None

################################################################################
    def execute(self, query: str, *fmt_args: Any) -> None:

        try:
            self._cursor.execute("SELECT 1")
        except:
            self._connect()

        load_dotenv()
        
        try:
            self._cursor.execute(query, fmt_args)
            self._connection.commit()
            if os.getenv("DEBUG") == "True":
                print(f"Database execution succeeded on query: '{query}', Args: {fmt_args}")
        except:
            print(f"Database execution failed on query: '{query}', Args: {fmt_args}")

################################################################################
    def fetchall(self) -> Tuple[Tuple[Any, ...]]:

        return self._cursor.fetchall()

################################################################################
    def fetchone(self) -> Tuple[Any, ...]:

        return self._cursor.fetchone()
    
################################################################################

    @property
    def insert(self) -> DatabaseInserter:

        return self._worker._inserter

################################################################################
    @property
    def update(self) -> DatabaseUpdater:

        return self._worker._updater

################################################################################

    @property
    def delete(self) -> DatabaseDeleter:

        return self._worker._deleter

################################################################################
