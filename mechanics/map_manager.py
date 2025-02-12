import random
from entities.unit import Unit
from entities.team import Team
from entities.obstacle import Obstacle
from entities import weapon
from entities.flag import Flag

class MapManager:
    def __init__(self, map_file, tile_size=50):
        self.map_file = map_file
        self.tile_size = tile_size

        self._obstacles = []
        self._units = []
        self._teams = []
        self._flags = []  # New list to store flags

        self.map_data = self._load_map(map_file)
        if not self.map_data:
            raise ValueError("Map file is empty or invalid!")
        
        self.map_width = len(self.map_data[0])
        self.map_height = len(self.map_data)

        self.available_weapons = [weapon.SubmachineGun(), weapon.Pistol(), weapon.MachineGun()]

    def _load_map(self, map_file):
        """Load raw map data from the file."""
        with open(map_file, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
        return lines

    def load_map(self):
        """Parse self.map_data and create obstacles/units/flags."""
        ally_team = Team("Allies", (0, 255, 0))
        enemy_team = Team("Enemies", (255, 0, 0))
        self._teams.extend([ally_team, enemy_team])

        for y, line in enumerate(self.map_data):
            for x, char in enumerate(line):
                position = (x * self.tile_size, y * self.tile_size)

                if char == "#":
                    self._obstacles.append(Obstacle(position))
                elif char == "U":
                    weapon = random.choice(self.available_weapons)
                    unit = Unit(position[0], position[1], ally_team, health=100, weapon=weapon)
                    ally_team.add_unit(unit)
                    self._units.append(unit)
                elif char == "E":
                    weapon = random.choice(self.available_weapons)
                    unit = Unit(position[0], position[1], enemy_team, health=100, weapon=weapon)
                    enemy_team.add_unit(unit)
                    self._units.append(unit)
                elif char == "F":  # New condition to parse flags
                    flag = Flag(position)
                    self._flags.append(flag)
                    print(f"Flag created at {position}")  # Debugging print statement

    def get_map_dimensions(self):
        return self.map_width, self.map_height

    def get_obstacles(self):
        return self._obstacles

    def get_units(self):
        return self._units

    def get_teams(self):
        return self._teams

    def get_allies(self):
        """Return the list of allied units."""
        ally_team = next((team for team in self._teams if team.name == "Allies"), None)
        return ally_team.units if ally_team else []

    def get_obstacles(self):
        """Return the list of obstacles."""
        return self._obstacles

    def get_units(self):
        """Return the list of units."""
        return self._units

    def get_teams(self):
        """Return the list of teams."""
        return self._teams

    def get_flags(self):
        """Return the list of flags."""
        return self._flags
