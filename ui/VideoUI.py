from ui.ui import *
import cv2

class VideoUI(ui):
    def __init__(self, x, y, width, height, video_path):
        super().__init__(x, y, width, height)
        self.cap = cv2.VideoCapture(video_path)
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.rect = pygame.Rect(x, y, frame_width, frame_height)
        self.frame = None
        self.get_next_frame()
        self.display_frame = self.frame
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.clock = pygame.time.Clock()

    def get_next_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.frame = frame
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.get_next_frame()

    def own_draw(self, screen):
        rect = self.global_rect()
        self.display_frame = self.resize_frame_to_fit(self.frame, rect)
        self.get_next_frame()
        screen.blit(self.display_frame, (rect.x, rect.y))
        self.clock.tick(self.fps)

    def handle_event(self, event):
        return False

    def resize_frame_to_fit(self, frame, rect):
        frame_width, frame_height = frame.get_size()
        rect_width, rect_height = rect.width, rect.height
        width_ratio = rect_width / frame_width
        height_ratio = rect_height / frame_height
        scale_ratio = min(width_ratio, height_ratio)
        new_width = int(frame_width * scale_ratio)
        new_height = int(frame_height * scale_ratio)
        return pygame.transform.scale(frame, (new_width, new_height))