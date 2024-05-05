import pygame as pg
from matrix import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        # Position and orientation
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

        # FOV and planes
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100

        # Movement settings
        self.moving_speed = 0.3
        self.rotation_speed = 0.02

        # Pitch and Yaw
        self.anglePitch = 0
        self.angleYaw = 0

        self.mouse_sensitivity = 0.001

        # Hide cursor and grab control
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

        self.last_mouse_position = pg.mouse.get_pos()

    def control(self):
        key = pg.key.get_pressed()

        # Basic movement
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed

        # Vertical movement
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        # Update mouse movement regardless of click
        current_mouse_position = pg.mouse.get_pos()
        pg.mouse.set_pos((self.render.WIDTH // 2, self.render.HEIGHT // 2))  # Reset mouse to center of the screen
        delta_x = current_mouse_position[0] - self.render.WIDTH // 2
        delta_y = current_mouse_position[1] - self.render.HEIGHT // 2

        self.camera_yaw(delta_x * self.mouse_sensitivity)
        self.camera_pitch(+delta_y * self.mouse_sensitivity)  # Negate y-axis to invert the up/down motion

    def camera_yaw(self, angle):
        self.angleYaw += angle

    def camera_pitch(self, angle):
        self.anglePitch += angle
        self.anglePitch = max(-math.pi / 2, min(math.pi / 2, self.anglePitch))

    def camera_update_axii(self):
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        self.forward = np.array([0, 0, 1, 1]) @ rotate
        self.right = np.array([1, 0, 0, 1]) @ rotate
        self.up = np.array([0, 1, 0, 1]) @ rotate

    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()



   # функции для формирвоания матриц
    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])