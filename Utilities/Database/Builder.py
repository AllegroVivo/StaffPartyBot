from __future__ import annotations
from psycopg2.extensions import cursor
from .Branch import DBWorkerBranch
################################################################################

__all__ = ("DatabaseBuilder",)

################################################################################
class DatabaseBuilder(DBWorkerBranch):
    """A utility class for building and asserting elements of the database."""

    def build_all(self) -> None:
        
        self._build_views()
        self._build_initial_records()
        
        print("Database lookin' good!")

################################################################################
    def _build_initial_records(self) -> None:

        for guild in self.bot.guilds:
            self.execute(
                "INSERT INTO bot_config (guild_id) VALUES (%s) "
                "ON CONFLICT DO NOTHING;",
                guild.id,
            )
            self.execute(
                "INSERT INTO roles (guild_id) VALUES (%s) "
                "ON CONFLICT DO NOTHING;",
                guild.id,
            )
  
################################################################################
    def _build_views(self) -> None:

        self.execute(
            "CREATE OR REPLACE VIEW profile_master "
            "AS "
            # Data indices 0 - 2 Internal
            "SELECT p._id,"
            "p.user_id,"
            "p.guild_id,"
            # Data indices 3 - 10 Details
            "d.char_name,"
            "d.url AS custom_url,"
            "d.color,"
            "d.jobs,"
            "d.rates,"
            "d.post_url,"
            "d.positions,"
            "d.dm_preference,"
            # Data indices 11 - 14 Personality
            "pr.likes,"
            "pr.dislikes,"
            "pr.personality,"
            "pr.aboutme,"
            # Data indices 15 - 24 At A Glance
            "a.gender,"
            "a.pronouns,"
            "a.race,"
            "a.clan,"
            "a.orientation,"
            "a.height,"
            "a.age,"
            "a.mare,"
            "a.data_centers,"
            # Data indices 24 - 25 Images
            "i.thumbnail,"
            "i.main_image "
            "FROM profiles p "
            "JOIN details d ON p._id = d._id "
            "JOIN personality pr ON p._id = pr._id "
            "JOIN ataglance a on p._id = a._id "
            "JOIN images i on p._id = i._id;"
        )
        
        self.execute(
            "CREATE OR REPLACE VIEW tuser_master "
            "AS "
            "SELECT t.user_id,"
            "t.guild_id,"
            "t.mute_list,"
            "d.char_name,"
            "d.notes,"
            "d.hiatus,"
            "d.data_centers,"
            "d.guidelines,"
            "c.image_url,"
            "c.job_pings "
            "FROM tusers t "
            "JOIN tuser_config c ON t.user_id = c.user_id "
            "JOIN tuser_details d ON t.user_id = d.user_id;"
        )
        
        self.execute(
            "CREATE OR REPLACE VIEW venue_master "
            "AS "
            "SELECT v._id," 
            "v.guild_id,"
            "v.users,"
            "v.positions,"
            "v.pending,"
            "v.post_url,"
            "v.name,"
            "v.description,"
            "v.hiring,"
            "v.mare_id,"
            "v.mare_pass,"
            "v.mute_list,"
            "l.data_center,"
            "l.world,"
            "l.zone,"
            "l.ward,"
            "l.plot,"
            "l.apartment,"
            "l.room,"
            "l.subdivision,"
            "a.level,"
            "a.nsfw,"
            "a.size,"
            "a.tags,"
            "u.discord_url,"
            "u.website_url,"
            "u.banner_url,"
            "u.logo_url,"
            "u.application_url "
            "FROM venues v "
            "JOIN venue_locations l ON v._id = l.venue_id "
            "JOIN venue_aag a ON v._id = a.venue_id "
            "JOIN venue_urls u ON v._id = u.venue_id;"
        )
    
################################################################################
    