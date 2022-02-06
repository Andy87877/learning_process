import pygame # pygame核心
import random # 產生亂數
import os # 檔案路徑

FPS = 60 # 一秒跑60次
WIDTH = 500 # 寬
HEIGHT = 600 # 高

WHITE = (255,255,255) # 白色
GREEN = (0,255,0) # 綠色
RED = (255,0,0) # 紅色
YELLOW = (255,255,0) # 黃色
BLACK = (0,0,0) # 黑色

# 紀錄用
score = 0 # 分數
playtime = 0 # 總時間
total_shoot = 0 # 總射擊
total_shoot_hit = 0 # 總射擊隕石

# 遊戲迴圈
show_init = True # 顯示遊戲初始畫面
end_init = False # 結束畫面
contorl_init = False # 控制畫面
running = True # 執行遊戲迴圈

# 遊戲初始化 and 創建視窗
pygame.init() # 遊戲初始化
pygame.mixer.init() # 音效初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 設定長寬
clock = pygame.time.Clock() # 定義電腦一秒跑幾次 
pygame.display.set_caption("太空生存戰") # 更改遊戲標題

# 載入圖片 
# (os.path是python檔案現在的路徑 img是圖片的資料夾 convert是轉變成pygame容易讀的格式)
background_img = pygame.image.load(os.path.join("img", "background.png")).convert() # 載入背景圖片路徑 
player_img = pygame.image.load(os.path.join("img", "player.png")).convert() # 載入飛船圖片路徑  
player_mini_img = pygame.transform.scale(player_img, (25, 19)) # 變成小飛船(檢視還有幾條命)
player_mini_img.set_colorkey(BLACK) # 把黑色變成透明
pygame.display.set_icon(player_mini_img) # 更改遊戲圖片
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert() # 載入子彈圖片路徑 
# rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert() # 載入隕石圖片路徑 
rock_imgs = [] # 隕石存在列表裡
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert()) # 載入隕石圖片路徑到list裡面

expl_anim = {} # 爆炸動畫圖片
expl_anim['lg'] = [] # 大爆炸
expl_anim['sm'] = [] # 小爆炸
expl_anim['player'] = [] # 飛船爆炸
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert() # 載入隕石爆炸圖片路徑到list裡面
    expl_img.set_colorkey(BLACK) # 把黑色變成透明
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75))) # 大爆炸字典 改大小
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30))) # 小爆炸字典 改大小

    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert() # 載入飛船爆炸圖片路徑到list裡面
    player_expl_img.set_colorkey(BLACK) # 把黑色變成透明
    expl_anim['player'].append(player_expl_img) # 飛船爆炸字典
power_imgs = {} # 道具
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert(); # 盾牌
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert(); # 槍


# 載入音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav")) # 載入射擊音效
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav")) # 載入槍音效
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav")) # 載入盾牌音效
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.wav")) # 載入飛船死亡音效
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav")) 
] # 隕石爆炸的音效存載列表裡
pygame.mixer.music.load(os.path.join("sound", "background.wav")) # 背景音樂
pygame.mixer.music.set_volume(0.4) # 調整背景音樂大小

font_name = os.path.join("font.ttf") # 引用字體
def draw_text(surf, text, size, x, y): # 把文字顯示在畫面上
    font = pygame.font.Font(font_name, size) # 創建文字物件
    text_surface = font.render(text, True, WHITE) # 渲染文字
    # 定位文字
    text_rect = text_surface.get_rect() 
    text_rect.centerx = x
    text_rect.top = y

    surf.blit(text_surface, text_rect) # 顯示出來

def new_rock(): # 生成隕石
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y): # 顯示血量
    if hp < 0: # 血量小於0
        hp = 0
    BAR_LENGTH = 100 #　血條寬度
    BAR_HIGHT = 10 #　血條高度
    fill = (hp/100)*BAR_LENGTH # 血量長度
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HIGHT) # 血條外框
    fill_rect = pygame.Rect(x, y, fill, BAR_HIGHT) # 血量長度
    pygame.draw.rect(surf, GREEN, fill_rect) # 顯示血量
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # 顯示外框

def draw_lives(surf, lives, img, x, y): # 顯示幾條命
    for i in range(lives): # 有幾條命
        img_rect = img.get_rect() # 圖片定位
        img_rect.x = x + 32*i # x定位於
        img_rect.y = y # y定位於
        surf.blit(img, img_rect) # 顯示出來

def draw_init(): # 初始畫面
    screen.blit(background_img, (0,0)) # 畫背景(圖,左上座標)
    # 顯示文字
    draw_text(screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, 'AD 或 ←→移動飛船 空白鍵發射子彈', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按C到控制選單', 22, WIDTH/2, HEIGHT/2+50)
    draw_text(screen, '按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update() # 畫面更新
    waiting = True # 等玩家按開始
    while waiting:
        clock.tick(FPS) # 一秒最多執行FPS次
        for event in pygame.event.get(): 
            # pygame.event.get() 為發生的事件
            if event.type == pygame.QUIT: # 按退出鍵
                pygame.quit() # 遊戲退出
                return True # 告訴電腦已退出
            elif event.type == pygame.KEYUP: # 按下鍵盤鍵
                if event.key == pygame.K_c:
                    contorl_init = True
                waiting = False # 遊戲開始
                return False # 告訴電腦未退出

def draw_end(): #顯示最後分數
    screen.blit(background_img, (0,0)) # 畫背景(圖,左上座標)
    draw_text(screen, '你的分數為'+str(score), 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '遊玩時間為'+str(playtime)+'秒', 22, WIDTH/2, HEIGHT/2+50)
    draw_text(screen, '射擊次數為'+str(total_shoot), 22, WIDTH/2, HEIGHT/2+100)
    draw_text(screen, '射擊到隕石的次數為'+str(total_shoot_hit), 22, WIDTH/2, HEIGHT/2+150)
    draw_text(screen, '按任意鍵回到首頁', 18, WIDTH/2, HEIGHT/2+200)
    pygame.display.update() # 畫面更新
    waiting = True # 等玩家按開始
    while waiting:
        clock.tick(FPS) # 一秒最多執行FPS次
        for event in pygame.event.get(): 
            # pygame.event.get() 為發生的事件
            if event.type == pygame.QUIT: # 按退出鍵
                pygame.quit() # 遊戲退出
                return True # 告訴電腦已退出
            elif event.type == pygame.KEYUP: # 按下鍵盤鍵
                waiting = False # 遊戲開始
                return False # 告訴電腦未退出

def draw_control():
    screen.blit(background_img, (0,0)) # 畫背景(圖,左上座標)
    draw_text(screen, '1321213'+str(score), 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵回到首頁', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update() # 畫面更新
    waiting = True # 等玩家按開始
    while waiting:
        clock.tick(FPS) # 一秒最多執行FPS次
        for event in pygame.event.get(): 
            # pygame.event.get() 為發生的事件
            if event.type == pygame.QUIT: # 按退出鍵
                pygame.quit() # 遊戲退出
                return True # 告訴電腦已退出
            elif event.type == pygame.KEYUP: # 按下鍵盤鍵
                waiting = False # 遊戲開始
                return False # 告訴電腦未退出

# sprite
# 創建類別 可以繼承內建sprite類別(pygame.sprite.Sprite)
class Player(pygame.sprite.Sprite): # 飛船
    def __init__(self): # 是__init__ 不是_init_
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        # image是展現圖片
        self.image = pygame.transform.scale(player_img, (50, 38)) # 圖片 (transform轉換大小)
        self.image.set_colorkey(BLACK) # 把黑色變成透明
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來
        # 碰撞判斷
        self.radius = 20 # 圓形半徑
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # 畫出圓形
  
        # 起始位置
        self.rect.centerx = WIDTH / 2 # x座標
        self.rect.bottom = HEIGHT - 10 # y座標

        self.speedx = 8 # 移動速度
        self.health = 100 # 血量
        self.lives = 3 # 生命
        self.hidden = False # 飛船是否隱藏
        self.hide_time = 0 # 隱藏時間
        self.gun = 1 # 子彈等級
        self.gun_time  = 0 # 吃到道具時間
    
    def update(self): # 讓player移動
        now = pygame.time.get_ticks() # 現在時間
        if self.gun > 1 and now - self.gun_time > 5000: # 如果道具的延遲時間已到
            self.gun -= 1 # 等級下降
            self.gun_time = now # 設回現在時間

        if self.hidden and now - self.hide_time > 1000: # 如果隱藏的延遲時間已到
            self.hidden = False # 解除隱藏
            self.rect.centerx = WIDTH / 2 # x座標
            self.rect.bottom = HEIGHT - 10 # y座標

        key_pressed = pygame.key.get_pressed() # 鍵盤有沒有被按
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]: # 鍵盤d鍵or右鍵被按
             self.rect.x += self.speedx # 往右
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]: # 鍵盤a鍵or左鍵被按
             self.rect.x -= self.speedx # 往左

        if self.rect.right > WIDTH: # 最右邊
            self.rect.right = WIDTH
        if self.rect.left < 0: # 最左邊
            self.rect.left = 0

    def shoot(self): # 發射子彈
        if not(self.hidden): # 如果不隱藏
            if self.gun == 1: # 沒有升級(1發)
                bullet = Bullet(self.rect.centerx, self.rect.top) # 回傳飛船座標
                all_sprites.add(bullet) # 子彈加入群組
                bullets.add(bullet) # 判斷子彈是否碰撞的群組
                shoot_sound.play() # 播出音效 
            elif self.gun >= 2: # 有升級(2發)
                bullet1 = Bullet(self.rect.left, self.rect.centery) # 回傳飛船座標
                bullet2 = Bullet(self.rect.right, self.rect.centery) # 回傳飛船座標
                all_sprites.add(bullet1) # 子彈加入群組
                all_sprites.add(bullet2) # 子彈加入群組
                bullets.add(bullet1) # 判斷子彈是否碰撞的群組
                bullets.add(bullet2) # 判斷子彈是否碰撞的群組
                shoot_sound.play() # 播出音效

    def hide(self): # 隱藏
        self.hidden = True # 已經隱藏
        self.hide_time = pygame.time.get_ticks() # 紀錄隱藏時間
        self.rect.center = (WIDTH/2, HEIGHT+500) # 移除遊戲畫面

    def gunup(self): # 道具 槍
        self.gun += 1 # 槍等級提升
        self.gun_time = pygame.time.get_ticks() # 紀錄升級時間

class Rock(pygame.sprite.Sprite ): # 隕石
    def __init__(self): # 是__init__ 不是_init_
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式  
        
        # image是展現圖片 
        self.image_ori = random.choice(rock_imgs) # 存沒有轉動的圖片 隨機選一張圖片
        self.image_ori.set_colorkey(BLACK) # 把黑色變成透明
        self.image = self.image_ori.copy() # 複製圖片
        
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來 
        # 碰撞判斷
        self.radius = int(self.rect.width * 0.85 / 2) # 圓形半徑
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) # 畫出圓形

        # 起始位置(隨機生成)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) # x座標
        self.rect.y = random.randrange(-180, -100) # y座標
        
        # 隕石移動
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

        #隕石旋轉
        self.total_degree = 0 # 總共角度
        self.rot_degree = random.randrange(-3, 3) # 旋轉度數
    
    def rotate(self): # 讓隕石旋轉
        self.total_degree += self.rot_degree # 轉動總角度 
        self.total_degree = self.total_degree % 360 # 0~359
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree) #旋轉圖片

        center = self.rect.center # 中心點
        self.rect = self.image.get_rect() # 重新定位中心點
        self.rect.center = center # 新的中心點

    def update(self): # 讓隕石下墜
        self.rotate() # 隕石旋轉
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right == 0: # 掉到邊邊就重來
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite): # 子彈
    def __init__(self, x, y): # 傳入飛船的x,y值
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        # image是展現圖片
        self.image = bullet_img # 圖片
        self.image.set_colorkey(BLACK) # 把黑色變成透明   
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來

        # 起始位置(要依飛船的位置)
        self.rect.centerx = x
        self.rect.bottom = y

        # 子彈移動速度
        self.speedy = -10
    
    def update(self): # 發射子彈
        self.rect.y += self.speedy
        if self.rect.bottom < 0: # 子彈飛到頂
            self.kill() # 移除子彈

class Explosion(pygame.sprite.Sprite): # 爆炸動畫
    def __init__(self, center, size): # 傳入隕石的信息
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        self.size = size # 爆炸規模
        # image是展現圖片
        self.image = expl_anim[self.size][0] # 圖片
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來

        self.rect.center = center # 起始位置
        self.frame = 0 # 更新到第幾張圖片
        self.last_update = pygame.time.get_ticks() # 最後一次更新圖片
        self.frame_rate = 50 # 過幾毫秒才會更新圖片
    
    def update(self): 
        now = pygame.time.get_ticks() # 現在的時間
        if now - self.last_update > self.frame_rate: # 可換下張圖片
            self.last_update = now # 更新圖片時間到現在
            self.frame += 1 # 換下張圖片
            if self.frame == len(expl_anim[self.size]): # 如果到最後一張
                self.kill() # 移除
            else:
                self.image = expl_anim[self.size][self.frame] # 更新
                center = self.rect.center # 中心點
                self.rect = self.image.get_rect() # 重新定位中心點
                self.rect.center = center # 新的中心點

class Power(pygame.sprite.Sprite): # 寶物
    def __init__(self, center): # 傳入隕石的信息
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        self.type = random.choice(['shield', 'gun']) # 代表的寶物
        # image是展現圖片
        self.image = power_imgs[self.type] # 圖片
        self.image.set_colorkey(BLACK) # 把黑色變成透明   
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來

        # 起始位置(要依隕石的位置)
        self.rect.center = center

        # 移動速度
        self.speedy = 3
    
    def update(self): 
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT: # 寶物到底
            self.kill() # 移除寶物

pygame.mixer.music.play(-1) # 播出背景音樂

while running:
    if show_init: # 遊戲初始畫面
        close = draw_init() # 畫初始畫面
        if close: # 玩家已離開
            break
        show_init = False # 開始遊戲
        
        # sprite可以顯示出來
        all_sprites = pygame.sprite.Group() # 創建sprite的群組

        rocks = pygame.sprite.Group() # 判斷隕石是否碰撞
        bullets = pygame.sprite.Group() # 判斷子彈是否碰撞
        powers = pygame.sprite.Group() # 判斷寶物是否碰撞

        player = Player() # 創建player
        all_sprites.add(player) # player加入sprite群組
        for i in range(30): # 30個隕石
            new_rock()
        score = 0 # 分數
        total_shoot = 0 # 總射擊
        total_shoot_hit = 0 # 設到隕石
        playtime = pygame.time.get_ticks() # 紀錄遊玩時間
        end_init = False

    if end_init: # 顯示分數
        close = draw_end() 
        if close: 
            break
        end_init = False 
        show_init = True

    if contorl_init: # 控制頁面
        close = draw_control() 
        if close: 
            break
        contorl_init = False 

    clock.tick(FPS) # 一秒最多執行FPS次
    # 取得輸入
    for event in pygame.event.get(): 
        # pygame.event.get() 為發生的事件
        if event.type == pygame.QUIT: # 按退出鍵
            running = False # 退出遊戲迴圈
        elif event.type == pygame.KEYDOWN: # 按下鍵盤鍵
            if event.key == pygame.K_SPACE: # 按下空白鍵
                player.shoot() # 發射子彈
                total_shoot += 1

    # 更新遊戲
    all_sprites.update() # 執行all_sprites的update函式

    # 判斷子彈和隕石是否碰撞(sprites,sprites,前面是否刪除,後面是否刪除)
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) 
    for hit in hits: # hits 是列表
        score += hit.radius # 加分數
        random.choice(expl_sounds).play() # 播出爆炸音效 
        expl = Explosion(hit.rect.center, 'lg') # 爆炸動畫
        all_sprites.add(expl) # expl加入sprite群組
        if random.random() > 0.99: # 掉寶機率
            pow = Power(hit.rect.center) # 掉寶
            all_sprites.add(pow) # pow加入sprite群組
            powers.add(pow) # 判斷寶物碰撞
        new_rock() # 補回隕石
        total_shoot_hit += 1

    # 判斷飛船和隕石是否碰撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle) # 判斷方式是圓形 
    for hit in hits: # 如果碰到
        player.health -= hit.radius # 扣血
        random.choice(expl_sounds).play()
        new_rock() # 補回隕石
        expl = Explosion(hit.rect.center, 'sm') # 隕石爆炸動畫
        all_sprites.add(expl) # expl加入sprite群組

        if player.health <= 0: # 血量歸零
            death_expl = Explosion(player.rect.center, 'player') # 死亡爆炸動畫
            all_sprites.add(death_expl) # die加入sprite群組
            die_sound.play() # 播放死亡音效
            player.lives -= 1 # 生命值-1
            player.health = 100 # 血量回滿 
            player.hide() # 飛船隱藏

    # 判斷飛船和寶物是否碰撞
    hits = pygame.sprite.spritecollide(player, powers, True) # 判斷碰撞
    for hit in hits: # 如果碰到
        if hit.type == 'shield': # 盾牌
            player.health += 20 # 加血
            if player.health > 100: # 滿血
                player.health = 100 # 就滿血
            shield_sound.play() # 播出音效
        elif hit.type == 'gun': # 槍
            player.gunup() # 吃到槍
            gun_sound.play() # 播出音效
            

    if player.lives == 0 and not(death_expl.alive()): # 生命值歸零 and 執行完die
        playtime = int((pygame.time.get_ticks() - playtime) / 1000)
        end_init = True
    # 畫面顯示
    screen.fill(BLACK) # 填滿顏色(R,G,B)
    screen.blit(background_img, (0,0)) # 畫背景(圖,左上座標)
    all_sprites.draw(screen) # 顯示sprite
    draw_text(screen, str(score), 18, WIDTH/2, 10) # 顯示遊戲分數
    draw_health(screen, player.health, 5, 15) # 顯示血條
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15) # 顯示生命值
    pygame.display.update() # 畫面更新
    
# 分數 遊玩時間 發射的子彈數 射到隕石次數 吃到盾牌 吃到槍 當場隕石 飛船速度 隕石速度