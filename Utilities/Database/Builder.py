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
        self._build_profile_tables()
        self._build_venue_tables()
        self._augment_tables()
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
            "guild_id BIGINT"
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
        self.execute(
            "CREATE TABLE IF NOT EXISTS tuser_details ("
            "user_id BIGINT PRIMARY KEY,"
            "guild_id BIGINT,"
            "char_name TEXT,"
            "notes TEXT,"
            "hiatus BOOLEAN DEFAULT FALSE,"
            "data_center INTEGER"
            ");"
        )
        
        self._refresh_tuser_view()
            
################################################################################
    def _build_profile_tables(self) -> None:
        
        self.execute(
            "CREATE TABLE IF NOT EXISTS profiles ("
            "_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "user_id BIGINT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS details ("
            "_id TEXT PRIMARY KEY,"
            "char_name TEXT,"
            "url TEXT,"
            "color INTEGER,"
            "jobs TEXT[],"
            "rates TEXT,"
            "post_url TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS ataglance ("
            "_id TEXT PRIMARY KEY,"
            "gender TEXT,"
            "pronouns INTEGER[],"
            "race TEXT,"
            "clan TEXT,"
            "orientation TEXT,"
            "height INTEGER,"
            "age TEXT,"
            "mare TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS personality ("
            "_id TEXT PRIMARY KEY,"
            "likes TEXT[],"
            "dislikes TEXT[],"
            "personality TEXT,"
            "aboutme TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS images ("
            "_id TEXT PRIMARY KEY,"
            "thumbnail TEXT,"
            "main_image TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS additional_images ("
            "_id TEXT PRIMARY KEY,"
            "profile_id TEXT,"
            "url TEXT,"
            "caption TEXT"
            ");"
        )
        
        self._refresh_profile_view()
    
################################################################################
    def _build_venue_tables(self) -> None:
        
        self.execute(
            "CREATE TABLE IF NOT EXISTS venues ("
            "_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "users BIGINT[],"
            "positions TEXT[]"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS venue_details ("
            "venue_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "name TEXT,"
            "description TEXT,"
            "accepting BOOLEAN DEFAULT TRUE,"
            "post_url TEXT,"
            "logo_url TEXT"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS venue_hours ("
            "venue_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "weekday INTEGER,"
            "open_time TIME,"
            "close_time TIME"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS venue_locations ("
            "venue_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "data_center INTEGER,"
            "world INTEGER,"
            "zone INTEGER,"
            "ward INTEGER,"
            "plot INTEGER"
            ");"
        )
        self.execute(
            "CREATE TABLE IF NOT EXISTS venue_aag ("
            "venue_id TEXT PRIMARY KEY,"
            "guild_id BIGINT,"
            "level INTEGER,"
            "nsfw BOOLEAN DEFAULT FALSE,"
            "style INTEGER,"
            "size INTEGER"
            ");"
        )
    
################################################################################
    def _augment_tables(self) -> None:
    
        self.execute(
            "ALTER TABLE bot_config "
            "ADD COLUMN IF NOT EXISTS venue_post_channel BIGINT;"
        )
    
################################################################################
    def _refresh_profile_view(self) -> None:

        self.execute(
            "CREATE OR REPLACE VIEW profile_master "
            "AS "
            # Data indices 0 - 2 Internal
            "SELECT p._id,"
            "p.user_id,"
            "p.guild_id,"
            # Data indices 3 - 8 Details
            "d.char_name,"
            "d.url AS custom_url,"
            "d.color,"
            "d.jobs,"
            "d.rates,"
            "d.post_url,"
            # Data indices 9 - 12 Personality
            "pr.likes,"
            "pr.dislikes,"
            "pr.personality,"
            "pr.aboutme,"
            # Data indices 13 - 20 At A Glance
            "a.gender,"
            "a.pronouns,"
            "a.race,"
            "a.clan,"
            "a.orientation,"
            "a.height,"
            "a.age,"
            "a.mare,"
            # Data indices 21 - 22 Images
            "i.thumbnail,"
            "i.main_image "
            "FROM profiles p "
            "JOIN details d ON p._id = d._id "
            "JOIN personality pr ON p._id = pr._id "
            "JOIN ataglance a on p._id = a._id "
            "JOIN images i on p._id = i._id;"
        )
        
################################################################################
    def _refresh_tuser_view(self) -> None:
        
        self.execute(
            "CREATE OR REPLACE VIEW tuser_master "
            "AS "
            "SELECT t.user_id,"
            "t.guild_id,"
            "d.char_name,"
            "d.notes,"
            "d.hiatus,"
            "d.data_center,"
            "c.image_url,"
            "c.job_pings "
            "FROM tusers t "
            "JOIN tuser_config c ON t.user_id = c.user_id "
            "JOIN tuser_details d ON t.user_id = d.user_id;"
        )
    
################################################################################
    