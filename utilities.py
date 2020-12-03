import pygame as pg
import settings as s
import groups as g
import water as w
import random

class Utility():
    def __init__(self, tile, coords, extension):
        image = pg.image.load("images/" + extension + "/" +  + tile["image"] + ".png").convert()
        location = (coords[1]*s.BLOCK_SIZE, coords[0]*s.BLOCK_SIZE)
        
        if extension == "chest":
            Chest(tile, image, location)

class Chest(pg.sprite.Sprite):
    def __init__(self, tile, image, location):
        super(Chest, self).__init__()
        self.surf = pg.transform.scale(image, (s.BLOCK_SIZE, s.BLOCK_SIZE))
        self.rect = self.surf.get_rect(topleft=location)
        self.surf.set_colorkey(s.GREEN)
        
        self.type = 'chest'
        
        self.is_open = False
        self.location = location
        self.variation = tile["info"]["variation"]
        
        g.utilities.add(self)
        g.non_solids.add(self)
        g.all_sprites.add(self)
        
    def open_chest(self):
        self.surf = pg.transform.scale(pg.image.load("images/utilities/" + self.variation + "_open.png").convert(), (s.BLOCK_SIZE, s.BLOCK_SIZE))
        self.surf.set_colorkey(s.GREEN)
        self.is_open = True
        
        return random.randint(0, 5)