import unittest
import os

from src import utils
from src.file import File


class TestFile(unittest.TestCase):
    VALID_PATH = os.path.join("test_sources", "test_file.txt")
    INVALID_PATH = "test_sources"

    def test_valid_file_initialization(self):
        file_obj = File(self.VALID_PATH)

        self.assertEqual(file_obj.path, os.path.abspath(self.VALID_PATH))
        self.assertEqual(file_obj.size, os.path.getsize(self.VALID_PATH))
        self.assertEqual(file_obj.name, "test_file.txt")
        self.assertEqual(file_obj.extension, ".txt")
        self.assertEqual(file_obj.last_modified,
                         os.path.getmtime(self.VALID_PATH))
        self.assertEqual(file_obj.created,
                         utils.creation_date(self.VALID_PATH))
        self.assertEqual(file_obj.files_count, None)

    def test_invalid_file_initialization(self):
        with self.assertRaises(ValueError):
            File(self.INVALID_PATH)

    def test_str_representation(self):
        file_obj = File(self.VALID_PATH)
        self.assertEqual(str(file_obj), "test_file.txt")

    def test_repr_representation(self):
        file_obj = File(self.VALID_PATH)
        self.assertEqual(repr(file_obj), "test_file.txt")


if __name__ == "__main__":
    unittest.main()
