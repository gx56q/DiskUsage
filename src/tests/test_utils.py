import unittest
from unittest.mock import patch, Mock
from src.utils import creation_date


class TestUtils(unittest.TestCase):

    @patch('src.utils.platform.system', return_value='Windows')
    @patch('src.utils.os.path.getctime', return_value=12345)
    def test_creation_date_windows(self, mock_getctime, mock_system):
        result = creation_date('some_path')
        self.assertEqual(result, 12345)

    @patch('src.utils.platform.system', return_value='Linux')
    @patch('src.utils.os.stat')
    def test_creation_date_linux_with_birthtime(self, mock_stat, mock_system):
        mock_stat.return_value.st_birthtime = 67890
        result = creation_date('some_path')
        self.assertEqual(result, 67890)

    @patch('src.utils.platform.system', return_value='Linux')
    @patch('src.utils.os.stat')
    def test_creation_date_linux_without_birthtime(self, mock_stat,
                                                   mock_system):
        mock_stat_obj = Mock(st_mtime=54321)
        del mock_stat_obj.st_birthtime
        mock_stat.return_value = mock_stat_obj

        result = creation_date('some_path')
        self.assertEqual(result, 54321)

    @patch('src.utils.platform.system',
           return_value='Darwin')
    @patch('src.utils.os.stat')
    def test_creation_date_mac_with_birthtime(self, mock_stat, mock_system):
        mock_stat.return_value.st_birthtime = 67890
        result = creation_date('some_path')
        self.assertEqual(result, 67890)

    @patch('src.utils.platform.system',
           return_value='Darwin')
    @patch('src.utils.os.stat')
    def test_creation_date_mac_without_birthtime(self, mock_stat, mock_system):
        mock_stat_obj = Mock(st_mtime=54321)
        del mock_stat_obj.st_birthtime
        mock_stat.return_value = mock_stat_obj

        result = creation_date('some_path')
        self.assertEqual(result, 54321)


if __name__ == '__main__':
    unittest.main()
