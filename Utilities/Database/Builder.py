from __future__ import annotations
from psycopg2.extensions import cursor
from .Branch import DBWorkerBranch
################################################################################

__all__ = ("DatabaseBuilder",)

################################################################################
class DatabaseBuilder(DBWorkerBranch):
    """A utility class for building and asserting elements of the database."""

    def build_all(self) -> None:

        self._build_bot_tables()
        self._build_position_tables()
        self._build_training_tables()
        self._build_initial_records()
        
        print("Database lookin' good!")
        
################################################################################
    def _build_bot_tables(self) -> None:
        
        self.execute(
            "CREATE TABLE IF NOT EXISTS bot_config ("
            "guild_id BIGINT PRIMARY KEY,"
            "log_channel BIGINT,"
            "signup_msg_channel BIGINT,"
            "signup_msg_id BIGINT"
            ");"
        )
        
################################################################################        
    def _build_position_tables(self) -> None:
        
        self.execute(
            "CREATE TABLE IF NOT EXISTS positions ("
            "_id TEXT PRIMARY KEY,"
            "_guild_id BIGINT,"
            "name TEXT UNIQUE"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS requirements ("
            "_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "position_id TEXT,"
            "description TEXT"
            ");"
        )
 
################################################################################
    def _build_initial_records(self) -> None:

        for guild in self.bot.guilds:
            self.execute(
                "INSERT INTO bot_config (guild_id) VALUES (%s) "
                "ON CONFLICT DO NOTHING;",
                guild.id,
            )
        
################################################################################
    def _build_training_tables(self) -> None:

        self.execute(
            "CREATE TABLE IF NOT EXISTS tusers ("
            "user_id BIGINT PRIMARY KEY ,"
            "guild_id BIGINT,"
            "name TEXT,"
            "notes TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS tuser_config ("
            "user_id BIGINT PRIMARY KEY,"
            "guild_id BIGINT,"
            "image_url TEXT,"
            "job_pings BOOLEAN DEFAULT TRUE"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS qualifications ("
            "_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "user_id BIGINT,"
            "position TEXT,"
            "level INTEGER"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS availability ("
            "user_id BIGINT,"
            "guild_id BIGINT,"
            "day INTEGER,"
            "start_time TIME,"
            "end_time TIME"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS trainings ("
            "_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "user_id BIGINT,"
            "position TEXT,"
            "trainer BIGINT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS requirement_overrides ("
            "user_id BIGINT,"
            "guild_id BIGINT,"
            "training_id TEXT,"
            "requirement_id TEXT,"
            "level INTEGER"
            ");"
        )
            
################################################################################
            