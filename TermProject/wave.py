from pico2d import *
from ext_pico2d import *
import gfw
import gobj
import json
from spawner import SpawnerGenerator

class WaveControl:
    enemy_dict = {}
    wave_list = []
    def __init__(self, ui):
        self.ui = ui
        self.wave = 1
