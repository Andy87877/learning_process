import pygame # pygame核心
import random # 產生亂數
import os # 載入圖片

FPS = 60 # 一秒跑60次
WIDTH = 500 # 寬
HEIGHT = 600 # 高

WHITE = (255,255,255) # 白色
GREEN = (0,255,0) # 綠色
RED = (255,0,0) # 紅色
YELLOW = (255,255,0) # 黃色
BLACK = (0,0,0) # 黑色

# 遊戲初始化 and 創建視窗
pygame.init() # 遊戲初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 設定長寬
clock = pygame.time.Clock() # 定義電腦一秒跑幾次
pygame.display.set_caption("太空生存戰") # 更改遊戲標題
running = True # 執行遊戲迴圈

# 載入圖片 
# (os.path是python檔案現在的路徑 img是圖片的資料夾 convert是轉變成pygame容易讀的格式)
background_img = pygame.image.load(os.path.join("img", "background.png")).convert() # 載入圖片路徑 

# sprite
# 創建類別 可以繼承內建sprite類別(pygame.sprite.Sprite)
class Player(pygame.sprite.Sprite): # 飛船
    def __init__(self): # 是__init__ 不是_init_
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        # image是展現圖片
        self.image = pygame.Surface((50, 40)) # 暫時的圖片
        self.image.fill(GREEN)
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來

        # 起始位置
        self.rect.centerx = WIDTH / 2 # x座標
        self.rect.bottom = HEIGHT - 10 # y座標

        self.speedx = 8 # 移動速度
    
    def update(self): # 讓player移動
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
        bullet = Bullet(self.rect.centerx, self.rect.top) # 回傳飛船座標
        all_sprites.add(bullet) # 子彈加入群組
        bullets.add(bullet) # 判斷子彈是否碰撞的群組


class Rock(pygame.sprite.Sprite): # 隕石
    def __init__(self): # 是__init__ 不是_init_
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        # image是展現圖片
        self.image = pygame.Surface((30, 40)) # 暫時的圖片
        self.image.fill(RED)
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來

        # 起始位置(隨機生成)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) # x座標
        self.rect.y = random.randrange(-100, -40) # y座標

        # 隕石移動
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
    
    def update(self): # 讓隕石下墜
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right == 0: # 掉到邊邊就重來
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite): # 子彈
    def __init__(self, x, y): # 還要傳入飛船的x,y值
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        # image是展現圖片
        self.image = pygame.Surface((10, 20)) # 暫時的圖片
        self.image.fill(YELLOW)
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
        
# sprite可以顯示出來
all_sprites = pygame.sprite.Group() # 創建sprite的群組

rocks = pygame.sprite.Group() # 判斷隕石是否碰撞
bullets = pygame.sprite.Group() # 判斷子彈是否碰撞

player = Player() # 創建player
all_sprites.add(player) # player加入sprite群組
for i in range(8): # 8個隕石
    rock = Rock() # 創建隕石
    all_sprites.add(rock) # 隕石加入sprite群組
    rocks.add(rock) # 判斷隕石是否碰撞的群組

# 遊戲迴圈
while running:
    clock.tick(FPS) #一秒最多執行FPS次
    # 取得輸入
    for event in pygame.event.get(): 
        # pygame.event.get() 為發生的事件
        if event.type == pygame.QUIT: # 按退出鍵
            running = False # 退出遊戲迴圈
        elif event.type == pygame.KEYDOWN: # 按下鍵盤鍵
            if event.key == pygame.K_SPACE: # 按下空白鍵
                player.shoot() # 發射子彈

    # 更新遊戲
    all_sprites.update() # 執行all_sprites的update函式

    # 判斷子彈和隕石是否碰撞(sprites,sprites,前面是否刪除,後面是否刪除)
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True) 
    for hit in hits: # 補回隕石
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    # 判斷飛船和隕石是否碰撞
    hits = pygame.sprite.spritecollide(player, rocks, False) 
    if hits:
        running = False

    # 畫面顯示
    screen.fill(BLACK) # 填滿顏色(R,G,B)
    screen.blit(background_img, (0,0)) # 畫背景(圖,左上座標)
    all_sprites.draw(screen) # 顯示sprite
    pygame.display.update() # 畫面更新
    