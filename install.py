# -*- coding utf-8 -*-
# @Time    : 2020/11/21 16:11
# @Author  : DesireYang
# @Email   : yangyin1106@163.com
# @File    : toExcel.py
# Software : PyCharm
# Explain  : 打包
from PyInstaller.__main__ import run


# -F:打包一个单个文件，如果你的代码都写在一个.py文件的话，可以用这个，如果是多个.py文件就别用
# -D, –onedir 打包多个文件，在dist中生成很多依赖文件，适合以框架形式编写工具代码，我个人比较推荐这样，代码易于维护
# -w:不带console输出控制台，window窗体格式
# --paths：依赖包路径('--paths=./py_xmind_env')
# --icon：图标
# --noupx：不用upx压缩
# --clean：清理掉临时文件

def install1():
    opts = ['-D', '-w', r'--icon=.\Icon\window.ico',
            '--noupx', '--clean',
            r'D:\VSCodeWorkspace\py-xmind\pyxMind.py']
    run(opts)


def install2():
    opts = ['-D', '-F', r'--paths=D:\ProgramData\Anaconda3\envs\py_xmind_env',
            '--noupx', '--clean',
            r'pyxMind.py']
    run(opts)


if __name__ == '__main__':
    install2()
