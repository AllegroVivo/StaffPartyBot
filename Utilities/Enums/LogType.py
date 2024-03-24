from ._Enum import FroggeEnum
################################################################################
class LogType(FroggeEnum):
    
    MemberJoin = 0
    MemberLeave = 1
    TrainingSignup = 2
    TrainingRemoved = 3
    TrainerAssigned = 4
    TrainingCompleted = 5
    UserHiatus = 6
    VenueUserAdded = 7
    VenueUserRemoved = 8
    VenueCreated = 9
    OwnerRemovalFlagged = 10
    VenueRemoved = 11

################################################################################
