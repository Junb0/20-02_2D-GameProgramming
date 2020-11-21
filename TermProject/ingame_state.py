import gfw
from pico2d import *
import gobj
from background import Background
from player import Player
import bullet
import enemy

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

    # enemy 테스트
    knh = enemy.Knh((1000, 400), 0, 0)
    gfw.world.add(gfw.layer.any, knh)
    nkm = enemy.Nkm((1000, 200), 0, 0)
    gfw.world.add(gfw.layer.any, nkm)
    krk = enemy.Krk((600, 300), 0, 0)
    gfw.world.add(gfw.layer.any, krk)

def update():
    gfw.world.update()
    gfw.world.sort_by_ground(gfw.layer.any)

    for e in gfw.world.objects_at(gfw.layer.any):
        if isinstance(e, enemy.Enemy):
            check_enemy(e)

def check_enemy(e):
    for b in gfw.world.objects_at(gfw.layer.any):
        if isinstance(b, bullet.LongBullet):
            if b.action == 'move' and e.action != 'die' and gobj.collides_box(b, e):
                e.decrease_life(b.damage, b.stun)
                b.action = 'hit'

def draw():
    gfw.world.draw()
    gobj.draw_collision_box()

def handle_event(e):
    global player
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

    player.handle_event(e)

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
