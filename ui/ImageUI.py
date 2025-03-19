from ui.ui import *

class ImageUI(ui):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(image_path)
        image_width, image_height = self.image.get_size()
        self.rect.width = image_width
        self.rect.height = image_height
        self.display_image = self.image
        self.compare_global = self.global_rect()

    def own_draw(self, screen):
        rect = self.global_rect()
        if rect != self.compare_global:
            self.compare_global = rect
            self.display_image = self.resize_image_to_fit(self.image, rect)
        screen.blit(self.display_image, (rect.x, rect.y))
    
    def handle_event(self, event):
        return False

    def resize_image_to_fit(self, image, rect):
        image_width, image_height = image.get_size()
        rect_width, rect_height = rect.width, rect.height
        width_ratio = rect_width / image_width
        height_ratio = rect_height / image_height
        scale_ratio = min(width_ratio, height_ratio)
        new_width = int(image_width * scale_ratio)
        new_height = int(image_height * scale_ratio)
        return pygame.transform.scale(image, (new_width, new_height))
