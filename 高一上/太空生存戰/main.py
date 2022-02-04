import pygame

FPS = 60 # 一秒跑60次
WHITE = (255,255,255) # 白色
WIDTH = 500 # 寬
HEIGHT = 600 # 高

# 遊戲初始化 and 創建視窗
pygame.init() # 遊戲初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 設定長寬
clock = pygame.time.Clock() # 定義電腦一秒跑幾次
running = True

# 遊戲迴圈
while running:
    clock.tick(FPS) #一秒最多執行FPS次
    # 取得輸入
    for event in pygame.event.get(): 
        # pygame.event.get() 為發生的事件
        if event.type == pygame.QUIT: # 按退出鍵
            running = False
    
    # 更新遊戲
    
    # 畫面顯示
    screen.fill(WHITE) # 填滿顏色(R,G,B)
    pygame.display.update() # 畫面更新