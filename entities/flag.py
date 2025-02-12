import pygame

class Flag:
    def __init__(self, position):
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], 30, 60)
        self.image = pygame.image.load("assets/sprites/flag_enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 60))
        self.captured_by = None  # Track which ally captured the flag

    def capture(self, ally_team, player):
        """Capture the flag by an ally and add score to the player."""
        self.captured_by = ally_team
        player.score += 1
        self.image = pygame.image.load("assets/sprites/flag_ally.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 60))
        print(f"Flag captured by {ally_team}. Player score: {player.score}")

    def is_captured(self):
        """Check if the flag is captured."""
        return self.captured_by is not None

    def render(self, screen, camera):
        """Render the flag on the screen."""
        screen_position = camera.apply(self.rect.topleft)
        screen.blit(self.image, screen_position)

