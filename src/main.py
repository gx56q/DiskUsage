import argparse
import du
import os
from alive_progress import alive_bar


def parse_args():
    parser = argparse.ArgumentParser(description='Disk Usage')
    parser.add_argument('path', type=str, help='Path to directory')
    return parser.parse_args()


class Main:
    def __init__(self):
        self.args = parse_args()
        self.du = du.DU(self.args.path)
        main_walk = os.walk(self.args.path)
        num_files = sum([len(files) for r, d, files in main_walk])
        num_dirs = len([d for r, d, files in main_walk])
        print(f'Number of directories: {num_dirs}')
        num_files += num_dirs
        with alive_bar(num_files) as bar:
            self.du.scan_directory(bar)
        self.du.sort_by_file_size()
        self.du.get_contents()


if __name__ == '__main__':
    Main()
