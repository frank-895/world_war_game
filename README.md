***World War Game***

This is a simple 2D plane battle game developed using Pygame. Players control a plane to shoot down enemy planes and avoid being hit. The game includes features such as health bars, lives, and power-ups.

**Features**

- User-Controlled Plane: Move and shoot at enemy planes.
- Enemy Planes: Automatically move towards the player and can be shot down.
- Projectiles: Shoot bullets and bombs to defeat enemies.
- Collectibles: Access power-ups and boosts, like extra lives, rapid fire and shields. 
- Health and Lives: Track player health and remaining lives.
- Levels: There are three levels to the game.
- Game Over State: Display when the player runs out of lives.

**Installation**

- Clone or download this repository.
- Ensure you have Python and Pygame installed. You can install Pygame using pip:

```
pip install pygame
```

- Controls: Use arrow keys to move and spacebar to shoot. Use w to drop bombs on the enemy
- Objective: Shoot down enemy planes and tanks and avoid getting hit.
- Health Management: Your plane has health and lives; avoid collisions and enemy bullets.

**Code Structure**

Classes:
- plane: Base class for all planes.
- user_plane: Class for the player-controlled plane.
- enemy_plane: Class for enemy planes.
- projectile: Base class for projectiles.
- bullet: Class for bullets fired by planes.
- bomb: Class for bombs dropped by planes.
- tank: Class for tanks in the second level.

**Lessons Learned**

Through developing this game, I learned:

- How to manage user input with Pygame.
- Techniques for handling collisions between objects.
- Implementing health and lives systems for game balance.
- Basic game design principles and state management.

**Future Improvements**

- Implement more advanced enemy AI.
- Create a scoring system and leaderboards.
- Improve graphics and sound effects.
