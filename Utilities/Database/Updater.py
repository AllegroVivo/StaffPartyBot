from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import (
        Position, 
        Requirement, 
        TUser,
        Availability, 
        Qualification, 
        Training,
        SignUpMessage
    )
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater(DBWorkerBranch):
    """A utility class for updating records in the database."""

    def _update_log_channel(self, guild_id: int, channel_id: Optional[int]) -> None:
        
        self.execute(
            "UPDATE bot_config SET log_channel = %s WHERE guild_id = %s;",
            channel_id, guild_id
        )
    
################################################################################
    def _update_position(self, position: Position) -> None:
        
        self.execute(
            "UPDATE positions SET name = %s WHERE _id = %s;",
            position.name, position.id
        )
    
################################################################################
    def _update_requirement(self, requirement: Requirement) -> None:
        
        self.execute(
            "UPDATE requirements SET description = %s WHERE _id = %s;",
            requirement.description, requirement.id
        )
        
################################################################################        
    def _update_tuser(self, tuser: TUser) -> None:
        
        self.execute(
            "UPDATE tusers SET name = %s, notes = %s WHERE user_id = %s;",
            tuser.name, tuser.notes, tuser.user_id
        )
        self.execute(
            "UPDATE tuser_config SET job_pings = %s WHERE user_id = %s;",
            tuser.config.trainee_pings, tuser.user_id
        )
        
################################################################################
    def _update_availability(self, availability: Availability) -> None:
        
        self.execute(
            "UPDATE availability SET start_time = %s, end_time = %s "
            "WHERE user_id = %s AND day = %s;",
            availability.start_time, availability.end_time,
            availability.user_id, availability.day.value
        )

################################################################################
    def _update_qualification(self, qualification: Qualification) -> None:      
    
        self.execute(
            "UPDATE qualifications SET level = %s WHERE _id = %s;",
            qualification.level.value, qualification.id
        )
        
################################################################################
    def _update_training(self, training: Training) -> None:
        
        self.execute(
            "UPDATE trainings SET trainer = %s WHERE _id = %s;",
            None if training.trainer is None else training.trainer.user_id,
            training.id
        )

        for requirement_id, level in training.requirement_overrides.items():
            self.execute(
                "SELECT * FROM requirement_overrides WHERE training_id = %s "
                "AND requirement_id = %s;",
                training.id, requirement_id
            )
            match = self.fetchone()

            if match:
                self.execute(
                    "UPDATE requirement_overrides SET level = %s "
                    "WHERE training_id = %s AND requirement_id = %s;",
                    level.value, training.id, requirement_id
                )
            else:
                self.execute(
                    "INSERT INTO requirement_overrides (user_id, guild_id, "
                    "training_id, requirement_id, level) "
                    "VALUES (%s, %s, %s, %s, %s);",
                    training.user_id, training.trainee.guild_id, 
                    training.id, requirement_id, level.value
                )
        
################################################################################
    def _update_signup_message(self, guild_id: int, message: SignUpMessage) -> None:
        
        self.execute(
            "UPDATE bot_config SET signup_msg_channel = %s, signup_msg_id = %s "
            "WHERE guild_id = %s;",
            message.channel.id if message.channel is not None else None,
            message.message.id if message.message is not None else None,
            guild_id
        )
        
################################################################################
    
    log_channel     = _update_log_channel
    position        = _update_position
    requirement     = _update_requirement
    tuser           = _update_tuser
    availability    = _update_availability
    qualification   = _update_qualification
    training        = _update_training
    signup_message  = _update_signup_message
    
################################################################################
    