import pygame
from pygame.locals import *
#pip install pygame
 
class Game:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 480
        self._image_surf = None

    def load(image):
        imageName = image
        imageTitle = "media/img/"+str(imageName)+".png"
        image = pygame.image.load(imageTitle)
        return image
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._image_surf = Game.load("startscreen") #background
        #self._image_ground = pygame.image.load("media/img/ground.png").convert()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: #enter key pressed
                self._image_surf = Game.load("morning_0") #change background
                #self._display_surf.blit(self._image_ground,(0,0))

                pygame.display.update()

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(self._image_surf,(0,0))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    SpaceGame = Game()
    SpaceGame.on_execute()

