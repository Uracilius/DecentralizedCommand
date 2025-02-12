The project is structured into key components:

1️⃣ entities/ (Game Objects)
Unit.py – Defines soldiers with health, accuracy, speed, and weapons.
Team.py – Manages teams (Allies vs. Enemies).
Obstacle.py – Defines obstacles that provide cover.
HardObstacle.py – Impassable obstacles.
Flag.py – Capture-the-flag mechanic.
Weapon.py – Weapons with different stats (Pistol, Machine Gun, etc.).
2️⃣ mechanics/  (Game Logic)
MapManager.py – Reads the map file, places units, obstacles, and flags.
CombatManager.py – Manages unit combat and engagements.
3️⃣ core/  (Game Engine Core)
Config.py – Stores screen size, FPS, and colors.
Camera.py – Handles player movement and camera scrolling.
Utils.py – Pathfinding (A* algorithm), utility functions.
4️⃣ rendering/ (Graphics & Rendering)
Renderer.py – Draws the battlefield, units, obstacles, and flags.

Units can move, take cover, attack enemies, and follow orders.
Pathfinding: Uses A Algorithm* to find the best route.
Combat: Units attack based on their weapon’s range and accuracy.
Cover System: Units take less damage if in cover.


To run, simply run python main.py. Nothing else!





Future improvements:
🏴 More unit types (Snipers, Tanks, Mechs).
🗺️ Map generator for procedural battlefields.
🤖 Smarter AI with flanking & formations.
🏆 Online multiplayer mode!