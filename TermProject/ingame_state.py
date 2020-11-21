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


def draw():
    gfw.world.draw()
    # gobj.draw_collision_box()

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
