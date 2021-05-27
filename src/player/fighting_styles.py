

class FS_Test_1:

    _FS_NAME        = "Test FS 1"
    _FS_EXPLANATION = "This is a test fighting style so it gives the player extra 10 AC"
    _FS_IMAGE       = None

    def __init__(self, player): 

        self.player = player

        self.player.armor_class += 10

class FS_Test_2:

    _FS_NAME        = "Test FS 2"
    _FS_EXPLANATION = "This is another test fighting style so it gives the player extra 10 AC"
    _FS_IMAGE       = None

    def __init__(self, player): 

        self.player = player

        self.player.maxhealth += 10

_AVALIBLE_FIGHTING_STYLES = [

    FS_Test_1,
    FS_Test_2
]