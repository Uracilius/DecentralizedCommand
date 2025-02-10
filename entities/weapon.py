class Weapon:
    def __init__(self, name, fire_rate, damage, bullets_per_volley, accuracy_modifier, range, sprite):
        """
        :param name: Name of the weapon.
        :param fire_rate: Cooldown in frames between volleys.
        :param damage: Damage per bullet.
        :param bullets_per_volley: Number of bullets fired per volley.
        :param accuracy: Accuracy of the weapon (percentage).
        :param range: Effective range of the weapon.
        :param sprite: Path to the sprite image file.
        """
        self.name = name
        self.fire_rate = fire_rate  # number of frames between shots (cooldown)
        self.damage = damage
        self.bullets_per_volley = bullets_per_volley
        self.accuracy_modifier = accuracy_modifier
        self.range = range
        self.sprite = sprite

    def __str__(self):
        return (f"Weapon: {self.name}, Fire Rate: {self.fire_rate} frames, "
                f"Damage: {self.damage}, Bullets per Volley: {self.bullets_per_volley}, "
                f"Accuracy Modifier: {self.accuracy_modifier}%, Range: {self.range}, "
                f"Sprite: {self.sprite}")

class Pistol(Weapon):
    def __init__(self):
        # Baseline weapon: one bullet per volley, 60 frames cooldown, 10 damage per bullet, 90% accuracy, 300 range.
        super().__init__(name="Pistol", fire_rate=60, damage=10, bullets_per_volley=1, accuracy_modifier=0.9, range=400, sprite="assets/sprites/pistol.png")

class MachineGun(Weapon):
    def __init__(self):
        # Fast firing weapon: three bullets per volley, very short cooldown, lower damage per bullet, 70% accuracy, 200 range.
        super().__init__(name="Machine Gun", fire_rate=15, damage=5, bullets_per_volley=3, accuracy_modifier=0.7, range=275, sprite="assets/sprites/machine_gun.png")

class SubmachineGun(Weapon):
    def __init__(self):
        # A moderate option: two bullets per volley, 30 frames cooldown, moderate damage per bullet, 80% accuracy, 250 range.
        super().__init__(name="Submachine Gun", fire_rate=30, damage=7, bullets_per_volley=2, accuracy_modifier=0.8, range=300, sprite="assets/sprites/submachine_gun.png")
