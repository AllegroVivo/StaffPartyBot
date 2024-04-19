from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, Optional

from Utilities import TrainingLevel, Weekday
from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import *
################################################################################

__all__ = ("DatabaseInserter",)

################################################################################
class DatabaseInserter(DBWorkerBranch):
    """A utility class for inserting new records into the database."""

    def _add_position(self, guild_id: int, pos_name: str) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO positions (_id, _guild_id, name) VALUES (%s, %s, %s);",
            new_id, guild_id, pos_name
        )
        
        return new_id

################################################################################
    def _add_requirement(self, guild_id: int, pos_id: str, description: str) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO requirements (_id, guild_id, position_id, description) "
            "VALUES (%s, %s, %s, %s);",
            new_id, guild_id, pos_id, description
        )
        
        return new_id
    
################################################################################
    def _add_tuser(self, guild_id: int, user_id: int, is_trainer: bool) -> None:
        
        self.execute(
            "INSERT INTO tusers (user_id, guild_id) VALUES (%s, %s) ",
            user_id, guild_id
        )
        self.execute(
            "INSERT INTO tuser_config (user_id, guild_id) VALUES (%s, %s) ",
            user_id, guild_id
        )
        self.execute(
            "INSERT INTO tuser_details (user_id, guild_id) VALUES (%s, %s) ",
            user_id, guild_id
        )
        self.execute(
            "INSERT INTO bg_checks (user_id, guild_id, is_trainer) "
            "VALUES (%s, %s, %s) ",
            user_id, guild_id, is_trainer
        )
        
################################################################################
    def _add_qualification(
        self,
        guild_id: int,
        user_id: int, 
        pos: Position,
        level: TrainingLevel
    ) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO qualifications (_id, guild_id, user_id, position, level) "
            "VALUES (%s, %s, %s, %s, %s);",
            new_id, guild_id, user_id, pos.id, level.value
        )
        
        return new_id

################################################################################
    def _add_availability(
        self, 
        user_id: int,
        guild_id: int, 
        day: Weekday,
        start: time, 
        end: time
    ) -> None:

        self.execute(
            "INSERT INTO availability (user_id, guild_id, day, start_time, end_time) "
            "VALUES (%s, %s, %s, %s, %s);",
            user_id, guild_id, day.value, start, end
        )
        
################################################################################
    def _add_training(self, guild_id: int, user_id: int, pos_id: str) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO trainings (_id, guild_id, user_id, position) "
            "VALUES (%s, %s, %s, %s);",
            new_id, guild_id, user_id, pos_id
        )
        
        return new_id

################################################################################
    def _add_requirement_override(
        self,
        guild_id: int, 
        training_id: str, 
        req_id: str, 
        level: int
    ) -> None:
        
        self.execute(
            "INSERT INTO requirement_overrides (training_id, guild_id, requirement_id, level) "
            "VALUES (%s, %s, %s, %s);",
            training_id, guild_id, req_id, level
        )
        
################################################################################
    def _add_profile(self, guild_id: int, user_id: int) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO profiles (_id, guild_id, user_id) VALUES (%s, %s, %s);",
            new_id, guild_id, user_id
        )
        self.execute("INSERT INTO details (_id) VALUES (%s);", new_id)
        self.execute("INSERT INTO ataglance (_id) VALUES (%s);", new_id)
        self.execute("INSERT INTO personality (_id) VALUES (%s);", new_id)
        self.execute("INSERT INTO images (_id) VALUES (%s);", new_id)
        
        return new_id
    
################################################################################
    def _add_additional_image(self, profile_id: str, url: str, caption: Optional[str]) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO additional_images (_id, profile_id, url, caption) "
            "VALUES (%s, %s, %s, %s);",
            new_id, profile_id, url, caption
        )
        
        return new_id
        
################################################################################
    def _add_venue(self, guild_id: int, name: str) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO venues (_id, guild_id, name) VALUES (%s, %s, %s);",
            new_id, guild_id, name
        )
        self.execute(
            "INSERT INTO venue_urls (venue_id) VALUES (%s);",
            new_id
        )
        self.execute(
            "INSERT INTO venue_locations (venue_id) VALUES (%s);",
            new_id
        )
        self.execute(
            "INSERT INTO venue_aag (venue_id) VALUES (%s);",
            new_id
        )
        
        return new_id
    
################################################################################
    def _add_venue_hours(
        self, 
        venue: Venue,
        day: Weekday, 
        start: time, 
        end: time
    ) -> None:
        
        self.execute(
            "INSERT INTO venue_hours (venue_id, guild_id, weekday, "
            "open_time, close_time) VALUES (%s, %s, %s, %s, %s);",
            venue.id, venue.guild_id, day.value, start, end
        )
        
################################################################################
    def _add_job_hours(
        self, 
        job_id: str,
        guild_id: int,
        day: Weekday,
        start: time,
        end: time
    ) -> None:

        self.execute(
            "INSERT INTO job_hours (job_id, guild_id, day, start_time, end_time) "
            "VALUES (%s, %s, %s, %s, %s);",
            job_id, guild_id, day.value, start, end
        )

################################################################################
    def _add_job_posting(self, guild_id: int, venue_id: str, user_id: int) -> str:
        
        new_id = self.generate_id()[:10]
        
        self.execute(
            "INSERT INTO job_postings (_id, guild_id, venue_id, user_id) "
            "VALUES (%s, %s, %s, %s);",
            new_id, guild_id, venue_id, user_id
        )
        
        return new_id
    
################################################################################
    def _add_profile_availability(
        self,
        profile_id: str,
        day: Weekday, 
        start: time,
        end: time
    ) -> None:
        
        self.execute(
            "INSERT INTO profile_availability (profile_id, day, "
            "start_time, end_time) "
            "VALUES (%s, %s, %s, %s);",
            profile_id, day.value, start, end
        )
        
################################################################################
    def _add_service(self, guild_id: int, name: str) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO services (_id, guild_id, name) VALUES (%s, %s, %s);",
            new_id, guild_id, name
        )
        self.execute(
            "INSERT INTO service_config (service_id) VALUES (%s);",
            new_id
        )
        
        return new_id
    
################################################################################
    def _add_service_profile(self, guild_id: int, user_id: int, service_id: str) -> str:
        
        new_id = self.generate_id()
        
        self.execute(
            "INSERT INTO service_profiles (_id, guild_id, user_id, service_id) "
            "VALUES (%s, %s, %s, %s);",
            new_id, guild_id, user_id, service_id
        )
        
        return new_id
    
################################################################################
    def _add_service_availability(
        self,
        profile_id: str,
        day: Weekday, 
        start: time,
        end: time
    ) -> None:
        
        self.execute(
            "INSERT INTO sp_availability (profile_id, day, start_time, end_time) "
            "VALUES (%s, %s, %s, %s);",
            profile_id, day.value, start, end
        )
        
################################################################################

    position                = _add_position
    requirement             = _add_requirement
    tuser                   = _add_tuser
    qualification           = _add_qualification
    availability            = _add_availability
    training                = _add_training
    req_override            = _add_requirement_override
    profile                 = _add_profile
    addl_image              = _add_additional_image
    venue                   = _add_venue
    venue_hours             = _add_venue_hours
    job_hours               = _add_job_hours
    job_posting             = _add_job_posting
    profile_availability    = _add_profile_availability
    service                 = _add_service
    service_profile         = _add_service_profile
    sp_availability         = _add_service_availability
    
################################################################################
    