import pygame
from pygame.locals import *
from pygame import mixer
from player import Player
from npc import Npc, Shopkeeper
from inventory import Inventory
from renderedtext import RenderedText
import sys
import os
from plant import Plant

#The use of multiple smaller classes (ex. Player & Npc) that
#work with a bigger class (Game) is an example of the use
#of the ADVANCED DESIGN PATTERN known as FACADE. It helps
#in easier code readibility and organization.

#The code uses the COMMON DESIGN PATTERN known as SINGLETON.
#It is implemented using a classic singleton, wherein an
#instance of a class is only created once (in this case, it
#is the Game class). Throughout the lifetime of the program,
#only one Game instance is needed, thus making the use of
#the singleton pattern useful.

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path,relative_path)


class Game:
    def __new__(cls): #create instance if none exist, else only use preexisting instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 480
        self._image_surf = None
        self.player = Player() #initialize player
        self.inventory = Inventory() #initialize inventory
        self.nonplayablechar = Npc() #initialize npc
        self.shopkeeper = Shopkeeper() #initialize shop npc
        self.renderedText = RenderedText() #initialize text to be rendered
        self.game_started = False
        self.starting_text_show = False
        self.show_inventory = False
        self.clock = pygame.time.Clock()
        self.garden = {} # keep track of all planted seeds
        self.picked_plants = []

    def load(image): #makes loading images easier
        imageName = image
        imageTitle = resource_path("media/img/"+str(imageName)+".png")
        image = pygame.image.load(imageTitle)
        return image
 
    def on_init(self):
        pygame.init()
        mixer.init()
        pygame.display.set_caption('Space Farm Game')

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._image_surf = Game.load("startscreen") #background

        self.playerSprite = Game.load("player_0")
        self.npcSprite = [Game.load("npc"), Game.load("npc_1"), Game.load("npc"), Game.load("npc_1"),]
        self.npc_rect = pygame.Rect((200,70),(80,35)) #npc boundaries
        self.shopkeeperSprite = Game.load("shop")
        self.shop_rect = pygame.Rect((470,70),(80,35)) #shopkeeper npc boundaries
        self.ground = Game.load("ground")
        self.star = Game.load("star")

        #sound effects
        error_url = resource_path("media/sounds/invalid.mp3")
        self.error_sound = pygame.mixer.Sound(error_url)
        buy_url = resource_path("media/sounds/buy.mp3")
        self.buy_sound = pygame.mixer.Sound(buy_url)
        open_url = resource_path("media/sounds/inventoryunzip.mp3")
        self.open_sound = pygame.mixer.Sound(open_url)

        npc_talk_url = resource_path("media/sounds/npctalk.mp3")
        self.npc_talk_sound = pygame.mixer.Sound(npc_talk_url)
        shop_talk_url = resource_path("media/sounds/shoptalk.mp3")
        self.shop_talk_sound = pygame.mixer.Sound(shop_talk_url)

        planting_url = resource_path("media/sounds/plant.wav")
        self.planting_sound = pygame.mixer.Sound(planting_url)
        water_url = resource_path("media/sounds/water.wav")
        self.water_sound = pygame.mixer.Sound(water_url)

        music_url = resource_path("media/sounds/earthshine.mp3")
        mixer.music.load(music_url)
        mixer.music.set_volume(0.7)
        mixer.music.play(-1) #plays forever

        font_url = resource_path("media/img/Pixeled.ttf")
        self.font = pygame.font.Font(font_url, 15)
        self.beginning_text = self.font.render(self.renderedText.tutorial1, True, pygame.Color(255,255,255))
        self.npc_text = self.font.render('', True, pygame.Color(255,255,255))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False #close the game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: #enter key pressed
                if self.game_started == False: #game isn't started so start it now
                    self._image_surf = Game.load("morning_0") #change background
                    self.game_started = True #start the game
                    self.starting_text_show = True #render beginning text instructions

            if event.key == pygame.K_t: #talk to npc
                if self.game_started == True:
                    if ((self.player.x > 125) and (self.player.x < 285) and (self.player.y > 50) and (self.player.y < 110)): #if near npc
                        if self.nonplayablechar.npc_talking == False:
                            pygame.mixer.Sound.play(self.npc_talk_sound)
                            self.beginning_text = self.font.render(self.renderedText.tutorial3, True, pygame.Color(255,255,255)) #move on to next tutorial
                            if self.nonplayablechar.first_time_talking == True:
                                self.npc_text = self.font.render(self.renderedText.npc1, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                                self.inventory.rockTotal += 50 #npc gives rocks only on first talk
                                self.nonplayablechar.first_time_talking = False
                            else:
                                self.npc_text = self.font.render(self.renderedText.npc2, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                            self.nonplayablechar.npc_talking = True #show npc text
                        else: #press t again to stop talking
                            self.npc_text = self.font.render(' ', True, pygame.Color(255,255,255))
                            self.nonplayablechar.value = 0 #animation stops
                            self.nonplayablechar.npc_talking = False

                    if ((self.player.x > 390) and (self.player.x < 600) and (self.player.y > 50) and (self.player.y < 110)): #if near SHOP NPC
                        if self.shopkeeper.shop_talking == False:
                            pygame.mixer.Sound.play(self.shop_talk_sound)
                            self.beginning_text = self.font.render(self.renderedText.tutorial5, True, pygame.Color(255,255,255)) #move on to next tutorial
                            self.shop_text = self.font.render(self.renderedText.shop, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                            self.shop_text1 = self.font.render(self.renderedText.shop1, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                            self.shop_text2 = self.font.render(self.renderedText.shop2, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                            self.shopkeeper.shop_talking = True #show SHOP npc text
                        else: #press t again to stop talking
                            self.beginning_text = self.font.render(self.renderedText.tutorial7, True, pygame.Color(255,255,255))
                            self.shopkeeper.shop_talking = False
                            self.shopkeeper.purchasing = False
                            self.shopkeeper.selling = False

                #else ignore because the player is not near anything to talk to

            if event.key == pygame.K_i: #open inventory
                pygame.mixer.Sound.play(self.open_sound)
                if self.show_inventory == True: #already open so close it
                    self.show_inventory = False
                else: #closed so open it
                    self.beginning_text = self.font.render(self.renderedText.tutorial4, True, pygame.Color(255,255,255))
                    self.show_inventory = True

            if event.key == pygame.K_b: #buy seeds from shop
                if self.shopkeeper.shop_talking == True: #currently talking to shop
                    #self.starting_text_show = False #tutorial ends for now
                    self.beginning_text = self.font.render(self.renderedText.tutorial6, True, pygame.Color(255,255,255))
                    self.purchase_text = self.font.render(self.renderedText.purchase, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                    self.purchase_text1 = self.font.render(self.renderedText.purchase1, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                    self.shopkeeper.purchasing = True
                    self.shopkeeper.selling = False

            if event.key == pygame.K_n: #sell plants to shop
                if self.shopkeeper.shop_talking == True: #currently talking to shop
                    self.sell_text = self.font.render(self.renderedText.sell, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                    self.sell_text1 = self.font.render(self.renderedText.sell1, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                    self.shopkeeper.selling = True
                    self.shopkeeper.purchasing = False

            if event.key == pygame.K_o: #buy OR sell elaberries
                if self.shopkeeper.purchasing == True: #purchase menu open
                    if self.inventory.rockTotal >= 10: #player can buy elaberry
                        self.inventory.elaberrySeeds += 1
                        self.inventory.rockTotal -= 10
                        pygame.mixer.Sound.play(self.buy_sound)
                    else: #player cannot afford it
                        pygame.mixer.Sound.play(self.error_sound)
                if self.shopkeeper.selling == True: #selling menu open
                    if self.inventory.elaberryGrown >= 1: #player has at least 1 grown elaberry
                        self.inventory.elaberryGrown -= 1
                        self.inventory.rockTotal += 40
                        pygame.mixer.Sound.play(self.buy_sound)
                    else: #player has no grown elaberry
                        pygame.mixer.Sound.play(self.error_sound)

            if event.key == pygame.K_p: #buy OR sell honeyshrooms
                if self.shopkeeper.purchasing == True: #purchase menu open
                    if self.inventory.rockTotal >= 5: #player can buy honeyshroom
                        self.inventory.honeyshroomSeeds += 1
                        self.inventory.rockTotal -= 5
                        pygame.mixer.Sound.play(self.buy_sound)
                    else: #player cannot afford it
                        pygame.mixer.Sound.play(self.error_sound)
                if self.shopkeeper.selling == True: #selling menu open
                    if self.inventory.honeyshroomGrown >= 1:
                        self.inventory.honeyshroomGrown -= 1
                        self.inventory.rockTotal += 20
                        pygame.mixer.Sound.play(self.buy_sound)
                    else: #player has no grown honeyshroom
                        pygame.mixer.Sound.play(self.error_sound)

            if event.key == pygame.K_f: #change between equipped seeds
                if self.inventory.equip == 1:
                    self.inventory.equip = 2
                    self.inventory.equipName = "Honeyshrooms"
                elif self.inventory.equip == 2:
                    self.inventory.equip = 1
                    self.inventory.equipName = "Elaberries"
                    
            if event.key == pygame.K_e: # planting
                if self.inventory.equipName == "Honeyshrooms": # "holding" honeyshrooms
                    if self.inventory.honeyshroomSeeds >= 1:
                        self.inventory.honeyshroomSeeds -=1
                        Game.create_plant(self,"honeyshroom")
                        print(self.garden)
                elif self.inventory.equipName == "Elaberries": # "holding" elaberries
                    if self.inventory.elaberrySeeds >= 1:
                        self.inventory.elaberrySeeds -=1
                        Game.create_plant(self,"elaberries")
                        print(self.garden)
                pygame.mixer.Sound.play(self.planting_sound)

            if event.key == pygame.K_q: # watering
                for key in self.garden:
                    if self.playerSprite_rect.colliderect(key.plant_bounds):
                        if key.stage < key.max_stage:
                            key.stage +=1
                            pygame.mixer.Sound.play(self.water_sound)
                        else:
                            if key.name == "honeyshroom_":
                                self.inventory.honeyshroomGrown +=1
                            elif key.name == "elaberries_":
                                self.inventory.elaberryGrown +=1
                            self.picked_plants.append(key)
                        # print(key.name + str(key.stage))
                for item in self.picked_plants:
                    del self.garden[item]
                    del item
                self.picked_plants.clear()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: #stopped moving left
                self.playerSprite = Game.load("player_4")
            if event.key == pygame.K_d: #stopped moving right
                self.playerSprite = Game.load("player_6")
            if event.key == pygame.K_s: #stopped moving down
                self.playerSprite = Game.load("player_0")
            if event.key == pygame.K_w: #stopped moving up
                self.playerSprite = Game.load("player_2")

        pygame.display.update()

    def on_loop(self):
        time_now = pygame.time.get_ticks()
        if (time_now > self.nonplayablechar.next_frame_time): #show npc animation
            if self.nonplayablechar.npc_talking == True: #npc was talked to
                inter_frame_delay = 1000 // self.nonplayablechar.fps   
                self.nonplayablechar.next_frame_time = time_now + inter_frame_delay
                self.nonplayablechar.value += 1
                if self.nonplayablechar.value >= len(self.npcSprite):
                    self.nonplayablechar.value = 0

    def create_plant(self, plant_name):
        self.plant = Plant(plant_name, self.player.x, self.player.y)
        # self.all_plants.setdefault((self.player.x, self.player.y), self.plant)
        self.garden.setdefault(self.plant, self.plant.plant_bounds)
        print(self.plant.name)
        self.plant_sprite = Game.load(self.plant.name + str(self.plant.stage))
        # self.plant_rect = self.plant_sprite.get_rect(bottomright = (self.player.x, self.player.y))
        # self._display_surf.blit(self.plant_sprite,(self.player.x,self.player.y))

    def on_render(self):
        self._display_surf.blit(self._image_surf,(0,0))

        if self.game_started == True:
            self.npc = self.npcSprite[self.nonplayablechar.value]

            #display all image assets once game starts
            self._display_surf.blit(self.star,(0,0))
            self._display_surf.blit(self.ground,(0,0))
            self._display_surf.blit(self.npc,(200,70))
            self._display_surf.blit(self.shopkeeperSprite,(470,70))
            self._display_surf.blit(self.playerSprite,(self.player.x,self.player.y))

            for key in self.garden:
                self.plant_sprite = Game.load(key.name + str(key.stage))
                # self.plant_rect = self.plant_sprite.get_rect(bottomright = (self.player.x, self.player.y))
                self._display_surf.blit(self.plant_sprite,key.plant_point)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.player.x -= 1
                self.player.x_change = -1
                self.playerSprite = Game.load("player_5")
                self.playerSprite_rect = self.playerSprite.get_rect(topleft = (self.player.x, self.player.y))
                if self.playerSprite_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.x_change > 0:
                        self.playerSprite_rect.right = self.npc_rect.left
                    elif self.player.x_change < 0:
                        self.playerSprite_rect.left = self.npc_rect.right
                    self.player.x = self.playerSprite_rect.x

                if self.playerSprite_rect.colliderect(self.shop_rect): #did player collide with SHOP npc?
                    if self.player.x_change > 0:
                        self.playerSprite_rect.right = self.shop_rect.left
                    elif self.player.x_change < 0:
                        self.playerSprite_rect.left = self.shop_rect.right
                    self.player.x = self.playerSprite_rect.x

            if keys[pygame.K_d]:
                self.player.x += 1
                self.player.x_change = 1
                self.playerSprite = Game.load("player_7")
                self.playerSprite_rect = self.playerSprite.get_rect(topleft = (self.player.x, self.player.y))
                if self.playerSprite_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.x_change > 0:
                        self.playerSprite_rect.right = self.npc_rect.left
                    elif self.player.x_change < 0:
                        self.playerSprite_rect.left = self.npc_rect.right
                    self.player.x = self.playerSprite_rect.x

                if self.playerSprite_rect.colliderect(self.shop_rect): #did player collide with SHOP npc?
                    if self.player.x_change > 0:
                        self.playerSprite_rect.right = self.shop_rect.left
                    elif self.player.x_change < 0:
                        self.playerSprite_rect.left = self.shop_rect.right
                    self.player.x = self.playerSprite_rect.x

            if keys[pygame.K_w]:
                self.player.y -= 1
                self.player.y_change = -1
                self.playerSprite = Game.load("player_3")
                self.playerSprite_rect = self.playerSprite.get_rect(topleft = (self.player.x, self.player.y))
                if self.playerSprite_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.y_change < 0:
                        self.playerSprite_rect.top = self.npc_rect.bottom
                    elif self.player.y_change > 0:
                        self.playerSprite_rect.bottom = self.npc_rect.top
                    self.player.y = self.playerSprite_rect.y

                if self.playerSprite_rect.colliderect(self.shop_rect): #did player collide with SHOP npc?
                    if self.player.y_change < 0:
                        self.playerSprite_rect.top = self.shop_rect.bottom
                    elif self.player.y_change > 0:
                        self.playerSprite_rect.bottom = self.shop_rect.top
                    self.player.y = self.playerSprite_rect.y

            if keys[pygame.K_s]:
                self.player.y += 1
                self.player.y_change = 1
                self.playerSprite = Game.load("player_1")
                self.playerSprite_rect = self.playerSprite.get_rect(topleft = (self.player.x, self.player.y))
                if self.playerSprite_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.y_change < 0:
                        self.playerSprite_rect.top = self.npc_rect.bottom
                    elif self.player.y_change > 0:
                        self.playerSprite_rect.bottom = self.npc_rect.top
                    self.player.y = self.playerSprite_rect.y

                if self.playerSprite_rect.colliderect(self.shop_rect): #did player collide with SHOP npc?
                    if self.player.y_change < 0:
                        self.playerSprite_rect.top = self.shop_rect.bottom
                    elif self.player.y_change > 0:
                        self.playerSprite_rect.bottom = self.shop_rect.top
                    self.player.y = self.playerSprite_rect.y

            #player walking boundaries
            if self.player.x < 0:
                self.player.x = 0

            if self.player.x > 570:
                self.player.x = 570
            
            if self.player.y > 370:
                self.player.y = 370

            if self.player.y < 60:
                self.player.y = 60
                
            if self.starting_text_show == True: #tutorial text
                if keys[pygame.K_a] or keys[pygame.K_s] or  keys[pygame.K_w] or  keys[pygame.K_d]: #player has used WASD
                    if self.player.first_move == True:
                        self.beginning_text = self.font.render(self.renderedText.tutorial2, True, pygame.Color(255,255,255)) #move on to next tutorial
                        self._display_surf.blit(self.beginning_text, (170,15))
                        self.player.first_move = False
                self._display_surf.blit(self.beginning_text, (170,15))

            if self.nonplayablechar.npc_talking == True: #npc talking text
                self._display_surf.blit(self.npc_text, (300,50))

            if self.shopkeeper.shop_talking == True: #SHOP npc talking text
                self._display_surf.blit(self.shop_text, (260, 115))
                self._display_surf.blit(self.shop_text1, (220, 150))
                self._display_surf.blit(self.shop_text2, (220, 190))
                if self.shopkeeper.purchasing == True:
                    self._display_surf.blit(self.purchase_text, (140, 225))
                    self._display_surf.blit(self.purchase_text1, (130, 265))
                if self.shopkeeper.selling == True:
                    self._display_surf.blit(self.sell_text, (140, 225))
                    self._display_surf.blit(self.sell_text1, (130, 265))

            if self.show_inventory == True: #inventory shows seed amount and rock (currency amount) and grown crops
                self.equippedSeeds = self.font.render('Equipped Seeds: ' + str(self.inventory.equipName), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.equippedSeeds, (10,330))
                self.elaSeeds = self.font.render('Elaberry Seeds: ' + str(self.inventory.elaberrySeeds), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.elaSeeds, (10,365))
                self.honSeeds = self.font.render('Honeyshroom Seeds: ' + str(self.inventory.honeyshroomSeeds), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.honSeeds, (10,400))
                self.wallet_text = self.font.render("Rocks: " + str(self.inventory.rockTotal), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.wallet_text, (10,435))
                self.elaberry = self.font.render('Elaberries: ' + str(self.inventory.elaberryGrown), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.elaberry, (470, 365))
                self.honeyshroom = self.font.render('Honeyshrooms: ' + str(self.inventory.honeyshroomGrown), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.honeyshroom, (420, 400))

        pygame.display.flip() #update sprite

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            self.clock.tick(60) #60 fps
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    SpaceGame = Game()
    #nextGame = Game()
    #print(SpaceGame is nextGame) #ensure only one Game instance is made
    SpaceGame.on_execute()