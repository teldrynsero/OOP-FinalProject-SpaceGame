import pygame
from pygame.locals import *
from pygame import mixer
#pip install pygame

class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 480
        self._image_surf = None
        self.x = 100
        self.y = 100
        self.x_change = 0
        self.y_change = 0
        self.velocity = 12
        self.value = 0 #to animate through npc sprites
        self.next_frame_time = 0 #calculate when to animate npc
        self.fps = 5 #npc fps
        self.game_started = False
        self.starting_text_show = False
        self.npc_talking = False
        self.clock = pygame.time.Clock()

    def load(image):
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

        mixer.music.load("media/sounds/earthshine.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()

        self.font = pygame.font.Font('media/Pixeled.ttf', 15)
        self.beginning_text = self.font.render('Use WASD keys to move.', True, pygame.Color(255,255,255))
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
                    self.starting_text_show = False #tutorial over for now
                    if ((self.x > 125) and (self.x < 285) and (self.y > 50) and (self.y < 110)):
                        if self.npc_talking == False:
                            self.npc_text = self.font.render('Hello there, strange one.', True, pygame.Color(255,255,255))
                            self.npc_talking = True #show npc text
                        else: #press t again to stop talking
                            self.npc_text = self.font.render(' ', True, pygame.Color(255,255,255))
                            self.value = 0
                            self.npc_talking = False
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
        if (time_now > self.next_frame_time): #show npc animation
            if self.npc_talking == True: #npc was talked to
                inter_frame_delay = 1000 // self.fps   
                self.next_frame_time = time_now + inter_frame_delay
                self.value += 1
                if self.value >= len(self.npc_cycle):
                    self.value = 0

    def on_render(self):
        self._display_surf.blit(self._image_surf,(0,0))

        if self.game_started == True:
            self.npc = self.npc_cycle[self.value]

            self._display_surf.blit(self.ground,(0,0))
            self._display_surf.blit(self.npc,(200,70))
            self._display_surf.blit(self.frog,(self.x,self.y))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.x -= 1
                self.x_change = -1
                self.frog = Game.load("player_5")
                print("x=")
                print(self.x)
                print("y=")
                print(self.y)
                self.frog_rect = self.frog.get_rect(topleft = (self.x, self.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.x_change > 0:
                        self.frog_rect.right = self.npc_rect.left
                    elif self.x_change < 0:
                        self.frog_rect.left = self.npc_rect.right
                    self.x = self.frog_rect.x

            if keys[pygame.K_d]:
                self.x += 1
                self.x_change = 1
                self.frog = Game.load("player_7")
                print("x=")
                print(self.x)
                print("y=")
                print(self.y)
                self.frog_rect = self.frog.get_rect(topleft = (self.x, self.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.x_change > 0:
                        self.frog_rect.right = self.npc_rect.left
                    elif self.x_change < 0:
                        self.frog_rect.left = self.npc_rect.right
                    self.x = self.frog_rect.x

            if keys[pygame.K_w]:
                self.y -= 1
                self.y_change = -1
                self.frog = Game.load("player_3")
                print("x=")
                print(self.x)
                print("y=")
                print(self.y)
                self.frog_rect = self.frog.get_rect(topleft = (self.x, self.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.y_change < 0:
                        self.frog_rect.top = self.npc_rect.bottom
                    elif self.y_change > 0:
                        self.frog_rect.bottom = self.npc_rect.top
                    self.y = self.frog_rect.y

            if keys[pygame.K_s]:
                self.y += 1
                self.y_change = 1
                self.frog = Game.load("player_1")
                print("x=")
                print(self.x)
                print("y=")
                print(self.y)
                self.frog_rect = self.frog.get_rect(topleft = (self.x, self.y))
                if self.frog_rect.colliderect(self.npc_rect): #did player collide with npc?
                    if self.y_change < 0:
                        self.frog_rect.top = self.npc_rect.bottom
                    elif self.y_change > 0:
                        self.frog_rect.bottom = self.npc_rect.top
                    self.y = self.frog_rect.y

            #player walking boundaries
            if self.x < 0:
                self.x = 0

            if self.x > 570:
                self.x = 570
            
            if self.y > 370:
                self.y = 370

            if self.y < 60:
                self.y = 60

            if self.starting_text_show == True: #tutorial text
                if keys[pygame.K_a] or keys[pygame.K_s] or  keys[pygame.K_w] or  keys[pygame.K_d]: #player has used WASD
                    self.beginning_text = self.font.render('Press T to talk to the alien.', True, pygame.Color(255,255,255)) #move on to next tutorial
                    self._display_surf.blit(self.beginning_text, (180,25))
                self._display_surf.blit(self.beginning_text, (180,25))

            if self.npc_talking == True:
                self._display_surf.blit(self.npc_text, (300,50))


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

