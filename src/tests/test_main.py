import unittest
from unittest.mock import patch, Mock
import main


class TestMain(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_default(self, mock_args):
        mock_args.return_value = Mock(path='./', filter=None, group=None,
                                      value=None, interactive=False)
        args = main.parse_args()
        self.assertEqual(args.path, './')
        self.assertIsNone(args.filter)
        self.assertIsNone(args.group)
        self.assertIsNone(args.value)
        self.assertFalse(args.interactive)

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args_full(self, mock_args):
        mock_args.return_value = Mock(path='./', filter='extension',
                                      group='date', value='txt',
                                      interactive=True)
        args = main.parse_args()
        self.assertEqual(args.filter, 'extension')
        self.assertEqual(args.group, 'date')
        self.assertEqual(args.value, 'txt')
        self.assertTrue(args.interactive)

    @patch('main.parse_args')
    @patch('main.curses.wrapper')
    def test_Main_interactive(self, mock_wrapper, mock_parse_args):
        mock_parse_args.return_value = Mock(path='./', filter=None, group=None,
                                            value=None, interactive=True)
        main_instance = main.Main()
        mock_wrapper.assert_called_once()

    @patch('main.parse_args')
    @patch('main.du.DU')
    @patch('main.os.walk')
    @patch('main.alive_bar')
    def test_Main_run_cli(self, mock_alive_bar, mock_walk, mock_DU,
                          mock_parse_args):
        mock_walk.return_value = [('/', [], ['file1.txt', 'file2.txt'])]
        mock_parse_args.return_value = Mock(path='./', filter=None, group=None,
                                            value=None, interactive=False)
        mock_bar_instance = Mock()
        mock_alive_bar.return_value.__enter__.return_value = mock_bar_instance
        main_instance = main.Main()
        mock_DU.assert_called_once_with('./', is_interactive=False)

    @patch('main.parse_args')
    @patch('main.du.DU')
    @patch('main.os.walk')
    @patch('main.alive_bar')
    def test_Main_run_cli_filter(self, mock_alive_bar, mock_walk, mock_DU,
                                 mock_parse_args):
        mock_walk.return_value = [('/', [], ['file1.txt', 'file2.txt'])]
        mock_parse_args.return_value = Mock(path='./', filter='extension',
                                            value='txt', group=None,
                                            interactive=False)
        mock_bar_instance = Mock()
        mock_alive_bar.return_value.__enter__.return_value = mock_bar_instance
        mock_du_instance = Mock()
        mock_DU.return_value = mock_du_instance
        main_instance = main.Main()
        mock_du_instance.print_contents.assert_called_once_with(sort_by='name',
                                                                filter_by=(
                                                                    'extension'
                                                                    , 'txt'),
                                                                group_by=None)


if __name__ == '__main__':
    unittest.main()
