import argparse
import curses
import os
import src.du as du
import src.ui as ui
from alive_progress import alive_bar


def parse_args():
    current_dir = os.getcwd()
    parser = argparse.ArgumentParser(description='Disk Usage')
    parser.add_argument('path', type=str, help='Path to directory',
                        default=current_dir, nargs='?')
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
        else:
            self.run_cli()

    def run_cli(self):
        disk_usage = du.DU(self.args.path, is_interactive=False)
        main_walk = os.walk(self.args.path)
        num_files = sum([len(files) for r, d, files in main_walk])
        num_dirs = len([d for r, d, files in main_walk])
        num_files += num_dirs
        with alive_bar(num_files) as bar:
            disk_usage.scan_directory(bar)
        filter_by = None
        if self.args.filter and self.args.value:
            filter_by = (self.args.filter, self.args.value)
        disk_usage.print_contents(sort_by='name',
                                  group_by=self.args.group,
                                  filter_by=filter_by)


if __name__ == '__main__':
    Main()
