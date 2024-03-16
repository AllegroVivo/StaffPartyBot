from typing import List

from discord import SelectOption

from ._Enum import FroggeEnum
from .DataCenter import DataCenter
################################################################################
class GameWorld(FroggeEnum):

    Adamantoise = 1
    Alpha = 2
    Balmung = 3
    Behemoth = 4
    Bismarck = 5
    Brynhildr = 6
    Cactuar = 7
    Cerberus = 8
    Coeurl = 9
    Diabolos = 10
    Excalibur = 11
    Exodus = 12
    Faerie = 13
    Famfrit = 14
    Gilgamesh = 15
    Goblin = 16
    Halicarnassus = 17
    Hyperion = 18
    Jenova = 19
    Lamia = 20
    Leviathan = 21
    Lich = 22
    Louisoix = 23
    Maduin = 24
    Malboro = 25
    Marilith = 26
    Mateus = 27
    Midgardsormr = 28
    Moogle = 29
    Odin = 30
    Omega = 31
    Phantom = 32
    Phoenix = 33
    Ragnarok = 34
    Raiden = 35
    Ravana = 36
    Sagittarius = 37
    Sargatanas = 38
    Sephirot = 39
    Seraph = 40
    Shiva = 41
    Siren = 42
    Sophia = 43
    Spriggan = 44
    Twintania = 45
    Ultros = 46
    Zalera = 47
    Zodiark = 48
    Zurvan = 49

################################################################################
    @staticmethod
    def select_options_by_dc(dc: DataCenter) -> List[SelectOption]:
        
        if dc is DataCenter.Aether:
            world_list = [
                GameWorld.Adamantoise,
                GameWorld.Cactuar,
                GameWorld.Faerie,
                GameWorld.Gilgamesh,
                GameWorld.Jenova,
                GameWorld.Midgardsormr,
                GameWorld.Sargatanas,
                GameWorld.Siren,
            ]
        elif dc is DataCenter.Crystal:
            world_list = [
                GameWorld.Balmung,
                GameWorld.Brynhildr,
                GameWorld.Coeurl,
                GameWorld.Diabolos,
                GameWorld.Goblin,
                GameWorld.Malboro,
                GameWorld.Mateus,
                GameWorld.Zalera,
            ]
        elif dc is DataCenter.Dynamis:
            world_list = [
                GameWorld.Halicarnassus,
                GameWorld.Maduin,
                GameWorld.Marilith,
                GameWorld.Seraph,
            ]
        elif dc is DataCenter.Primal:
            world_list = [
                GameWorld.Behemoth,
                GameWorld.Excalibur,
                GameWorld.Exodus,
                GameWorld.Famfrit,
                GameWorld.Hyperion,
                GameWorld.Lamia,
                GameWorld.Leviathan,
                GameWorld.Ultros,
            ]
        elif dc is DataCenter.Chaos:
            world_list = [
                GameWorld.Cerberus,
                GameWorld.Louisoix,
                GameWorld.Moogle,
                GameWorld.Omega,
                GameWorld.Phantom,
                GameWorld.Ragnarok,
                GameWorld.Sagittarius,
                GameWorld.Spriggan,
            ]
        elif dc is DataCenter.Light:
            world_list = [
                GameWorld.Alpha,
                GameWorld.Lich,
                GameWorld.Odin,
                GameWorld.Phoenix,
                GameWorld.Raiden,
                GameWorld.Shiva,
                GameWorld.Twintania,
                GameWorld.Zodiark,
            ]
        else:
            world_list = [
                GameWorld.Bismarck,
                GameWorld.Ravana,
                GameWorld.Sephirot,
                GameWorld.Sophia,
                GameWorld.Zurvan,
            ]
            
        return [world.select_option for world in world_list]
    
################################################################################
