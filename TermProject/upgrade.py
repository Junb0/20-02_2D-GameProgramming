from pico2d import *
from ext_pico2d import *
import gfw
import gobj
import tower
import sound

class UpgradeControl:
    table_ad = [(10, 10), (12, 51), (15, 98), (20, 150), (26, 99999)]
    table_ammo = [(5, 9), (7, 34), (10, 81), (14, 131), (20, 99999)]
    table_tower = [(0, 30), (0, 50), (0, 70), (0, 100), (0, 99999)]
    table_repair = [(30, 10), (30, 20), (30, 30), (30, 50), (0, 99999)]
    def __init__(self, ui, player):
        self.ui = ui
        self.player = player
        self.ad_up_count = 0
        self.ammo_up_count = 0
        self.tower_count = 0
        self.repair_count = 0
        self.player.weapon.damage = self.table_ad[self.ad_up_count][0]
        self.player.weapon.max_ammo = self.table_ammo[self.ammo_up_count][0]
        self.ui.ad_ui = '(+%d) %dG' % (self.ad_up_count, self.table_ad[self.ad_up_count][1])
        self.ui.magazine_ui = '(+%d) %dG' % (self.ammo_up_count, self.table_ammo[self.ammo_up_count][1])
        self.ui.tower_ui = '(+%d) %dG' % (self.tower_count, self.table_tower[self.tower_count][1])
        self.ui.repair_ui = '%dG' % self.table_repair[self.repair_count][1]
        self.tower_attack_speed = 4
    def handle_event(self, e):
        if e.type == SDL_KEYDOWN and e.key == SDLK_1:
            self.upgrade_ad()
        if e.type == SDL_KEYDOWN and e.key == SDLK_2:
            self.upgrade_ammo()
        if e.type == SDL_KEYDOWN and e.key == SDLK_3:
            self.upgrade_tower()
        if e.type == SDL_KEYDOWN and e.key == SDLK_4:
            self.repair()

    def upgrade_ad(self):
        if self.ad_up_count >= len(self.table_ad) - 1:
            sound.se_upgrade_fail.play()
            if not 'Already Upgraded to Maximum.' in self.ui.messages1:
                self.ui.messages1.append('Already Upgraded to Maximum.')
        elif self.player.gold >= self.table_ad[self.ad_up_count][1]:
            self.player.gold -= self.table_ad[self.ad_up_count][1]
            gobj.CONSUMED_GOLD += self.table_ad[self.ad_up_count][1]
            self.ad_up_count += 1
            self.player.weapon.damage = self.table_ad[self.ad_up_count][0]
            self.player.weapon.stun += 0.03
            if self.ad_up_count == 2:
                self.player.weapon.stun += 0.1
                self.ui.messages2.append('Enemy Stun Time Increased!')
                sound.se_upgrade_bonus.play()
            if self.ad_up_count == 4:
                self.player.weapon.fire_delay *= 0.8
                self.ui.messages2.append('Attack Speed Increased!')
                sound.se_upgrade_bonus.play()
            self.ui.ad_ui = '(+%d) %dG' % (self.ad_up_count, self.table_ad[self.ad_up_count][1])
            if self.ad_up_count >= len(self.table_ad) - 1:
                self.ui.ad_ui = '(+%d) MAX' % self.ad_up_count
            self.ui.messages1.append('Upgrade Complete')
            sound.se_upgrade_success.play()
        else:
            sound.se_upgrade_fail.play()
            if not 'Not Enough Gold' in self.ui.messages1:
                self.ui.messages1.append('Not Enough Gold')

    def upgrade_ammo(self):
        if self.ammo_up_count >= len(self.table_ammo) - 1:
            sound.se_upgrade_fail.play()
            if not 'Already Upgraded to Maximum.' in self.ui.messages1:
                self.ui.messages1.append('Already Upgraded to Maximum.')
        elif self.player.gold >= self.table_ammo[self.ammo_up_count][1]:
            self.player.gold -= self.table_ammo[self.ammo_up_count][1]
            gobj.CONSUMED_GOLD += self.table_ammo[self.ammo_up_count][1]
            self.ammo_up_count += 1
            self.player.weapon.max_ammo = self.table_ammo[self.ammo_up_count][0]
            self.player.weapon.fire_delay *= 0.95
            if self.ammo_up_count == 2:
                self.player.weapon.fire_delay *= 0.8
                self.ui.messages2.append('Attack Speed Increased!')
                sound.se_upgrade_bonus.play()
            if self.ammo_up_count == 4:
                self.player.body.speed += 100
                self.ui.messages2.append('Move Speed Increased!')
                sound.se_upgrade_bonus.play()
            self.ui.magazine_ui = '(+%d) %dG' % (self.ammo_up_count, self.table_ammo[self.ammo_up_count][1])
            if self.ammo_up_count >= len(self.table_ammo) - 1:
                self.ui.magazine_ui = '(+%d) MAX' % self.ammo_up_count
            self.ui.messages1.append('Upgrade Complete')
            sound.se_upgrade_success.play()
        else:
            sound.se_upgrade_fail.play()
            if not 'Not Enough Gold' in self.ui.messages1:
                self.ui.messages1.append('Not Enough Gold')

    def upgrade_tower(self):
        if self.tower_count >= len(self.table_tower) - 1:
            sound.se_upgrade_fail.play()
            if not 'Already Upgraded to Maximum.' in self.ui.messages1:
                self.ui.messages1.append('Already Upgraded to Maximum.')
        elif self.player.gold >= self.table_tower[self.tower_count][1]:
            self.player.gold -= self.table_tower[self.tower_count][1]
            gobj.CONSUMED_GOLD += self.table_tower[self.tower_count][1]
            self.tower_count += 1
            if self.tower_count == 1:
                tmp = tower.Tower((200, 110), self.tower_attack_speed)
                gfw.world.add(gfw.layer.any, tmp)
            if self.tower_count == 2:
                tmp = tower.Tower((200, 220), self.tower_attack_speed)
                gfw.world.add(gfw.layer.any, tmp)
                for t in gfw.world.objects_at(gfw.layer.any):
                    if isinstance(t, tower.Tower):
                        t.attack_delay = 3
                self.tower_attack_speed = 3
                self.ui.messages2.append("Tower Attack Speed Increased!")
                sound.se_upgrade_bonus.play()
            if self.tower_count == 3:
                tmp = tower.Tower((200, 330), self.tower_attack_speed)
                gfw.world.add(gfw.layer.any, tmp)
            if self.tower_count == 4:
                for t in gfw.world.objects_at(gfw.layer.any):
                    if isinstance(t, tower.Tower):
                        t.damage += 20
                self.ui.messages2.append("Tower Attack Damage Increased!")
                sound.se_upgrade_bonus.play()
            self.ui.tower_ui = '(+%d) %dG' % (self.tower_count, self.table_tower[self.tower_count][1])
            if self.tower_count >= len(self.table_tower) - 1:
                self.ui.tower_ui = '(+%d) MAX' % self.tower_count
            self.ui.messages1.append('Upgrade Complete')
            sound.se_upgrade_success.play()
        else:
            sound.se_upgrade_fail.play()
            if not 'Not Enough Gold' in self.ui.messages1:
                self.ui.messages1.append('Not Enough Gold')

    def repair(self):
        if self.repair_count >= len(self.table_repair) - 1:
            sound.se_upgrade_fail.play()
            if not 'Already Upgraded to Maximum.' in self.ui.messages1:
                self.ui.messages1.append('Already Upgraded to Maximum.')
        elif self.player.life >= 100:
            sound.se_upgrade_fail.play()
            if not 'Already Full HP' in self.ui.messages1:
                self.ui.messages1.append('Already Full HP')
        elif self.player.gold >= self.table_repair[self.repair_count][1]:
            self.player.gold -= self.table_repair[self.repair_count][1]
            gobj.CONSUMED_GOLD += self.table_repair[self.repair_count][1]
            self.repair_count += 1
            self.player.life = clamp(0, self.player.life + self.table_repair[self.repair_count][0], 100)
            self.ui.messages1.append('Repair Complete')
            sound.se_upgrade_success.play()
            self.ui.repair_ui = '%dG' % self.table_repair[self.repair_count][1]
            if self.repair_count >= len(self.table_repair) - 1:
                self.ui.repair_ui = 'MAX'
        else:
            sound.se_upgrade_fail.play()
            if not 'Not Enough Gold' in self.ui.messages1:
                self.ui.messages1.append('Not Enough Gold')