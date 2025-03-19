import pygame
from ui.ui import ui
from ui.Window import Window
from ui.TextBox import TextBox

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


# 主循环
running = True
root_ui = ui(0, 0, width, height)
text_box = TextBox(0, 0, 100, 50, '你好!')
text_box1 = TextBox(0, 0, 100, 50, '你好!')


# 修改主循环以使用窗口类
window = Window(100, 100, 300, 200)
window.add_child(text_box)

window1 = Window(100, 300, 300, 200)
window1.add_child(text_box1)

root_ui.add_child(window)
root_ui.add_child(window1)


# 修改主循环以使用窗口类
outer_window = Window(400, 100, 300, 200)
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