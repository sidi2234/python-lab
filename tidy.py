import argparse
import os
import sys
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser(description='按扩展名统计文件数量')
    parser.add_argument('--path', required=True, help="要扫描的目录")
    parser.add_argument('--dry-run', action="store_true", help="只统计不修改数量")
    parser.add_argument('--top', type=int, default=None, help="显示前top个文件")
    return parser.parse_args()


def iter_files(path: str):
    for root, dirs, files in os.walk(path):
        for f in files:
            yield os.path.join(root, f)


def collect_stats(files):
    stats = defaultdict(lambda: [0, 0])
    for f in files:
        try:
            size = os.path.getsize(f)
        except OSError as e:
            print(f"警告:跳过{f}({e})", file=sys.stderr)
            continue
        ext = os.path.splitext(f)[1].lower() or "(无扩展名)"
        stats[ext][0] += 1
        stats[ext][1] += size
    return stats

def format_size(n):
    units=["B","KB","MB","GB","TB"]
    i=0
    while n>=1024 and i<len(units)-1:
        n=n/1024
        i=i+1
    return str(n)+units[i]




def main():
    args = parse_args()
    # print(args.path)
    # print(args.dry_run)
    # print(args.top)
    if not os.path.isdir(args.path):
        print(f"错误:目录不存在或不是目录:{args.path}", file=sys.stderr)
        sys.exit(1)
    if not os.access(args.path, os.R_OK):
        print(f"错误:没有读取权限:{args.path}", file=sys.stderr)
    files = iter_files(args.path)
    stats = collect_stats(files)

    print(stats)


if __name__ == "__main__":
    main()
