import pygame
from ui.window import *

# 初始化pygame
pygame.init()

# 设置窗口大小
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('按钮UI示例')

# 定义颜色
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# 定义按钮点击事件函数
def button1_action():
    print('按钮1被点击')

def button2_action():
    print('按钮2被点击')


# 主循环
running = True
root_ui = ui(0, 0, width, height)



# 修改主循环以使用窗口类
outer_window = Window(100, 100, 300, 200)
# 每个窗口内部生成窗口阵列
def generate(root_window, level):
    for j in range(3):
        for k in range(3):
            inner_window = Window(100 + j * 50, 100 + k * 50, 50, 50)
            if level - 1 > 0:
                generate(inner_window, level - 1)
            root_window.add_child(inner_window)
root_ui.add_child(outer_window)

generate(outer_window, 2)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        root_ui.handle_event(event)
    screen.fill(WHITE)
    root_ui.draw(screen)
    pygame.display.flip()
# 退出pygame
pygame.quit()