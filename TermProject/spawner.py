from pico2d import *
import gfw
import gobj
import enemy
import random

class EnemySpawner:
    image = None
    FPS = 12

    def __init__(self, pos, enemy_class, add_damage, add_hp):
        self.pos = pos
        self.add_damage = add_damage
        self.add_hp = add_hp
        self.enemy_class = enemy_class
        self.image = gfw.image.load(gobj.RES_DIR + '/Sprites/enemies/spawn.png')
        self.fidx = 0
        self.time = 0

    def draw(self):
        width, height = 48, 48
        sx = (self.fidx % 14) * width
        sy = 0
        self.image.clip_composite_draw(sx, sy, width, height, 0, '', *self.pos, width * gobj.PIXEL_SCOPE, height * gobj.PIXEL_SCOPE)

    def update(self):
        self.time += gfw.delta_time
        self.fidx = round(self.time * self.FPS)
        if self.fidx >= 14:
            self.spawn_enemy()
            self.remove()

    def spawn_enemy(self):
        tmp = self.enemy_class(self.pos, self.add_damage, self.add_hp)
        gfw.world.add(gfw.layer.any, tmp)

    def remove(self):
        gfw.world.remove(self)

    def get_ground(self):
        x, y = self.pos
        return x - 10 * gobj.PIXEL_SCOPE, y - 24 * gobj.PIXEL_SCOPE, x + 5 * gobj.PIXEL_SCOPE, y - 24 * gobj.PIXEL_SCOPE

class SpawnerGenerator:
    def spawn_knh_random(self, add_damage = 0, add_hp = 0):
        pos = get_canvas_width() - random.randint(50, 100), random.randint(80, 400)
        tmp = EnemySpawner(pos, enemy.Knh, add_damage ,add_hp)
        gfw.world.add(gfw.layer.any, tmp)

    def spawn_krk_random(self, add_damage = 0, add_hp = 0):
        pos = get_canvas_width() - random.randint(50, 100), random.randint(80, 400)
        tmp = EnemySpawner(pos, enemy.Krk, add_damage ,add_hp)
        gfw.world.add(gfw.layer.any, tmp)

    def spawn_nkm_random(self, add_damage = 0, add_hp = 0):
        pos = get_canvas_width() - random.randint(50, 100), random.randint(80, 400)
        tmp = EnemySpawner(pos, enemy.Nkm, add_damage ,add_hp)
        gfw.world.add(gfw.layer.any, tmp)