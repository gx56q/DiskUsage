import unittest
from unittest.mock import patch, MagicMock, Mock
from src.ui import ProgressBar, count_files, format_entry, UI, main


class TestProgressBar(unittest.TestCase):
    def setUp(self):
        self.stdscr_mock = MagicMock()
        self.progress_bar = ProgressBar(self.stdscr_mock, 0, 0, 100, 100)

    def test_update(self):
        self.progress_bar.update(10)
        self.assertEqual(self.progress_bar.current, 10)

    def test_draw(self):
        self.progress_bar.update(50)
        self.stdscr_mock.addstr.assert_called()


class TestUtilityFunctions(unittest.TestCase):
    def test_count_files_linux(self):
        with patch('platform.system', return_value="Linux"), patch(
                'subprocess.check_output', return_value=b'10\n'):
            result = count_files("/path")
            self.assertEqual(result, 10)

    def test_format_entry(self):
        class MockEntry:
            name = "test_file.txt"
            size = 1024
            files_count = 1
            level = 1
            last_modified = 1681231230.0
            created = 1581231230.0
            owner = "test_user"

        entry = MockEntry()
        formatted = format_entry(entry)
        self.assertTrue("test_file.txt" in formatted)
        self.assertTrue("test_user" in formatted)


class TestUI(unittest.TestCase):

    @patch('curses.wrapper')
    @patch('src.ui.count_files', return_value=100)
    @patch('src.ui.UI.load_directory')
    def setUp(self, load_directory_mock, count_files_mock,
              curses_wrapper_mock):
        self.stdscr_mock = MagicMock()
        self.ui = UI(self.stdscr_mock)

    def test_initialization(self):
        self.assertIsNone(self.ui.current_grouping)
        self.assertIsNone(self.ui.current_filter)
        self.assertIsNone(self.ui.progress_bar)
        self.assertEqual(self.ui.selection, 0)
        self.assertIn("extension", self.ui.valid_types)

    def test_get_display_entries_without_grouping(self):
        mock_content = ['item1', 'item2']
        self.ui.current_du.contents = mock_content
        result = self.ui.get_display_entries()
        self.assertEqual(result, mock_content)

    def test_get_display_entries_with_grouping(self):
        mock_grouped_contents = {
            'Group1': ['item1', 'item2'],
            'Group2': ['item3', 'item4']
        }
        self.ui.current_du.grouped_contents = mock_grouped_contents
        self.ui.current_grouping = 'mock_grouping'
        result = self.ui.get_display_entries()
        expected = ['Group: Group1', 'item1', 'item2', 'Group: Group2',
                    'item3', 'item4']
        self.assertEqual(result, expected)

    def test_format_entry(self):
        mock_entry = MagicMock()
        mock_entry.name = "test_entry"
        mock_entry.size = 1024
        mock_entry.files_count = 10
        mock_entry.level = 1
        mock_entry.last_modified = 1635024902
        mock_entry.created = 1634924902
        mock_entry.owner = "user"

        formatted_str = format_entry(mock_entry)
        self.assertIn("test_entry", formatted_str)
        self.assertIn("1024", formatted_str)
        self.assertIn("user", formatted_str)
        self.assertIn("10", formatted_str)
        self.assertIn("1", formatted_str)
        self.assertIn("2021-10-24 02:35:02", formatted_str)
        self.assertIn("2021-10-22 22:48:22", formatted_str)

    def test_display_header(self):
        self.ui.display_header()
        self.stdscr_mock.addstr.assert_any_call("Name".ljust(30))
        self.stdscr_mock.addstr.assert_any_call("Size".ljust(15))
        self.stdscr_mock.addstr.assert_any_call("Files count".ljust(15))
        self.stdscr_mock.addstr.assert_any_call("Level".ljust(10))
        self.stdscr_mock.addstr.assert_any_call("Last modified".ljust(25))
        self.stdscr_mock.addstr.assert_any_call("Created".ljust(25))
        self.stdscr_mock.addstr.assert_any_call("Owner".ljust(10))
        self.stdscr_mock.addstr.assert_any_call("\n" + "-" * 130 + "\n")

    @patch('src.ui.curses.curs_set', autospec=True)
    @patch('src.ui.UI', autospec=True)
    def test_main_function(self, ui_mock, curs_set_mock):
        stdscr_mock = MagicMock()
        ui_instance_mock = ui_mock.return_value
        main(stdscr_mock)
        curs_set_mock.assert_called_once_with(0)
        ui_mock.assert_called_once_with(stdscr_mock)
        ui_instance_mock.navigate.assert_called_once()

    @patch('src.ui.curses')
    def test_display_options(self, curses_mock):
        curses_mock.LINES = 10
        stdscr_mock = MagicMock()
        explorer = UI(stdscr_mock)
        explorer.display_options()
        options = [
            (f"[F]ilter:", ", ".join(explorer.valid_types)),
            ("[G]roup:", ", ".join(explorer.valid_types))
        ]
        y_position = 10 - 3
        for option, values in options:
            stdscr_mock.addstr.assert_any_call(y_position, 0,
                                               f"{option} {values}",
                                               curses_mock.A_BOLD)
            y_position += 1


class TestUINavigate(unittest.TestCase):
    @patch('src.ui.curses', create=True)
    @patch('src.ui.du.DU', create=True)
    def setUp(self, mock_du, mock_curses):
        self.mock_du = mock_du
        self.mock_curses = mock_curses
        self.mock_curses.LINES = 24
        self.mock_curses.KEY_DOWN = 258
        self.mock_curses.KEY_UP = 259
        self.mock_curses.KEY_RIGHT = 261
        self.mock_curses.KEY_LEFT = 260
        self.stdscr_mock = Mock()
        self.ui_instance = UI(self.stdscr_mock)
        self.ui_instance.current_du.contents = ["content1", "content2"]

    def test_navigate_quit(self):
        self.stdscr_mock.getch.return_value = ord('q')
        self.ui_instance.navigate()
        self.stdscr_mock.getch.assert_called_once()



if __name__ == '__main__':
    unittest.main()
