import pygame
from core import utils
from entities import weapon

class Unit(pygame.sprite.Sprite):
    def __init__(self, x, y, team, health=100, accuracy=80, speed=2, weapon=weapon.Pistol()):
        super().__init__()
        
        self.tile_size = 50  # Keep a standard size

        

        self.direction = pygame.Vector2(0, -1)  
        
        rect_size = self.tile_size // 2    # Smaller rect inside the circle
        
        self.image = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, team.color, (0, 0, rect_size, rect_size))
        
        self.rect = self.image.get_rect(center=(x + self.tile_size // 2, y + self.tile_size // 2))
        
        self.position = pygame.math.Vector2(x, y)
        self.health = health
        self.team = team

        # Load and scale the original sprite based on team
        if team.name == "Allies":
            self.original_image = pygame.image.load("assets/sprites/soldiers_ally.png").convert_alpha()
        else:
            self.original_image = pygame.image.load("assets/sprites/soldiers_enemy.png").convert_alpha()
            
        self.original_image = pygame.transform.scale(self.original_image, (self.tile_size, self.tile_size))  

        # Ensure self.image starts as the scaled image
        self.image = self.original_image.copy()

        self.selected = False
        self.path = []
        
        
        self.difficulty_multiplier = 1.0
        
        self.speed = speed * self.difficulty_multiplier
        

        self.cooldown_timer = 0
        self.accuracy = accuracy*weapon.accuracy_modifier
        self.in_cover = False
        self.cover_direction = None
        self.search_cooldown = 30
        self.search_timer = 0
        self.weapon = weapon
        print(f"Unit {self.team.name} initialized at {self.rect.topleft} (Expected: {self.position})")
    
    def update_speed(self, speed):
        self.speed = speed * self.difficulty_multiplier

    def set_difficulty_multiplier(self, multiplier):
        self.difficulty_multiplier = multiplier
        self.update_speed(self.speed)
        print(f"Difficulty multiplier set to {multiplier}.")

    def check_cover(self, obstacles):
        self.in_cover = False
        self.cover_direction = None
        for obs in obstacles:
            dx = self.rect.centerx - obs.rect.centerx
            dy = self.rect.centery - obs.rect.centery
            if abs(dx) <= obs.rect.width // 2 + 10 and abs(dy) <= obs.rect.height // 2 + 10:
                if abs(dx) > abs(dy):
                    self.cover_direction = "left" if dx > 0 else "right"
                else:
                    self.cover_direction = "top" if dy > 0 else "bottom"
                self.in_cover = True
                return

    def take_damage(self, damage, attacker_position):
        if self.in_cover:
            dx = self.rect.centerx - attacker_position[0]
            dy = self.rect.centery - attacker_position[1]
            attacker_direction = "left" if dx > 0 else "right" if abs(dx) > abs(dy) else "top" if dy > 0 else "bottom"
            if attacker_direction == self.cover_direction:
                damage *= 0.001 * self.difficulty_multiplier
                print(f"Unit is protected by cover in direction: {self.cover_direction}, damage:{damage}")
        self.health -= damage * self.difficulty_multiplier

    def select(self, is_selected):
        self.selected = is_selected
        self.image.fill((0, 255, 255) if is_selected else self.team.color)

    def set_path(self, path):
        self.path = path if path else []
        if not path:
            print("No valid path found.")

    def move_towards_next_tile(self):
        if self.path:
            next_position = pygame.math.Vector2(self.path[0])
            direction = next_position - self.position
            if direction.length() < self.speed:
                self.path.pop(0)
                self.position = next_position
            else:
                direction = direction.normalize() * self.speed
                self.position += direction

                # Update direction based on movement
                if direction.length() > 0:
                    self.direction = direction

            self.rect.topleft = (round(self.position.x), round(self.position.y))


    def search_and_destroy(self, enemies, obstacles, hard_obstacles, all_units):
        """ Make unit move towards the nearest enemy if it's outranged, but stop jittering. """
        if self.search_timer > 0:
            self.search_timer -= 1
            return
        if not enemies:
            return
        
        nearest_enemy = min(enemies, key=lambda e: pygame.math.Vector2(self.rect.center).distance_to(e.rect.center))
        enemy_distance = pygame.math.Vector2(self.rect.center).distance_to(nearest_enemy.rect.center)

        if enemy_distance <= self.weapon.range * 0.9:
            return  


        direction_to_enemy = (pygame.math.Vector2(nearest_enemy.rect.center) - self.position).normalize()
        stop_position = self.position + direction_to_enemy * (enemy_distance - self.weapon.range + 5)  # Stop just before range

        path = utils.astar_pathfinding(
            start=self.rect.center,
            end=stop_position,
            obstacles=obstacles,
            hard_obstacles=hard_obstacles,
            units=all_units,
            tile_size=self.tile_size,
            map_width=self.tile_size * 20,
            map_height=self.tile_size * 20
        )

        if not path:
            self.position += direction_to_enemy * self.speed
            self.rect.topleft = (round(self.position.x), round(self.position.y))
        else:
            self.set_path(path)

        self.search_timer = self.search_cooldown
        

    @staticmethod
    def move_in_formation(units, leader, destination, hard_obstacles, formation="line", spacing=50):
        formation_offsets = []
        if formation == "line":
            formation_offsets = [(i * spacing, 0) for i in range(len(units))]
        elif formation == "square":
            side = int(len(units) ** 0.5)
            formation_offsets = [(x * spacing, y * spacing) for y in range(side) for x in range(side)]
        elif formation == "arrow":
            formation_offsets = [(0, 0)] + [(i * spacing, i * spacing) for i in range(1, len(units) // 2 + 1)]
        path = utils.astar_pathfinding(
            start=leader.rect.center,
            end=destination,
            obstacles=[],
            hard_obstacles=hard_obstacles,
            tile_size=leader.tile_size,
            map_width=leader.tile_size * 20,
            map_height=leader.tile_size * 20
        )
        leader.set_path(path)
        for i, unit in enumerate(units):
            if unit != leader and i < len(formation_offsets):
                target_position = (leader.rect.center[0] + formation_offsets[i][0], leader.rect.center[1] + formation_offsets[i][1])
                path = utils.astar_pathfinding(
                    start=unit.rect.center,
                    end=target_position,
                    obstacles=[],
                    hard_obstacles=hard_obstacles,
                    tile_size=unit.tile_size,
                    map_width=unit.tile_size * 20,
                    map_height=unit.tile_size * 20
                )
                unit.set_path(path)

    def update(self, enemies, obstacles, hard_obstacles, units):
        """ Update movement, combat logic, and AI behavior. """
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

        if self.selected:
            self.move_towards_next_tile()
            self.check_cover(obstacles)
        else:
            self.search_and_destroy(enemies, obstacles, hard_obstacles=hard_obstacles, all_units=units)

        self.move_towards_next_tile()

        # Rotate sprite based on movement direction
        angle = -self.direction.angle_to(pygame.Vector2(0, 1))  

        if self.direction.y > 0:  
            angle += 180  

        rotated_image = pygame.transform.rotate(self.original_image, angle)


        self.rect = rotated_image.get_rect(center=self.rect.center)  # Maintain center
        self.image = rotated_image