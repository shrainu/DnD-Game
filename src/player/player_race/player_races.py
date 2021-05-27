from src.player.player_entity import PlayerEntity


# RACE_DATA ----------------------------------------------------------
class Race_RaceData:

    race_names_list = []
    race_list = []


# BASE_RACE ----------------------------------------------------------
class Race_BaseRace():

    RACE_NAME = "Base_Race"

    def __init__(self, player, player_race, str_bonus = 0, dex_bonus = 0, con_bonus = 0, int_bonus = 0, wis_bonus = 0, cha_bonus = 0, movement_speed = 30):

        player.player_race = player_race

        # initialize stats
        player.stat_str += str_bonus
        player.stat_dex += dex_bonus
        player.stat_con += con_bonus
        player.stat_int += int_bonus
        player.stat_wis += wis_bonus
        player.stat_cha += cha_bonus

        # initialize other aspects
        player.movement_speed = movement_speed


# HUMAN --------------------------------------------------------------
class Race_Human(Race_BaseRace):

    RACE_NAME = "Human"

    def __init__(self, player):
        
        # Initialize parent
        super().__init__(
            player          =player,
            player_race     =Race_Human,
            str_bonus       =1,
            dex_bonus       =1,
            con_bonus       =1,
            int_bonus       =1,
            wis_bonus       =1,
            cha_bonus       =1,
            movement_speed  =30
        )


# ELF ----------------------------------------------------------------
class Race_Elf(Race_BaseRace):

    RACE_NAME = "Elf"

    def __init__(self, player):
        
        # Initialize parent
        super().__init__(
            player          =player,
            player_race     =Race_Elf,
            str_bonus       =0,
            dex_bonus       =2,
            con_bonus       =0,
            int_bonus       =0,
            wis_bonus       =0,
            cha_bonus       =0,
            movement_speed  =30
        )


# HALF-ELF -----------------------------------------------------------
class Race_HalfElf(Race_BaseRace):

    RACE_NAME = "Half-Elf"

    def __init__(self, player):
        
        # Initialize parent
        super().__init__(
            player          =player,
            player_race     =Race_HalfElf,
            str_bonus       =0,
            dex_bonus       =0,
            con_bonus       =0,
            int_bonus       =0,
            wis_bonus       =0,
            cha_bonus       =2,
            movement_speed  =30
        )


# TIEFLING -----------------------------------------------------------
class Race_Tiefling(Race_BaseRace):

    RACE_NAME = "Tiefling"

    def __init__(self, player):
        
        # Initialize parent
        super().__init__(
            player          =player,
            player_race     =Race_Tiefling,
            str_bonus       =0,
            dex_bonus       =0,
            con_bonus       =0,
            int_bonus       =1,
            wis_bonus       =0,
            cha_bonus       =2,
            movement_speed  =30
        )


# RACE DATAS ---------------------------------------------------------
_AVALIBLE_RACES = [

    Race_Human,
    Race_Elf,
    Race_HalfElf,
    Race_Tiefling
]
'''
Currently disabled due a player parameter is necessary in order to
create any of the player_race objects..
# Add all the race names to Race_RaceData's race_names list
Race_RaceData.race_names_list = [
    Race_Human.race_name,
    Race_Elf.race_name,
    Race_HalfElf.race_name,
    Race_Tiefling.race_name,
]
# Add all race to Race_RaceData's race list
__human = Race_Human()
__elf = Race_Elf()
__half_elf = Race_HalfElf()
__tiefling = Race_Tiefling()
Race_RaceData.race_list = [
    __human,
    __elf,
    __half_elf,
    __tiefling,
]
'''