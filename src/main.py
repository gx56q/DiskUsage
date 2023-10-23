import argparse
import curses

import du
import os
import ui
from alive_progress import alive_bar


def parse_args():
    parser = argparse.ArgumentParser(description='Disk Usage')
    parser.add_argument('path', type=str, help='Path to directory')
    parser.add_argument('-f', '--filter', dest="filter",
                        choices=['extension', 'size', 'date', 'owner',
                                 'nesting'],
                        help='Filter by given criterion')
    parser.add_argument('-g', '--group', dest="group",
                        choices=['extension', 'size', 'date', 'owner',
                                 'nesting'],
                        help='Group by given criterion')
    parser.add_argument('-v', '--value', dest="value",
                        help='Specific value for filtering '
                             '(e.g. ".txt" for extension or'
                             ' "2023-10-21" for date)')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Launch interactive UI')
    return parser.parse_args()


class Main:
    def __init__(self):
        self.args = parse_args()

        if self.args.interactive:
            curses.wrapper(ui.main)
            return
        else:
            self.run_cli()

    def run_cli(self):
        self.du = du.DU(self.args.path)
        main_walk = os.walk(self.args.path)
        num_files = sum([len(files) for r, d, files in main_walk])
        num_dirs = len([d for r, d, files in main_walk])
        num_files += num_dirs
        with alive_bar(num_files) as bar:
            self.du.scan_directory(bar)
        filter_by = None
        if self.args.filter and self.args.value:
            filter_by = (self.args.filter, self.args.value)
        self.du.get_contents_print(sort_by='file_count', group_by=self.args.group,
                             filter_by=filter_by)


if __name__ == '__main__':
    Main()
