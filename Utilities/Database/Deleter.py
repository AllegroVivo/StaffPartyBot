from __future__ import annotations

from typing import TYPE_CHECKING

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Availability, Qualification, Training
################################################################################

__all__ = ("DatabaseDeleter",)

################################################################################
class DatabaseDeleter(DBWorkerBranch):
    """A utility class for deleting data from the database."""

    def _delete_requirement(self, req_id: str) -> None:
        
        self.execute(
            "DELETE FROM requirements WHERE _id = %s;",
            req_id,
        )
      
################################################################################  
    def delete_availability(self, availability: Availability) -> None:
        
        self.execute(
            "DELETE FROM availability WHERE user_id = %s AND day = %s;",
            availability.parent.user_id, availability.day.value,
        )

################################################################################
    def delete_qualification(self, qualification: Qualification) -> None:
        
        self.execute(
            "DELETE FROM qualifications WHERE _id = %s;",
            qualification.id,
        )
        
################################################################################        
    def delete_training(self, training: Training) -> None:
        
        self.execute(
            "DELETE FROM trainings WHERE _id = %s;",
            training.id,
        )
        self.execute(
            "DELETE FROM requirement_overrides WHERE training_id = %s",
            training.id,
        )
        
################################################################################

    requirement    = _delete_requirement
    availability   = delete_availability
    qualification  = delete_qualification
    training       = delete_training
    
################################################################################
    