class Team:
    def __init__(self, name, color):
        """A team with a name and units."""
        self.name = name
        self.color = color
        self.units = []

    def add_unit(self, unit):
        """Add a unit to the team."""
        self.units.append(unit)
