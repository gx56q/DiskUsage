import os
import curses
import platform
import subprocess
from src import du
from datetime import datetime as dt

ts_format = "%Y-%m-%d %H:%M:%S"


class ProgressBar:
    def __init__(self, stdscr, y, x, total_width, total):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.total_width = total_width
        self.bar_width = min(50, total_width - 20)
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


def count_files(directory):
    if platform.system() == "Windows":
        cmd = f'dir "{directory}" /s /b /a:-d | find /v /c "::"'
        total = subprocess.check_output(cmd, shell=True).decode(
            'utf-8').strip()
    else:
        cmd = ['find', directory, '-type', 'f', '|', 'wc', '-l']
        total = subprocess.check_output(' '.join(cmd), shell=True).decode(
            'utf-8').strip()
    return int(total)


def format_entry(entry):
    return (f"{entry.name:<30}{entry.size:<15}"
            f"{entry.files_count if entry.files_count else '-':<15}"
            f"{entry.level:<10}"
            f"{dt.fromtimestamp(entry.last_modified).strftime(ts_format):<25}"
            f"{dt.fromtimestamp(entry.created).strftime(ts_format):<25}"
            f"{entry.owner:<10}")


class UI:
    def __init__(self, stdscr, initial_path="."):
        self.valid_types = ["extension", "size", "file_count",
                            "date_created", "date_modified", "owner",
                            "nesting"]
        self.current_grouping = None
        self.current_filter = None
        self.progress_bar = None
        self.stdscr = stdscr
        self.current_dir = os.path.abspath(initial_path)
        self.selection = 0
        self.current_du = du.DU(self.current_dir)
        self.load_directory()

    def load_directory(self):
        self.stdscr.clear()
        self.display_header()

        total_files_and_dirs = count_files(self.current_dir)
        self.progress_bar = ProgressBar(self.stdscr, curses.LINES - 1, 0, 700,
                                        total_files_and_dirs)
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
        self.stdscr.addstr(0, 0, f"Current Directory: {self.current_dir}\n",
                           curses.A_BOLD)
        self.display_header()

        entries_to_display = []

        if self.current_grouping is not None \
                and self.current_du.grouped_contents:
            for group_name, entries in \
                    self.current_du.grouped_contents.items():
                entries_to_display.append(f"Group: {group_name}")
                entries_to_display.extend(entries)
        else:
            entries_to_display = self.current_du.contents

        max_lines = curses.LINES - 7
        start_index = self.selection - max_lines + 1
        if start_index < 0:
            start_index = 0
        end_index = start_index + max_lines

        for i, entry in enumerate(entries_to_display[start_index:end_index]):
            y_position = i + 3
            if y_position >= curses.LINES - 1:
                break
            if isinstance(entry, str):
                self.stdscr.addstr(y_position, 0, entry, curses.A_BOLD)
                continue
            format_str = format_entry(entry)
            if i + start_index == self.selection:
                self.stdscr.addstr(y_position, 0, format_str, curses.A_REVERSE)
            else:
                self.stdscr.addstr(y_position, 0, format_str)

        self.stdscr.refresh()
        self.display_options()

    def navigate(self):
        while True:
            entries_to_display = self.get_display_entries()
            key = self.stdscr.getch()
            if key == ord('q'):
                break

            elif key == ord('F') or key == ord('f'):
                self.stdscr.addstr(curses.LINES - 1, 10, "Enter filter type: ")
                curses.echo()
                filter_type = self.stdscr.getstr().decode("utf-8")
                curses.noecho()
                if filter_type not in self.valid_types:
                    self.stdscr.addstr(curses.LINES - 1, 10,
                                       "Invalid filter type!")
                    self.stdscr.refresh()
                    continue
                self.stdscr.addstr(curses.LINES - 1, 10,
                                   f"Enter value for {filter_type}: ")
                curses.echo()
                filter_value = self.stdscr.getstr().decode("utf-8")
                curses.noecho()
                self.current_du.filter_contents(filter_type, filter_value)
                self.refresh_screen()

            elif key == ord('G') or key == ord('g'):
                self.selection = 0
                self.stdscr.addstr(curses.LINES - 1, 10,
                                   "Enter group by type: ")
                curses.echo()
                group_type = self.stdscr.getstr().decode("utf-8")
                curses.noecho()
                if group_type not in self.valid_types:
                    self.stdscr.addstr(curses.LINES - 1, 10,
                                       "Invalid group type!")
                    self.stdscr.refresh()
                    continue
                self.current_du.get_group_by(group_type)
                self.current_grouping = group_type
                self.refresh_screen()

            if key == curses.KEY_DOWN and self.selection < len(
                        entries_to_display) - 1:
                self.selection += 1
                while isinstance(entries_to_display[self.selection],
                                 str) and self.selection < len(
                        entries_to_display) - 1:
                    self.selection += 1

            elif key == curses.KEY_UP and self.selection > 0:
                self.selection -= 1
                while isinstance(entries_to_display[self.selection],
                                 str) and self.selection > 0:
                    self.selection -= 1

            if key == 10 or key == curses.KEY_RIGHT:
                selected_entry = entries_to_display[self.selection]
                if isinstance(selected_entry, str):
                    continue
                new_path = os.path.join(self.current_dir,
                                        selected_entry.name)
                if os.path.isdir(new_path):
                    self.current_grouping = None
                    self.current_dir = new_path
                    self.current_du = du.DU(self.current_dir)
                    self.load_directory()
                    self.selection = 0
                else:
                    continue

            elif key == curses.KEY_LEFT:
                self.selection = 0
                self.current_grouping = None
                self.current_dir = os.path.dirname(self.current_dir)
                self.current_du = du.DU(self.current_dir)
                self.load_directory()
            elif key == ord('R') or key == ord('r'):
                self.selection = 0
                self.current_grouping = None
                self.current_filter = None
                self.load_directory()
            self.refresh_screen()

    def get_display_entries(self):
        if self.current_grouping is not None \
                and self.current_du.grouped_contents:
            entries_to_display = []
            for group_name, entries in \
                    self.current_du.grouped_contents.items():
                entries_to_display.append(f"Group: {group_name}")
                entries_to_display.extend(entries)
            return entries_to_display
        else:
            return self.current_du.contents

    def display_options(self):
        options = [
            (f"[F]ilter:", ", ".join(self.valid_types)),
            ("[G]roup:", ", ".join(self.valid_types))
        ]
        y_position = curses.LINES - 3
        for option, values in options:
            self.stdscr.addstr(y_position, 0, f"{option} {values}",
                               curses.A_BOLD)
            y_position += 1
        self.stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    explorer = UI(stdscr)
    explorer.navigate()


if __name__ == "__main__":
    curses.wrapper(main)
