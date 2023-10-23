import unittest
from contextlib import redirect_stdout
from src.du import DU
import os


class TestDU(unittest.TestCase):
    TEST_DIR = "test_sources"

    def setUp(self):
        self.du = DU(TestDU.TEST_DIR, is_interactive=False)

    def test_initialization(self):
        self.assertEqual(self.du.main_dir_path,
                         os.path.abspath(TestDU.TEST_DIR))
        self.assertTrue(self.du.parent_dir)
        self.assertIsNone(self.du.current_sort)
        self.assertIsNone(self.du.current_grouping)
        self.assertIsNone(self.du.current_filter)

    def test_filter_contents(self):
        current_user = os.getlogin()
        self.du.filter_contents('owner', current_user)
        for content in self.du.contents:
            self.assertEqual(content.owner, current_user)

        self.du.filter_contents('extension', '.txt')
        for content in self.du.contents:
            if hasattr(content, 'extension'):
                self.assertEqual(content.extension, '.txt')

    def test_sort_by(self):
        self.du.sort_by('name')
        names = [content.name for content in self.du.contents]
        self.assertEqual(names, sorted(names))

        self.du.sort_by('file_size')
        sizes = [content.size for content in self.du.contents]
        self.assertEqual(sizes, sorted(sizes, reverse=True))

        self.du.sort_by('file_count')
        file_counts = [content.files_count for content in self.du.contents]
        self.assertEqual(file_counts, sorted(file_counts, reverse=True))

        self.du.sort_by('file_extension')
        extensions = [content.extension for content in self.du.contents]
        self.assertEqual(extensions, sorted(extensions))

    def test_get_group_by(self):
        groups = self.du.get_group_by('extension')
        for key, items in groups.items():
            for item in items:
                if hasattr(item, 'extension'):
                    self.assertEqual(item.extension, key)
                else:
                    self.assertEqual(key, 'Directory')

    def test_update_contents(self):
        self.du.update_contents(filter_by=('owner', os.getlogin()))
        self.assertEqual(self.du.current_filter, ('owner', os.getlogin()))
        self.du.update_contents(sort_by='name')
        names = [content.name for content in self.du.contents]
        self.assertEqual(names, sorted(names))

    def test_clear(self):
        self.du.clear()
        self.assertEqual(self.du.contents, [])
        self.assertEqual(self.du.parent_dir.dirs, {})
        self.assertEqual(self.du.parent_dir.files, [])

    def test_scan_directory(self):
        self.du = DU(TestDU.TEST_DIR, is_interactive=False)
        def mock_bar(): pass
        self.du.scan_directory(mock_bar)
        self.assertNotEqual(self.du.contents, [])

    def test_print_contents(self):
        import io
        f = io.StringIO()
        with redirect_stdout(f):
            self.du.print_contents()
        content_str = f.getvalue()
        self.assertIn("Contents of", content_str)


if __name__ == '__main__':
    unittest.main()
