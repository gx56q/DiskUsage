import os
from pwd import getpwuid


class File:
    def __init__(self, path):
        if not os.path.isfile(path):
            raise ValueError(f'{path} is not a file')
        self.path = os.path.abspath(path)
        self.size = os.path.getsize(self.path)
        self.name = os.path.basename(self.path)
        self.extension = os.path.splitext(path)[1]
        self.level = os.path.dirname(self.path).count(os.sep)
        self.last_modified = os.path.getmtime(self.path)
        self.created = os.path.getctime(self.path)
        self.owner = getpwuid(os.stat(self.path).st_uid).pw_name
        self.files_count = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
