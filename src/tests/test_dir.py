import unittest
from src.dir import Dir
from src.file import File
import os


class TestDir(unittest.TestCase):
    TEST_DIR = "test_sources/test_dir"
    TEST_DIR_2 = "test_sources/test_dir/test_dir_2"
    TEST_FILE_TXT = "test_sources/test_dir/test_file.txt"
    TEST_FILE_MD = "test_sources/test_dir/test_file.md"

    def setUp(self):
        self.dir = Dir(TestDir.TEST_DIR)

    def test_initialization(self):
        self.assertEqual(self.dir.name, 'test_dir')
        self.assertEqual(self.dir.level, os.path.dirname(self.dir.path)
                         .count(os.sep))
        self.assertTrue(isinstance(self.dir.last_modified, float))
        self.assertTrue(isinstance(self.dir.created, float))
        self.assertTrue(self.dir.owner)
        self.assertEqual(self.dir.size, 0)
        self.assertEqual(self.dir.files_count, 0)
        self.assertEqual(self.dir.files, [])
        self.assertEqual(self.dir.dirs, {})

    def test_add_file(self):
        file_size = os.path.getsize(self.TEST_FILE_TXT)
        self.dir.add_file(self.TEST_FILE_TXT)
        self.assertEqual(len(self.dir.files), 1)
        self.assertTrue(isinstance(self.dir.files[0], File))
        self.assertEqual(self.dir.size, file_size)
        self.assertEqual(self.dir.files_count, 1)

    def test_add_dir(self):
        self.dir.add_dir(self.TEST_DIR)
        self.assertEqual(len(self.dir.dirs), 1)
        self.assertTrue(isinstance(self.dir.dirs[os.path.abspath(self.TEST_DIR)], Dir))

    def test_get_files_count(self):
        self.dir.add_file(self.TEST_FILE_TXT)
        self.dir.add_file(self.TEST_FILE_MD)
        self.assertEqual(self.dir.get_files_count(), 2)

    def test_get_dirs_count(self):
        self.dir.add_dir(os.path.abspath(self.TEST_DIR_2))
        print(self.dir.dirs)
        self.assertEqual(self.dir.get_dirs_count(), 1)


if __name__ == '__main__':
    unittest.main()
