import pygame as pg
import settings as s
import groups as g
import keybinds as k

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__()
        
        self.standing_imgs_r = []
        self.walking_imgs_r = []
        self.sliding_imgs_r = []
        self.falling_imgs_r = []
        self.breathing_imgs_r = []
        
        walking_frames = 5
        falling_frames = 5
        sliding_frames = 1
        standing_frames = 1
        breathing_frames = 4
        
        for i in range(standing_frames):
            self.standing_imgs_r.append(pg.transform.scale(pg.image.load("images/player/player_standing_" + str(i) + ".png").convert(), s.PLAYER_SIZE))
        
        for i in range(walking_frames):
            image = pg.image.load("images/player/player_walking_" + str(i) + ".png").convert()
            image = pg.transform.scale(image, s.PLAYER_SIZE)
            self.walking_imgs_r.append(image)
            
        for i in range(sliding_frames):
            image = pg.image.load("images/player/player_sliding_" + str(i) + ".png").convert()
            image = pg.transform.scale(image, s.PLAYER_SIZE)
            self.sliding_imgs_r.append(image)
            
        for i in range(falling_frames):
            image = pg.image.load("images/player/player_falling_" + str(i) + ".png").convert()
            image = pg.transform.scale(image, s.PLAYER_SIZE)
            self.falling_imgs_r.append(image)
            
        for i in range(breathing_frames):
            image = pg.image.load("images/player/player_breathing_" + str(i) + ".png").convert()
            image = pg.transform.scale(image, s.PLAYER_SIZE)
            self.breathing_imgs_r.append(image)
            
        self.standing_imgs_l = [pg.transform.flip(image, True, False) for image in self.standing_imgs_r]
        self.walking_imgs_l = [pg.transform.flip(image, True, False) for image in self.walking_imgs_r]
        self.sliding_imgs_l = [pg.transform.flip(image, True, False) for image in self.sliding_imgs_r]
        self.falling_imgs_l = [pg.transform.flip(image, True, False) for image in self.falling_imgs_r]
        self.breathing_imgs_l = [pg.transform.flip(image, True, False) for image in self.breathing_imgs_r]
        
        self.right_images = [self.standing_imgs_r, self.walking_imgs_r, self.sliding_imgs_r, self.falling_imgs_r, self.breathing_imgs_r]
        self.left_images = [self.standing_imgs_l, self.walking_imgs_l, self.sliding_imgs_l, self.falling_imgs_l, self.breathing_imgs_l]
        
        self.is_standing = 0
        self.is_walking = 1
        self.is_sliding = 2
        self.is_falling = 3 
        self.breath = 4
        
        self.images = self.right_images
        
        self.open_chest = None
        
        self.stage = 0
        self.index = 0
        
        self.health = 100
        self.coins = 0
        
        self.is_breathing = False
        
        self.start_pos = (x*s.BLOCK_SIZE + s.BLOCK_SIZE//2, y*s.BLOCK_SIZE)
        
        self.surf = self.right_images[self.stage][self.index]
        self.surf.set_colorkey(s.GREEN)
        self.rect = self.surf.get_rect(center=self.start_pos)
        
        self.toprect = pg.Rect(self.rect.left, self.rect.top-1, self.rect.width, 1)
        self.bottomrect = pg.Rect(self.rect.left, self.rect.bottom, self.rect.width, 1)
        self.rightrect = pg.Rect(self.rect.right, self.rect.top, 1, self.rect.height)
        self.leftrect = pg.Rect(self.rect.left-1, self.rect.top, 1, self.rect.height)
        
        self.is_on_ground = False
        self.can_move_right = True
        self.can_move_up = True
        self.can_move_left = True
        
        self.moveX = 0
        self.moveY = 0
        
        self.jumps = 0
        
        self.kill_Y = 0
    
    def update(self):
        if self.rect.y > self.kill_Y:
            self.rect.center = self.start_pos
        
        self.moveX = 0
        
        keys = pg.key.get_pressed()
        
        if keys[k.WALK_LEFT]:
            self.moveX = s.PLAYER_SPEED
            self.images = self.left_images
        elif keys[k.WALK_RIGHT]:
            self.moveX = -s.PLAYER_SPEED
            self.images = self.right_images
        if keys[k.OPEN]:
            if self.open_chest:
                coins = self.open_chest.open_chest()
                self.coins += coins
        
        if self.moveY >= s.MAX_FALL_SPEED:
            self.moveY = s.MAX_FALL_SPEED
        else:
            self.moveY += s.GRAVITY
            
        self.collision_test()
            
        if self.moveX > 0:
            self.images = self.left_images
        elif self.moveX < 0:
            self.images = self.right_images
            
        if self.moveY < 0 or self.moveY > 0:
            self.stage = self.is_falling
            self.is_breathing = False
        elif self.moveX != 0:
            self.stage = self.is_walking
            self.is_breathing = False
        elif self.is_breathing:
            self.is_breathing = True
            
            if self.index >= 3:
                self.is_breathing = False
                self.stage = self.is_standing
        else:
            self.stage = self.is_standing
            
        self.update_rects()
            
        for i in range(abs(round(self.moveX))):
            if self.moveX > 0 and self.can_move_left:
                self.rect.x -= 1
            elif self.moveX < 0 and self.can_move_right:
                self.rect.x += 1
            
            self.update_rects()
            self.collision_test()
            
        for i in range(abs(round(self.moveY))):
            if self.moveY > 0 and not self.is_on_ground:
                self.rect.y += 1
            elif self.moveY < 0 and self.can_move_up:
                self.rect.y -= 1
            
            self.update_rects()
            self.collision_test()
            
    def advance_animation(self):
        self.index = (self.index + 1) % len(self.images[self.stage])
        self.surf = self.images[self.stage][self.index].convert()
        self.surf.set_colorkey(s.GREEN, pg.RLEACCEL)
        
    def collision_test(self):
        self.can_move_up = True
        self.can_move_left = True
        self.can_move_right = True
        self.is_on_ground = False
        
        for solid in g.solids:
            if self.toprect.colliderect(solid.rect):
                self.can_move_up = False
                self.moveY = 1
            if self.bottomrect.colliderect(solid.rect):
                self.is_on_ground = True
                self.jumps = 0
                
                if self.moveY > 0:
                    self.moveY = 0
            if self.rightrect.colliderect(solid.rect):
                self.can_move_right = False
                
                if self.moveX < 0:
                    self.moveX = 0
            if self.leftrect.colliderect(solid.rect):
                self.can_move_left = False
                
                if self.moveX > 0:
                    self.moveX = 0
        
        self.open_chest = None
        
        for utility in g.utilities:
            if self.rect.x in range(utility.rect.x-s.BLOCK_SIZE, utility.rect.x+s.BLOCK_SIZE):
                if self.rect.y in range(utility.rect.y-s.BLOCK_SIZE, utility.rect.y+s.BLOCK_SIZE):
                    if utility.type == 'chest' and utility.is_open == False:
                        self.open_chest = utility
        return
    
    def update_rects(self):
        self.toprect = pg.Rect(self.rect.left, self.rect.top-1, self.rect.width, 1)
        self.bottomrect = pg.Rect(self.rect.left, self.rect.bottom, self.rect.width, 1)
        self.rightrect = pg.Rect(self.rect.right, self.rect.top, 1, self.rect.height)
        self.leftrect = pg.Rect(self.rect.left-1, self.rect.top, 1, self.rect.height)
        
    def start_breath(self):
        self.stage = self.breath
        self.is_breathing = True
        self.index = 0
        
    def jump(self):
        if self.jumps < s.PLAYER_JUMPS:
            if self.moveY > -s.PLAYER_MAX_JUMP_FORCE - s.PLAYER_JUMP_FORCE:
                self.moveY -= s.PLAYER_JUMP_FORCE
            else:
                self.moveY = -s.PLAYER_MAX_JUMP_FORCE
            self.jumps += 1