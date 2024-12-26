---
typora-root-url: png
---

# Activity

###### lifetime：

```
onCreate(), onStart(), onResume(), onPause(), onStop(), onDestory(), onRestart()
```

<img src="/activity生命周期.png" alt="activity生命周期" style="zoom:50%;"/>

#### AndroidManifest

```kotlin
android:exported//包含<intent-filter>，默认为true，不包含默认为false。是否允许其他应用调用此组件。

android:label//activity的名字

<intent-filter>
	<action android:name="android.intent.action.MAIN" />
	<category android:name="android.intent.category.LAUNCHER" />
</intent-filter>
```

#### 插件

>
> id 'kotlin-android-extensions' //简化findViewById

#### Activity的启动

##### 显式启动

```kotlin
Intent(Context packageContext, Class<?> cls)

val intent = Intent(this, SecondActivity::class.java)
startActivty(intent)
```



##### 隐式启动

###### Action和Category

> Action：表示启动窗口时符合的动作。
>
> Category：表示启动窗口时符合的类别。

每个intent只能指定一个action，但可以有多个category

```kotlin
val intent = Intent("com.example.activitytest.ACTIONS_START")
intent.addCategory("com.example.activitytest.MY_CATEGORY")
intent.addCategory("com.example.activitytest.MY_CATEGORY")
startActivity(intent)
```

默认category

```kotlin
android.intent.category.DEFAULT
```

intent同时满足action和category，没有指定category，自动添加默认的category。



###### 从目标activity获得返回值

：Activity_A通过startActivityForResult()去启动Activity_B

：Activity_B在finish之前，通过setResult()传递参数给Activity_A

：Activity_A通过重写onActivityResult()拿到返回值

```java
Activity_A:

Intent intent = new Intent(this, Activity_B.class);
startActivityForResult(intent, requestCodeA);

@Override
protected void onActivityResult(int requestCode, int resultCode, Intent data){
    super.onActivityResult(requestCode, resultCode, data);
    if(resultCode == RESULT_OK && requestCode == requestCodeA) {
        //TODO
    }
}
```

```
Activity_B：

Intent intent = new Intent();
intent.putExtra("result", "...result...");
setResult(RESULT_OK, intent);
finish();
```

*Activity_A去启动Activity_B时，Activity_A的onPause()先调用，紧接着依次执行Activity_B的onCreate(), onStart(), onResume()，最后才执行Activity_A的onStop()。*

#### 启动模式

###### Standard

：默认模式，新启动的activity放在返回栈顶，同一个activity能被实例化多次。

###### singleTop

：栈顶复用模式，如果当前activity在栈顶，则不创建新的activity，复用存在的activity。

###### singleTask

：栈内复用模式，如果当前activity在栈内存在，则不创建新的activity，把栈内存在的activity复用，并清除自身实例上面的activity（LAUNCHER Activity除外）。

###### singleInstance

：单独栈模式，当前activity会创建一个新的单独的返回栈。

##### 启动模式配置

###### 清单文件配置

```xml
launchMode = “standard”
```

###### intent配置

```java
//singleInstance
intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

//singleTop
intent.addFlag(Intent.FLAG_ACTIVITY_SINGLE_top);

//singleTask
intent.addFlag(Intent.FLAG_ACTIVITY_CLEAR_TOP);
```

