from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, Optional

from Utilities import TrainingLevel, Weekday
from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Position
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
    def _add_tuser(self, guild_id: int, user_id: int) -> None:
        
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
        self, user_id: int,
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

    position        = _add_position
    requirement     = _add_requirement
    tuser           = _add_tuser
    qualification   = _add_qualification
    availability    = _add_availability
    training        = _add_training
    req_override    = _add_requirement_override
    profile         = _add_profile
    addl_image      = _add_additional_image
    
################################################################################
    