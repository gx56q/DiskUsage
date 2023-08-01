# TODO: change to from os import path, stat
import os
from pwd import getpwuid
import file


class Dir:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.name = os.path.basename(self.path)
        self.level = os.path.dirname(self.path).count(os.sep)
        self.last_modified = os.path.getmtime(self.path)
        self.created = os.path.getctime(self.path)
        self.owner = getpwuid(os.stat(self.path).st_uid).pw_name
        self.size = os.path.getsize(self.path)
        self.files_count = 0
        self.files = []
        self.dirs = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def get_files_count(self):
        for d in self.dirs.values():
            self.files_count += d.get_files_count()
        return self.files_count

    def add_file(self, file_to_add):
        f = file.File(file_to_add)
        self.files.append(f)
        self.size += f.size
        self.files_count += 1

    def add_dir(self, dir_path):
        dir_path = os.path.abspath(dir_path)
        d = Dir(dir_path)
        self.dirs.update({dir_path: d})
