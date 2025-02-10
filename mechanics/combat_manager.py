import pygame
import logging
from entities.bullet import Bullet


class CombatManager:
    def __init__(self):
        self.bullets = pygame.sprite.Group()
        self.scheduled_bullets = []

        # Initialize the mixer if it's not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Load sounds safely
        self.fire_sound = self.load_sound("assets/sounds/shot.mp3")
        self.hit_sound = self.load_sound("assets/sounds/hit.mp3")

        logging.info("CombatManager initialized.")

    def load_sound(self, file_path):
        """ Load a sound file safely. If it fails, return None. """
        try:
            return pygame.mixer.Sound(file_path)
        except Exception as e:
            logging.error(f"Error loading sound {file_path}: {e}")
            return None

    def handle_combat(self, units, obstacles):
        """ Update unit combat logic and manage bullet spawning. """
        logging.debug("Handling combat...")

        teams = {unit.team for unit in units}
        team_units = {team: [u for u in units if u.team == team] for team in teams}

        for unit in units:
            if unit.health <= 0:
                continue  # Dead units should not act

            logging.debug(f"Processing unit {unit.team.name} at {unit.rect.topleft} (HP: {unit.health})")

            enemies = [e for t, group in team_units.items() if t != unit.team for e in group]
            unit.update(enemies, obstacles, units)

            for enemy in enemies:
                if enemy.health > 0 and self.is_in_range(unit, enemy) and unit.cooldown_timer <= 0:
                    self.spawn_bullet(unit, enemy, enemies)
                    unit.cooldown_timer = unit.weapon.fire_rate

        self.update_bullets()  # Process scheduled bullets
        self.bullets.update()

    def is_in_range(self, unit, enemy):
        """ Check if the enemy is within the unit's weapon range. """
        distance = pygame.math.Vector2(unit.rect.center).distance_to(enemy.rect.center)
        return distance <= unit.weapon.range

    def spawn_bullet(self, attacker, target, enemies):
        start_time = pygame.time.get_ticks()
        bullets_per_volley = attacker.weapon.bullets_per_volley
        delay_per_bullet = 50  # 50 ms between each bullet (adjustable)

        for i in range(bullets_per_volley):
            fire_time = start_time + (i * delay_per_bullet)
            self.scheduled_bullets.append((fire_time, attacker, target, enemies))  # Pass enemies here

        logging.info(f"{bullets_per_volley} bullets scheduled from {attacker.rect.center} to {target.rect.center}")

    def update_bullets(self):
        """ Spawn scheduled bullets when their time comes. """
        current_time = pygame.time.get_ticks()
        bullets_to_spawn = [b for b in self.scheduled_bullets if current_time >= b[0]]

        for fire_time, attacker, target, enemies in bullets_to_spawn: 
            if self.fire_sound:
                self.fire_sound.play()

            bullet = Bullet(start_pos=attacker.rect.center, target_unit=target, attacker=attacker, enemies=enemies)
            self.bullets.add(bullet)

            self.scheduled_bullets.remove((fire_time, attacker, target, enemies))  

    def render_bullets(self, screen, camera):
        """ Render bullets on screen. """
        for bullet in self.bullets:
            position = camera.apply(bullet.rect.center)
            pygame.draw.circle(screen, bullet.color, (int(position[0]), int(position[1])), bullet.radius)
