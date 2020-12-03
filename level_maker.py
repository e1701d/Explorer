import json
import pygame as pg
import settings as s
import tilemap
import groups as g
import tile_list

map_name = input("Map to load (To create new map simply type the new name for the map): ")
new_map = {}

autosave_inverval = 5000

clock = pg.time.Clock()

true_scroll = [0,0]

scroll_x = 0
scroll_y = 0

menu_rectangle = pg.Surface((s.WIDTH//6, s.HEIGHT))
menu_rectangle.fill(((222,184,135)))

default_tile = {
    "info":  {
        "image": "dirt",
        "player_spawn": "FALSE",
        "is_solid": "TRUE",
        "can_climb": "FALSE",
    }
}

def button(image, x, y, selected_tile):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    
    surf = pg.transform.scale(pg.image.load("images/" + tile_list.TILE_LIST[image] + "/" + image + ".png").convert(), (s.BLOCK_SIZE, s.BLOCK_SIZE))
    
    if x+s.BLOCK_SIZE > mouse[0] > x and y+s.BLOCK_SIZE > mouse[1] > y:
        s.SCREEN.blit(surf, (x,y,s.BLOCK_SIZE,s.BLOCK_SIZE))
        
        if click[0] == 1 and selected_tile["info"]["image"] != image:
            selected_tile["info"]["image"] = image
            print("Selected Tile: " + image)
    else:
        s.SCREEN.blit(surf,(x,y,s.BLOCK_SIZE,s.BLOCK_SIZE))
        
    return None

def load_map():
    global new_map
    
    try:
        new_map = tilemap.Map(map_name)
        new_map.make_map()
    except FileNotFoundError:
        save_map()
    
def save_map():
    with open("maps/" + map_name + ".json", "w") as file:
        json.dump(new_map.data, file, indent=4)

def set_up():
    load_map()
    
    s.SCREEN = pg.display.set_mode((s.WIDTH, s.HEIGHT))
    pg.display.set_caption("Level Editor")
    
def render(selected_tile):
    global true_scroll
    true_scroll[0] -= scroll_x
    true_scroll[1] -= scroll_y
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    
    s.SCREEN.fill(s.BLACK)

    for sprite in g.background:
        s.SCREEN.blit(sprite.surf, (sprite.X-scroll[0], sprite.Y-scroll[1]))
        
    for sprite in g.non_solids:
        s.SCREEN.blit(sprite.surf, (sprite.location[0]-scroll[0], sprite.location[1]-scroll[1]))
        
    for sprite in g.solids:
        s.SCREEN.blit(sprite.surf, (sprite.location[0]-scroll[0], sprite.location[1]-scroll[1]))
        
    for sprite in g.enemies:
        s.SCREEN.blit(sprite.surf, (sprite.location[0]-scroll[0], sprite.location[1]-scroll[1]))
        
    s.SCREEN.blit(menu_rectangle, menu_rectangle.get_rect(topleft=(0,0)))
    
    for i, image in enumerate(tile_list.TILE_LIST):
        if tile_list.TILE_LIST[image] != "":
            button(image, s.WIDTH//6-s.BLOCK_SIZE, i*s.BLOCK_SIZE+100, selected_tile)
        
    clock.tick(s.FPS)
    pg.display.update()
    
def handle_clicks(selected_tile):
    global scroll_x, scroll_y
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    
    #keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()
    
    mouse_pos = pg.mouse.get_pos()
    snapped_mouse = ((mouse_pos[0]+scroll[0])//s.BLOCK_SIZE, (mouse_pos[1]+scroll[1])//s.BLOCK_SIZE)
    
    scroll_x = 0
    scroll_y = 0
    
    if mouse[0]:
        if mouse_pos[0] > s.WIDTH//6:
            new_map.add_tile(snapped_mouse, selected_tile["info"])
            new_map.data[str(snapped_mouse[1]) + "," + str(snapped_mouse[0])] = {}
            new_map.data[str(snapped_mouse[1]) + "," + str(snapped_mouse[0])][selected_tile["info"]["image"]] = {}
            new_map.data[str(snapped_mouse[1]) + "," + str(snapped_mouse[0])][selected_tile["info"]["image"]] = selected_tile
    elif mouse[2]:
        if mouse_pos[0] > s.WIDTH//6:
            new_map.data.pop(str(snapped_mouse[1]) + "," + str(snapped_mouse[0]), None)
    elif mouse[1]:
        scroll_x, scroll_y = pg.mouse.get_rel()
        
def main():
    set_up()
    selected_tile = default_tile
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_map()
                pg.quit()
                quit()
                
        handle_clicks(selected_tile)
        render(selected_tile)
                
                
if __name__ == "__main__":
    main()
        