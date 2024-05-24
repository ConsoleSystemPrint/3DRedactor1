import unittest
from main import *
from object_3d import *
from unittest.mock import MagicMock, patch


class TestObject3D(unittest.TestCase):
    def setUp(self):
        self.render = MagicMock(spec=SoftwareRender)
        self.object = Object3D(self.render)

    def test_translate(self):
        initial_vertices = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
        self.object.vertices = initial_vertices.copy()
        self.object.translate([1, 1, 1])
        expected_vertices = initial_vertices @ np.array([[1, 0, 0, 1],
                                                         [0, 1, 0, 1],
                                                         [0, 0, 1, 1],
                                                         [0, 0, 0, 1]])
        np.testing.assert_array_almost_equal(self.object.vertices, expected_vertices)

    def test_scale(self):
        initial_vertices = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
        self.object.vertices = initial_vertices.copy()
        self.object.scale(2)
        expected_vertices = initial_vertices @ np.diag([2, 2, 2, 1])
        np.testing.assert_array_almost_equal(self.object.vertices, expected_vertices)

    def test_rotate_x(self):
        initial_vertices = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
        self.object.vertices = initial_vertices.copy()
        self.object.rotate_x(np.pi)
        expected_vertices = initial_vertices @ rotate_x(np.pi)
        np.testing.assert_array_almost_equal(self.object.vertices, expected_vertices)

    def test_rotate_y(self):
        initial_vertices = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
        self.object.vertices = initial_vertices.copy()
        self.object.rotate_y(np.pi)
        expected_vertices = initial_vertices @ rotate_y(np.pi)
        np.testing.assert_array_almost_equal(self.object.vertices, expected_vertices)

    def test_rotate_z(self):
        initial_vertices = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
        self.object.vertices = initial_vertices.copy()
        self.object.rotate_z(np.pi)
        expected_vertices = initial_vertices @ rotate_z(np.pi)
        np.testing.assert_array_almost_equal(self.object.vertices, expected_vertices)

    @patch('object_3d.pg.draw.polygon')
    def test_screen_projection(self, mock_draw_polygon):
        self.object.vertices = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
        self.object.color_faces = [(pg.Color('red'), [0, 1])]
        self.render.camera.camera_matrix.return_value = np.eye(4)
        self.render.projection.projection_matrix = np.eye(4)
        self.render.projection.to_screen_matrix = np.eye(4)
        self.object.screen_projection()
        mock_draw_polygon.assert_called_once()

    @patch('object_3d.pg.draw.circle')
    def test_draw_vertices(self, mock_draw_circle):
        self.object.vertices = np.array([[0, 0, 0, 1], [1, 1, 1, 1]])
        self.object.draw_vertices = True
        self.object.color_faces = [(pg.Color('red'), [0])]
        self.render.camera.camera_matrix.return_value = np.eye(4)
        self.render.projection.projection_matrix = np.eye(4)
        self.render.projection.to_screen_matrix = np.eye(4)
        self.object.screen_projection()
        mock_draw_circle.assert_called()


if __name__ == "__main__":
    unittest.main()