import pygame as pg
import groups as g

class Sky(pg.sprite.Sprite):
    def __init__(self, location, image):
        super(Sky, self).__init__()
        
        try:
            self.surf = pg.image.load("images/backgrounds/" + image + ".png").convert()
            self.rect = self.surf.get_rect(bottomleft=location)
        
            g.background.add(self)
        
            self.X, self.Y = [float(self.rect.left), float(self.rect.bottom)]
            
            self.speed = 0.1
        except IOError:
            pass
        
    def update(self):
        self.rect = self.surf.get_rect(bottomleft=(round(self.X//1), round(self.Y//1)))