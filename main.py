import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Cấu hình màn hình Mobile
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blox Fruits 2D - Fixed Inventory Bug")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
LIGHT_GREEN = (50, 205, 50)
BROWN = (101, 67, 33)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
PURPLE = (138, 43, 226)
YELLOW = (255, 215, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
ORANGE = (255, 140, 0)
PINK = (255, 105, 180)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
SNOW_WHITE = (240, 248, 255)
SAND = (238, 214, 175)
LAVA = (178, 34, 34)

ISLANDS = {
    1: {"name": "Đảo Khởi Đầu", "bg": (112, 197, 206), "ground": GREEN, "mult": 1.0, "req_lvl": 1},
    2: {"name": "Đảo Hải Tặc", "bg": (210, 105, 30), "ground": BROWN, "mult": 1.8, "req_lvl": 10},
    3: {"name": "Đảo Băng Tuyết", "bg": (175, 215, 230), "ground": SNOW_WHITE, "mult": 2.8, "req_lvl": 25},
    4: {"name": "Đảo Sa Mạc", "bg": (255, 222, 173), "ground": SAND, "mult": 4.2, "req_lvl": 50},
    5: {"name": "Đảo Mộc Độc", "bg": (60, 179, 113), "ground": DARK_GRAY, "mult": 6.5, "req_lvl": 80},
    6: {"name": "Đảo Sấm Sét", "bg": (72, 61, 139), "ground": YELLOW, "mult": 10.0, "req_lvl": 120},
    7: {"name": "Đảo Ma Quái", "bg": (47, 79, 79), "ground": PURPLE, "mult": 15.0, "req_lvl": 170},
    8: {"name": "Đảo Hỏa Sơn", "bg": (139, 0, 0), "ground": LAVA, "mult": 22.0, "req_lvl": 230},
    9: {"name": "Đảo Hải Quân", "bg": (25, 25, 112), "ground": WHITE, "mult": 32.0, "req_lvl": 300},
    10: {"name": "Đảo Raid / Ma Vương", "bg": (70, 0, 90), "ground": MAGENTA, "mult": 50.0, "req_lvl": 400}
}

SWORD_SHOP = [
    {"name": "Katana", "price": 1000, "dmg_bonus": 15},
    {"name": "Tam Kiếm", "price": 5000, "dmg_bonus": 35},
    {"name": "Hắc Kiếm Yoru", "price": 20000, "dmg_bonus": 80}
]

GUN_SHOP = [
    {"name": "Súng Cỏn", "price": 800, "dmg_bonus": 10},
    {"name": "Súng Trường", "price": 4000, "dmg_bonus": 25},
    {"name": "Súng Bazooka", "price": 15000, "dmg_bonus": 60}
]

FRUIT_COLORS = {
    "Trái Lửa": (255, 69, 0),
    "Trái Nước": (0, 191, 255),
    "Trái Gió": (0, 255, 255),
    "Trái Đất": (139, 69, 19),
    "Trái Độc": (148, 0, 211),
    "Trái Sấm Sét": (255, 255, 0),
    "Trái Hố Đen": (75, 0, 130)
}

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 12, bold=True)
font_large = pygame.font.SysFont("Arial", 18, bold=True)


class VirtualButton:
    def __init__(self, x, y, w, h, text, color=GRAY):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.is_pressed = False

    def draw(self, surface):
        current_color = (200, 200, 200) if self.is_pressed else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=6)
        
        txt_surface = font.render(self.text, True, WHITE)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed:
                self.is_pressed = False
        return False


# Nút điều khiển
btn_left = VirtualButton(20, 520, 60, 60, "Trái")
btn_right = VirtualButton(85, 520, 60, 60, "Phải")

btn_jump = VirtualButton(1200, 520, 65, 60, "Nhảy")
btn_attack = VirtualButton(1130, 520, 65, 60, "Đánh")

btn_skill1 = VirtualButton(1060, 520, 55, 60, "Sk 1", DARK_GRAY)
btn_skill2 = VirtualButton(1000, 520, 55, 60, "Sk 2", MAGENTA)
btn_skill3 = VirtualButton(940, 520, 55, 60, "Sk 3", BLUE)
btn_skill4 = VirtualButton(880, 520, 55, 60, "Sk 4", ORANGE)
btn_skill5 = VirtualButton(820, 520, 55, 60, "Sk 5", RED)
btn_skill6 = VirtualButton(760, 520, 55, 60, "Sk 6", PURPLE)

btn_inv = VirtualButton(1160, 15, 95, 38, "Kho Đồ", DARK_GRAY)
btn_awake = VirtualButton(1055, 15, 95, 38, "Thức Tỉnh", PURPLE)
btn_stats = VirtualButton(950, 15, 95, 38, "Cộng Điểm", DARK_GRAY)
btn_quest = VirtualButton(845, 15, 95, 38, "Nhiệm Vụ", DARK_GRAY)

btn_npc_interact = VirtualButton(0, 0, 100, 40, "Tương Tác", LIGHT_GREEN)


class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 380, 40, 60)
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.jump_power = -12
        self.grounded = False
        
        self.stat_points = 5
        self.stat_str = 0   
        self.stat_def = 0   
        self.stat_fruit = 0 

        self.max_hp = 100
        self.hp = 100
        self.invulnerable_timer = 0
        
        self.level = 1
        self.exp = 0
        self.max_exp = 100
        self.gold = 5000
        self.fragments = 4000000

        self.weapon = "Kiếm Gỗ"
        self.weapon_bonus_dmg = 0
        self.weapon_mastery = 0
        
        self.equipped_fruit = None
        self.fruit_level = 1 
        
        self.hotbar = ["Kiếm Gỗ", None, None, None, None]
        self.stored_fruits = ["Trái Lửa", "Trái Nước"]

        self.facing = "right"
        self.quest_active = False
        self.quest_target = 3
        self.quest_progress = 0
        self.quest_island_id = 1

    def move(self):
        self.vy += 0.5
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.bottom >= 450:
            self.rect.bottom = 450
            self.vy = 0
            self.grounded = True

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def take_damage(self, amount):
        if self.invulnerable_timer == 0:
            self.hp -= amount
            if self.hp < 0: self.hp = 0
            self.invulnerable_timer = 30

    def reset_stats(self):
        total_used = self.stat_str + self.stat_def + self.stat_fruit
        self.stat_points += total_used
        self.stat_str = 0
        self.stat_def = 0
        self.stat_fruit = 0
        self.max_hp = 100
        self.hp = self.max_hp

    def draw(self, surface):
        if self.invulnerable_timer % 4 < 2:
            pygame.draw.rect(surface, YELLOW, self.rect, border_radius=5)
            eye_x = self.rect.x + 28 if self.facing == "right" else self.rect.x + 5
            pygame.draw.rect(surface, BLACK, (eye_x, self.rect.y + 12, 6, 6))

        pygame.draw.rect(surface, BLACK, (self.rect.x - 5, self.rect.y - 12, 50, 6))
        hp_ratio = self.hp / self.max_hp
        if hp_ratio > 0:
            pygame.draw.rect(surface, RED, (self.rect.x - 5, self.rect.y - 12, 50 * hp_ratio, 6))

    def gain_exp(self, amount, gold_amount, current_island_id):
        self.exp += amount
        self.gold += gold_amount
        
        if self.quest_active:
            self.quest_progress += 1
            if self.quest_progress >= self.quest_target:
                self.quest_active = False
                mult = ISLANDS[current_island_id]["mult"]
                self.gold += int(500 * mult)
                self.exp += int(250 * mult)
                self.quest_progress = 0

        if self.exp >= self.max_exp:
            self.level += 1
            self.exp -= self.max_exp
            self.max_exp = int(self.max_exp * 1.35)
            self.stat_points += 3 
            self.max_hp = 100 + (self.stat_def * 20)
            self.hp = self.max_hp


class Projectile:
    def __init__(self, x, y, direction, damage, color, size, is_fruit=False, is_aoe=False, is_skill6=False, speed=12):
        self.rect = pygame.Rect(x, y, size, size)
        self.vx = direction * speed
        self.damage = damage
        self.color = color
        self.is_fruit = is_fruit
        self.is_aoe = is_aoe
        self.is_skill6 = is_skill6

    def update(self):
        self.rect.x += self.vx

    def draw(self, surface):
        if self.is_skill6:
            center = self.rect.center
            radius = self.rect.width // 2
            pygame.draw.circle(surface, PURPLE, center, radius)
            pygame.draw.circle(surface, MAGENTA, center, radius - 8)
            pygame.draw.circle(surface, BLUE, (center[0] - 15, center[1]), radius // 2 + 5, 4)
            pygame.draw.circle(surface, RED, (center[0] + 15, center[1]), radius // 2 + 5, 4)
            pygame.draw.circle(surface, WHITE, center, 12)
        elif self.is_aoe:
            pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width)
            pygame.draw.circle(surface, WHITE, self.rect.center, self.rect.width // 2, 2)
        elif self.is_fruit:
            pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width // 2)
            pygame.draw.circle(surface, WHITE, (self.rect.centerx - 3, self.rect.centery - 3), 3)
        else:
            pygame.draw.ellipse(surface, self.color, self.rect)


class Enemy:
    def __init__(self, player_level, island_id):
        self.rect = pygame.Rect(random.randint(700, 1150), 390, 45, 60)
        self.island_id = island_id
        
        mult = ISLANDS[island_id]["mult"]
        self.max_hp = int((40 + player_level * 8) * mult)
        self.hp = self.max_hp
        self.speed = 1.5 + (island_id * 0.1)
        self.damage = int((8 + player_level * 2) * mult)
        
        self.exp_reward = int((30 + player_level * 5) * mult)
        self.gold_reward = int((40 + player_level * 6) * mult)
        self.f_reward = random.randint(500, 2000)
        self.stun_timer = 0  

    def update(self, player):
        if self.stun_timer > 0:
            self.stun_timer -= 1
            return

        if self.rect.x > player.rect.x + 40:
            self.rect.x -= self.speed
        elif self.rect.x < player.rect.x - 40:
            self.rect.x += self.speed

        if self.rect.colliderect(player.rect):
            player.take_damage(self.damage)

    def draw(self, surface):
        color = PURPLE if self.stun_timer > 0 else RED
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, BLACK, (self.rect.x, self.rect.y - 10, self.rect.width, 6))
        hp_width = (self.hp / self.max_hp) * self.rect.width
        if hp_width > 0:
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, hp_width, 6))


def main():
    player = Player()
    enemies = []
    projectiles = []

    running = True
    current_ui = None  
    message_text = ""
    message_timer = 0
    current_island_id = 1

    npc_quest_x = 180
    npc_reset_x = 300
    npc_sword_x = 450
    npc_gun_x = 620
    npc_gacha_x = 780
    npc_boat_x = 1100

    while running:
        clock.tick(60)
        island_info = ISLANDS[current_island_id]
        screen.fill(island_info["bg"])

        near_npc = None
        if abs(player.rect.x - npc_quest_x) < 70:
            near_npc = "quest"; btn_npc_interact.rect.x, btn_npc_interact.rect.y = npc_quest_x - 30, 320
        elif abs(player.rect.x - npc_reset_x) < 70:
            near_npc = "reset"; btn_npc_interact.rect.x, btn_npc_interact.rect.y = npc_reset_x - 30, 320
        elif abs(player.rect.x - npc_sword_x) < 70:
            near_npc = "sword"; btn_npc_interact.rect.x, btn_npc_interact.rect.y = npc_sword_x - 30, 320
        elif abs(player.rect.x - npc_gun_x) < 70:
            near_npc = "gun"; btn_npc_interact.rect.x, btn_npc_interact.rect.y = npc_gun_x - 30, 320
        elif abs(player.rect.x - npc_gacha_x) < 70:
            near_npc = "gacha"; btn_npc_interact.rect.x, btn_npc_interact.rect.y = npc_gacha_x - 30, 320
        elif abs(player.rect.x - npc_boat_x) < 70:
            near_npc = "boat"; btn_npc_interact.rect.x, btn_npc_interact.rect.y = npc_boat_x - 30, 320

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

            if btn_inv.check_event(event): current_ui = None if current_ui == 'inventory' else 'inventory'
            if btn_awake.check_event(event): current_ui = None if current_ui == 'awakening' else 'awakening'
            if btn_stats.check_event(event): current_ui = None if current_ui == 'stats' else 'stats'
            if btn_quest.check_event(event): current_ui = None if current_ui == 'quest' else 'quest'

            if not current_ui:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Bấm chọn/Ăn item trên Hotbar
                    hotbar_start_x = 180
                    for idx in range(5):
                        slot_rect = pygame.Rect(hotbar_start_x + idx * 62, 520, 58, 58)
                        if slot_rect.collidepoint(event.pos):
                            item = player.hotbar[idx]
                            if item:
                                if item in FRUIT_COLORS:
                                    # ĂN TRÁI ÁC QUỶ: Đổi trang bị & XÓA KHỎI HOTBAR (FIX BUG)
                                    player.equipped_fruit = item
                                    player.hotbar[idx] = None  # Xóa sạch khỏi Hotbar!
                                    message_text = f"Đã ăn: {item}! (Trái biến mất khỏi ô)"
                                    message_timer = 90
                                else:
                                    player.weapon = item
                                    message_text = f"Trang bị: {item}"
                                    message_timer = 60

                    if btn_jump.rect.collidepoint(event.pos) and player.grounded:
                        player.vy = player.jump_power; player.grounded = False

                    if btn_attack.rect.collidepoint(event.pos):
                        player.weapon_mastery += 1
                        dir_val = 1 if player.facing == "right" else -1
                        base_dmg = 20 + player.weapon_bonus_dmg + (player.stat_str * 5)
                        
                        if any(g["name"] in player.weapon for g in GUN_SHOP):
                            gun_dmg = int(base_dmg * 0.8)
                            spawn_x = player.rect.right if dir_val == 1 else player.rect.left
                            projectiles.append(Projectile(spawn_x, player.rect.y + 25, dir_val, gun_dmg, YELLOW, 10))
                        else:
                            for enemy in enemies:
                                if abs(enemy.rect.x - player.rect.x) < 90 and abs(enemy.rect.y - player.rect.y) < 50:
                                    enemy.hp -= base_dmg; enemy.stun_timer = 25  

                    dir_val = 1 if player.facing == "right" else -1
                    color = FRUIT_COLORS.get(player.equipped_fruit, WHITE) if player.equipped_fruit else WHITE
                    spawn_x = player.rect.right if dir_val == 1 else player.rect.left

                    if btn_skill1.rect.collidepoint(event.pos):
                        if not player.equipped_fruit: message_text = "Chưa Ăn Trái Ác Quỷ!"; message_timer = 90
                        else:
                            dmg = 35 + (player.fruit_level * 10) + (player.stat_fruit * 8)
                            projectiles.append(Projectile(spawn_x, player.rect.y + 20, dir_val, dmg, color, 20, is_fruit=True))

                    if btn_skill2.rect.collidepoint(event.pos):
                        if not player.equipped_fruit: message_text = "Chưa Ăn Trái Ác Quỷ!"; message_timer = 90
                        elif player.fruit_level < 2: message_text = "Thức tỉnh Cấp 2 mới mở!"; message_timer = 90
                        else:
                            dmg = 60 + (player.fruit_level * 15) + (player.stat_fruit * 12)
                            projectiles.append(Projectile(spawn_x, player.rect.y + 10, dir_val, dmg, color, 45, is_fruit=True, is_aoe=True))

                    if btn_skill3.rect.collidepoint(event.pos):
                        if not player.equipped_fruit: message_text = "Chưa Ăn Trái Ác Quỷ!"; message_timer = 90
                        elif player.fruit_level < 3: message_text = "Thức tỉnh Cấp 3 mới mở!"; message_timer = 90
                        else:
                            dmg = 40 + (player.stat_fruit * 10)
                            for i in range(3):
                                projectiles.append(Projectile(spawn_x - (i * 25 * dir_val), player.rect.y + 15, dir_val, dmg, YELLOW, 22, is_fruit=True, speed=16))

                    if btn_skill4.rect.collidepoint(event.pos):
                        if not player.equipped_fruit: message_text = "Chưa Ăn Trái Ác Quỷ!"; message_timer = 90
                        elif player.fruit_level < 4: message_text = "Thức tỉnh Cấp 4 mới mở!"; message_timer = 90
                        else:
                            dmg = 120 + (player.stat_fruit * 18)
                            projectiles.append(Projectile(spawn_x, player.rect.y - 10, dir_val, dmg, CYAN, 65, is_fruit=True, is_aoe=True, speed=9))

                    if btn_skill5.rect.collidepoint(event.pos):
                        if not player.equipped_fruit: message_text = "Chưa Ăn Trái Ác Quỷ!"; message_timer = 90
                        elif player.fruit_level < 5: message_text = "Thức tỉnh Cấp 5 mới mở!"; message_timer = 90
                        else:
                            dmg = 250 + (player.stat_fruit * 30)
                            projectiles.append(Projectile(spawn_x, player.rect.y - 30, dir_val, dmg, RED, 90, is_fruit=True, is_aoe=True, speed=7))

                    if btn_skill6.rect.collidepoint(event.pos):
                        if not player.equipped_fruit:
                            message_text = "Chưa Ăn Trái Ác Quỷ!"; message_timer = 90
                        elif player.fruit_level < 6:
                            message_text = "Thức tỉnh Cấp 6 mới dùng được!"; message_timer = 90
                        else:
                            dmg = 30000 + (player.stat_fruit * 500)
                            projectiles.append(Projectile(spawn_x, player.rect.y - 40, dir_val, dmg, PURPLE, 110, is_fruit=True, is_aoe=True, is_skill6=True, speed=10))
                            message_text = "TỬ SẮC THỨC TỈNH (30.000 DAM)!"
                            message_timer = 60

                    if near_npc and btn_npc_interact.rect.collidepoint(event.pos):
                        if near_npc == "reset":
                            if player.fragments >= 50:
                                player.fragments -= 50; player.reset_stats()
                                message_text = "Đã Tẩy Điểm!"; message_timer = 90
                            else: message_text = "Cần 50 Điểm F để Tẩy!"; message_timer = 90
                        elif near_npc == "quest":
                            if not player.quest_active:
                                player.quest_active = True
                                player.quest_progress = 0
                                player.quest_island_id = current_island_id
                                message_text = f"Đã nhận Nhiệm Vụ Đảo {current_island_id}!"
                            else: message_text = f"Tiến độ Q: {player.quest_progress}/3"
                            message_timer = 90
                        elif near_npc == "sword": current_ui = 'shop_sword'
                        elif near_npc == "gun": current_ui = 'shop_gun'
                        elif near_npc == "gacha":
                            if player.gold >= 300:
                                new_fruit = random.choice(list(FRUIT_COLORS.keys()))
                                player.stored_fruits.append(new_fruit)
                                player.gold -= 300
                                message_text = f"Gacha ra {new_fruit} (Đã thêm vào Kho đồ)!"
                            else: message_text = "Cần 300 Gold!"
                            message_timer = 90
                        elif near_npc == "boat": current_ui = 'map_select'

            else:
                box_rect = pygame.Rect(380, 50, 520, 480)
                close_btn_rect = pygame.Rect(860, 60, 30, 30)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if close_btn_rect.collidepoint(event.pos) or not box_rect.collidepoint(event.pos):
                        if not (btn_inv.rect.collidepoint(event.pos) or btn_stats.rect.collidepoint(event.pos) or btn_quest.rect.collidepoint(event.pos) or btn_awake.rect.collidepoint(event.pos)):
                            current_ui = None

                    elif current_ui == 'shop_sword':
                        for idx, item in enumerate(SWORD_SHOP):
                            btn_r = pygame.Rect(410, 150 + idx * 90, 460, 70)
                            if btn_r.collidepoint(event.pos):
                                if player.gold >= item["price"]:
                                    player.gold -= item["price"]
                                    player.weapon = item["name"]
                                    player.weapon_bonus_dmg = item["dmg_bonus"]
                                    player.hotbar[0] = item["name"]
                                    message_text = f"Mua thành công {item['name']}!"
                                    message_timer = 90; current_ui = None
                                else: message_text = "Không đủ tiền!"; message_timer = 90

                    elif current_ui == 'shop_gun':
                        for idx, item in enumerate(GUN_SHOP):
                            btn_r = pygame.Rect(410, 150 + idx * 90, 460, 70)
                            if btn_r.collidepoint(event.pos):
                                if player.gold >= item["price"]:
                                    player.gold -= item["price"]
                                    player.weapon = item["name"]
                                    player.weapon_bonus_dmg = item["dmg_bonus"]
                                    player.hotbar[1] = item["name"]
                                    message_text = f"Mua thành công {item['name']}!"
                                    message_timer = 90; current_ui = None
                                else: message_text = "Không đủ tiền!"; message_timer = 90

                    elif current_ui == 'map_select':
                        for isl_id in range(1, 11):
                            row = (isl_id - 1) // 2
                            col = (isl_id - 1) % 2
                            btn_rect = pygame.Rect(400 + col * 240, 110 + row * 70, 220, 55)
                            if btn_rect.collidepoint(event.pos):
                                req_lvl = ISLANDS[isl_id]["req_lvl"]
                                if player.level >= req_lvl:
                                    current_island_id = isl_id
                                    player.rect.x = 100
                                    enemies.clear()
                                    message_text = f"Đến {ISLANDS[isl_id]['name']}!"
                                    message_timer = 90; current_ui = None
                                else: message_text = f"Cần Cấp {req_lvl}!"; message_timer = 90

                    elif current_ui == 'stats':
                        if player.stat_points > 0:
                            if pygame.Rect(780, 190, 40, 30).collidepoint(event.pos): 
                                player.stat_str += 1; player.stat_points -= 1
                            elif pygame.Rect(780, 235, 40, 30).collidepoint(event.pos): 
                                player.stat_def += 1; player.stat_points -= 1; player.max_hp += 20; player.hp += 20
                            elif pygame.Rect(780, 280, 40, 30).collidepoint(event.pos): 
                                player.stat_fruit += 1; player.stat_points -= 1

                    elif current_ui == 'inventory':
                        # BẤM LẤY TRÁI TỪ KHO RA HOTBAR
                        for idx, fruit_name in enumerate(list(player.stored_fruits)):
                            item_rect = pygame.Rect(410, 140 + idx * 65, 460, 50)
                            if item_rect.collidepoint(event.pos):
                                placed = False
                                for s_idx in range(2, 5): # Tìm ô Hotbar trống
                                    if player.hotbar[s_idx] is None:
                                        player.hotbar[s_idx] = fruit_name
                                        player.stored_fruits.remove(fruit_name)
                                        message_text = f"Đưa {fruit_name} ra Hotbar (Ô {s_idx+1})!"
                                        message_timer = 90
                                        placed = True
                                        break
                                if not placed:
                                    message_text = "Thanh Hotbar đã đầy!"
                                    message_timer = 90
                                break

                    elif current_ui == 'awakening':
                        btn_upgrade = pygame.Rect(530, 380, 220, 50)
                        if btn_upgrade.collidepoint(event.pos):
                            if not player.equipped_fruit:
                                message_text = "Chưa trang bị Trái Ác Quỷ!"
                            elif player.fruit_level >= 6:
                                message_text = "Đã đạt cấp Thức Tỉnh tối đa (Cấp 6)!"
                            else:
                                req_f = player.fruit_level * 500000
                                if player.fragments >= req_f:
                                    player.fragments -= req_f
                                    player.fruit_level += 1
                                    message_text = f"Thức tỉnh thành công Cấp {player.fruit_level}!"
                                else:
                                    message_text = f"Cần {req_f} F để Thức Tỉnh!"
                            message_timer = 90

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        player.vx = 0
        if btn_left.rect.collidepoint(mouse_pos) and mouse_pressed[0]: player.vx = -player.speed; player.facing = "left"
        elif btn_right.rect.collidepoint(mouse_pos) and mouse_pressed[0]: player.vx = player.speed; player.facing = "right"

        if not current_ui:
            player.move()
            if player.hp <= 0: player.hp = player.max_hp; player.rect.x = 100; message_text = "Hồi sinh!"; message_timer = 120

            if len(enemies) < 3: enemies.append(Enemy(player.level, current_island_id))

            for enemy in enemies[:]:
                enemy.update(player)
                if enemy.hp <= 0:
                    player.gain_exp(enemy.exp_reward, enemy.gold_reward, current_island_id)
                    player.fragments += enemy.f_reward
                    enemies.remove(enemy)

            for proj in projectiles[:]:
                proj.update()
                for enemy in enemies:
                    if proj.rect.colliderect(enemy.rect):
                        enemy.hp -= proj.damage
                        enemy.stun_timer = 15  
                        if proj in projectiles and not proj.is_aoe: projectiles.remove(proj)
                        break
                if proj.rect.x < 0 or proj.rect.x > SCREEN_WIDTH:
                    if proj in projectiles: projectiles.remove(proj)

        pygame.draw.rect(screen, BROWN, (0, 450, SCREEN_WIDTH, 150))
        pygame.draw.rect(screen, island_info["ground"], (0, 450, SCREEN_WIDTH, 20))

        pygame.draw.rect(screen, YELLOW, (npc_quest_x, 380, 40, 70))
        screen.blit(font.render("Nhiệm Vụ", True, WHITE), (npc_quest_x - 15, 355))

        pygame.draw.rect(screen, PINK, (npc_reset_x, 380, 40, 70))
        screen.blit(font.render("Tẩy Điểm", True, WHITE), (npc_reset_x - 15, 355))

        pygame.draw.rect(screen, ORANGE, (npc_sword_x, 380, 40, 70))
        screen.blit(font.render("NPC Kiếm", True, WHITE), (npc_sword_x - 15, 355))

        pygame.draw.rect(screen, BLUE, (npc_gun_x, 380, 40, 70))
        screen.blit(font.render("NPC Súng", True, WHITE), (npc_gun_x - 15, 355))

        pygame.draw.rect(screen, PURPLE, (npc_gacha_x, 380, 40, 70))
        screen.blit(font.render("Gacha", True, WHITE), (npc_gacha_x - 10, 355))

        pygame.draw.polygon(screen, BROWN, [(npc_boat_x - 20, 430), (npc_boat_x + 60, 430), (npc_boat_x + 40, 460), (npc_boat_x, 460)])
        pygame.draw.rect(screen, WHITE, (npc_boat_x + 15, 380, 10, 50))
        screen.blit(font.render("Thuyền", True, WHITE), (npc_boat_x, 355))

        if near_npc and not current_ui: btn_npc_interact.draw(screen)

        player.draw(screen)
        for enemy in enemies: enemy.draw(screen)
        for proj in projectiles: proj.draw(screen)

        ui_bg = pygame.Surface((460, 115))
        ui_bg.set_alpha(190); ui_bg.fill(BLACK)
        screen.blit(ui_bg, (10, 10))

        screen.blit(font.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE), (20, 15))
        pygame.draw.rect(screen, DARK_GRAY, (130, 16, 240, 18), border_radius=5)
        hp_w = (player.hp / player.max_hp) * 240
        if hp_w > 0: pygame.draw.rect(screen, RED, (130, 16, hp_w, 18), border_radius=5)

        screen.blit(font.render(f"Cấp: {player.level} | EXP: {player.exp}/{player.max_exp}", True, WHITE), (20, 40))
        screen.blit(font.render(f"Gold: {player.gold}$ | Điểm F: {player.fragments} | {island_info['name']}", True, YELLOW), (20, 62))
        screen.blit(font.render(f"Vũ khí: {player.weapon} | Trái: {player.equipped_fruit or 'Chưa ăn'} (Cấp {player.fruit_level})", True, WHITE), (20, 84))

        btn_left.draw(screen); btn_right.draw(screen)
        btn_jump.draw(screen); btn_attack.draw(screen)
        btn_skill1.draw(screen); btn_skill2.draw(screen); btn_skill3.draw(screen); btn_skill4.draw(screen); btn_skill5.draw(screen); btn_skill6.draw(screen)
        btn_inv.draw(screen); btn_awake.draw(screen); btn_stats.draw(screen); btn_quest.draw(screen)

        # Vẽ Hotbar
        hotbar_start_x = 180
        for idx in range(5):
            slot_rect = pygame.Rect(hotbar_start_x + idx * 62, 520, 58, 58)
            pygame.draw.rect(screen, DARK_GRAY, slot_rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, slot_rect, 2, border_radius=8)

            item = player.hotbar[idx]
            if item:
                if item in FRUIT_COLORS:
                    pygame.draw.rect(screen, FRUIT_COLORS[item], (slot_rect.x + 6, slot_rect.y + 6, 46, 46), border_radius=6)
                    txt = font.render(item.replace("Trái ", ""), True, WHITE)
                    screen.blit(txt, txt.get_rect(center=slot_rect.center))
                else:
                    is_active = (item == player.weapon)
                    color_w = YELLOW if is_active else WHITE
                    txt = font.render(item[:4], True, color_w)
                    screen.blit(txt, txt.get_rect(center=slot_rect.center))

        if current_ui:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200); overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            box = pygame.Rect(380, 50, 520, 480)
            pygame.draw.rect(screen, DARK_GRAY, box, border_radius=12)
            pygame.draw.rect(screen, WHITE, box, 2, border_radius=12)

            close_btn_rect = pygame.Rect(860, 60, 30, 30)
            pygame.draw.rect(screen, RED, close_btn_rect, border_radius=6)
            screen.blit(font.render("X", True, WHITE), (870, 64))

            if current_ui == 'shop_sword':
                screen.blit(font_large.render("CỬA HÀNG RÈN KIẾM", True, ORANGE), (520, 80))
                for idx, item in enumerate(SWORD_SHOP):
                    btn_r = pygame.Rect(410, 140 + idx * 100, 460, 80)
                    pygame.draw.rect(screen, BROWN, btn_r, border_radius=8)
                    screen.blit(font_large.render(item["name"], True, YELLOW), (btn_r.x + 15, btn_r.y + 15))
                    screen.blit(font_large.render(f"Giá: {item['price']}$", True, GREEN), (btn_r.x + 300, btn_r.y + 25))

            elif current_ui == 'shop_gun':
                screen.blit(font_large.render("CỬA HÀNG SÚNG HẢI QUÂN", True, BLUE), (490, 80))
                for idx, item in enumerate(GUN_SHOP):
                    btn_r = pygame.Rect(410, 140 + idx * 100, 460, 80)
                    pygame.draw.rect(screen, DARK_GRAY, btn_r, border_radius=8)
                    screen.blit(font_large.render(item["name"], True, YELLOW), (btn_r.x + 15, btn_r.y + 15))
                    screen.blit(font_large.render(f"Giá: {item['price']}$", True, GREEN), (btn_r.x + 300, btn_r.y + 25))

            elif current_ui == 'map_select':
                screen.blit(font_large.render("CHỌN ĐẢO DI CHUYỂN", True, YELLOW), (510, 70))
                for isl_id in range(1, 11):
                    row = (isl_id - 1) // 2
                    col = (isl_id - 1) % 2
                    btn_rect = pygame.Rect(400 + col * 240, 110 + row * 70, 220, 55)
                    unlocked = player.level >= ISLANDS[isl_id]["req_lvl"]
                    pygame.draw.rect(screen, GREEN if unlocked else GRAY, btn_rect, border_radius=8)
                    screen.blit(font.render(f"{isl_id}. {ISLANDS[isl_id]['name']}", True, WHITE), (btn_rect.x + 10, btn_rect.y + 8))

            elif current_ui == 'stats':
                screen.blit(font_large.render("CỘNG ĐIỂM CHỈ SỐ", True, YELLOW), (530, 85))
                screen.blit(font.render(f"Điểm chưa dùng: {player.stat_points}", True, GREEN), (430, 130))
                
                screen.blit(font.render(f"Sức Mạnh (Cận chiến/Kiếm): {player.stat_str}", True, WHITE), (430, 195))
                pygame.draw.rect(screen, LIGHT_GREEN, (780, 190, 40, 30), border_radius=5); screen.blit(font.render("+", True, WHITE), (795, 195))

                screen.blit(font.render(f"Phòng Thủ (Máu & Giáp): {player.stat_def}", True, WHITE), (430, 240))
                pygame.draw.rect(screen, LIGHT_GREEN, (780, 235, 40, 30), border_radius=5); screen.blit(font.render("+", True, WHITE), (795, 240))

                screen.blit(font.render(f"Trái Ác Quỷ (Sát thương skill): {player.stat_fruit}", True, WHITE), (430, 285))
                pygame.draw.rect(screen, LIGHT_GREEN, (780, 280, 40, 30), border_radius=5); screen.blit(font.render("+", True, WHITE), (795, 285))

            elif current_ui == 'inventory':
                screen.blit(font_large.render("KHO ĐỒ TRÁI ÁC QUỶ", True, YELLOW), (510, 80))
                if not player.stored_fruits:
                    screen.blit(font.render("Kho đồ trống! Hãy đi Gacha thêm trái.", True, WHITE), (480, 200))
                else:
                    for idx, fruit_name in enumerate(player.stored_fruits):
                        item_rect = pygame.Rect(410, 140 + idx * 65, 460, 50)
                        pygame.draw.rect(screen, DARK_GRAY, item_rect, border_radius=8)
                        pygame.draw.rect(screen, FRUIT_COLORS.get(fruit_name, WHITE), item_rect, 2, border_radius=8)
                        screen.blit(font_large.render(fruit_name, True, YELLOW), (item_rect.x + 15, item_rect.y + 12))
                        screen.blit(font.render("Bấm để chuyển ra Hotbar", True, GREEN), (item_rect.x + 260, item_rect.y + 16))

            elif current_ui == 'awakening':
                screen.blit(font_large.render("THỨC TỈNH TRÁI ÁC QUỶ", True, PURPLE), (500, 80))
                
                curr_f = player.equipped_fruit if player.equipped_fruit else "Chưa Ăn Trái Nào"
                screen.blit(font_large.render(f"Trái Đang Dùng: {curr_f}", True, YELLOW), (430, 140))
                screen.blit(font_large.render(f"Cấp Độ Thức Tỉnh: Cấp {player.fruit_level} / 6", True, GREEN), (430, 180))
                
                req_f = player.fruit_level * 500000 if player.fruit_level < 6 else 0
                screen.blit(font.render(f"Điểm F Hiện Có: {player.fragments}", True, WHITE), (430, 240))
                screen.blit(font.render(f"Cần Để Thức Tỉnh Cấp Tiếp Theo: {req_f} F", True, RED if player.fragments < req_f else GREEN), (430, 270))

                screen.blit(font.render("Tác Dụng: Tăng mạnh sát thương Skill & Mở khóa Skill mới!", True, CYAN), (430, 320))

                btn_upgrade = pygame.Rect(530, 380, 220, 50)
                pygame.draw.rect(screen, PURPLE if player.fruit_level < 6 else GRAY, btn_upgrade, border_radius=8)
                pygame.draw.rect(screen, WHITE, btn_upgrade, 2, border_radius=8)
                screen.blit(font_large.render("NÂNG CẤP THỨC TỈNH", True, WHITE), (btn_upgrade.x + 15, btn_upgrade.y + 12))

            elif current_ui == 'quest':
                screen.blit(font_large.render("NHIỆM VỤ HIỆN TẠI", True, YELLOW), (530, 100))
                if player.quest_active:
                    screen.blit(font.render(f"Tiến độ: {player.quest_progress} / {player.quest_target} Quái", True, GREEN), (430, 200))
                else: screen.blit(font.render("Chưa nhận nhiệm vụ nào!", True, WHITE), (430, 160))

        if message_timer > 0:
            msg_surface = font_large.render(message_text, True, YELLOW)
            screen.blit(msg_surface, (SCREEN_WIDTH // 2 - 200, 60))
            message_timer -= 1

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
