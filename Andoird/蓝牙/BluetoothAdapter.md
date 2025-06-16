#### EXTRA_PREVIOUS_STATE

```java
    public static final String EXTRA_PREVIOUS_STATE =
            "android.bluetooth.adapter.extra.PREVIOUS_STATE";
```

蓝牙状态变化时前一个状态，比如从ON->OFF,则PREVIOUS_STATE为ON, STATE为OFF。


#### ACTION_CONNECTION_STATE_CHANGED

不关心本地设备连接了哪个profile，只关心连接状态可以使用，配合`getConnectionState`主动获取状态，依然只是知道是否已连接，并不知道连接的是哪个远程设备，想要知道每个远程设备的连接情况，需要注册每个profile的代理监听，首次建立代理也能马上获取到连接信息。


#### ACTION_BLUETOOTH_ADDRESS_CHANGED

广播本地设备蓝牙地址变化，蓝牙地址可以使用随机地址


#### getBluetoothLeAdvertiser()

它用于获取BLE广告控制器，使设备能主动广播 BLE 信号（成为外围设备/Peripheral）。


#### isBleScanAlwaysAvailable

低功耗蓝牙是否一致扫描，哪怕经典蓝牙关闭。
由飞行模式和settings global属性`ble_scan_always_enabled`控制


#### disable(boolean persist)

关闭蓝牙可以设置下次开机后是否仍然保持关闭状态，默认是true。


#### getIoCapability/setIoCapability

设置蓝牙设备的交互能力：
1. IO_CAPABILITY_OUT=0, 只显示
2. IO_CAPABILITY_IO=1, 输入显示
3. IO_CAPABILITY_IN=2, 只输入
4. IO_CAPABILITY_NONE=3, 无输入显示能力
5. IO_CAPABILITY_KBDISP=4, 显示和键盘
6. IO_CAPABILITY_MAX=5, 全能力
7. IO_CAPABILITY_UNKNOWN=255


#### ActiveDevice

setActiveDevice/removeActiveDevice，一般用于多设备连接时


