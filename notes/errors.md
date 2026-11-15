## 1.ModuleNotFoundError:
- 报错最后一行: No module named 'requests'
- 我以为:其实我写入import requests时pycharm自己就报错了,然后直接告诉我我没安装这个库
- 真正原因:装到conda的Python上了



## 2.IndentationError
- 报错最后一行:unindent does not match any outer indentation level
- 这个pycharm也直接报错告诉我缩减不对,在运行程序之前就能修改
- 真正原因:缩进不对,导致后面if判断的代码结构不对

## 3.TypeError:
- 报错最后一行:'NoneType' object is not subscriptable
- 我以为是:其实我并不知道这个是什么类型的报错,单看NoneType感觉就是没有这个类型
- 真正原因:函数返回是None,不能取下标
- 怎么发现的:通过断点调试

## 4.FileNotFoundError
- 报错最后一行:No such file or directory
- 真正原因:在程序中打开文件是相对路径+cwd,在终端中cd到上一级目录,缺少路径找不到文件