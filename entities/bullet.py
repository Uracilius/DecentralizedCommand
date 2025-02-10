import pygame
import random

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, attacker, target_unit, speed=5, color=(255, 255, 0), radius=5, accuracy=80, enemies=[]):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=start_pos)

        self.position = pygame.math.Vector2(start_pos)
        self.target_unit = target_unit
        self.accuracy = accuracy  # Store accuracy for offset calculations

        if target_unit:
            self.target_pos = pygame.math.Vector2(target_unit.rect.center)
            self.apply_accuracy_offset()
        else:
            self.target_pos = None

        # Calculate direction based on adjusted target position
        direction_vector = self.target_pos - self.position if self.target_pos else pygame.math.Vector2(1, 0)
        if direction_vector.length() == 0:
            direction_vector = pygame.math.Vector2(1, 0)

        self.damage = attacker.weapon.damage
        self.direction = direction_vector.normalize() * speed
        self.speed = speed
        self.lifespan = 100
        self.color = color
        self.radius = radius
        self.enemies = enemies  # Store the list of enemies

    def apply_accuracy_offset(self):
        """Modify the target position based on accuracy."""
        if self.accuracy < 100:  # Only apply deviation if accuracy is not perfect
            inaccuracy_factor = (100 - self.accuracy) * 3  # Higher inaccuracy means higher deviation
            offset_x = random.uniform(-inaccuracy_factor, inaccuracy_factor)
            offset_y = random.uniform(-inaccuracy_factor, inaccuracy_factor)
            self.target_pos.x += offset_x
            self.target_pos.y += offset_y

    def update(self):
        if self.target_unit and self.target_unit.health > 0:
            self.target_pos = pygame.math.Vector2(self.target_unit.rect.center)
            self.apply_accuracy_offset()  # Reapply inaccuracy if target moves

        self.position += self.direction
        self.rect.center = (round(self.position.x), round(self.position.y))

        # Collision check with all enemies
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self, enemy):
                if enemy.health > 0:
                    enemy.take_damage(self.damage, self.position)
                self.kill()
                break  # Exit the loop after collision

        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()
