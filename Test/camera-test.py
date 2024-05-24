import unittest
from numpy.distutils.fcompiler import pg
from camera import *
from unittest.mock import Mock

class TestCamera(unittest.TestCase):

    def setUp(self):
        self.render = Mock()
        self.render.WIDTH = 800
        self.render.HEIGHT = 600

        self.position = [0, 0, 0]
        self.camera = Camera(self.render, self.position)

    def test_initial_position(self):
        np.testing.assert_array_equal(self.camera.position, np.array([0, 0, 0, 1]))

    def test_movement_forward(self):
        self.camera.position = np.array([0, 0, 0, 1])
        pg.key.get_pressed = lambda: [False, False, True, False]
        self.camera.control()
        np.testing.assert_array_almost_equal(
            self.camera.position,
            np.array([0, 0, 0.3, 1])
        )

    def test_yaw_rotation(self):
        initial_yaw = self.camera.angleYaw
        self.camera.camera_yaw(0.1)
        self.assertEqual(self.camera.angleYaw, initial_yaw + 0.1)

    def test_pitch_rotation(self):
        initial_pitch = self.camera.anglePitch
        self.camera.camera_pitch(0.1)
        self.assertEqual(self.camera.anglePitch, initial_pitch + 0.1)

    def test_camera_update_axii(self):
        self.camera.camera_yaw(0.1)
        self.camera.camera_update_axii()

        self.assertFalse(np.array_equal(self.camera.forward, np.array([0, 0, 1, 1])))
        self.assertFalse(np.array_equal(self.camera.right, np.array([1, 0, 0, 1])))
        self.assertFalse(np.array_equal(self.camera.up, np.array([0, 1, 0, 1])))

    def test_translate_matrix(self):
        translate_matrix = self.camera.translate_matrix()
        expected_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        np.testing.assert_array_equal(translate_matrix, expected_matrix)

    def test_rotate_matrix(self):
        rotate_matrix = self.camera.rotate_matrix()
        expected_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        np.testing.assert_array_equal(rotate_matrix, expected_matrix)

if __name__ == '__main__':
    unittest.main()