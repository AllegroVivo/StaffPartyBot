from __future__ import annotations

from typing import TYPE_CHECKING, List

from Utilities import DataCenter, GameWorld

if TYPE_CHECKING:
    from Classes import Position
################################################################################

__all__ = ("BGCheckVenue",)

################################################################################
class BGCheckVenue:

    __slots__ = (
        "_name",
        "_dc",
        "_world",
        "_jobs",
    )

################################################################################
    def __init__(self, name: str, dc: DataCenter, world: GameWorld, jobs: List[str]) -> None:

        self._name: str = name
        self._dc: DataCenter = dc
        self._world: GameWorld = world
        self._jobs: List[str] = jobs

################################################################################
    @classmethod
    def from_db_string(cls, db_string: str) -> BGCheckVenue:
        
        name, dc, world, jobs = db_string.split("::")
        return cls(name, DataCenter(dc), GameWorld(world), jobs.split("||"))
    
################################################################################
    @property
    def name(self) -> str:
        
        return self._name
        
################################################################################
    @property
    def data_center(self) -> DataCenter:
        
        return self._dc
    
################################################################################
    @property
    def world(self) -> GameWorld:
        
        return self._world
    
################################################################################
    @property
    def jobs(self) -> List[str]:
        
        return self._jobs
    
################################################################################
    def _to_db_string(self) -> str:
        
        jobs = "||".join(self._jobs)
        return f"{self._name}::{self._dc.value}::{self._world.value}::{jobs}"
    
################################################################################
