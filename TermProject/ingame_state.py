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
    gfw.world.init(['bg', 'bullet' , 'character', 'ui'])
    Player.load_all_images()
    global player
    player = Player()
    gfw.world.add(gfw.layer.character, player)
    bg = Background('Sprites/Backgrounds/stage1/spr_bkg_stage1.png')
    gfw.world.add(gfw.layer.bg, bg)
    # bullet 테스트
    nkmblt = bullet.NkmBullet((600, 300), 100)
    gfw.world.add(gfw.layer.bullet, nkmblt)
    knhblt = bullet.KnhBullet((600, 400), 100)
    gfw.world.add(gfw.layer.bullet, knhblt)
    # enemy 테스트
    knh = enemy.Knh((800, 400), 0, 0)
    gfw.world.add(gfw.layer.character, knh)

def update():
    gfw.world.update()

    for e in gfw.world.objects_at(gfw.layer.character):
        if isinstance(e, enemy.Enemy):
            check_enemy(e)

def check_enemy(e):
    for b in gfw.world.objects_at(gfw.layer.bullet):
        if b.action == 'move' and e.action != 'die' and isinstance(b, bullet.LongBullet):
            if gobj.collides_box(b, e):
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
