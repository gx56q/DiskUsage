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
        self.size = os.stat(self.path).st_size
        self.files_count = 0
        self.total_obj = 0
        self.files = []
        self.dirs = []
        self.scan_directory()

    def get_total_obj(self):
        return self.total_obj

    def add_file(self, file_to_add):
        f = file.File(file_to_add)
        self.files.append(f)
        self.size += f.size
        self.files_count += 1
        self.total_obj += 1

    def add_dir(self, dir_to_add):
        directory = Dir(dir_to_add)
        self.dirs.append(directory)
        self.size += directory.size
        self.total_obj += 1
        self.total_obj += directory.total_obj

    def scan_directory(self):
        for file_or_dir in os.listdir(self.path):
            full_path = os.path.join(self.path, file_or_dir)
            if os.path.isfile(full_path):
                self.add_file(full_path)
            elif os.path.isdir(full_path):
                self.add_dir(full_path)

    '''def get_dir_tree(self):
        tree = f'{self.name} ({self.size} bytes)\n'
        for file in self.files:
            tree += f'{"    " * file.level}{file.name} ({file.size} bytes)\n'
        return tree'''
