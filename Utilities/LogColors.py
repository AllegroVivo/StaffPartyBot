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
}
################################################################################
