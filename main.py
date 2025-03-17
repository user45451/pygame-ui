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

# 主循环
running = True
root_ui = ui(0, 0, width, height)



# 修改主循环以使用窗口类
# 生成2个根节点窗口
for i in range(2):
    outer_window = Window(100 + i * 400, 100, 300, 200)
    # 嵌套生成4层窗口
    parent_window = outer_window
    for level in range(3):
        new_children = []
        for j in range(3):
            for k in range(3):
                inner_window = Window(100 + j * 50, 100 + k * 50, 50, 50)
                parent_window.add_child(inner_window)
                new_children.append(inner_window)
        parent_window = new_children[0] if new_children else parent_window
    root_ui.add_child(outer_window)


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