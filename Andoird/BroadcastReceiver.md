# BroadcastReceiver

#### 有序广播（ordered broadcasts）

：同步执行的广播，接收者有优先级的先后顺序，广播可以被截断。

#### 标准广播（normal broadcasts）

：异步执行的广播，接收者同时收到，不会被截断。



#### 接收广播

##### 静态注册

：在AndroidManifest中注册，全局生效。

```xml
<uses-permission android:name = "android.permission.RECEIVE_BOOR_COMPLETED" />
...
<receiver
          android:name = ".BootCompleteReceiver"
          android:enable = "true"
          android:exported = "true">
	<intent-filter>
    	<action android:name = "android.intent.action.BOOT_COMPLETED" />
    </intent-filter>
</receiver>
```

##### 动态注册

：代码中注册，activity关闭后失效。

```kotlin
//监听系统时间变化的广播
class MainActivity : AppCompatActivity() {
    lateinit var timeChangeReceiver : TimeChangeReceiver
    
    override fun onCreate(saveInstanceState : Bundle?) {
        super.onCreate(saveInstanceState)
        setContentView(R.layout.activity_main)
        val intentFilter = IntentFilter()
        intentFilter.addAction("android.intent.action.TIME_TICK")
        timeChangeReceiver = TimeChangeReceiver()
        registerReceiver(timeChangeReceiver, intentFilter)//注册
    }
    
    override fun onDestory() {
        super.onDestory()
        unregisterReceiver(timeChangeReceiver)//取消注册
    }
}

inner class TimeChangeReceiver : BroadcastReceiver() {
    override fun onReceive(intent : Intent, context : Context) {
        //TODO
    }
}
```



#### 发送广播

##### 发送标准广播

```kotlin
val intent = Intent("com.example.broadcasettest.MY_BROADCASET")
intent.setPackage(packageName)//自定义的广播都是隐式的，需要指定接收的apk，不然静态注册接收不到隐式广播
sendBroadcast(intent)
```

##### 发送有序广播

```
val intent = Intent("com.example.broadcasettest.MY_BROADCASET")
intent.setPackage(packageName)//自定义的广播都是隐式的，需要指定接收的apk，不然静态注册接收不到隐式广播
sendOrderedBroadcast(intent, null)
```

```kotlin
//接收放静态注册,设置优先级 100
<intent-filter android:priority = "100">
	<action android:name = "android.intent.action.BOOT_COMPLETED" />
</intent-filter>

override fun onReceive(context : Context, intent : Intent) {
    ...
    abortBroadcast()//截断广播
}
```

