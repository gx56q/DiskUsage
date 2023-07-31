import argparse
import progressbar
import du


def parse_args():
    parser = argparse.ArgumentParser(description='Disk Usage')
    parser.add_argument('path', type=str, help='Path to directory')
    return parser.parse_args()


class Main:
    def __init__(self):
        self.args = parse_args()
        self.du = du.DU(self.args.path)


if __name__ == '__main__':
    Main()
