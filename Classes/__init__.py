from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Packages
    from .Jobs import *
    from .Positions import *
    from .Profiles import *
    from .Services import *
    from .Training import *
    from .Venues import *
    from .XIVVenues import *
    
    # Modules
    from .Bot import StaffPartyBot
    from .ChannelManager import ChannelManager
    from .GuildData import GuildData
    from .GuildManager import GuildManager
    from .HelpMessage import HelpMessage
    from .Logger import Logger
    from .RoleManager import RoleManager
    from .Webhooks import FroggeHookManager
################################################################################
    