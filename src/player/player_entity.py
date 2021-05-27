import math


class PlayerEntity:


    def __init__(self):

        self.player_name    = None

        self.player_race    = None
        self.player_class   = None

        # initialize stats
        self.stat_str   = 0
        self.stat_dex   = 0
        self.stat_con   = 0
        self.stat_int   = 0
        self.stat_wis   = 0
        self.stat_cha   = 0

        # Combat stats
        self.experience     = 0
        self.level          = 0
        self.hit_dice       = 0
        self.max_health     = self.hit_dice + ((self.hit_dice//2) * self.level - 1) + (((self.stat_con - 10)//2) * self.level)
        self.current_heath  = self.max_health
        self.armor_class    = 10 + ((self.stat_dex - 10)//2)
        self.proficiency_b  = math.ceil((self.level/4)) + 1 # NOT SURE IF THIS WORKS CHECK IT PROPERLY IN THE FUTURE

        # initialize other aspects
        self.movement_speed         = 0
        self.attack_per_action      = 0
        self.action_per_turn        = 0
        self.bonus_action_per_turn  = 0
        
        # initialize resistances
        self.cold_resitance         = False
        self.fire_resitance         = False
        self.acid_resistance        = False
        self.poison_resitance       = False
        self.radiant_resistance     = False
        self.necrotic_resistance    = False
        self.thunder_resitance      = False
        self.lightning_resistance   = False
        self.psychic_resistance     = False
        self.force_resistance       = False

        # spellcasting
        self.cantrips       = []
        self.spells         = []
        self.level_1_spell  = []
        self.level_2_spell  = []
        self.level_3_spell  = []
        self.level_4_spell  = []
        self.level_5_spell  = []
        self.level_6_spell  = []
        self.level_7_spell  = []
        self.level_8_spell  = []
        self.level_9_spell  = []



