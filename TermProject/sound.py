import gfw
import gobj
from pico2d import *

def init():
    global bgm_ingame, bgm_title, se_player_fire, se_enemy_hit, se_enemy_die, se_player_reload
    global se_upgrade_success, se_upgrade_fail, se_upgrade_bonus, se_spawn_enemy, se_victory, se_defeat
    global se_enemy_attack, se_enemy_bullet_hit, se_generate_enemy
    bgm_ingame = load_music('res/Sounds/BGM1.mp3')
    bgm_ingame.set_volume(round(10 * gobj.BGM_VOLUME))
    bgm_title = load_music('res/Sounds/BGM2.mp3')
    bgm_title.set_volume(round(10 * gobj.BGM_VOLUME))
    se_player_fire = load_wav('res/Sounds/SE0.wav')
    se_player_fire.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_hit = load_wav('res/Sounds/SE1.wav')
    se_enemy_hit.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_die = load_wav('res/Sounds/SE2.wav')
    se_enemy_die.set_volume(round(3 * gobj.SE_VOLUME))
    se_player_reload = load_wav('res/Sounds/SE3.wav')
    se_player_reload.set_volume(round(3 * gobj.SE_VOLUME))
    se_upgrade_success = load_wav('res/Sounds/SE4.wav')
    se_upgrade_success.set_volume(round(3 * gobj.SE_VOLUME))
    se_upgrade_fail = load_wav('res/Sounds/SE5.wav')
    se_upgrade_fail.set_volume(round(2 * gobj.SE_VOLUME))
    se_upgrade_bonus = load_wav('res/Sounds/SE6.wav')
    se_upgrade_bonus.set_volume(round(3 * gobj.SE_VOLUME))
    se_spawn_enemy = load_wav('res/Sounds/SE10.wav')
    se_spawn_enemy.set_volume(round(2 * gobj.SE_VOLUME))
    se_victory = load_wav('res/Sounds/SE11.wav')
    se_victory.set_volume(round(3 * gobj.SE_VOLUME))
    se_defeat = load_wav('res/Sounds/SE12.wav')
    se_defeat.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_attack = load_wav('res/Sounds/SE8.wav')
    se_enemy_attack.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_bullet_hit = load_wav('res/Sounds/SE9.wav')
    se_enemy_bullet_hit.set_volume(round(1 * gobj.SE_VOLUME))
    se_generate_enemy = load_wav('res/Sounds/SE13.wav')
    se_generate_enemy.set_volume(round(8 * gobj.SE_VOLUME))

def delete_sounds():
    global bgm_ingame, bgm_title
    del bgm_ingame
    del bgm_title
    print("delete sounds")

def update_volume():
    global bgm_ingame, bgm_title, se_player_fire, se_enemy_hit, se_enemy_die, se_player_reload
    global se_upgrade_success, se_upgrade_fail, se_upgrade_bonus, se_spawn_enemy, se_victory, se_defeat
    global se_enemy_attack, se_enemy_bullet_hit, se_generate_enemy
    bgm_ingame.set_volume(round(10 * gobj.BGM_VOLUME))
    bgm_title.set_volume(round(10 * gobj.BGM_VOLUME))
    se_player_fire.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_hit.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_die.set_volume(round(3 * gobj.SE_VOLUME))
    se_player_reload.set_volume(round(3 * gobj.SE_VOLUME))
    se_upgrade_success.set_volume(round(3 * gobj.SE_VOLUME))
    se_upgrade_fail.set_volume(round(2 * gobj.SE_VOLUME))
    se_upgrade_bonus.set_volume(round(3 * gobj.SE_VOLUME))
    se_spawn_enemy.set_volume(round(2 * gobj.SE_VOLUME))
    se_victory.set_volume(round(3 * gobj.SE_VOLUME))
    se_defeat.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_attack.set_volume(round(3 * gobj.SE_VOLUME))
    se_enemy_bullet_hit.set_volume(round(1 * gobj.SE_VOLUME))
    se_generate_enemy.set_volume(round(8 * gobj.SE_VOLUME))