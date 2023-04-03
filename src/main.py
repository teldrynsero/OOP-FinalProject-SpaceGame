import pygame
from pygame.locals import *
from pygame import mixer
from player import Player
from npc import Npc, Shopkeeper
from inventory import Inventory
from renderedtext import RenderedText
import sys
import os

#The use of multiple smaller classes (Player and Npc) that
#work with a bigger class (Game) is an example of the use
#of the ADVANCED DESIGN PATTERN known as FACADE. It helps
#in easier code readibility and organization.

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path,relative_path)

class Game:
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
        self.shop_rect = pygame.Rect((470,70),(80,35)) #npc boundaries
        self.ground = Game.load("ground")
        self.star = Game.load("star")

        music_url = resource_path("media/sounds/earthshine.mp3")
        mixer.music.load(music_url)
        mixer.music.set_volume(0.7)
        mixer.music.play()

        font_url = resource_path("media/Pixeled.ttf")
        self.font = pygame.font.Font(font_url, 15)
        self.beginning_text = self.font.render(self.renderedText.tutorial1, True, pygame.Color(255,255,255))
        self.npc_text = self.font.render('', True, pygame.Color(255,255,255))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False #close the game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: #enter key pressed
                self._image_surf = Game.load("morning_0") #change background
                self.game_started = True #start the game
                self.starting_text_show = True #render beginning text instructions

            if event.key == pygame.K_t: #talk to npc
                if self.game_started == True:
                    if ((self.player.x > 125) and (self.player.x < 285) and (self.player.y > 50) and (self.player.y < 110)): #if near npc
                        if self.nonplayablechar.npc_talking == False:
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
                            self.beginning_text = self.font.render(self.renderedText.tutorial5, True, pygame.Color(255,255,255)) #move on to next tutorial
                            self.shop_text = self.font.render(self.renderedText.shop, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                            self.shop_text1 = self.font.render(self.renderedText.shop1, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                            self.shop_text2 = self.font.render(self.renderedText.shop2, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                            self.shopkeeper.shop_talking = True #show SHOP npc text
                        else: #press t again to stop talking
                            self.shopkeeper.shop_talking = False
                            self.shopkeeper.purchasing = False
                            self.shopkeeper.selling = False

                #else ignore because the player is not near anything to talk to

            if event.key == pygame.K_i: #open inventory
                if self.show_inventory == True: #already open so close it
                    self.show_inventory = False
                else: #closed so open it
                    self.beginning_text = self.font.render(self.renderedText.tutorial4, True, pygame.Color(255,255,255))
                    #self.starting_text_show = False #tutorial ends for now
                    self.show_inventory = True

            if event.key == pygame.K_b: #buy seeds from shop
                if self.shopkeeper.shop_talking == True: #currently talking to shop
                    self.starting_text_show = False #tutorial ends for now
                    self.purchase_text = self.font.render(self.renderedText.purchase, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                    self.purchase_text1 = self.font.render(self.renderedText.purchase1, True, pygame.Color(255,255,255),pygame.Color(155,52,179))
                    self.shopkeeper.purchasing = True
                    self.shopkeeper.selling = False
            if event.key == pygame.K_n: #sell plants to shop
                if self.shopkeeper.shop_talking == True: #currently talking to shop
                    #print("sell here")
                    self.shopkeeper.selling = True
                    self.shopkeeper.purchasing = False

            if event.key == pygame.K_o: #buy elaberries
                if self.shopkeeper.purchasing == True: #purchase menu open
                    if self.inventory.rockTotal >= 10:
                        self.inventory.elaberrySeeds += 1
                        self.inventory.rockTotal -= 10

            if event.key == pygame.K_p: #buy elaberries
                if self.shopkeeper.purchasing == True: #purchase menu open
                    if self.inventory.rockTotal >= 5:
                        self.inventory.honeyshroomSeeds += 1
                        self.inventory.rockTotal -= 5

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

    def on_render(self):
        self._display_surf.blit(self._image_surf,(0,0))

        if self.game_started == True:
            self.npc = self.npcSprite[self.nonplayablechar.value]

            self._display_surf.blit(self.star,(0,0))
            self._display_surf.blit(self.ground,(0,0))
            self._display_surf.blit(self.npc,(200,70))
            self._display_surf.blit(self.shopkeeperSprite,(470,70))
            self._display_surf.blit(self.playerSprite,(self.player.x,self.player.y))

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
                self._display_surf.blit(self.shop_text, (260, 175))
                self._display_surf.blit(self.shop_text1, (220, 210))
                self._display_surf.blit(self.shop_text2, (220, 250))
                if self.shopkeeper.purchasing == True:
                    self._display_surf.blit(self.purchase_text, (140, 285))
                    self._display_surf.blit(self.purchase_text1, (130, 325))

            if self.show_inventory == True: #inventory shows seed amount and rock (currency amount)
                self.elaSeeds = self.font.render('Elaberry Seeds: ' + str(self.inventory.elaberrySeeds), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.elaSeeds, (10,365))
                self.honSeeds = self.font.render('Honeyshroom Seeds: ' + str(self.inventory.honeyshroomSeeds), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.honSeeds, (10,400))
                self.wallet_text = self.font.render("Rocks: " + str(self.inventory.rockTotal), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.wallet_text, (10,435))

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
    SpaceGame.on_execute()