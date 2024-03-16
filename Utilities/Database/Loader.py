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
            "venue_details" : self._load_venue_details(),
            "venue_locations" : self._load_venue_locations(),
            "venue_hours" : self._load_venue_hours(),
            "venue_aag" : self._load_venue_ataglance(),
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

        self.execute("SELECT * FROM venues;")
        return self.fetchall()
    
################################################################################
    def _load_venue_details(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_details;")
        return self.fetchall()
    
################################################################################
    def _load_venue_locations(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_locations;")
        return self.fetchall()
    
################################################################################
    def _load_venue_hours(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_hours;")
        return self.fetchall()
    
################################################################################
    def _load_venue_ataglance(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_aag;")
        return self.fetchall()
    
################################################################################
    