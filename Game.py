import random
import math
import arcade
import os

STARTING_ENEMY_COUNT = 6
SCALE = 0.5
SCREEN_WIDTH = 1500
OFFSCREEN_SPACE = 200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Alien Cleaner"
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
LEFT_LIMIT = -OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE


class TurningSprite(arcade.Sprite):
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))


class EnemySprite(arcade.Sprite):
    def __init__(self, image_file_name, scale):
        super().__init__(image_file_name, scale=scale)
        self.size = 0

    def update(self):
        super().update()
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT


class ShipSprite(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.respawning = 0
        self.respawn()

    def respawn(self):
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2
        self.angle = 0

    def update(self):
        if self.respawning:
            self.respawning += 1
            self.alpha = self.respawning
            if self.respawning > 250:
                self.respawning = 0
                self.alpha = 255

        super().update()


class BulletSprite(TurningSprite):
    def update(self):
        super().update()
        if self.center_x < -100 or self.center_x > 1500 or \
                self.center_y > 1100 or self.center_y < -100:
            self.kill()


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0
        self.background = arcade.load_texture("images/background.png")

        self.set_mouse_visible(False)
        self.game_over = False
        self.all_sprites_list = None
        self.enemy_list = None
        self.bullet_list = None
        self.ship_life_list = None
        self.score = 0
        self.player_sprite = None
        self.lives = 3

    def start_new_game(self):
        self.frame_count = 0
        self.game_over = False

        self.all_sprites_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.ship_life_list = arcade.SpriteList()

        self.score = 0
        self.player_sprite = ShipSprite("images/plane.gif", 0.2)
        self.all_sprites_list.append(self.player_sprite)
        self.lives = 3

        cur_pos = 10
        for i in range(self.lives):
            life = arcade.Sprite("images/plane.gif", 0.25)
            life.center_x = cur_pos + life.width
            life.center_y = life.height
            cur_pos += life.width
            self.all_sprites_list.append(life)
            self.ship_life_list.append(life)

        image_list = ("images/enemy1.gif", "images/enemy1.gif", "images/enemy1.gif", "images/enemy1.gif",
                      "images/enemy1.gif")

        for i in range(STARTING_ENEMY_COUNT):
            image_nu = random.randrange(5)
            enemy_sprite = EnemySprite(image_list[image_nu], 0.3)
            enemy_sprite.guid = "Enemy"

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 3 - 1
            enemy_sprite.change_y = random.random() * 3 - 1

            enemy_sprite.change_angle = (random.random() - 0.5) * 3
            enemy_sprite.size = 3
            self.all_sprites_list.append(enemy_sprite)
            self.enemy_list.append(enemy_sprite)

    def on_draw(self):
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.all_sprites_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 1250, 70, arcade.color.BLACK_BEAN, 15)

        output = f"Enemy Count: {len(self.enemy_list)}"
        arcade.draw_text(output, 1250, 50, arcade.color.RED_DEVIL, 15)

    def on_key_release(self, symbol, modifiers):
        if symbol == arcade.key.A:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.D:
            self.player_sprite.change_angle = 0

    def on_key_press(self, symbol, modifiers):
        if not self.player_sprite.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = BulletSprite("images/bullet.png", 0.08)
            bullet_sprite.guid = "Bullet"

            bullet_speed = 14
            bullet_sprite.change_y = \
                math.cos(math.radians(self.player_sprite.angle)) * bullet_speed
            bullet_sprite.change_x = \
                -math.sin(math.radians(self.player_sprite.angle)) \
                * bullet_speed

            bullet_sprite.center_x = self.player_sprite.center_x
            bullet_sprite.center_y = self.player_sprite.center_y
            bullet_sprite.update()

            self.all_sprites_list.append(bullet_sprite)
            self.bullet_list.append(bullet_sprite)

        if symbol == arcade.key.A:
            self.player_sprite.change_angle = 4
        elif symbol == arcade.key.D:
            self.player_sprite.change_angle = -4

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def split_enemy_(self, enemy: EnemySprite):
        x = enemy.center_x
        y = enemy.center_y
        self.score += 1

        if enemy.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = ["images/escape pod.gif", "images/escape pod.gif"]

                enemy_sprite = EnemySprite(image_list[image_no],
                                              SCALE * 1)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 2.5 - 1.25
                enemy_sprite.change_y = random.random() * 2.5 - 1.25

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 3

                self.all_sprites_list.append(enemy_sprite)
                self.enemy_list.append(enemy_sprite)

        elif enemy.size == 3:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = ["images/alien.png", "images/alien.png"]

                enemy_sprite = EnemySprite(image_list[image_no],
                                                SCALE * 0.5)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3 - 1.5
                enemy_sprite.change_y = random.random() * 3 - 1.5

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 2

                self.all_sprites_list.append(enemy_sprite)
                self.enemy_list.append(enemy_sprite)

        elif enemy.size == 2:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = ["images/skull.png",
                              "images/skull.png"]

                enemy_sprite = EnemySprite(image_list[image_no],
                                            SCALE * 0.03)

                enemy_sprite.center_y = y
                enemy_sprite.center_x = x

                enemy_sprite.change_x = random.random() * 3.5 - 1.75
                enemy_sprite.change_y = random.random() * 3.5 - 1.75

                enemy_sprite.change_angle = (random.random() - 0.5) * 2
                enemy_sprite.size = 1

                self.all_sprites_list.append(enemy_sprite)
                self.enemy_list.append(enemy_sprite)

    def update(self, x):

        self.frame_count += 1

        if not self.game_over:
            self.all_sprites_list.update()

            for bullet in self.bullet_list:
                enemy_plain = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                enemy_spatial = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                if len(enemy_plain) != len(enemy_spatial):
                    print("ERROR")

                enemies = enemy_spatial

                for enemy in enemies:
                    self.split_enemy_(enemy)
                    bullet.kill()
                    enemy.kill()

            if not self.player_sprite.respawning:
                enemies = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
                if len(enemies) > 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        self.split_enemy_(enemies[0])
                        enemies[0].kill()
                        self.ship_life_list.pop().kill()
                        print("OBLITERATED")
                    else:
                        self.game_over = True
                        print("GAME OVER")


def main():
    window = MyGame()
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()


