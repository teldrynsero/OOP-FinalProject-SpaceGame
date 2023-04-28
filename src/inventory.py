class Inventory:
    def __init__(self):
        self.equip = 1 #the seed the player is currently holding
        self.equipName = " "
        self.rockTotal = 0 #currency
        self.elaberrySeeds = 0
        self.honeyshroomSeeds = 0
        self.elaberryGrown = 0
        self.honeyshroomGrown = 0

    def update(self, plant):
        if plant.name == "honeyshroom":
            self.honeyshroomGrown += 1
        elif plant.name == "elaberries":
            self.elaberryGrown += 1