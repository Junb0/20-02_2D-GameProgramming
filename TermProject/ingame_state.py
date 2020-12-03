import gfw
from pico2d import *
import gobj
from background import Background
from player import Player
from ui import UIFrame
from wave import WaveControl
from wall import Wall
import bullet
import enemy

from upgrade import UpgradeControl

canvas_width = 1280
canvas_height = 720

def enter():
    gfw.world.init(['bg', 'any', 'ui'])
    Player.load_all_images()
    global player
    player = Player()
    gfw.world.add(gfw.layer.any, player)
    bg = Background('Sprites/Backgrounds/stage1/spr_bkg_stage1.png')
    gfw.world.add(gfw.layer.bg, bg)
    ui = UIFrame(player)
    gfw.world.add(gfw.layer.ui, ui)
    generate_wall()
    global WC
    WC = WaveControl(ui)
    global UC
    UC = UpgradeControl(ui, player)

def update():
    gfw.world.update()
    gfw.world.sort_by_ground(gfw.layer.any)

    for e in gfw.world.objects_at(gfw.layer.any):
        if isinstance(e, enemy.Enemy):
            check_enemy(e)
    check_life()
    WC.update()

def check_enemy(e):
    for b in gfw.world.objects_at(gfw.layer.any):
        if isinstance(b, bullet.LongBullet) or isinstance(b, bullet.ShortBullet):
            if b.action == 'move' and e.action != 'die' and gobj.collides_box(b, e):
                die = e.decrease_life(b.damage, b.stun)
                print(b.damage)
                b.action = 'hit'
                b.time = 0
                if die:
                    player.gold += e.drop_gold

def check_life():
    for b in gfw.world.objects_at(gfw.layer.any):
        if isinstance(b, bullet.RainBullet) or isinstance(b, bullet.NkmBullet) or isinstance(b,bullet.KnhBullet):
            if b.check_hit() and b.action == 'move':
                b.action = 'hit'
                b.time = 0
                player.life -= b.damage

def generate_wall():
    wall1 = Wall((10, 70))
    wall2 = Wall((10, 136))
    wall3 = Wall((10, 202))
    wall4 = Wall((10, 268))
    wall5 = Wall((10, 334))
    wall6 = Wall((10, 4))
    gfw.world.add(gfw.layer.any, wall1)
    gfw.world.add(gfw.layer.any, wall2)
    gfw.world.add(gfw.layer.any, wall3)
    gfw.world.add(gfw.layer.any, wall4)
    gfw.world.add(gfw.layer.any, wall5)
    gfw.world.add(gfw.layer.any, wall6)

def draw():
    gfw.world.draw()
    #gobj.draw_collision_box()

def handle_event(e):
    global player
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

    player.handle_event(e)
    UC.handle_event(e)

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
