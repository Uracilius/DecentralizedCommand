import pygame

class Renderer:
    def __init__(self, screen, tile_size, camera):
        self.screen = screen
        self.tile_size = tile_size
        self.camera = camera

    def render_map(self, obstacles, hard_obstacles, colors):
        for obstacle in obstacles:
            position = self.camera.apply(obstacle.position)
            pygame.draw.rect(
                self.screen,
                colors["brown"],
                (position[0], position[1], self.tile_size, self.tile_size)
            )
            pygame.draw.rect(
                self.screen,
                (100, 50, 0),
                (position[0], position[1], self.tile_size, self.tile_size),
                3
            )
        for hard_obstacle in hard_obstacles:
            position = self.camera.apply(hard_obstacle.position)
            pygame.draw.rect(
                self.screen,
                (0, 0, 0),
                (position[0], position[1], self.tile_size, self.tile_size)
            )
            
    def render_bullets(self, combat_manager):
        """Render all bullets managed by the CombatManager."""
        combat_manager.render_bullets(self.screen, self.camera)

    def render_units(self, units, colors):
        for unit in units:
            position = self.camera.apply(unit.position)
            self.screen.blit(unit.image, position)

            # # Draw the unit as a circle
            unit_center = (position[0] + self.tile_size // 2, position[1] + self.tile_size // 2)
            unit_radius = self.tile_size // 3
            # pygame.draw.circle(
            #     self.screen,
            #     unit.team.color,
            #     unit_center,
            #     unit_radius
            # )

            # Health bar
            health_bar_length = self.tile_size // 2
            health_ratio = max(unit.health / 100, 0)
            pygame.draw.rect(
                self.screen,
                colors["red"],
                (position[0] + 10, position[1], health_bar_length, 5)
            )
            pygame.draw.rect(
                self.screen,
                colors["green"],
                (position[0] + 10, position[1], int(health_bar_length * health_ratio), 5)
            )

            # Render the weapon at the bottom of the unit sprite and smaller than the unit
            if unit.weapon and unit.weapon.sprite:
                # Load the weapon sprite
                weapon_sprite = pygame.image.load(unit.weapon.sprite)
                # Scale it down (for example, to half the tile size)
                weapon_size = self.tile_size // 2
                weapon_sprite = pygame.transform.scale(weapon_sprite, (weapon_size, weapon_size))
                # Calculate the bottom of the unit's sprite (the circle)
                bottom_of_unit = unit_center[1] + unit_radius
                # Center the weapon horizontally with the unit
                weapon_x = unit_center[0] - weapon_size // 2
                # Position the weapon so that its top is aligned with the bottom of the unit
                weapon_y = bottom_of_unit
                self.screen.blit(weapon_sprite, (weapon_x, weapon_y))

    def render_ground(self, screen_width, screen_height, colors):
        """Render the ground layer as a grid with the camera's offset."""
        start_x = -(self.camera.x % self.tile_size)  
        start_y = -(self.camera.y % self.tile_size)
        for y in range(start_y, screen_height, self.tile_size):
            for x in range(start_x, screen_width, self.tile_size):
                world_x = x + self.camera.x
                world_y = y + self.camera.y
                pygame.draw.rect(
                    self.screen,
                    colors["gray"],
                    (x, y, self.tile_size, self.tile_size)
                )

    def render_flags(self, flags):
        """Render flags on the map."""
        for flag in flags:
            flag.render(self.screen, self.camera)

