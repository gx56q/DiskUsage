import os
import dir


class DU:
    def __init__(self, path):
        main_dir = os.path.abspath(path)
        if not os.path.isdir(main_dir):
            raise ValueError(f'{main_dir} is not a directory')
        self.parent_dir = dir.Dir(main_dir)
        self.contents = []
        self.sort_by_file_size()

    def get_contents(self):
        return self.contents

    def sort_by_file_size(self):
        sorted_dirs = sorted(self.parent_dir.dirs,
                             key=lambda x: x.size, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.size, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_file_count(self):
        sorted_dirs = sorted(self.parent_dir.dirs,
                             key=lambda x: x.files_count, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.size, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_file_extension(self):
        sorted_dirs = sorted(self.parent_dir.dirs,
                             key=lambda x: x.size, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.extension, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_time_last_modified(self):
        sorted_dirs = sorted(self.parent_dir.dirs,
                             key=lambda x: x.last_modified, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.last_modified, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_time_created(self):
        sorted_dirs = sorted(self.parent_dir.dirs,
                             key=lambda x: x.created, reverse=True)
        sorted_files = sorted(self.parent_dir.files,
                              key=lambda x: x.created, reverse=True)
        self.contents = sorted_dirs + sorted_files

    def sort_by_owner(self):
        sorted_dirs = sorted(self.parent_dir.dirs, key=lambda x: x.owner,
                             reverse=True)
        sorted_files = sorted(self.parent_dir.files, key=lambda x: x.owner,
                              reverse=True)
        self.contents = sorted_dirs + sorted_files
