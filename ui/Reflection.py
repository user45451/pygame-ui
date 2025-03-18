from ui.ui import *

class Pointer:
    value : float
    def __init__(self, value):
        self.value = value

class Reflection(ui): # 将自己的中心坐标反射到给定的指针，并且会根据指针的变化而移动
    def __init__(self, x : Pointer, y : Pointer, width, height):
        super().__init__(x.value - width / 2, y.value - height / 2, width, height)
        self.x = x
        self.y = y
        self.color = [(200,200,200),(255,0,0),(0,0,255)]
        self.color_index = 0
        self.hover_time = 0
    def own_draw(self, screen):
        rect = self.global_rect()
        pygame.draw.rect(screen, self.color[self.color_index], rect, 2)
        self.rect.x = int(self.x.value - self.rect.width / 2)
        self.rect.y = int(self.y.value - self.rect.height / 2)
    def hovered_event(self, event):
        self.hover_time /= 2
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.color_index = 1
        else:
            self.color_index = 2
    def drag_event(self, event):
        # 窗口移动的事件
        if event:
            if mouse_state['left']:
                # 更新窗口位置
                self.rect.x = event.pos[0] - self.drag_offset_x
                self.rect.y = event.pos[1] - self.drag_offset_y
                self.x.value = self.rect.x + self.rect.width / 2
                self.y.value = self.rect.y + self.rect.height / 2
    def handle_event(self, event):
        self.hover_time += 1
        if self.hover_time > 100:
            self.color_index = 0
        return False