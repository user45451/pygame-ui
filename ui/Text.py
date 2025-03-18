from ui.ui import *
class TextBox(ui):
    def __init__(self, x, y, width, height, text=''):
        super().__init__(x, y, width, height)
        self.text = text
        # 使用原始字符串以避免转义序列问题
        self.font = pygame.font.Font(r'c:\Windows\Fonts\simhei.ttf', 36)
        self.cursor_position = 0
    def own_draw(self, screen):
        rect = self.global_rect()
        pygame.draw.rect(screen, (155, 155, 155), rect)
        lines = self.text.split('\n')
        y_offset = 0
        # 根据global_rect的宽高计算缩放比例
        rect = self.global_rect()
        scale_x = rect.width / max([self.font.size(line)[0] for line in lines]) if lines else 1
        scale_y = rect.height / (self.font.get_linesize() * len(lines)) if lines else 1
        scale = min(scale_x, scale_y)
        # 调整字体大小
        new_font_size = int(self.font.get_height() * scale)
        new_font = pygame.font.Font(r'c:\Windows\Fonts\simhei.ttf', new_font_size)
        for line in lines:
            text_surface = new_font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (rect.x, rect.y + y_offset))
            y_offset += new_font.get_linesize()
        # 根据文本长度和行高扩展大小
        text_width = max([self.font.size(line)[0] for line in lines]) if lines else 0
        text_height = self.font.get_linesize() * len(lines)
        self.rect.width = max(10, text_width)
        self.rect.height = max(10, text_height)
        # 绘制光标
        cursor_x = rect.x
        cursor_y = rect.y
        current_position = 0
        # 考虑字体缩放后的光标位置计算
        scaled_font = pygame.font.Font(r'c:\Windows\Fonts\simhei.ttf', new_font_size)
        for i, line in enumerate(lines):
            if current_position + len(line) + lines[:i].count('\n') < self.cursor_position:
                cursor_x = rect.x + scaled_font.size(line)[0]
                cursor_y += scaled_font.get_linesize()
                current_position += len(line) + 1
            else:
                remaining_chars = self.cursor_position - current_position - lines[:i].count('\n')
                cursor_x = rect.x + scaled_font.size(line[:remaining_chars])[0]
                break
        pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + scaled_font.get_linesize()), 2)
    def set_text(self, text):
        self.text = text
    def drag_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 获取鼠标点击位置
            mouse_x, mouse_y = event.pos
            rect = self.global_rect()
            # 计算鼠标点击位置相对于文本框的坐标
            relative_x = mouse_x - rect.x
            relative_y = mouse_y - rect.y
            # 根据global_rect的宽高计算缩放比例
            rect = self.global_rect()
            lines = self.text.split('\n')
            scale_x = rect.width / max([self.font.size(line)[0] for line in lines]) if lines else 1
            scale_y = rect.height / (self.font.get_linesize() * len(lines)) if lines else 1
            scale = min(scale_x, scale_y)
            # 根据行高计算点击所在的行
            line_index = int(relative_y // (self.font.get_linesize() * scale))
            if line_index < len(lines):
                line = lines[line_index]
                # 根据字符宽度计算点击所在的字符位置
                for i in range(len(line) + 1):
                    char_width = self.font.size(line[:i])[0] * scale
                    half_char_width = self.font.size(line[i:i+1])[0] * scale / 2 if i < len(line) else 0
                    if char_width - half_char_width > relative_x:
                        self.cursor_position = sum(len(l) + 1 for l in lines[:line_index]) + i - 1
                        if self.cursor_position < 0:
                            self.cursor_position = 0
                        break
                else:
                    self.cursor_position = sum(len(l) + 1 for l in lines[:line_index]) + len(line)
        if event.type == pygame.TEXTINPUT:
            self.text = self.text[:self.cursor_position] + event.text + self.text[self.cursor_position:]
            self.cursor_position += len(event.text)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
            elif event.key == pygame.K_RETURN:
                self.text = self.text[:self.cursor_position] + '\n' + self.text[self.cursor_position:]
                self.cursor_position += 1
            elif event.key == pygame.K_LEFT:
                if self.cursor_position > 0:
                    self.cursor_position -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position < len(self.text):
                    self.cursor_position += 1
            elif event.key == pygame.K_DELETE:
                if self.cursor_position < len(self.text):
                    self.text = self.text[:self.cursor_position] + self.text[self.cursor_position + 1:]
    def handle_event(self, event):
        return False
