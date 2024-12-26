# Service

#### 多线程的基本用法

```kotlin
//继承Thread
class MyThread : Thread() {
    override fun run() {
        //TODO
    }
}

new MyThread().start()


//实现Runnable接口
class MyThread : Runnable {
    override fun run() {
        //TODO
    }
}

val myThread = MyThread()
Thread(myThread).start()

//lambda
Thread {
    //TODO
}.start()


//Android kotlin
thread {
    //TODO
}
```

#### 在子线程更新UI

##### 异步消息处理机制

###### 1. Message

：线程之间传递信息。

> message.what  //用于传递消息代码，用于识别
>
> message.arg1(arg2)  //用于传递int型值
>
> message.obj  //用于传递对象

###### 2. Handler

：用于发送和处理消息。

> sendMessage()
>
> post()
>
> handleMessage()

###### 3. MessageQueue

：消息队列，用于存放所有通过handler发送的消息，一个线程只有一个MessageQueue对象。

###### 4. Looper

：消息队列的管家，将消息队列中的消息取出传递给Handler的handleMessage()方法。每个线程只有一个looper对象。

```kotlin
val messageCode = 1
val handler = object : Handler(Looper.getMaininLooper()) {
    override fun handleMessage(msg : Message) {
        when (msg.what) {
            //TODO
        }
    }
}

thread {
    val msg = Message()
    msg.what = messageCode
    handler.sendMessage(msg)
}
```

##### 使用AsyncTask

```kotlin
abstract class AsyncTask<Params, Progress, Result>() {}
//Params 传给后台使用的参数
//Progress 进度单位
//Result 结果返回类型
```

###### 1. onPreExecute()

：在后台任务执行开始前调用，界面上的初始化操作。

###### 2. doInBackground(Params...)

：子线程中运行，执行耗时任务，通过return返回结果，UI操作调用**publishProgress(Progress...)**方法。

###### 3. onProgressUpdate(Progress...)

：当后台任务调用了publishProgress()方法后，此方法被调用，Progress参数由后台传递。

###### 4. onPostExecute(Result)

：后台return的数据作为参数传入方法中。



<!--Unit 不需要传入传出参数，类似于void-->

<!--vararg 可变参数（可以传入一个数组）-->

```kotlin
class DownloadTask : AsyncTask<Unit, Int, Boolean>(){
    
    override fun onPreExecute() {
        progressDialog.show()
    }
    
    override fun doInBackground(vararg params : Unit?) = try{
        while(true) {
            val downloadPercent = doDownload() //返回int类型的方法
            publishProgress(downloadPercent)
            if (downloadPercent >= 100) {
                break
            }
        }
        true
    }catch (e : Exception) {
        false
    }
    
    override fun onProgressUpdate(vararg values : Int?) {
        progressDialog.setMessage("Download ${valuse[0]}%")
    }
    
    override fun onPostExecute(result : Boolean) {
        progressDialog.dismiss()
        if (result) {
            //TODO
        }else {
            //TODO
        }
    }
}
```

