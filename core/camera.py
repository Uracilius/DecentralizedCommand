class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height, tile_size):
        self.x = 0
        self.y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
        self.scroll_speed = 20

    def move(self, dx, dy):
        """Move the camera, ensuring it stays within bounds."""
        self.x = max(0, min(self.x + dx, self.map_width - self.screen_width))
        self.y = max(0, min(self.y + dy, self.map_height - self.screen_height))

    def apply(self, position):
        """Offset a position by the camera's current position."""
        return position[0] - self.x, position[1] - self.y
