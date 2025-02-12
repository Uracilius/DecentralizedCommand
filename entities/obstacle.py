import pygame

class Obstacle:
    def __init__(self, position):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 40, 40)

    def colliderect(self, other_rect):
        """Allows Obstacle objects to be used like pygame.Rect in collisions."""
        return self.rect.colliderect(other_rect)

class HardObstacle(Obstacle):
    def __init__(self, position):
        super().__init__(position)
        self.rect = pygame.Rect(position[0], position[1], 40, 40)
        self.color = (100, 100, 100)

    def colliderect(self, other_rect):
        """Allows Obstacle objects to be used like pygame.Rect in collisions."""
        return self.rect.colliderect(other_rect)