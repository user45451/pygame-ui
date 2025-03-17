import pygame

GRAY = (200, 200, 200)


def gravity_update(rect, gravity):
    new_rect = rect.copy()
    new_rect.x = rect.x + (gravity[2] - rect.x) * (1 - gravity[4])
    new_rect.y = rect.y + (gravity[3] - rect.y) * (1 - gravity[5])
    new_rect.width *= gravity[4]
    new_rect.height *= gravity[5]
    new_rect.x += gravity[0]
    new_rect.y += gravity[1]
    return new_rect
class ui:
    def __init__(self, x, y, width, height):
        self.root_ui = self
        self.rect = pygame.Rect(x, y, width, height)
        self.gravity = [0,0,0,0,1,1] # offset-x, offset-y, scale-at-x, scale-at-y, scale-x, scale-y
        self.inner_gravity = [0,0,0,0,1,1]
        self.children = []
        self.drag_offset_x = 0
        self.drag_offset_y = 0
    def add_child(self, child): # 不需要重载的函数
        if child is self:
            return  # 避免自身添加到自身导致无限循环
        child.root_ui = self
        child.rebuild()
        self.children.append(child)
    def rebuild(self): # 搭配 add_child 重定向root节点的时候会执行一次，最好重载
        return None
    def global_rect(self):
        return gravity_update(self.rect, self.gravity)
    def draw(self, screen): # 绘制函数不需要重载
        self.own_draw(screen)
        for child in self.children:
            child.gravity = self.inner_gravity
            child.draw(screen)
    def own_draw(self, screen):
        rect = self.global_rect()
        pygame.draw.rect(screen, GRAY, rect, 2)

    def hovered_post(self): # 不需要重载的函数
        for child in self.children:
            if child.global_rect().collidepoint(pygame.mouse.get_pos()):
                return child.hovered_post()
        return self
    def hovered_event(self, event):
        return None

    def drag_post(self, event): # 不需要重载的函数
        for child in self.children:
            if child.global_rect().collidepoint(pygame.mouse.get_pos()):
                return child.drag_post(event)
        self.drag_offset_x = event.pos[0] - self.rect.x # 记录鼠标点击位置的偏移量
        self.drag_offset_y = event.pos[1] - self.rect.y
        return self
    def drag_event(self, event):
        return None
    
    def handle_event(self, event): # drag_event不符合预期需要将所有ui都重载一遍
        mouse_event['hover'] = self.hovered_post()
        mouse_event['drag'] = self.drag_post(event) if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 else mouse_event['drag'] # 鼠标左键拖拽
        mouse_event['hover'].hovered_event(event)
        mouse_event['drag'].drag_event(event)
        if event.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
            handle_mouse_events(event)
        return any(child.handle_event(event) for child in self.children)
# 创建一个ui实例作为根节点
root_ui = ui(0, 0, 800, 600) # 这里假设窗口大小为800x600
mouse_state = {
    'left': False,
    'right': False,
    'middle': False
}
mouse_event = {
    'hover': root_ui,
    'drag': root_ui,
}

def handle_mouse_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            mouse_state['left'] = True
        elif event.button == 2:
            mouse_state['middle'] = True
        elif event.button == 3:
            mouse_state['right'] = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            mouse_state['left'] = False
        elif event.button == 2:
            mouse_state['middle'] = False
        elif event.button == 3:
            mouse_state['right'] = False

