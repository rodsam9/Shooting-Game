import random
import arcade
import math
import os

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 0.4
SPRITE_SCALING_LASER = 0.8
ENEMY_COUNT = 15

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Germaphobe Beta"

SPRITE_SPEED = 0.20
BULLET_SPEED = 5

HEALTHBAR_WIDTH = 25
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -10

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25

class ENEMY(arcade.Sprite):

    def follow_sprite(self, player_sprite):
        # This tells the enemies to go to the main guy

        if self.center_y < player_sprite.center_y:
            self.center_y += min(SPRITE_SPEED, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(SPRITE_SPEED, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(SPRITE_SPEED, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(SPRITE_SPEED, self.center_x - player_sprite.center_x)

    def __init__(self, image, scale, max_health):
        super().__init__(image, scale)

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health

    def draw_health_number(self):
        # Draw how many health the enemies have

        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        # Draw the health bar

        # Draw the red background
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - 10,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None

        # Set up the player
        self.player_sprite = None

    def setup(self):

        # Set up the game

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite)

        # Create the enemies
        for i in range(ENEMY_COUNT):

            # Create the enemy image
            enemy = ENEMY(":resources:images/enemies/slimeGreen.png", SPRITE_SCALING_ENEMY, max_health=2)

            # Position the enemy
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            enemy.center_y = random.randrange(120, SCREEN_HEIGHT)

            # Add the enemy to the lists
            self.enemy_list.append(enemy)

        # Set the background color
        arcade.set_background_color(arcade.color.AUROMETALSAURUS)

    def on_draw(self):
        # render the screen befroe start drawing
        arcade.start_render()

        # Draw all the sprites
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        for enemy in self.enemy_list:
            enemy.draw_health_number()
            enemy.draw_health_bar()

    def on_mouse_press(self, x, y, button, modifiers):
        # Called whenever the mouse button is clicked

        # Create a bullet
        bullet = arcade.Sprite(":resources:images/topdown_tanks/tankDark_barrel3.png", SPRITE_SCALING_LASER)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # angle the bullet
        bullet.angle = math.degrees(angle)
        print(f"Bullet angle: {bullet.angle:.2f}")

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the lists
        self.bullet_list.append(bullet)

    def on_update(self, delta_time):
        """ Movement and game logic """

        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player_sprite)

        # update all sprites
        self.bullet_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:

            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            # For every enemy we hit, process
            for enemy in hit_list:
                # Make sure this is the right sprite
                if not isinstance(enemy, ENEMY):
                    raise TypeError("List contents must be all ints")

                # Remove one health point
                enemy.cur_health -= 1

                # Check health
                if enemy.cur_health <= 0:
                    # enemy dead
                    enemy.remove_from_sprite_lists()

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()