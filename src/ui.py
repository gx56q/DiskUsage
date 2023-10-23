import os
import curses
import platform
import subprocess
from datetime import datetime as dt


from src import du


ts_format = "%Y-%m-%d %H:%M:%S"

class ProgressBar:
    def __init__(self, stdscr, y, x, total_width, total):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.total_width = total_width
        self.bar_width = min(50, total_width - 20)  # Setting the maximum width of the progress bar
        self.total = total
        self.current = 0

    def update(self, increment=1):
        self.current += increment
        self.draw()

    def draw(self):
        percentage = (self.current / self.total) * 100
        label = f"Progress: {percentage:.2f}%"

        filled_width = int((self.current / self.total) * self.bar_width)

        bar = ' ' * self.bar_width
        bar = '#' * filled_width + bar[filled_width:]

        self.stdscr.addstr(self.y, self.x, f"{label} [{bar}]")
        self.stdscr.refresh()


class UI:
    def __init__(self, stdscr, initial_path="."):
        self.progress_bar = None
        self.stdscr = stdscr
        self.current_dir = os.path.abspath(initial_path)
        self.selection = 0
        self.current_du = du.DU(self.current_dir)
        self.load_directory()

    def count_files(self, directory):
        if platform.system() == "Windows":
            cmd = f'dir "{directory}" /s /b /a:-d | find /v /c "::"'
            total = subprocess.check_output(cmd, shell=True).decode(
                'utf-8').strip()
        else:
            cmd = ['find', directory, '-type', 'f', '|', 'wc', '-l']
            total = subprocess.check_output(' '.join(cmd), shell=True).decode(
                'utf-8').strip()
        return int(total)

    def load_directory(self):
        self.stdscr.clear()
        self.display_header()

        total_files_and_dirs = self.count_files(self.current_dir)
        self.progress_bar = ProgressBar(self.stdscr, curses.LINES - 1, 0, 700, total_files_and_dirs)
        self.current_du.scan_directory(self.progress_bar)
        self.refresh_screen()

    def display_header(self):
        headers = [
            ("Name", 30),
            ("Size", 15),
            ("Files count", 15),
            ("Level", 10),
            ("Last modified", 25),
            ("Created", 25),
            ("Owner", 10)
        ]
        for header, width in headers:
            self.stdscr.addstr(header.ljust(width))
        self.stdscr.addstr("\n" + "-" * 130 + "\n")

    def refresh_screen(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, f"Current Directory: {self.current_dir}\n", curses.A_BOLD)
        self.display_header()
        entries = self.current_du.contents

        max_lines = curses.LINES - 4
        start_index = self.selection - max_lines + 1
        if start_index < 0:
            start_index = 0
        end_index = start_index + max_lines

        for i, entry in enumerate(entries[start_index:end_index]):
            y_position = i + 3
            if y_position >= curses.LINES - 1:
                break
            if i + start_index == self.selection:
                format_str = (f"{entry.name:<30}{entry.size:<15}"
                              f"{entry.files_count if entry.files_count else '-':<15}"
                              f"{entry.level:<10}"
                              f"{dt.fromtimestamp(entry.last_modified).strftime(ts_format):<25}"
                              f"{dt.fromtimestamp(entry.created).strftime(ts_format):<25}"
                              f"{entry.owner:<10}")
                self.stdscr.addstr(y_position, 0, format_str, curses.A_REVERSE)
            else:
                format_str = (f"{entry.name:<30}"
                              f"{entry.size:<15}"
                              f"{entry.files_count if entry.files_count else '-':<15}"
                              f"{entry.level:<10}"
                              f"{dt.fromtimestamp(entry.last_modified).strftime(ts_format):<25}"
                              f"{dt.fromtimestamp(entry.created).strftime(ts_format):<25}"
                              f"{entry.owner:<10}")
                self.stdscr.addstr(y_position, 0, format_str)
        self.stdscr.refresh()

    def navigate(self):
        while True:
            key = self.stdscr.getch()
            if key == ord('q'):
                break
            elif key == curses.KEY_DOWN and self.selection < len(
                    self.current_du.contents) - 1:
                self.selection += 1
            elif key == curses.KEY_UP and self.selection > 0:
                self.selection -= 1
            elif key == 10 or key == curses.KEY_RIGHT:  # Enter key
                selected_entry = self.current_du.contents[self.selection]
                new_path = os.path.join(self.current_dir, selected_entry.name)
                if os.path.isdir(new_path):
                    self.current_dir = new_path
                    self.current_du = du.DU(self.current_dir)
                    self.load_directory()
                    self.selection = 0
                else:
                    self.stdscr.addstr(1, 0,
                                       f"Selected file: {selected_entry.name}")
                    self.stdscr.refresh()
                    self.stdscr.getch()
            elif key == curses.KEY_LEFT:
                self.current_dir = os.path.dirname(self.current_dir)
                self.current_du = du.DU(self.current_dir)
                self.load_directory()
                self.selection = 0
            self.refresh_screen()


def main(stdscr):
    curses.curs_set(0)
    explorer = UI(stdscr)
    explorer.navigate()


if __name__ == "__main__":
    curses.wrapper(main)
