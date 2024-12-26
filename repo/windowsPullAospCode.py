import xml.dom.minidom

import os

from subprocess import call

# 1. 修改为源码要保存的路径
rootdir = "E:/workspace/AOSP/ub"
# 2. 设置 git 安装的路径
git = "D:/Git/bin/git.exe"
# 3. 修改为第一步中 manifest 中 default.xml 保存的路径
dom = xml.dom.minidom.parse("E:/workspace/AOSP/manifest/default.xml")

root = dom.documentElement

# 4. 没有梯子使用清华源下载
prefix = git + " clone https://android.googlesource.com/"
# prefix = git + " clone https://aosp.tuna.tsinghua.edu.cn/"

suffix = ".git"  

if not os.path.exists(rootdir):  

    os.mkdir(rootdir)  

for node in root.getElementsByTagName("project"):  

    os.chdir(rootdir)  

    d = node.getAttribute("path")  

    last = d.rfind("/")  

    if last != -1:  

        d = rootdir + "/" + d[:last]  

        if not os.path.exists(d):  

            os.makedirs(d)  

        os.chdir(d)  

    cmd = prefix + node.getAttribute("name") + suffix  

    call(cmd)