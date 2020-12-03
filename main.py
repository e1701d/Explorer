import pygame as pg
import settings as s
import player as p
import groups as g
#import background_objects as bo
import tilemap as tm
import keybinds as k

pg.init()

pg.display.set_caption("Explorer")
pg.display.set_icon(pg.image.load(s.ICON_IMAGE))

clock = pg.time.Clock()

pg.time.set_timer(s.CHECK_FPS, s.CHECK_FPS_INTERVAL)
pg.time.set_timer(s.ADVANCE_ANIMATION, s.ANIMATION_LENGTH)
pg.time.set_timer(s.BREATH, s.BREATH_INTERVAL)

player = None

solids = pg.sprite.Group()
enemies = pg.sprite.Group()
background = pg.sprite.Group()

true_scroll = [0,0]

all_sprites = pg.sprite.Group()

loaded_map = "test2"

def small_display(text):
    font = pg.font.SysFont(None, s.SMALL_FONT_SIZE)
    new_text = font.render(text, True, s.BLACK)
    return new_text

def text_objects(text, font):
    textSurface = font.render(text, True, s.BLACK)
    return textSurface, textSurface.get_rect()

def set_up():
    global player
              
    game_map = tm.Map(loaded_map)
    game_map.make_map()
    
    #bo.Sky((-s.WIDTH, game_map.height-s.HEIGHT*1.25), loaded_map.lower())
    
    player_x, player_y = game_map.player_spawn
    player = p.Player(player_x, player_y)
    player.kill_Y = 1000

def render(fps):
    if loaded_map == "Grass":
        s.SCREEN.fill(s.GRASS_BACKGROUND_COLOR)
    elif loaded_map == "Snow":
        s.SCREEN.fill(s.SNOW_BACKGROUND_COLOR)
    elif loaded_map == "Sand":
        s.SCREEN.fill(s.SAND_BACKGROUND_COLOR)
    else:
        s.SCREEN.fill(s.DEFAULT_BACKGROUND_COLOR)
    
    true_scroll[0] += (player.rect.x-true_scroll[0]-s.WIDTH/2+s.PLAYER_SIZE[0])//30
    true_scroll[1] += (player.rect.y-true_scroll[1]-s.HEIGHT/2)//30
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    for sprite in g.background:
        s.SCREEN.blit(sprite.surf, (sprite.X-scroll[0]*sprite.speed, sprite.Y-scroll[1]*sprite.speed))
        
    for sprite in g.non_solids:
        s.SCREEN.blit(sprite.surf, (sprite.location[0]-scroll[0], sprite.location[1]-scroll[1]))
        
    for sprite in g.solids:
        s.SCREEN.blit(sprite.surf, (sprite.location[0]-scroll[0], sprite.location[1]-scroll[1]))
        
    for sprite in g.enemies:
        s.SCREEN.blit(sprite.surf, (sprite.location[0]-scroll[0], sprite.location[1]-scroll[1]))
        
    s.SCREEN.blit(player.surf, (player.rect.x-scroll[0], player.rect.y-scroll[1]))
    
    s.SCREEN.blit(small_display(str(fps)),(0, 0))
    
    coins_text = "Coins: " + str(player.coins)
    s.SCREEN.blit(small_display(coins_text), (s.WIDTH-(len(coins_text))*10, 0))
    
    clock.tick(s.FPS)
    pg.display.update()

def main():
    set_up()
    fps = 0
    
    while True:
        player.update()
        g.background.update()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == k.JUMP:
                    player.jump()
            if event.type == s.CHECK_FPS:
                fps = round(clock.get_fps())
            if event.type == s.ADVANCE_ANIMATION:
                player.advance_animation()
            if event.type == s.BREATH and player.stage == player.is_standing:
                player.start_breath()
        render(fps)
        
if __name__ == "__main__":
    main()