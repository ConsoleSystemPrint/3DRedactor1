from object_3d import *
from camera import *
from projection import *
import pygame as pg


class SoftwareRender:
    def __init__(self):
        pg.init()
        self.move_object_mode = False
        self.last_mouse_position = None
        # разрешение поверхности для отрисовки
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()
        self.move_object_mode = False  # Режим перемещения объекта

        self.scale_object_mode = False
        self.last_mouse_position = None

        self.object_visible = True

    def create_objects(self):
        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.object = self.get_object_from_file('resources/stand.obj')
        self.object.rotate_y(-math.pi / 4)
        self.object_visible = True

    def toggle_object_visibility(self):
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

    def run(self):
        while True:
            self.draw()
            self.object.draw()
            if not self.move_object_mode and not self.scale_object_mode:  # Если не в режиме перемещения и не в режиме масштабирования
                self.camera.control()
            self.handle_events()  # Обработка событий, включая нажатие клавиши 'U'
            if self.scale_object_mode:
                scroll = pg.mouse.get_rel()[1]  # Получение изменения положения колеса мыши
                self.object.scale(scroll * 0.1)  # Масштабирование объекта
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                self.handle_keys(event)  # Обработка нажатия клавиш
                if event.key == pg.K_g:
                    self.toggle_move_object_mode()
            if self.move_object_mode:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        self.last_mouse_position = pg.mouse.get_pos()
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.last_mouse_position = None
                elif event.type == pg.MOUSEMOTION:
                    if self.last_mouse_position:
                        self.move_object(pg.mouse.get_pos())
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()


    def toggle_move_object_mode(self):
        self.move_object_mode = not self.move_object_mode
        pg.mouse.set_visible(self.move_object_mode)
        if self.move_object_mode:
            pg.event.get()  # Очистить очередь событий мыши после переключения режимов

    def move_object(self, current_mouse_position):
        if self.last_mouse_position:
            dx = current_mouse_position[0] - self.last_mouse_position[0]
            dy = current_mouse_position[1] - self.last_mouse_position[1]
            self.object.translate([dx * 0.5, -dy * 0.5, 0])  # Масштабируем перемещение
            self.last_mouse_position = current_mouse_position


        ### Активация и деактивация режима изменения размера
    def toggle_scale_object_mode(self):
        self.scale_object_mode = not self.scale_object_mode
        pg.mouse.set_visible(self.scale_object_mode)

    def handle_keys(self, event):
        if event.key == pg.K_k:
            self.toggle_scale_object_mode()

     ### Обработка событий мыши для изменения размера
    def handle_mouse_events(self, event):
        if self.scale_object_mode:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.last_mouse_position = pg.mouse.get_pos()
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.last_mouse_position = None
            elif event.type == pg.MOUSEMOTION:
                if self.last_mouse_position:
                    current_mouse_position = pg.mouse.get_pos()
                    self.scale_object(current_mouse_position)

    def scale_object(self, current_mouse_position):
        if self.last_mouse_position:
            dx = current_mouse_position[0] - self.last_mouse_position[0]
            scale_factor = 1 + dx * 0.01
            self.object.scale(scale_factor)
            self.last_mouse_position = current_mouse_position


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()