#### 拉取Android源码
repo init -u https://android.googlesource.com/platform/manifest -b android-14.0.0_r33 --repo-url clone.bundle

#### 拉取AOSP Car-libs源码
repo init -u https://android.googlesource.com/platform/manifest -b ub-automotive-master-20231102 --repo-url clone.bundle

#### AOSP切换分支
1. cd .repo/manifests
2. git branch -a | cut -d / -f 3
查看manifest里存在哪些分支，通过repo init重新初始化然后sync

#### 给pixel下载驱动

1. 在https://source.android.com/docs/setup/reference/build-numbers?hl=zh-cn 找到对应分支的buildID
2. 在https://developers.google.com/android/drivers?hl=zh-cn 根据buildID找到对应pixel版本的两个驱动文件(google和Qualcomm)
3. 将两个驱动的脚本放到aosp根目录并执行
4. make编译

#### libncurses.so.5问题

- 问题：高版本ubuntu默认带有libncurses6，没有5，aosp10编译找不到libncurses.so.5。
- 解决办法：
cd /usr/lib/x86_64-linux-gnu/
sudo ln -s libncurses.so.6 libncurses.so.5
sudo ln -s libtinfo.so.6 libtinfo.so.5

#### fastboot刷机

1. adb reboot bootloader
2. export ANDROID_PRODUCT_OUT=<img路径>
3. fastboot flashall -w

