#### ubuntu下更改DNS域名
/etc/resolv.conf

#### 确认系统架构
uname -m

#### 确认可执行文件的的架构，比如
file /system/bin/ip
file /system/lib/libiprouteutil.so

#### 安装posix手册
sudo apt install manpages-posix-dev

<<<<<<< Updated upstream
#### 同步文件
rsync -ah --info=progress2 --delete ./aosp-13 /media/luna/T7SSD/
=======
#### 移动硬盘挂载失败
sudo fsck.ext4 -f /dev/sda1
>>>>>>> Stashed changes
