import pygame as pg
import settings as s
import groups as g

class Floor():
    def __init__(self, tile, coords, extension):
        image_name = "images/" + extension + "/" +  tile["image"] + ".png"
        image = pg.image.load("images/" + extension + "/" +  tile["image"] + ".png").convert()
        location = (coords[1]*s.BLOCK_SIZE, coords[0]*s.BLOCK_SIZE)
        
        if extension == "floors":
            if tile["is_solid"] == "TRUE":
                Solid(tile, image, location)
            else:
                NonSolid(tile, image, location)
        elif extension == "trees":
            Tree(tile, image, location)

class Solid(pg.sprite.Sprite):
    def __init__(self, tile, image, location):
        super(Solid, self).__init__()
        self.surf = pg.transform.scale(image, (s.BLOCK_SIZE, s.BLOCK_SIZE))
        self.rect = self.surf.get_rect(topleft=location)
        self.surf.set_colorkey(s.GREEN)
        
        g.solids.add(self)
        g.all_sprites.add(self)
        
        self.location = location
        self.image = image
        
class NonSolid(pg.sprite.Sprite):
    def __init__(self, tile, image, location):
        super(NonSolid, self).__init__()
        self.surf = pg.transform.scale(image, (s.BLOCK_SIZE, s.BLOCK_SIZE))
        self.rect = self.surf.get_rect(topleft=location)
        self.surf.set_colorkey(s.GREEN)
        
        g.non_solids.add(self)
        g.all_sprites.add(self)
        
        self.location = location
        self.image = image
        
class Tree(pg.sprite.Sprite):
    def __init__(self, tile, image, location):
        super(Tree, self).__init__()
        self.surf = pg.transform.scale(image, (s.BLOCK_SIZE*4, s.BLOCK_SIZE*4))
        self.rect = self.surf.get_rect(bottomleft=(location[0], location[1]))
        self.surf.set_colorkey(s.GREEN)
        
        g.non_solids.add(self)
        g.all_sprites.add(self)
        
        self.location = location
        self.image = image