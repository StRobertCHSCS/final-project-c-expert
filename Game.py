import arcade
import math
import os


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "KILLER SPACE"
BULLET1_SPEED = 5
BULLET2_SPEED = 5
ENEMYLASER_SPEED = 6


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.background = arcade.load_texture("images/background.jpg")

        self.frame_count = 0

        self.enemy_list = None
        self.bullet1_list = None
        self.bullet2_list = None
        self.player_list = None
        self.player = None
        self.enemy = None
        self.enemylaser_list = None

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.bullet1_list = arcade.SpriteList()
        self.bullet2_list = arcade.SpriteList()
        self.enemylaser_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Add player ship
        self.player = arcade.Sprite("images/plane.gif", 0.25)
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = arcade.Sprite("images/enemy1.gif", 0.3)
        enemy.center_x = 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add top-right enemy ship
        enemy = arcade.Sprite("images/enemy1.gif", 0.3)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

    def on_draw(self):

        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.enemy_list.draw()
        self.bullet1_list.draw()
        self.bullet2_list.draw()
        self.player_list.draw()
        self.enemylaser_list.draw()

    def update(self, delta_time):

        self.frame_count += 1

        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)-90

            if self.frame_count % 60 == 0:
                enemylaser = arcade.Sprite("images/bullet.png", 0.19)
                enemylaser.center_x = start_x
                enemylaser.center_y = start_y

                # Angle the bullet sprite
                enemylaser.angle = math.degrees(angle)

                enemylaser.change_x = math.cos(angle) * ENEMYLASER_SPEED
                enemylaser.change_y = math.sin(angle) * ENEMYLASER_SPEED

                self.enemylaser_list.append(enemylaser)

        # Get rid of the bullet when it flies off-screen
        for enemylaser in self.enemylaser_list:
            if enemylaser.top < 0:
                enemylaser.kill()

        self.enemylaser_list.update()
        self.bullet1_list.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):

        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        # Create a bullet
        bullet1 = arcade.Sprite("images/laser.png", 0.3)
        # The image points to the right, and we want it to point up. So
        # rotate it.
        bullet1.angle = 90

        # Give the bullet a speed
        bullet1.change_y = BULLET1_SPEED

        # Position the bullet
        bullet1.center_x = self.player.center_x
        bullet1.bottom = self.player.top

        # Add the bullet to the appropriate lists
        self.bullet1_list.append(bullet1)

        for bullet1 in self.bullet1_list:
            if bullet1.top < 0:
                bullet1.kill()

        self.bullet1_list.update()


def update(self):
    """ Movement and game logic """

    # Call update on bullet sprites
    self.bullet1_list.update()
    self.enemylaser_list.update()

    # Loop through each bullet
    for bullet1 in self.bullet1_list:
        if bullet1.bottom > SCREEN_HEIGHT:
            bullet1.kill()

        # Loop through each bullet
    for enemylaser in self.enemylaser_list:
        if enemylaser.bottom > SCREEN_HEIGHT:
            enemylaser.kill()


def on_key_press(self, key):

    bullet2 = arcade.Sprite("images/player_bullets.png", 0.1)

    if key == arcade.key.SPACE: bullet2.angle = 90

    # Give the bullet a speed
    bullet2.change_y = BULLET2_SPEED

    # Position the bullet
    bullet2.center_x = self.player.center_x
    bullet2.bottom = self.player.top

    # Add the bullet to the appropriate lists
    self.bullet2_list.append(bullet2)

    self.bullet2_list.update()

    # Loop through each bullet
    for bullet2 in self.bullet2_list:

        if bullet2.bottom > SCREEN_HEIGHT:
            bullet2.kill()



def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

