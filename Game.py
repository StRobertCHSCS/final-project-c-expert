import arcade
import math
import os


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "KILLER SPACE"
BULLET_SPEED = 4


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_mouse_visible(False)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.background = arcade.load_texture("images/background.jpg")

        self.frame_count = 0

        self.enemy_list = None
        self.bullet_list = None
        self.player_list = None
        self.player = None

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Add player ship
        self.player = arcade.Sprite("images/plane.gif", 0.5,)
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = arcade.Sprite("images/enemy1.gif", 0.5)
        enemy.center_x = 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add top-right enemy ship
        enemy = arcade.Sprite("images/enemy1.gif", 0.5)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

    def on_draw(self):

        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

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
                bullet = arcade.Sprite("images/laser.png", 0.43)
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.kill()

        self.bullet_list.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):

        self.player.center_x = x
        self.player.center_y = y


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

