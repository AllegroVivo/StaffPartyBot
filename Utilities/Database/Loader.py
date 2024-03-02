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
            "tusers"    : self._load_tusers(),
            "tconfig" : self._load_tuser_config(),
            "availability" : self._load_availability(),
            "qualifications" : self._load_qualifications(),
            "trainings" : self._load_trainings(),
            "requirement_overrides" : self._load_requirement_overrides(),
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
        
        self.execute("SELECT * FROM tusers;")
        return self.fetchall()
    
################################################################################
    def _load_tuser_config(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM tuser_config;")
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
