#import settings as s
import tiles as t
import utilities as u
import tile_list
import json

class Map:
    def __init__(self, map_name):
        self.data = {}
        with open("maps/" + map_name.lower() + ".json", 'rt') as new_map:
            self.data = json.load(new_map)
                
        #self.tilewidth = len(self.data[0])
        #self.tileheight = len(self.data)
        #self.width = self.tilewidth*s.BLOCK_SIZE
        #self.height = self.tileheight*s.BLOCK_SIZE
        
        self.map_name = map_name
        
        self.player_spawn = ()
        
    def make_map(self):  
        for tile_location in self.data:
            for tile in self.data[tile_location]:
                coords = tuple(map(int, tile_location.split(',')))        
                data = self.data[tile_location][tile]["info"]       
                self.add_tile(coords, data)
    
    def add_tile(self, coords, data):
        coords = (coords[1], coords[0])
        
        if data["player_spawn"] == "TRUE":
            self.player_spawn = (coords)
            
        if data["image"] and data["image"] in tile_list.TILE_LIST:
            image = tile_list.TILE_LIST[data["image"]]
            
            if image == "floors":
                t.Floor(data, coords, "floors")
            elif image == "trees":
                t.Tree(data, coords, "trees")
            elif image == "chest":
                u.Utility(data, coords, "chest")