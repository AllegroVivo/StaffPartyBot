from __future__ import annotations
from psycopg2.extensions import cursor
from .Branch import DBWorkerBranch
################################################################################

__all__ = ("DatabaseBuilder",)

################################################################################
class DatabaseBuilder(DBWorkerBranch):
    """A utility class for building and asserting elements of the database."""

    def build_all(self) -> None:

        self.build_bot_tables()
        self.build_initial_records()
        
        print("Database lookin' good!")
        
################################################################################
    def build_bot_tables(self) -> None:
        
        self.execute(
            "CREATE TABLE IF NOT EXISTS bot_config ("
            "guild_id BIGINT PRIMARY KEY,"
            "log_channel BIGINT"
            ");"
        )
 
################################################################################
    def build_initial_records(self) -> None:

        for guild in self.bot.guilds:
            self.execute(
                "INSERT INTO bot_config (guild_id) VALUES (%s) "
                "ON CONFLICT DO NOTHING;",
                guild.id,
            )
        
################################################################################
        