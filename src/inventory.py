class Inventory:
    """keeps track of the player characters items and what they are holding
    """
    def __init__(self):
        """initialize default number of items and empty hand
        """
        self.equip = 1 #the seed the player is currently holding
        self.equipName = " "
        self.rockTotal = 0 #currency
        self.elaberrySeeds = 0
        self.honeyshroomSeeds = 0
        self.elaberryGrown = 0
        self.honeyshroomGrown = 0

    def update(self, plant):
        """update number of items when a plant it is subscribed to has been changed

        Args:
            plant (object): a plant to be watered then harvested
        """
        if plant.name == "honeyshroom":
            self.honeyshroomGrown += 1
        elif plant.name == "elaberries":
            self.elaberryGrown += 1