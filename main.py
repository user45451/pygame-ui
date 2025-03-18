import pygame
from ui import window
from ui.window import *
from ui.Text import TextBox

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