from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Tuple

from .Branch import DBWorkerBranch

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("DatabaseLoader",)

################################################################################
class DatabaseLoader(DBWorkerBranch):
    """A utility class for loading data from the database."""

    def load_all(self) -> Dict[str, Any]:
        """Performs all sub-loaders and returns a dictionary of their results."""

        return {
            "bot_config": self._load_bot_config(),
            "positions" : self._load_positions(),
            "requirements" : self._load_requirements(),
            "tusers" : self._load_tusers(),
            "availability" : self._load_availability(),
            "qualifications" : self._load_qualifications(),
            "trainings" : self._load_trainings(),
            "requirement_overrides" : self._load_requirement_overrides(),
            "profiles" : self._load_profiles(),
            "additional_images" : self._load_additional_images(),
            "venues" : self._load_venues(),
            "venue_hours" : self._load_venue_hours(),
            "job_postings" : self._load_job_postings(),
            "hours" : self._load_job_hours(),
            "bg_checks" : self._load_bg_checks(),
            "roles" : self._load_roles(),
            "channels": self._load_channels(),
            "profile_availability" : self._load_profile_availability(),
            "service_configs" : self._load_service_configs(),
            "service_profiles" : self._load_service_profiles(),
            "services" : self._load_services(),
            "sp_availability" : self._load_sp_availability(),
            "sp_images" : self._load_sp_images(),
            "group_trainings": self._load_group_trainings(),
            "group_training_signups": self._load_group_training_signups(),
        }

################################################################################
    def _load_bot_config(self) -> Tuple[Any, ...]:
        
        self.execute("SELECT * FROM bot_config;")
        return self.fetchall()
        
################################################################################
    def _load_positions(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM positions;")
        return self.fetchall()
    
################################################################################
    def _load_requirements(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM requirements;")
        return self.fetchall()
    
################################################################################
    def _load_tusers(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM tuser_master;")
        return self.fetchall()
    
################################################################################
    def _load_availability(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM availability;")
        return self.fetchall()
    
################################################################################
    def _load_qualifications(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM qualifications;")
        return self.fetchall()
    
################################################################################
    def _load_trainings(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM trainings;")
        return self.fetchall()
    
################################################################################
    def _load_requirement_overrides(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM requirement_overrides;")
        return self.fetchall()
    
################################################################################
    def _load_profiles(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM profile_master;")
        return self.fetchall()

################################################################################
    def _load_additional_images(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM additional_images;")
        return self.fetchall()
    
################################################################################
    def _load_venues(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_master;")
        return self.fetchall()
    
################################################################################
    def _load_venue_hours(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_hours;")
        return self.fetchall()
    
################################################################################
    def _load_job_postings(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM job_postings;")
        return self.fetchall()
    
################################################################################
    def _load_job_hours(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM job_hours;")
        return self.fetchall()
    
################################################################################
    def _load_bg_checks(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM bg_checks;")
        return self.fetchall()
    
################################################################################
    def _load_roles(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM roles;")
        return self.fetchall()
    
################################################################################
    def _load_channels(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM channels;")
        return self.fetchall()
    
################################################################################
    def _load_profile_availability(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM profile_availability;")
        return self.fetchall()
    
################################################################################
    def _load_service_configs(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM service_config;")
        return self.fetchall()
    
################################################################################
    def _load_service_profiles(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM service_profiles;")
        return self.fetchall()
    
################################################################################
    def _load_services(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM services;")
        return self.fetchall()
    
################################################################################
    def _load_sp_availability(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM sp_availability;")
        return self.fetchall()
    
################################################################################
    def _load_sp_images(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM sp_images;")
        return self.fetchall()
    
################################################################################
    def _load_group_trainings(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM group_trainings;")
        return self.fetchall()
    
################################################################################
    def _load_group_training_signups(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM group_training_signups;")
        return self.fetchall()
    
################################################################################
