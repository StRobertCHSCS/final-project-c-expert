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
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE


class TurningSprite(arcade.Sprite):
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x))


class ShipSprite(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale)

        self.thrust = 0
        self.speed = 0
        self.max_speed = 4
        self.drag = 0.05
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
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0

        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        self.speed += self.thrust
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        self.change_x = -math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed

        self.center_x += self.change_x
        self.center_y += self.change_y

        super().update()


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

        image_list = ("images/enemy1.gif",
                      "images/enemy1.gif",
                      "images/enemy1.gif",
                      "images/enemy1.gif")

        for i in range(STARTING_ENEMY_COUNT):
            image_no = random.randrange(4)
            enemy_sprite = EnemySprite(image_list[image_no], 0.3)
            enemy_sprite.guid = "Enemy"

            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

            enemy_sprite.change_x = random.random() * 2 - 1
            enemy_sprite.change_y = random.random() * 2 - 1

            enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            self.all_sprites_list.append(enemy_sprite)
            self.enemy_list.append(enemy_sprite)

    def on_draw(self):
        arcade.start_render()

        self.all_sprites_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 1250, 70, arcade.color.WHITE, 13)

        output = f"Enemies Obliterated: {len(self.enemy_list)}"
        arcade.draw_text(output, 1250, 50, arcade.color.WHITE, 13)

    def on_key_release(self, symbol, modifiers):
        """ Called whenever a key is released. """
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = 0

    def on_key_press(self, symbol, modifiers):
        if not self.player_sprite.respawning and symbol == arcade.key.SPACE:
            bullet_sprite = BulletSprite("images/bullet.png", 0.08)
            bullet_sprite.guid = "Bullet"

            bullet_speed = 13
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

        if symbol == arcade.key.LEFT:
            self.player_sprite.change_angle = 3
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_angle = -3
        elif symbol == arcade.key.UP:
            self.player_sprite.thrust = 0.15
        elif symbol == arcade.key.DOWN:
            self.player_sprite.thrust = -.2

    def split_enemy_(self, enemy: EnemySprite):
        x = enemy.center_x
        y = enemy.center_y
        self.score += 1

        if enemy.size == 4:
            for i in range(3):
                image_no = random.randrange(2)
                image_list = ["images/escape pod.gif",
                              "images/escape pod.gif"]

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
                image_list = ["images/alien.png",
                              "images/alien.png"]

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
                    enemy.kill()
                    bullet.kill()

            if not self.player_sprite.respawning:
                enemies = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
                if len(enemies) > 0:
                    if self.lives > 0:
                        self.lives -= 1
                        self.player_sprite.respawn()
                        self.split_enemy_(enemies[0])
                        enemies[0].kill()
                        self.ship_life_list.pop().kill()
                        print("Crash")
                    else:
                        self.game_over = True
                        print("Game over")


def main():
    window = MyGame()
    window.start_new_game()
    arcade.run()


if __name__ == "__main__":
    main()


