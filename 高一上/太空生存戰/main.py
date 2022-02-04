from ctypes.wintypes import HICON
import pygame

FPS = 60 # 一秒跑60次
WIDTH = 500 # 寬
HEIGHT = 600 # 高

WHITE = (255,255,255) # 白色
GREEN = (0,255,0) # 綠色

# 遊戲初始化 and 創建視窗
pygame.init() # 遊戲初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 設定長寬
clock = pygame.time.Clock() # 定義電腦一秒跑幾次
pygame.display.set_caption("太空生存戰") # 更改遊戲標題
running = True # 執行遊戲迴圈

# sprite
class Player(pygame.sprite.Sprite): # 創建類別 可以繼承內建sprite類別(pygame.sprite.Sprite)
    def __init__(self): # 是__init__ 不是_init_
        pygame.sprite.Sprite.__init__(self) # 內建的sprite的初始函式
        # image是展現圖片
        self.image = pygame.Surface((50, 40)) # 暫時的圖片
        self.image.fill(GREEN)
        # rect是定位圖片
        self.rect = self.image.get_rect() # 圖片框起來

        # 座標
        self.rect.center = (WIDTH/2, HEIGHT/2) # 中心點
    
    def update(self): # 讓player移動
        self.rect.x += 2 # 往右
        #if self.rect

#可以顯示出來
all_sprites = pygame.sprite.Group() # 創建sprite的群組
player = Player() # 創建player
all_sprites.add(player) # player加入sprite群組

# 遊戲迴圈
while running:
    clock.tick(FPS) #一秒最多執行FPS次
    # 取得輸入
    for event in pygame.event.get(): 
        # pygame.event.get() 為發生的事件
        if event.type == pygame.QUIT: # 按退出鍵
            running = False # 退出遊戲迴圈
    
    # 更新遊戲
    all_sprites.update() # 執行all_sprites的updataa函式
    
    # 畫面顯示
    screen.fill(WHITE) # 填滿顏色(R,G,B)
    all_sprites.draw(screen) # 顯示sprite
    pygame.display.update() # 畫面更新
    