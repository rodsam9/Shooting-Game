import random
import arcade
import math
import os

from arcade.color import BLACK, WHITE

SPRITE_SCALING_PLAYER = 0.25
SPRITE_SCALING_ENEMY = 0.1
SPRITE_SCALING_ENEMY_2 = 0.15
SPRITE_SCALING_ENEMY_3 = 0.3
SPRITE_SCALING_BULLET = 0.15

ENEMY_COUNT = 15

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Germaphobe"

SPRITE_SPEED = 0.20
BULLET_SPEED = 5

HEALTHBAR_WIDTH = 25
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -10

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25

MOVEMENT_SPEED = 5

class PLAYER(arcade.Sprite):

    def __init__(self, image, scale, player_max_health):
        super().__init__(image, scale)

        # Add extra attributes for health
        self.player_max_health = player_max_health
        self.player_cur_health = player_max_health

    def player_draw_health_number(self):
        # Draw how many health the enemies have

        health_string = f"{self.player_cur_health}/{self.player_max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def player_draw_health_bar(self):
        # Draw the health bar

        # Draw the red background
        if self.player_cur_health < self.player_max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.player_cur_health / self.player_max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - 10,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)

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

    def __init__(self, image, scale, enemy_max_health):
        super().__init__(image, scale)

        # Add extra attributes for health
        self.enemy_max_health = enemy_max_health
        self.enemy_cur_health = enemy_max_health

    def enemy_draw_health_number(self):
        # Draw how many health the enemies have

        health_string = f"{self.enemy_cur_health}/{self.enemy_max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def enemy_draw_health_bar(self):
        # Draw the health bar

        # Draw the red background
        if self.enemy_cur_health < self.enemy_max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.enemy_cur_health / self.enemy_max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - 10,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)
class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        start_x = 220
        start_y = 370
        arcade.draw_text("GERMAPHOBE", start_x, start_y, arcade.color.GREEN, 50)
    
        self.player_sprite = PLAYER("shooting_game/assets/dr.png", SPRITE_SCALING_PLAYER, player_max_health=10)

        start_x = 208
        start_y = 270
        arcade.draw_text("Use the arrow keys on your keyboard to move around", start_x, start_y, arcade.color.RED, 15)
        
        start_x = 310
        start_y = 240
        arcade.draw_text("Use your mouse to aim", start_x, start_y, arcade.color.RED, 15)

        start_x = 360
        start_y = 210
        arcade.draw_text("Click to Shoot", start_x, start_y, arcade.color.RED, 15)

        start_x = 330
        start_y = 110
        arcade.draw_text("Click to start", start_x, start_y, arcade.color.WHITE, 20)
        arcade.draw_rectangle_outline(center_x=395, center_y=123, width=200, height=50, color=WHITE)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)
        arcade.run()


class GameOverView(arcade.View):
    """ Class to manage the game over view """
    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw the game over view """
        arcade.start_render()
        arcade.draw_text("Game Over!\n", SCREEN_WIDTH/2, SCREEN_HEIGHT/2.5,
                         arcade.color.RED, 100, anchor_x="center")
        start_x = 290
        start_y = 270
        arcade.draw_text(f"You died in wave: {self.window.level}", start_x, start_y, arcade.color.RED, 20)
        arcade.draw_text("Click ESCAPE to return to Main Menu.\n", SCREEN_WIDTH/2, SCREEN_HEIGHT/4,
                         arcade.color.WHITE, 25, anchor_x="center")
        

    def on_key_press(self, key, _modifiers):
        """ If user hits escape, go back to the main menu view """
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)

class Room:
    def __init__(self):
        self.background = None

    def setup_room_1():
        room = Room()
        room.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        return room

class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        #super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None
        self.bullet_list = None

        # Set up the player
        self.player_sprite = None
        self.enemy_health = 2
        self.enemy_health2 = 5
        self.enemy_health3 = 10
        self.good = True
        self.window.level = 1
        self.updated_level = -1
        self.amount_of_enemies = 5
        self.speed = SPRITE_SPEED
        # Game Sounds
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt3.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit1.wav")
        self.death_sound = arcade.load_sound(":resources:sounds/hit5.wav")

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.width = SCREEN_WIDTH

    def levels(self):
        
        while self.good:
            if self.window.level >= 0 and self.window.level <= 3: 
                for i in range(self.amount_of_enemies):

                    # Create the enemy image
                    enemy = ENEMY("shooting_game/assets/germ1.png", SPRITE_SCALING_ENEMY, self.enemy_health)
                    #enemy2 = ENEMY("shooting_game/assets/germ2.png", SPRITE_SCALING_ENEMY_2, self.enemy_health2)
                    #enemy3 = ENEMY("shooting_game/assets/germ3.png", SPRITE_SCALING_ENEMY_3, self.enemy_health3)

                    # Position the enemy
                    enemy.center_x = random.randrange(SCREEN_WIDTH)
                    enemy.center_y = random.randrange(120, SCREEN_HEIGHT)

                    #enemy2.center_x = random.randrange(SCREEN_WIDTH)
                    #enemy2.center_y = random.randrange(120, SCREEN_HEIGHT)

                    #enemy3.center_x = random.randrange(SCREEN_WIDTH)
                    #enemy3.center_y = random.randrange(120, SCREEN_HEIGHT)

                    # Add the enemy to the lists
                    self.enemy_list.append(enemy)
                    #self.enemy_list.append(enemy2)
                    #self.enemy_list.append(enemy3)

                if self.enemy_list == 0:
                    self.window.level = self.updated_level + 1
                else:
                    self.good = False

            elif self.window.level > 3 and self.window.level < 6:
                for i in range(self.amount_of_enemies):

                    # Create the enemy image
                    enemy = ENEMY("shooting_game/assets/germ1.png", SPRITE_SCALING_ENEMY, self.enemy_health)
                    enemy2 = ENEMY("shooting_game/assets/germ2.png", SPRITE_SCALING_ENEMY_2, self.enemy_health2)
                    #enemy3 = ENEMY("shooting_game/assets/germ3.png", SPRITE_SCALING_ENEMY_3, self.enemy_health3)

                    # Position the enemy
                    enemy.center_x = random.randrange(SCREEN_WIDTH)
                    enemy.center_y = random.randrange(120, SCREEN_HEIGHT)

                    enemy2.center_x = random.randrange(SCREEN_WIDTH)
                    enemy2.center_y = random.randrange(120, SCREEN_HEIGHT)

                    #enemy3.center_x = random.randrange(SCREEN_WIDTH)
                    #enemy3.center_y = random.randrange(120, SCREEN_HEIGHT)

                    # Add the enemy to the lists
                    self.enemy_list.append(enemy)
                    self.enemy_list.append(enemy2)
                    #self.enemy_list.append(enemy3)

                if self.enemy_list == 0:
                    self.level = self.updated_level + 1
                else:
                    self.good = False
            else:
                for i in range(self.amount_of_enemies):

                    # Create the enemy image
                    enemy = ENEMY("shooting_game/assets/germ1.png", SPRITE_SCALING_ENEMY, self.enemy_health)
                    enemy2 = ENEMY("shooting_game/assets/germ2.png", SPRITE_SCALING_ENEMY_2, self.enemy_health2)
                    enemy3 = ENEMY("shooting_game/assets/germ3.png", SPRITE_SCALING_ENEMY_3, self.enemy_health3)

                    # Position the enemy
                    enemy.center_x = random.randrange(SCREEN_WIDTH)
                    enemy.center_y = random.randrange(120, SCREEN_HEIGHT)

                    enemy2.center_x = random.randrange(SCREEN_WIDTH)
                    enemy2.center_y = random.randrange(120, SCREEN_HEIGHT)

                    enemy3.center_x = random.randrange(SCREEN_WIDTH)
                    enemy3.center_y = random.randrange(120, SCREEN_HEIGHT)

                    # Add the enemy to the lists
                    self.enemy_list.append(enemy)
                    self.enemy_list.append(enemy2)
                    self.enemy_list.append(enemy3)

                if self.enemy_list == 0:
                    self.window.level = self.updated_level + 1
                else:
                    self.good = False
                
               
   
    def setup(self):

        # Set up the game

        # Sprite lists
        self.window.level = 1
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_sprite = PLAYER("shooting_game/assets/dr.png", SPRITE_SCALING_PLAYER, player_max_health=10)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 300
        self.player_list.append(self.player_sprite)

        self.levels()

        # Set the background color
        arcade.set_background_color(arcade.color.AUROMETALSAURUS)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


    def on_draw(self):
        # render the screen befroe start drawing
        arcade.start_render()

        # Draw all the sprites
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

        output = f"Level: {self.window.level}"
        arcade.draw_text(output, 10, 35, arcade.color.WHITE, 15)

        for player in self.player_list:
            player.player_draw_health_number()
            player.player_draw_health_bar()

        for enemy in self.enemy_list:
            enemy.enemy_draw_health_number()
            enemy.enemy_draw_health_bar()
        
        # for enemy2 in self.enemy_list:
        #     enemy2.enemy_draw_health_number()
        #     enemy2.enemy_draw_health_bar()
        
        # for enemy3 in self.enemy_list:
        #     enemy3.enemy_draw_health_number()
        #     enemy3.enemy_draw_health_bar()



    def on_mouse_press(self, x, y, button, modifiers):
        # Called whenever the mouse button is clicked
        
        arcade.play_sound(self.gun_sound)
        # Create a bullet
        bullet = arcade.Sprite("shooting_game/assets/bullet2.png", SPRITE_SCALING_BULLET)

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
        # bullet.angle = math.degrees(angle)
        # print(f"Bullet angle: {bullet.angle:.2f}")

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED

        # Add the bullet to the lists
        self.bullet_list.append(bullet)

        
    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        self.player_list.update()

        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player_sprite)
        
        for enemy2 in self.enemy_list:
            enemy2.follow_sprite(self.player_sprite)
        
        for enemy3 in self.enemy_list:
            enemy3.follow_sprite(self.player_sprite)

        # update all sprites
        self.bullet_list.update()

        if len(self.enemy_list) == 0 and self.window.level > self.updated_level:
            self.window.level += 1
            self.good = True
            self.levels()
            self.amount_of_enemies += 2
            #self.enemy_health += 1
            self.speed += .20


        for enemy in self.enemy_list:

            player_hit = arcade.check_for_collision_with_list(enemy, self.player_list)

            if len(player_hit) > 0:
                enemy.remove_from_sprite_lists()

            for player in player_hit:
                # Make sure this is the right sprite
                if not isinstance(player, PLAYER):
                    raise TypeError("List contents must be all ints")

                    # Remove one health point
                player.player_cur_health -= 1

                    # Check health
                if player.player_cur_health <= 0:
                    game_over = GameOverView()
                    self.window.show_view(game_over)
                    arcade.run()
                    # enemy dead
                    player.remove_from_sprite_lists()
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)

        for enemy2 in self.enemy_list:

            player_hit = arcade.check_for_collision_with_list(enemy2, self.player_list)

            if len(player_hit) > 0:
                enemy2.remove_from_sprite_lists()

            for player in player_hit:
                # Make sure this is the right sprite
                if not isinstance(player, PLAYER):
                    raise TypeError("List contents must be all ints")

                    # Remove one health point
                player.player_cur_health -= 1

                    # Check health
                if player.player_cur_health <= 0:
                    # enemy dead
                    player.remove_from_sprite_lists()
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)

        for enemy3 in self.enemy_list:

            player_hit = arcade.check_for_collision_with_list(enemy3, self.player_list)

            if len(player_hit) > 0:
                enemy3.remove_from_sprite_lists()

            for player in player_hit:
                # Make sure this is the right sprite
                if not isinstance(player, PLAYER):
                    raise TypeError("List contents must be all ints")

                    # Remove one health point
                player.player_cur_health -= 1

                    # Check health
                if player.player_cur_health <= 0:
                    # enemy dead
                    player.remove_from_sprite_lists()
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)

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
                enemy.enemy_cur_health -= 1

                # Check health
                if enemy.enemy_cur_health <= 0:
                    # enemy dead
                    enemy.remove_from_sprite_lists()
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)

            for enemy2 in hit_list:
                # Make sure this is the right sprite
                if not isinstance(enemy2, ENEMY):
                    raise TypeError("List contents must be all ints")

                # Remove one health point
                enemy2.enemy_cur_health -= 1

                # Check health
                if enemy2.enemy_cur_health <= 0:
                    # enemy dead
                    enemy2.remove_from_sprite_lists()
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)
            
            for enemy3 in hit_list:
                # Make sure this is the right sprite
                if not isinstance(enemy, ENEMY):
                    raise TypeError("List contents must be all ints")

                # Remove one health point
                enemy3.enemy_cur_health -= 1

                # Check health
                if enemy3.enemy_cur_health <= 0:
                    # enemy dead
                    enemy3.remove_from_sprite_lists()
                    arcade.play_sound(self.death_sound)
                else:
                    # Not dead
                    arcade.play_sound(self.hit_sound)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.remove_from_sprite_lists()



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Germaphobe")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()
    window.level = 0
    # game = MyGame()
    # game.setup()
    # arcade.run()


if __name__ == "__main__":
    main()