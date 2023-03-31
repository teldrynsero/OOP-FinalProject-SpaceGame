import pygame
from pygame.locals import *
from pygame import mixer
from player import Player
from npc import Npc
from inventory import Inventory
from renderedtext import RenderedText

#The use of multiple smaller classes (Player and Npc) that
#work with a bigger class (Game) is an example of the use
#of the ADVANCED DESIGN PATTERN known as FACADE. It helps
#in easier code readibility and organization.

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 480
        self._image_surf = None
        self.player = Player() #initialize player
        self.inventory = Inventory() #initialize inventory
        self.nonplayablechar = Npc() #initialize npc
        self.renderedText = RenderedText() #initialize text to be rendered
        self.game_started = False
        self.starting_text_show = False
        self.show_inventory = False
        self.clock = pygame.time.Clock()

    def load(image): #makes loading images easier
        imageName = image
        imageTitle = "media/img/"+str(imageName)+".png"
        image = pygame.image.load(imageTitle)
        return image
 
    def on_init(self):
        pygame.init()
        mixer.init()
        pygame.display.set_caption('Space Farm Game')

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._image_surf = Game.load("startscreen") #background

        self.frog = Game.load("player_0")
        self.npc_cycle = [Game.load("npc"), Game.load("npc_1"), Game.load("npc"), Game.load("npc_1"),]
        self.npc_rect = pygame.Rect((200,70),(80,35)) #npc boundaries
        self.ground = Game.load("ground")
        self.star = Game.load("star")

        mixer.music.load("media/sounds/earthshine.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()

        self.font = pygame.font.Font('media/Pixeled.ttf', 15)
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
                                self.npc_text = self.font.render(self.renderedText.npc1, True, pygame.Color(255,255,255))
                                self.inventory.rockTotal += 50 #npc gives rocks only on first talk
                                self.nonplayablechar.first_time_talking = False
                            else:
                                self.npc_text = self.font.render(self.renderedText.npc2, True, pygame.Color(255,255,255))
                            self.nonplayablechar.npc_talking = True #show npc text
                        else: #press t again to stop talking
                            self.npc_text = self.font.render(' ', True, pygame.Color(255,255,255))
                            self.nonplayablechar.value = 0 #animation stops
                            self.nonplayablechar.npc_talking = False

                #else ignore because the player is not near anything to talk to

            if event.key == pygame.K_i: #open inventory
                if self.show_inventory == True: #already open so close it
                    self.show_inventory = False
                else: #closed so open it
                    self.starting_text_show = False #tutorial ends for now
                    self.show_inventory = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: #stopped moving left
                self.frog = Game.load("player_4")
            if event.key == pygame.K_d: #stopped moving right
                self.frog = Game.load("player_6")
            if event.key == pygame.K_s: #stopped moving down
                self.frog = Game.load("player_0")
            if event.key == pygame.K_w: #stopped moving up
                self.frog = Game.load("player_2")

        pygame.display.update()

    def on_loop(self):
        time_now = pygame.time.get_ticks()
        if (time_now > self.nonplayablechar.next_frame_time): #show npc animation
            if self.nonplayablechar.npc_talking == True: #npc was talked to
                inter_frame_delay = 1000 // self.nonplayablechar.fps   
                self.nonplayablechar.next_frame_time = time_now + inter_frame_delay
                self.nonplayablechar.value += 1
                if self.nonplayablechar.value >= len(self.npc_cycle):
                    self.nonplayablechar.value = 0

    def on_render(self):
        self._display_surf.blit(self._image_surf,(0,0))

        if self.game_started == True:
            self.npc = self.npc_cycle[self.nonplayablechar.value]

            self._display_surf.blit(self.star,(0,0))
            self._display_surf.blit(self.ground,(0,0))
            self._display_surf.blit(self.npc,(200,70))
            self._display_surf.blit(self.frog,(self.player.x,self.player.y))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.player.x -= 1
                self.player.x_change = -1
                self.frog = Game.load("player_5")
                self.frog_rect = self.frog.get_rect(topleft = (self.player.x, self.player.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.x_change > 0:
                        self.frog_rect.right = self.npc_rect.left
                    elif self.player.x_change < 0:
                        self.frog_rect.left = self.npc_rect.right
                    self.player.x = self.frog_rect.x

            if keys[pygame.K_d]:
                self.player.x += 1
                self.player.x_change = 1
                self.frog = Game.load("player_7")
                self.frog_rect = self.frog.get_rect(topleft = (self.player.x, self.player.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.x_change > 0:
                        self.frog_rect.right = self.npc_rect.left
                    elif self.player.x_change < 0:
                        self.frog_rect.left = self.npc_rect.right
                    self.player.x = self.frog_rect.x

            if keys[pygame.K_w]:
                self.player.y -= 1
                self.player.y_change = -1
                self.frog = Game.load("player_3")
                self.frog_rect = self.frog.get_rect(topleft = (self.player.x, self.player.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.y_change < 0:
                        self.frog_rect.top = self.npc_rect.bottom
                    elif self.player.y_change > 0:
                        self.frog_rect.bottom = self.npc_rect.top
                    self.player.y = self.frog_rect.y

            if keys[pygame.K_s]:
                self.player.y += 1
                self.player.y_change = 1
                self.frog = Game.load("player_1")
                self.frog_rect = self.frog.get_rect(topleft = (self.player.x, self.player.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.player.y_change < 0:
                        self.frog_rect.top = self.npc_rect.bottom
                    elif self.player.y_change > 0:
                        self.frog_rect.bottom = self.npc_rect.top
                    self.player.y = self.frog_rect.y

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
                    self.beginning_text = self.font.render(self.renderedText.tutorial2, True, pygame.Color(255,255,255)) #move on to next tutorial
                    self._display_surf.blit(self.beginning_text, (180,25))
                self._display_surf.blit(self.beginning_text, (180,25))

            if self.nonplayablechar.npc_talking == True: #npc talking text
                self._display_surf.blit(self.npc_text, (300,50))

            if self.show_inventory == True: #inventory shows seed amount and rock (currency amount)
                self.elaSeeds = self.font.render('Elaberry Seeds: ' + str(self.inventory.elaberrySeeds), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.elaSeeds, (10,360))
                self.honSeeds = self.font.render('Honeyshroom Seeds: ' + str(self.inventory.honeyshroomSeeds), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.honSeeds, (10,395))
                self.wallet_text = self.font.render("Rocks: " + str(self.inventory.rockTotal), True, pygame.Color(255,255,255), pygame.Color(155,52,179))
                self._display_surf.blit(self.wallet_text, (10,430))

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