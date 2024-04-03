from typing import Dict

from Utilities import LogType, FroggeColor
################################################################################
# Set of colors for the log embeds.
LOG_COLORS: Dict[LogType, FroggeColor] = {
    LogType.MemberJoin: FroggeColor.brand_green(),
    LogType.MemberLeave: FroggeColor.brand_red(),
    LogType.TrainingSignup: FroggeColor.blue_green(),
    LogType.TrainingRemoved: FroggeColor.dark_sea_green(),
    LogType.TrainerAssigned: FroggeColor.dark_orange(),
    LogType.TrainingCompleted: FroggeColor.deep_sky_blue(),
    LogType.UserHiatus: FroggeColor.yellow(),
    LogType.VenueUserAdded: FroggeColor.blue_violet(),
    LogType.VenueUserRemoved: FroggeColor.light_pink(),
    LogType.VenueCreated: FroggeColor.dark_orange_red(),
    LogType.OwnerRemovalFlagged: FroggeColor.greenish_yellow(),
    LogType.VenueRemoved: FroggeColor.brick_red(),
    LogType.TempJobPosted: FroggeColor.orange_chocolate(),
    LogType.TempJobAccepted: FroggeColor.jungle_green(),
    LogType.TempJobCanceled: FroggeColor.deep_pink(),
    LogType.BGCheckSubmitted: FroggeColor.cornflower_blue(),
    LogType.BGCheckApproved: FroggeColor.fuchsia(),
}
################################################################################
