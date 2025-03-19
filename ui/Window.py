from ui.ui import *
from ui.Reflection import *

class Window(ui):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.offset_x = 0
        self.offset_y = 0
        self.color = [(100,100,100),(0,255,0),(0,0,255)]
        self.color_index = 0

        self.left = Pointer(x)
        self.top = Pointer(y)
        self.right = Pointer(x + width)
        self.bottom = Pointer(y + height)

        self.topleftResize = Reflection(self.left, self.top, 10, 10)
        self.rightbottomResize = Reflection(self.right, self.bottom, 10, 10)
        self.toprightResize = Reflection(self.right, self.top, 10, 10)
        self.leftbottomResize = Reflection(self.left, self.bottom, 10, 10)
    def rebuild(self):
        self.root_ui.add_child(self.topleftResize)
        self.root_ui.add_child(self.rightbottomResize)
        self.root_ui.add_child(self.toprightResize)
        self.root_ui.add_child(self.leftbottomResize)
    def full(self): # 全局窗口变换, 鼠标移动窗口的时候可能会有比例缩放问题
        bouding_box = [float('inf'), float('inf'), float('-inf'), float('-inf')]
        for child in self.children:
            bouding_box[0] = min(child.rect.x, bouding_box[0])
            bouding_box[1] = min(child.rect.y, bouding_box[1])
            bouding_box[2] = max(child.rect.x + child.rect.width, bouding_box[2])
            bouding_box[3] = max(child.rect.y + child.rect.height, bouding_box[3])
        rect = self.global_rect()
        rect_center = [rect.x + rect.width / 2, rect.y + rect.height / 2]
        box_center = [(bouding_box[0] + bouding_box[2]) / 2, (bouding_box[1] + bouding_box[3]) / 2]
        box_size = [bouding_box[2] - bouding_box[0], bouding_box[3] - bouding_box[1]]
        scaled = min([self.rect.width / box_size[0], self.rect.height / box_size[1]])
        if box_size[0] > 0 and box_size[1] > 0:
            self.inner_gravity = [rect_center[0] - box_center[0], rect_center[1] - box_center[1], box_center[0], box_center[1], self.gravity[4] * scaled, self.gravity[5] * scaled]
    def move(self): # 相对窗口坐标系变换
        self.inner_gravity = [self.gravity[0] + self.rect.x, self.gravity[1] + self.rect.y, 0, 0, 1, 1]
    def own_draw(self, screen):
        rect = self.global_rect()
        pygame.draw.rect(screen, self.color[self.color_index], rect, 2)
        # 将浮点数转换为整数以避免类型错误
        self.rect.x = int(self.left.value)
        self.rect.y = int(self.top.value)
        self.rect.width = int(self.right.value - self.left.value)
        self.rect.height = int(self.bottom.value - self.top.value)
        self.full()
        # self.move()
    def hovered_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.color_index = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.color_index = 2
        else:
            self.color_index = 0
    def drag_event(self, event):
        # 窗口移动的事件
        if event:
            if mouse_state['left']:
                # 更新窗口位置
                self.rect.x = event.pos[0] - self.drag_offset_x
                self.rect.y = event.pos[1] - self.drag_offset_y
                self.left.value = event.pos[0] - self.drag_offset_x
                self.top.value = event.pos[1] - self.drag_offset_y
                self.right.value = self.left.value + self.rect.width
                self.bottom.value = self.top.value + self.rect.height
    def handle_event(self, event):
        for child in self.children: # 遍历子节点
            child.handle_event(event)  # 递归处理子节点的事件
        return False

