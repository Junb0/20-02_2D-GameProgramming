from pico2d import *
from ext_pico2d import *
import gfw
import gobj
import json
from spawner import SpawnerGenerator
import enemy

class WaveControl:
    enemy_dict = {}
    wave_list = []
    ACTIONS = ['open','pre', 'spawning', 'end', 'game_over']
    SG = SpawnerGenerator()
    HP_MAG = [-0.2, 0, 0.12]

    def __init__(self, ui, difficulty):
        self.ui = ui
        self.wave = 0
        self.start_time = 0
        self.start_messages = []
        self.end_time = 0
        self.end_messages = []
        self.small_waves = []
        self.small_wave_time = 0
        self.action = 'open'
        self.is_end = False
        self.game_over_time = 3
        self.difficulty = difficulty

        with open(gobj.res('wave.json')) as f:
            data = json.load(f)
            self.enemy_dict = data['enemy_dict']
            self.wave_list = data['wave_list']

    def do_open(self):
        self.wave += 1
        self.start_time = self.wave_list[0]['start_delay']
        self.start_messages += self.wave_list[0]['start_messages']
        self.small_waves = self.wave_list[0]['small_waves']
        self.end_time = self.wave_list[0]['end_delay']
        self.end_messages += self.wave_list[0]['end_messages']
        self.wave_list.pop(0)
        self.action = 'pre'
        self.ui.wave_ui = self.wave
        pass

    def do_pre(self):
        if self.start_messages:
            self.ui.messages1 += self.start_messages
            del self.start_messages[:]
        self.start_time -= gfw.delta_time
        if self.start_time <= 0:
            self.action = 'spawning'

    def generate_enemies(self, enemies):
        for e in enemies:
            if self.enemy_dict[e][0] == 1:
                self.SG.spawn_knh_random(self.enemy_dict[e][1], self.enemy_dict[e][2] + 60 * self.HP_MAG[self.difficulty - 1])
            if self.enemy_dict[e][0] == 2:
                self.SG.spawn_krk_random(self.enemy_dict[e][1], self.enemy_dict[e][2] + 140 * self.HP_MAG[self.difficulty - 1])
            if self.enemy_dict[e][0] == 3:
                self.SG.spawn_nkm_random(self.enemy_dict[e][1], self.enemy_dict[e][2] + 90 * self.HP_MAG[self.difficulty - 1])

    def do_spawning(self):
        if self.small_wave_time <= 0:
            self.generate_enemies(self.small_waves[0]['enemies'])
            self.small_wave_time = self.small_waves[0]['delay']
            self.small_waves.pop(0)
        self.small_wave_time -= gfw.delta_time
        if self.small_wave_time <= 0 and not self.small_waves:
            self.action = 'end'

    def do_end(self):
        if self.end_messages:
            self.ui.messages1 += self.end_messages
            del self.end_messages[:]
        self.end_time -= gfw.delta_time
        if self.end_time <= 0:
            if self.wave_list:
                self.action = 'open'
            else:
                self.action = 'game_over'
                self.ui.messages2.append('All Waves Complete!')

    def do_game_over(self):
        cnt = 0
        for e in gfw.world.objects_at(gfw.layer.any):
            if isinstance(e, enemy.Enemy):
                cnt += 1
        if cnt == 0:
            if self.game_over_time <= 0:
                self.is_end = True
                gobj.IS_VICTORY = True
            else:
                self.game_over_time -= gfw.delta_time

    def update(self):
        if self.action == 'open':
            self.do_open()
        if self.action == 'pre':
            self.do_pre()
        if self.action == 'spawning':
            self.do_spawning()
        if self.action == 'end':
            self.do_end()
        if self.action == 'game_over':
            self.do_game_over()

