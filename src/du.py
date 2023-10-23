import os
from src import dir
from datetime import datetime as dt
from collections import defaultdict

ts_format = '%d-%m-%Y %H:%M:%S'


def print_element(el):
    print(
        f'{el.name:<30}{el.size:<15}'
        f'{el.files_count if el.files_count else "-":<15}'
        f'{el.level:<10}'
        f'{dt.fromtimestamp(el.last_modified).strftime(ts_format):<25}'
        f'{dt.fromtimestamp(el.created).strftime(ts_format):<25}'
        f'{el.owner:<10}')


class DU:
    def __init__(self, path, is_interactive=True):
        self.is_interactive = is_interactive
        self.current_sort = None
        self.current_grouping = None
        self.current_filter = None
        self.grouped_contents = None
        self.main_dir_path = os.path.abspath(path)
        if not os.path.isdir(self.main_dir_path):
            raise ValueError(f'{self.main_dir_path} is not a directory')
        self.parent_dir = dir.Dir(self.main_dir_path)
        self.contents = []

    def filter_contents(self, criterion, value):
        filters = {
            'owner': lambda x: x.owner == value,
            'nesting': lambda x: x.level == value,
            'size': lambda x: x.size == value,
            'file_count': lambda x: x.files_count == value,
            'date_modified': lambda x: int(x.last_modified) == int(
                dt.strptime(value, '%d-%m-%Y').timestamp()),
            'date_created': lambda x: int(x.created) == int(
                dt.strptime(value, '%d-%m-%Y').timestamp()),
            'extension':
                lambda x: hasattr(x, 'extension') and x.extension == value
        }
        self.contents = [el for el in self.contents if filters[criterion](el)]

    def combined_sort(self, dir_key, file_key):
        sorted_dirs = sorted(self.parent_dir.dirs.values(), key=dir_key,
                             reverse=True)
        sorted_files = sorted(self.parent_dir.files, key=file_key,
                              reverse=True)
        return sorted_dirs + sorted_files

    def sort_by(self, criterion):
        sort_options = {
            'name': (lambda x: x.name, lambda x: x.name),
            'file_size': (lambda x: x.size, lambda x: x.size),
            'file_count': (lambda x: x.files_count, lambda x: x.name),
            'file_extension': (lambda x: x.size, lambda x: x.extension),
            'time_modified': (
                lambda x: x.last_modified, lambda x: x.last_modified),
            'time_created': (lambda x: x.created, lambda x: x.created),
            'owner': (lambda x: x.owner, lambda x: x.owner),
            'nesting': (lambda x: x.level, lambda x: x.level),
        }
        if criterion in sort_options:
            dir_key, file_key = sort_options[criterion]
            self.contents = self.combined_sort(dir_key, file_key)

    def get_group_by(self, criterion):
        if self.grouped_contents and criterion == self.current_grouping:
            return self.grouped_contents
        group_options = {
            'extension': lambda x: x.extension if hasattr(x,
                                                          'extension') else
            'Directory',
            'date': lambda x: dt.fromtimestamp(x.last_modified).strftime(
                '%d-%m-%Y'),
            'size_or_files_count':
                lambda x: x.files_count if hasattr(x, 'files_count')
                else x.size,
            'owner': lambda x: x.owner,
            'nesting': lambda x: x.level
        }

        if criterion in group_options:
            key_func = group_options[criterion]
            grouped_contents = defaultdict(list)
            for el in self.contents:
                key = key_func(el)
                grouped_contents[key].append(el)
            self.grouped_contents = dict(sorted(grouped_contents.items()))
            self.current_grouping = criterion
            return self.grouped_contents

    def update_contents(self, filter_by=None, sort_by='name', group_by=None):
        if sort_by and sort_by != self.current_sort:
            self.current_sort = sort_by
            self.sort_by(sort_by)
        if filter_by and filter_by != self.current_filter:
            self.current_filter = filter_by
            self.filter_contents(*filter_by)
        if group_by and group_by != self.current_grouping:
            self.current_grouping = group_by
            self.grouped_contents = self.get_group_by(group_by)

    def print_contents(self, sort_by=None, group_by=None, filter_by=None):
        if sort_by:
            self.sort_by(sort_by)
        if filter_by:
            self.filter_contents(*filter_by)
        print(f'Contents of {self.main_dir_path}')
        print(
            f'{"Name":<30}'
            f'{"Size":<15}'
            f'{"Files count":<15}'
            f'{"Level":<10}'
            f'{"Last modified":<25}'
            f'{"Created":<25}'
            f'{"Owner":<10}')
        print('-' * 130)
        print_element(self.parent_dir)
        print('-' * 130)
        if group_by:
            grouped_contents = self.get_group_by(group_by)
            for key, items in grouped_contents.items():
                print(f'\nGroup: {key}\n' + '-' * 130)
                for el in items:
                    print_element(el)
        else:
            for el in self.contents:
                print_element(el)
        print('-' * 130)

    def clear(self):
        self.contents = []
        self.parent_dir.dirs = {}
        self.parent_dir.files = []

    def scan_directory(self, bar):
        def get_dir_contents(parent_dir, dir_path, progress_bar):
            dir_path = os.path.abspath(dir_path)
            try:
                list_dir = os.listdir(dir_path)
            except PermissionError:
                return
            for file_to_add in list_dir:
                file_to_add = os.path.join(dir_path, file_to_add)
                file_to_add = os.path.abspath(file_to_add)
                if os.path.isfile(file_to_add):
                    parent_dir.add_file(file_to_add)
                    if not self.is_interactive:
                        progress_bar()
                    else:
                        progress_bar.update()
                elif os.path.isdir(file_to_add):
                    parent_dir.add_dir(file_to_add)
                    get_dir_contents(parent_dir.dirs[file_to_add], file_to_add,
                                     progress_bar)
                    parent_dir.size += parent_dir.dirs[file_to_add].size
        self.clear()
        get_dir_contents(self.parent_dir, self.main_dir_path, bar)
        self.sort_by('name')
        self.update_contents()
