import unittest
from main import *
from unittest.mock import patch, MagicMock

class Test3DEditor(unittest.TestCase):
    def setUp(self):
        self.app = SoftwareRender()

    @patch('main.Object3D')
    def test_load_and_toggle_object_visibility(self, MockObject3D):
        self.app.load_and_toggle_object_visibility()
        self.assertTrue(self.app.object_visible)
        self.app.load_and_toggle_object_visibility()
        self.assertFalse(self.app.object_visible)
        MockObject3D.assert_called_once()

    def test_toggle_move_object_mode(self):
        self.app.toggle_move_object_mode()
        self.assertTrue(self.app.move_object_mode)
        self.app.toggle_move_object_mode()
        self.assertFalse(self.app.move_object_mode)

    def test_toggle_scale_object_mode(self):
        self.app.toggle_scale_object_mode()
        self.assertTrue(self.app.scale_object_mode)
        self.app.toggle_scale_object_mode()
        self.assertFalse(self.app.scale_object_mode)

    @patch('pygame.event.get')
    def test_handle_events_quit(self, mock_event_get):
        mock_event_get.return_value = [MagicMock(type=pg.QUIT)]
        with self.assertRaises(SystemExit):
            self.app.handle_events()

    @patch('main.SoftwareRender.load_and_toggle_object_visibility')
    def test_button_callback(self, mock_load_and_toggle_object_visibility):
        for button in self.app.buttons:
            if button.text == 'Появление объекта':
                button.callback()
                mock_load_and_toggle_object_visibility.assert_called_once()

    def test_handle_keys(self):
        events = [
            MagicMock(type=pg.KEYDOWN, key=pg.K_g),
            MagicMock(type=pg.KEYDOWN, key=pg.K_u),
            MagicMock(type=pg.KEYDOWN, key=pg.K_t)
        ]
        for event in events:
            with patch.object(self.app, 'toggle_move_object_mode') as mock_move_mode, \
                    patch.object(self.app, 'toggle_scale_object_mode') as mock_scale_mode, \
                    patch.object(self.app, 'load_and_toggle_object_visibility') as mock_load_and_toggle:

                self.app.handle_keys(event)
                if event.key == pg.K_g:
                    mock_move_mode.assert_called_once()
                elif event.key == pg.K_u:
                    mock_scale_mode.assert_called_once()
                elif event.key == pg.K_t:
                    mock_load_and_toggle.assert_called_once()


if __name__ == '__main__':
    unittest.main()