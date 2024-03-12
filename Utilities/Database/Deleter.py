from __future__ import annotations

from typing import TYPE_CHECKING

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    from Classes import Availability, Qualification, Training, AdditionalImage
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
    def _delete_availability(self, availability: Availability) -> None:
        
        self.execute(
            "DELETE FROM availability WHERE user_id = %s AND day = %s;",
            availability.parent.user_id, availability.day.value,
        )

################################################################################
    def _delete_qualification(self, qualification: Qualification) -> None:
        
        self.execute(
            "DELETE FROM qualifications WHERE _id = %s;",
            qualification.id,
        )
        
################################################################################        
    def _delete_training(self, training: Training) -> None:
        
        self.execute(
            "DELETE FROM trainings WHERE _id = %s;",
            training.id,
        )
        self.execute(
            "DELETE FROM requirement_overrides WHERE training_id = %s",
            training.id,
        )
        
################################################################################        
    def _delete_additional_image(self, additional: AdditionalImage) -> None:
        
        self.execute(
            "DELETE FROM additional_images WHERE _id = %s;",
            additional.id
        )
        
################################################################################

    requirement         = _delete_requirement
    availability        = _delete_availability
    qualification       = _delete_qualification
    training            = _delete_training
    profile_addl_image  = _delete_additional_image
    
################################################################################
    