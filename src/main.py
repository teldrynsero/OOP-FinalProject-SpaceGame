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
        self.velocity = 12
        self.game_started = False
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
        self.ground = Game.load("ground")
        mixer.music.load("media/sounds/earthshine.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()
        self.font = pygame.font.Font('media/Pixeled.ttf', 32)
        #self._display_surf.blit(self._image_surf,(0,0))
        #pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: #enter key pressed
                self._image_surf = Game.load("morning_0") #change background
                self.game_started = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.frog = Game.load("player_4")
            if event.key == pygame.K_d:
                self.frog = Game.load("player_6")
            if event.key == pygame.K_s:
                self.frog = Game.load("player_0")
            if event.key == pygame.K_w:
                self.frog = Game.load("player_2")

        pygame.display.update()

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(self._image_surf,(0,0))

        if self.game_started == True:
            self._display_surf.blit(self.ground,(0,0))
            self._display_surf.blit(self.frog,(self.x,self.y))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                #text = self.font.render('you pressed left', True, (0, 255, 0),(0, 0, 128))
                self.x -= 1
                self.frog = Game.load("player_5")
                print(self.x)

            if keys[pygame.K_d]:
                #text = self.font.render('you pressed left', True, (0, 255, 0),(0, 0, 128))
                self.x += 1
                self.frog = Game.load("player_7")
                print(self.x)

            if keys[pygame.K_w]:
                #text = self.font.render('you pressed left', True, (0, 255, 0),(0, 0, 128))
                self.y -= 1
                self.frog = Game.load("player_3")
                print(self.y)

            if keys[pygame.K_s]:
                #text = self.font.render('you pressed left', True, (0, 255, 0),(0, 0, 128))
                self.y += 1
                self.frog = Game.load("player_1") 
                print(self.y)

            #player walking boundaries
            if self.x < 0:
                self.x = 0

            if self.x > 570:
                self.x = 570
            
            if self.y > 370:
                self.y = 370

            if self.y < 60:
                self.y = 60

        pygame.display.flip()


    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            self.clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    SpaceGame = Game()
    SpaceGame.on_execute()

