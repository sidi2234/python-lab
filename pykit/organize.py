import os
import sys
from pathlib import Path
import argparse


def parse_args():
    parser= argparse.ArgumentParser()
    parser.add_argument('--path',required=True,help="文件路径")
    parser.add_argument('--dry-run',action='store_true',help='只打印不移动')
    parser.add_argument('--by-date',action='store_true',help='按修改时间归档')
    return parser.parse_args()

def validate_path(path):
    p=Path(path)
    if not p.exists():
        sys.exit('当前路径不存在')
    if not p.is_dir():
        sys.exit("路径不是目录")
    resolved=p.resolve()
    if resolved.parent==resolved :
        sys.exit('无权访问根目录')

    if resolved==Path.home().resolve():
        sys.exit('无权访问用户主目录')

    windir=Path(os.environ.get('WINDIR',r"C:\Windows")).resolve()
    if resolved==windir or windir in resolved.parents:
        sys.exit('无权访问Windows目录')

    return resolved
blacklist={'node_modules','__pycache__'}
def is_blacklisted(p:Path)->bool:
    if p.name.startswith('.'):
        return True
    if any(part in blacklist for part in p.parts):
        return True
    return False
def scan(base:Path):
    for entry in base.iterdir():
        if is_blacklisted(entry):
            continue
        if entry.is_dir():
            yield from scan(entry)
        elif entry.is_file():
            yield entry

