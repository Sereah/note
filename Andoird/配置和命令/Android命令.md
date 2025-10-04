#### 查看apk包
adb shell pm list packages -a -f |grep com.xxx.xxxx

#### 查看系统android版本
adb shell getprop ro.build.version.release

#### adb进入QNX，视不同的项目而定
busybox telnet 172.31.207.204

#### adb查看包里包含指定action的activity
dumpsys package com.zone.hmi.settings | grep -A 10 "android.intent.action.MAIN"

#### 查看activity启动时间
adb shell am start -W <Activity>

#### Android黑白夜切换
cmd uimode night yes

#### 系统属性设置/查看
getprop/setprop sys.carplay.route

#### 手动加载驱动
insmod usbmfi.ko

#### 查看RRO对应关系
cmd overlay list
cmd overlay dump <package>


#### Carplay开发命令

##### 查看mfi usb驱动状态
dmesg |grep usbmfi

##### 有线连接前切换对应USB口为主机模式，插上CP后，CP会将USB口切换为从设备模式
echo host > /sys/devices/platform/soc/a800000.ssusb/mode

##### USB连接需要将USB网卡添加到路由，这个视不同的项目而定
ip -6 route add default dev mfincm0 table local_network proto static scope link metric 512

