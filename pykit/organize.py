import shutil
from datetime import datetime
import os
import sys
from pathlib import Path
import argparse

BLACKLIST={"node_modules", "__pycache__"}
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
def list_targets(src:Path):
    target_list,skipped=[],0
    for entry in src.iterdir():
        if entry.name.startswith('.') or entry.name in BLACKLIST:
            skipped+=1
            continue
        if entry.is_file():
            target_list.append(entry)
    return target_list,skipped

def target_dir_for(f,src,by_date):
    if by_date:
        mtime= f.stat().st_mtime
        d_time=datetime.fromtimestamp(mtime)
        s=d_time.strftime("%Y-%m")
        return src/s
    s=f.suffix.lstrip(".").lower() or "no_suffix"
    return src/s

def unique_path(dst:Path)->Path:
    i=1
    while True:
        candidate=dst.with_name(f"{dst.stem} ({i}){dst.suffix}")
        if not candidate.exists():
            return candidate
        i+=1

def move_one(f,dst,dry_run)->None:
    if dry_run:
        print(f"[DRY] {f.name}->{dst.parent}/")
        return
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.move(str(f),str(dst))
    print(f"[OK] {f.name}->{dst.name}")
