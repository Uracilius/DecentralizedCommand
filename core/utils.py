import heapq
import pygame
import math

def astar_pathfinding(start, end, obstacles, units, tile_size, map_width, map_height):
    start_tile = (start[0] // tile_size, start[1] // tile_size)
    end_tile = (end[0] // tile_size, end[1] // tile_size)

    if start_tile == end_tile:
        return [start]

    def heuristic(a, b):
        dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
        return dx + dy + (math.sqrt(2) - 2) * min(dx, dy)

    def is_valid_tile(tile):
        x, y = tile
        rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        if any(rect.colliderect(obs) for obs in obstacles): 
            return False
        if any(rect.colliderect(unit.rect) for unit in units if unit.alive()):
            return False
        return 0 <= x < map_width and 0 <= y < map_height

    def get_neighbors(node):
        x, y = node
        neighbors = []
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, 1), (1, -1), (-1, -1)
        ]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid_tile((nx, ny)):
                neighbors.append((nx, ny))
        return neighbors

    if not is_valid_tile(end_tile):
        possible_tiles = []
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                tile = (end_tile[0] + dx, end_tile[1] + dy)
                if is_valid_tile(tile):
                    distance = heuristic(start_tile, tile)
                    possible_tiles.append((distance, tile))

        if possible_tiles:
            possible_tiles.sort()
            end_tile = possible_tiles[0][1]

    open_set = []
    heapq.heappush(open_set, (0, start_tile))
    open_set_lookup = {start_tile}
    came_from = {}
    g_score = {start_tile: 0}
    f_score = {start_tile: heuristic(start_tile, end_tile)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        open_set_lookup.remove(current)

        if current == end_tile:
            path = []
            while current in came_from:
                path.append((current[0] * tile_size + tile_size // 2, current[1] * tile_size + tile_size // 2))
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end_tile)

                if neighbor not in open_set_lookup:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_lookup.add(neighbor)

    return []
