

class A_Star:

    def __init__(self):
        
        self.open_tiles = []
        self.closed_tiles = []
    
    def calculate_heuristic(self, tile, goal):

        base = [abs(goal.tilemap_pos[0] - tile.tilemap_pos[0]), abs(goal.tilemap_pos[1] - tile.tilemap_pos[1])]

        base_total = base[0] + base[1]
 
        reminder = abs(base[0] - base[1])

        diognal = ((base_total - reminder)//2) * 14

        horizontal = reminder * 10

        return diognal + horizontal

    def calculate_total_tile_cost(self, tile, goal, start):

        tile.g_cost = self.calculate_heuristic(tile, start)
        tile.h_cost = self.calculate_heuristic(tile, goal)
        tile.f_cost = tile.g_cost + tile.h_cost

    def sort_list(self, list_to_sort):

        for start_index in range(len(list_to_sort)):

            best_tile_index = start_index

            for current_index in range(start_index, len(list_to_sort)):

                if list_to_sort[current_index].f_cost < list_to_sort[best_tile_index].f_cost:

                    best_tile_index = current_index

            temp = list_to_sort[best_tile_index]

            list_to_sort[best_tile_index] = list_to_sort[start_index]
            list_to_sort[start_index] = temp

    def find_path(self, start, goal):

        path = []

        self.open_tiles.clear()
        self.closed_tiles.clear()
        self.open_tiles.append(start)

        while len(self.open_tiles) != 0:

            self.sort_list(self.open_tiles)

            current_tile = self.open_tiles[0]

            self.open_tiles.remove(current_tile)
            self.closed_tiles.append(current_tile)

            if current_tile.tilemap_pos == goal.tilemap_pos:

                path_tile = goal

                while path_tile != start:

                    path.append(path_tile)
                    path_tile = path_tile.parent_tile
                
                path.reverse()

                return path
            
            for neighbour_tile in current_tile.neighbour_tiles:

                if neighbour_tile.obstacle or neighbour_tile.occupier is not None or self.closed_tiles.count(neighbour_tile) > 0:
                    continue

                if neighbour_tile.f_cost < current_tile.f_cost or self.open_tiles.count(neighbour_tile) < 1:
                    self.calculate_total_tile_cost(neighbour_tile, goal, start)
                    neighbour_tile.parent_tile = current_tile
                    if self.open_tiles.count(neighbour_tile) < 1:
                        self.open_tiles.append(neighbour_tile)







