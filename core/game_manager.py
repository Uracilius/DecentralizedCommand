import pygame
import logging
from core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLORS
from rendering.renderer import Renderer
from mechanics.map_manager import MapManager
from core.camera import Camera
from core import utils
from mechanics.combat_manager import CombatManager
import random

class Player:
    def __init__(self):
        self.score = 0

class Button:
    def __init__(self, rect, text, callback, font, text_color, button_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.text_color = text_color
        self.button_color = button_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.button_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered(event.pos):
                self.callback()

class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Strategy Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.state = "MENU"
        self.difficulty_modifier = 1.0  # Default difficulty

        self.menu_font = pygame.font.Font(None, 36)
        button_width = 200
        button_height = 50
        start_button_rect = pygame.Rect(
            (SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height - 10),
            (button_width, button_height)
        )
        exit_button_rect = pygame.Rect(
            (SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 10),
            (button_width, button_height)
        )
        restart_button_rect = pygame.Rect(
            (SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 70),
            (button_width, button_height)
        )
        self.menu_buttons = [
            Button(start_button_rect, "Start", self.show_difficulty_selection, self.menu_font, COLORS["black"], COLORS["white"]),
            Button(exit_button_rect, "Exit", self.exit_game, self.menu_font, COLORS["black"], COLORS["white"])
        ]

        self.difficulty_buttons = [
            Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50), "Easy", lambda: self.set_difficulty(0.5), self.menu_font, COLORS["black"], COLORS["white"]),
            Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50), "Normal", lambda: self.set_difficulty(1.0), self.menu_font, COLORS["black"], COLORS["white"]),
            Button((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50), "Hard", lambda: self.set_difficulty(2.0), self.menu_font, COLORS["black"], COLORS["white"])
        ]
        self.game_over_buttons = [
            Button(restart_button_rect, "Restart", self.restart_game, self.menu_font, COLORS["black"], COLORS["white"]),
            Button(exit_button_rect, "Exit", self.exit_game, self.menu_font, COLORS["black"], COLORS["white"])
        ]

        self.tile_size = 50
        self.dragging = False

        self.map_manager = MapManager("assets/maps/test_map.txt", self.tile_size)
        self.map_manager.load_map()
        map_width, map_height = self.map_manager.get_map_dimensions()

        self.real_map_width = map_width * self.tile_size
        self.real_map_height = map_height * self.tile_size

        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.real_map_width, self.real_map_height, self.tile_size)
        self.renderer = Renderer(self.screen, self.tile_size, self.camera)

        self.teams = self.map_manager.get_teams()
        self.units = self.map_manager.get_units()
        self.obstacles = self.map_manager.get_obstacles()
        self.hard_obstacles = []  # Initialize hard obstacles list
        self.flags = self.map_manager.get_flags()  # Get flags from map manager

        self.combat_manager = CombatManager()
        self.player = Player()

        self.menu_music = pygame.mixer.Sound("assets/music/main_menu_music_1.mp3")
        self.combat_music = pygame.mixer.Sound("assets/music/combat.mp3")
        self.play_menu_music()

        self.player = Player()  # Initialize player with score
        self.flags = self.map_manager.get_flags()  # Get flags from map manager
        print(f"Flags loaded: {self.flags}")  # Debugging print statement

    def play_menu_music(self):
        """Play the menu music."""
        menu_music_files = ["assets/music/main_menu_music_1.mp3", "assets/music/main_menu_music_2.mp3"]
        selected_music = random.choice(menu_music_files)
        pygame.mixer.music.load(selected_music)
        pygame.mixer.music.play(-1)

    def play_combat_music(self):
        """Play the combat music."""
        pygame.mixer.music.load("assets/music/combat.mp3")
        pygame.mixer.music.play(-1)

    def start_game(self):
        """Callback for the Start button; switch to game state."""
        print("Starting game...")
        self.state = "GAME"
        self.play_combat_music()

    def restart_game(self):
        """Callback for the Restart button; restart the game."""
        print("Restarting game...")
        self.__init__()
        self.start_game()

    def exit_game(self):
        """Callback for the Exit button; quit the game."""
        print("Exiting game...")
        self.running = False

    def handle_menu_events(self, events):
        """Process events when the menu is active."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.menu_buttons:
                button.handle_event(event)

    def handle_game_over_events(self, events):
        """Process events when the game is over."""
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.game_over_buttons:
                button.handle_event(event)

    def handle_game_events(self, events):
        """Process events during gameplay."""
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
                    self.play_menu_music()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.dragging = True
                    self.start_drag_pos = mouse_pos
                    self.selection_rect = pygame.Rect(self.start_drag_pos, (0, 0))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging:
                    self.dragging = False
                    adjusted_rect = self.selection_rect.move(self.camera.x, self.camera.y)
                    selected_any = False
                    for unit in self.units:
                        if adjusted_rect.colliderect(unit.rect):
                            unit.select(True)
                            selected_any = True
                            logging.debug(f"Selected unit at {unit.rect.topleft}")
                            break
                        else:
                            unit.select(False)
                    if not selected_any:
                        logging.debug("No unit selected.")

                elif event.button == 3:
                    world_pos = (mouse_pos[0] + self.camera.x, mouse_pos[1] + self.camera.y)
                    for unit in self.units:
                        if unit.selected:
                            if unit.path and unit.path[-1] == world_pos:
                                continue
                            path = utils.astar_pathfinding(
                                start=unit.rect.center,
                                end=world_pos,
                                obstacles=self.obstacles,
                                hard_obstacles=self.hard_obstacles,
                                tile_size=self.tile_size,
                                map_width=self.real_map_width,
                                map_height=self.real_map_height,
                                units=self.units
                            )
                            unit.set_path(path)
                            logging.debug(f"Path for unit at {unit.rect.topleft}: {path}")

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    current_mouse_pos = mouse_pos
                    self.selection_rect.width = current_mouse_pos[0] - self.start_drag_pos[0]
                    self.selection_rect.height = current_mouse_pos[1] - self.start_drag_pos[1]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.move(0, -self.camera.scroll_speed)
        if keys[pygame.K_s]:
            self.camera.move(0, self.camera.scroll_speed)
        if keys[pygame.K_a]:
            self.camera.move(-self.camera.scroll_speed, 0)
        if keys[pygame.K_d]:
            self.camera.move(self.camera.scroll_speed, 0)
    
    def update_game(self):
            """Update game logic (combat, unit removal, flag capture, etc.)"""
            self.combat_manager.handle_combat(self.units, self.obstacles, self.hard_obstacles)
            self.units = [u for u in self.units if u.health > 0]

            # Check for flag captures
            for flag in self.flags:
                if not flag.is_captured():
                    for unit in self.units:
                        if unit.team.name == "Allies" and flag.rect.colliderect(unit.rect):
                            flag.capture(unit.team, self.player)
                            
            # Check for win condition
            if all(flag.is_captured() for flag in self.flags):
                self.state = "WIN"

            # Check for lose condition
            if not any(unit.team.name == "Allies" for unit in self.units):
                self.state = "GAME_OVER"


    def play_menu_music(self):
        pygame.mixer.music.load("assets/music/main_menu_music_1.mp3")
        pygame.mixer.music.play(-1)

    def play_combat_music(self):
        pygame.mixer.music.load("assets/music/combat.mp3")
        pygame.mixer.music.play(-1)

    def show_difficulty_selection(self):
        self.state = "DIFFICULTY_SELECTION"

    def set_difficulty(self, modifier):
        self.difficulty_modifier = modifier
        self.start_game()

    def start_game(self):
        self.state = "GAME"
        self.play_combat_music()
        self.teams = self.map_manager.get_teams()
        self.units = self.map_manager.get_units()
        self.obstacles = self.map_manager.get_obstacles()
        self.hard_obstacles = self.map_manager.get_hard_obstacles()
        self.flags = self.map_manager.get_flags()
        
        for unit in self.units:
            unit.set_difficulty_multiplier(self.difficulty_modifier)
        self.combat_manager.set_difficulty_multiplier(self.difficulty_modifier)

    def exit_game(self):
        self.running = False

    def handle_menu_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.menu_buttons:
                button.handle_event(event)

    def handle_difficulty_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            for button in self.difficulty_buttons:
                button.handle_event(event)

    def render_menu(self):
        self.screen.fill(COLORS["white"])
        for button in self.menu_buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def render_difficulty_selection(self):
        self.screen.fill(COLORS["white"])
        for button in self.difficulty_buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def render_game(self):
        """Render the gameplay screen."""
        self.screen.fill(COLORS["black"])
        self.renderer.render_ground(SCREEN_WIDTH, SCREEN_HEIGHT, COLORS)
        self.renderer.render_map(self.obstacles, self.hard_obstacles, COLORS)
        self.renderer.render_units(self.units, COLORS)
        self.renderer.render_bullets(self.combat_manager)
        self.renderer.render_flags(self.flags)

        mouse_pos = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 24)
        text_surface = font.render(f"{mouse_pos}", True, COLORS["white"])
        self.screen.blit(text_surface, (mouse_pos[0] + 10, mouse_pos[1] + 10))

        if self.dragging:
            pygame.draw.rect(self.screen, COLORS["white"], self.selection_rect, 1)

        pygame.display.flip()

    def render_game_over(self):
        """Render the game over screen."""
        self.screen.fill(COLORS["black"])
        font = pygame.font.Font(None, 72)
        text_surface = font.render("GAME OVER", True, COLORS["red"])
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text_surface, text_rect)
        for button in self.game_over_buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def render_win(self):
        """Render the win screen."""
        self.screen.fill(COLORS["black"])
        font = pygame.font.Font(None, 72)
        text_surface = font.render("YOU WIN", True, COLORS["green"])
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(text_surface, text_rect)
        for button in self.game_over_buttons:
            button.draw(self.screen)
        pygame.display.flip()

    def debug_teams_and_units(self):
        for team in self.teams:
            logging.debug(f"{team.name} ({len(team.units)} units):")
            for unit in team.units:
                logging.debug(f"  Unit at {unit.position}, Health: {unit.health}, Weapon: {unit.weapon.__str__()}")


    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.state == "MENU":
                self.handle_menu_events(events)
                self.render_menu()
            elif self.state == "DIFFICULTY_SELECTION":
                self.handle_difficulty_events(events)
                self.render_difficulty_selection()
            elif self.state == "GAME":
                self.handle_game_events(events)
                self.update_game()
                self.render_game()
            elif self.state == "GAME_OVER":
                self.handle_game_over_events(events)
                self.render_game_over()
            elif self.state == "WIN":
                self.handle_game_over_events(events)
                self.render_win()

            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()
