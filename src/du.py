import os
import dir


class DU:
    def __init__(self, path):
        self.main_dir_path = os.path.abspath(path)
        if not os.path.isdir(self.main_dir_path):
            raise ValueError(f'{self.main_dir_path} is not a directory')
        self.parent_dir = dir.Dir(self.main_dir_path)
        self.contents = []

    def get_contents(self):
        print(self.parent_dir, self.parent_dir.size)
        for el in self.contents:
            print(el, el.size)

    def scan_directory(self, bar):
        def get_dir_contents(parent_dir, dir_path, progress_bar):
            dir_path = os.path.abspath(dir_path)
            try:
                list_dir = os.listdir(dir_path)
            except PermissionError:
                print(f'Permission denied: {dir_path}')
                return
            for file_to_add in list_dir:
                file_to_add = os.path.join(dir_path, file_to_add)
                file_to_add = os.path.abspath(file_to_add)
                if os.path.isfile(file_to_add):
                    parent_dir.add_file(file_to_add)
                    progress_bar()
                elif os.path.isdir(file_to_add):
                    parent_dir.add_dir(file_to_add)
                    get_dir_contents(parent_dir.dirs[file_to_add], file_to_add,
                                     progress_bar)
                    parent_dir.size += parent_dir.dirs[file_to_add].size

        get_dir_contents(self.parent_dir, self.main_dir_path, bar)

    def sort_by_file_size(self):
        sorted_dirs = sorted(self.parent_dir.dirs.values(),
                             key=lambda x: x.size, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.size, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_file_count(self):
        sorted_dirs = sorted(self.parent_dir.dirs.values(),
                             key=lambda x: x.files_count, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.size, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_file_extension(self):
        sorted_dirs = sorted(self.parent_dir.dirs.values(),
                             key=lambda x: x.size, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.extension, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_time_last_modified(self):
        sorted_dirs = sorted(self.parent_dir.dirs.values(),
                             key=lambda x: x.last_modified, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.last_modified, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_time_created(self):
        sorted_dirs = sorted(self.parent_dir.dirs.values(),
                             key=lambda x: x.created, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.created, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_owner(self):
        sorted_dirs = sorted(self.parent_dir.dirs.values(),
                             key=lambda x: x.owner, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.owner, reverse=True)
        self.contents = sorted_dirs + sorted_files