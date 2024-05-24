from object_3d import *
from camera import *
from projection import *
import pygame as pg


class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pg.font.SysFont(None, 24)
        self.color = pg.Color('white')

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def is_clicked(self, event_pos):
        return self.rect.collidepoint(event_pos)

class SoftwareRender:
    def __init__(self):
        pg.init()
        self.last_mouse_position = None
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.move_object_mode = False
        self.scale_object_mode = False
        self.object_visible = False

        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)

        # Добавляем кнопки к интерфейсу
        self.buttons = [
            Button('Появление объекта', 150, 10, 240, 30, self.load_and_toggle_object_visibility),
            Button('Перемещение объекта', 150, 50, 240, 30, self.toggle_move_object_mode),
            Button('Масштабирование объекта', 150, 90, 240, 30, self.toggle_scale_object_mode)
        ]

    def load_and_toggle_object_visibility(self):
        if not hasattr(self, 'object'):
            self.object = self.get_object_from_file('resources/stand.obj')
            self.object.rotate_y(-math.pi / 4)
        self.object_visible = not self.object_visible

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pg.Color('black'))
        if self.object_visible:
            self.object.draw()

        # Отрисовка кнопок
        for button in self.buttons:
            button.draw(self.screen)

    def run(self):
        while True:
            self.draw()
            if not self.move_object_mode and not self.scale_object_mode:
                self.camera.control()
            self.handle_events()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

    def handle_events(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                self.handle_keys(event)

            # Обработка нажатий на кнопки
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        button.callback()

            if self.move_object_mode:
                if event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP] and event.button == 1:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.last_mouse_position = pg.mouse.get_pos()
                    elif event.type == pg.MOUSEBUTTONUP:
                        self.last_mouse_position = None
                elif event.type == pg.MOUSEMOTION and self.last_mouse_position:
                    self.move_object(pg.mouse.get_pos())

            elif keys[pg.K_LCTRL] and event.type == pg.MOUSEBUTTONDOWN and (event.button == 4 or event.button == 5):
                self.scale_object(event)

    def handle_keys(self, event):
        if event.key == pg.K_g:
            self.toggle_move_object_mode()
        elif event.key == pg.K_u:
            self.toggle_scale_object_mode()
        elif event.key == pg.K_t:
            self.load_and_toggle_object_visibility()

    def toggle_move_object_mode(self):
        self.move_object_mode = not self.move_object_mode
        pg.mouse.set_visible(self.move_object_mode)
        if self.move_object_mode:
            pg.event.get()

    def toggle_scale_object_mode(self):
        self.scale_object_mode = not self.scale_object_mode
        pg.mouse.set_visible(self.scale_object_mode)
        if self.scale_object_mode:
            pg.event.get()

    def move_object(self, current_mouse_position):
        if self.last_mouse_position:
            dx = current_mouse_position[0] - self.last_mouse_position[0]
            dy = current_mouse_position[1] - self.last_mouse_position[1]
            self.object.translate([dx * 0.5, -dy * 0.5, 0])
            self.last_mouse_position = current_mouse_position

    def scale_object(self, event):
        scale_factor = 1.1 if event.button == 4 else 0.9
        self.object.scale(scale_factor)

def main():
    app = SoftwareRender()
    app.run()

if __name__ == "__main__":
    main()