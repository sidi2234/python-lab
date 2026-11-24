import sys

from organize import parse_args, validate_path, list_targets, target_dir_for, unique_path, move_one


def main():
    args=parse_args()
    src=validate_path(args.path)
    files,skipped=list_targets(src)
    ok=0
    failed=[]
    for f in files:
        dst_dir=target_dir_for(f,src,args.by_date)
        dst=dst_dir/f.name
        if dst.exists():
            dst=unique_path(dst)
        try :
            move_one(f,dst,args.dry_run)
            ok+=1
        except OSError as e:
            failed.append((f,e))
    print('----')
    print(f"{'计划移动' if args.dry_run else '移动'} {ok}个,失败{len(failed)}个,跳过隐藏文件和目录{skipped}个")
    for f ,e in failed:
        print(f"   - {f.name}: {e}")

    sys.exit(0 if not failed else 1)



if __name__=='__main__':
    main()