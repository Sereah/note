##### 其他

internal 修饰的方法，在public之下，限制public的方法只能在模块内调用。

##### 循环

> [0,10] --> 0 .. 10

> [0,10) --> 0 until 10

> step 2 --> 递增2

```kotlin
fun main() {
	for (i in 0 until 10 step 2) {
		println(i)
	}
}
```

> [10, 0] --> 10 downTo 0



##### 面向对象

init{}中写主构造函数的逻辑。

constructor() 次构造函数，必须继承主构造函数，如果没有就继承父类的主构造函数。

 

> 数据类 --> data class
>
> 单例类 --> object class



##### lambda

> list集合

不可变集合：listOf()，只能读取不能增删。

可变集合：mutableListOf()

> set集合

不可变集合：setOf()，不能存放重复数据。

可变集合：mutableSetOf()，不能存放重复数据。

> map集合

```kotlin
val map = mapOf("a" to 1, "b" to 2, "three" to 3)
```



> Lambda表达式推导

lambda语法结构：{参数1：参数类型，参数2：参数类型 -> 函数体}

```kotlin
1.
val list = listOf("a","bb")
val lambda = {ele: String -> ele.length}
val maxByOrNull = list.maxByOrNull(lambda)
println(maxByOrNull)
```

```kotlin
2.lambda表达式替换
val list = listOf("a","bb")
val maxByOrNull = list.maxByOrNull({ele: String -> ele.length})
println(maxByOrNull)
```

```kotlin
3.lambda表达式是函数最后一个参数时，可以把lambda表达式移到()外面
val list = listOf("a","bb")
val maxByOrNull = list.maxByOrNull(){ele: String -> ele.length}
println(maxByOrNull)
```

```kotlin
4.lambda表达式是函数唯一一个参数时，可以移除()
val list = listOf("a","bb")
val maxByOrNull = list.maxByOrNull{ele: String -> ele.length}
println(maxByOrNull)
```

```kotlin
5.lambda表达式有参数类型推导机制，如果只有一个参数的时候可以不用申明参数，并且函数体的参数用it代替。
val list = listOf("a","bb")
val maxByOrNull = list.maxByOrNull{it.length}
println(maxByOrNull)
```



###### 函数式API

> map：将集合的元素映射成另外的值，映射规则在lambda函数体表示，最终生成一个新的集合。

```kotlin
val list = listOf("a","bb")
println(list.map { it.uppercase() })
//[A, BB]
```



> filter：过滤集合中的元素

```kotlin
val list = listOf("a","bb")
println(list.filter { it.length == 2 }.map { it.uppercase() })
//[BB]
```



> any：集合中元素至少一个满足条件。
>
> all：集合中所有元素满足条件。



###### java函数式api的使用

> 定义：kotlin中调用一个java方法，并且该方法接收一个 Java单抽象方法接口 参数，此时就可以使用函数式API。

```kotlin
例:Runnable接口就是单抽象方法接口。
//java实现Runnable接口
new Thread(new Runnable(){
    @Override
    public void run(){
        System.out.println("hello thread.")
    }
}).start()

//kotlin写法
Thread(object: Runnable {
    override fun run() {
        println("hello thread.")
    }
}).start()

//此时Thread的构造函数就符合函数式API的条件
Thread{
    println("hello thread.")
}.start()
```



##### kotlin的空指针控制

> kotlin将空指针判断提前到编译期，一切没有加?的参数变量都是非空。

例如：Int表示非空整型，Int?表示可为空的整型。

> 对象?.方法
>
> 对象不为空的时候正常调用方法，为空时什么也不做。

> val c = a ?: b
>
> a不等于null的时候赋值给c，a为空的时候b赋值给c。

> !!变量
>
> 此时告诉编译器变量一定不为空。



##### 函数默认参数

给函数的参数一个默认值，调用的时候如果不给这个参数传值，就会用默认的，省去了次构造函数的作用。



##### 延迟初始化

> 判断adapter是否初始化

```
::adapter.isInitialized
```

##### sealed class 密封类

> 判断完子类中所有条件，不需要else

##### 扩展函数

```
fun ClassName.function(){}
```

##### 高阶函数

```kotlin
fun main(args: Array<String>) {
    val resultPlus = numberDemo(1,2,::plus)
    println(resultPlus)	
    println(numberDemo(1,2,::minus))
}

fun numberDemo(num1: Int, num2: Int, operation: (Int, Int) -> Int): Int {
    return operation(num1, num2)
}

fun plus(num1: Int, num2: Int): Int {
    return num1 + num2
}

fun minus(num1: Int, num2: Int): Int {
    return num2 - num1
}
```

> 使用lambda表达式替换函数

```
fun main(args: Array<String>) {

    println(numberDemo(1, 2) { n1, n2 ->
        n1 + n2
    })
    println(numberDemo(1, 2) { n1, n2 ->
        n2 - n1
    })
}

fun numberDemo(num1: Int, num2: Int, operation: (Int, Int) -> Int): Int {
    return operation(num1, num2)
}


```

> 在字节码文件中，每个lambda表达式都会生产一个匿名函数，使用内敛函数inline的方式可以消除匿名函数带来的开销。
>
> 内联函数原理是：
>
> 1. 在运行时把lambda表达式的代码替换到函数类型参数调用的地方。
> 1. 然后把内联函数的代码替换到调用内联函数的地方。

```kotlin
fun main(args: Array<String>) {

    var start = System.currentTimeMillis()
    println(numberDemo(1, 2) { n1, n2 ->
        n1 + n2
    })
    println(numberDemo(1, 2) { n1, n2 ->
        n2 - n1
    })

    var end = System.currentTimeMillis()

    println("const ${end - start} ms")
}

inline fun numberDemo(num1: Int, num2: Int, operation: (Int, Int) -> Int): Int {
    return operation(num1, num2)
}
```

```
3
1
const 0 ms
```

```kotlin
fun main(args: Array<String>) {

    var start = System.currentTimeMillis()
    println(numberDemo(1, 2) { n1, n2 ->
        n1 + n2
    })
    println(numberDemo(1, 2) { n1, n2 ->
        n2 - n1
    })

    var end = System.currentTimeMillis()

    println("const ${end - start} ms")
}

fun numberDemo(num1: Int, num2: Int, operation: (Int, Int) -> Int): Int {
    return operation(num1, num2)
}
```

```
3
1
const 3 ms
```

> 使用内联函数之后运行时间明显快了。
>
> 不使用内联则在lambda表达式前面加上noinline。
>
> 内联的函数类型参数在编译的时候会进行代码替换，也就是没有真正的参数属性，不能进行参数传递。
>
> 内联函数所引用的lambda可以进行参数返回（返回的是lambda上一级函数），非内联函数的lambda只能进行局部返回（返回lambda内部）。

> 高阶函数创建了匿名类或者lambda表达式，使用inline就会报错，因为内联函数允许lambda使用return，而高阶函数的匿名函数不允许使用return产生冲突。
>
> 在高阶函数的函数类型参数前加上crossinline解决冲突，表示一定不会在高阶函数的匿名函数中使用return，但可以使用局部return@function

##### 标准函数

> 标准函数指Standara.kt中的函数，可以自由调用标准函数。

###### 作用域函数

> 标准函数中有一部分函数唯一目的是在对象的上下文中执行代码块。但一个对象调用作用域函数并且提供一个lambda表达式的时候，会形成一个作用域，在此作用域中访问对象而不需要对象名。

###### let

```kotlin
fun doStudy(study: Study?){
    study?.let {
        it.doHomework()
        it.readBooks()
    }
}
```

###### with

```kotlin
with(obj){
            // 这里是 ojb 的上下文
            "value" // with 函数的返回值
}
```

###### run

与with类似，with是传入对象参数，run是对象调用run函数。

```kotlin
fun printFruits(){
    val list = listOf("Apple", "Banana", "Orange", "Pear", "Grape")
    val result = StringBuilder().run {
        append("Start eating fruits. \n")
        for (fruit in list) {
            append(fruit).append("\n")
        }
        append("Ate all fruits.")
        toString()
    }
    println(result)
}
```

###### apply

与run类似，对象调用apply函数，但是返回的是对象本身，而with和run返回的是最后一行代码。

```kotlin
fun printFruits(){
    val list = listOf("Apple", "Banana", "Orange", "Pear", "Grape")
    val result = StringBuilder().apply {
        append("Start eating fruits. \n")
        for (fruit in list) {
            append(fruit).append("\n")
        }
        append("Ate all fruits.")
    }
    println(result.toString())
}
```

###### also

与let用法一样，不同点是let返回最后一行代码，also返回对象本身，可以用作链式调用。

```kotlin
fun getRandomInt(): Int {
    return Random.nextInt(100).also {
        writeToLog("getRandomInt() generated value $it")
    }
}

val i = getRandomInt()
```

###### takeIf和takeUnless

可以将对象嵌入到调用链中做状态检查。

takeIf -> 符合的话就返回对象本身，不符合返回null。

takeUnless -> 符合返回null，不符合返回对象本身。

```kotlin
val str = "Hello"
val caps = str.takeIf { it.isNotEmpty() }?.toUpperCase()
println(caps)
```



##### ViewModel

> viewModel通过ViewModelProvider获取对象，因为ViewModel生命周期不与activity绑定。

```kotlin
lateinit var viewModel: CountViewModel
viewModel = ViewModelProvider(this, CountViewModelFactory(countReserved)).get(CountViewModel::class.java)
```

使用步骤：

```kotlin
//1. 创建activity对应的viewModel：
countViewModel(countReserved : Int) : ViewModel() {}
//2. 创建viewModel对应的factory：
CountViewModelFactory(private val countReserved : Int) : ViewModelProvider.Factory {
	override fun <T : ViewModel?> create(modelClass : Class<T>) : T {
        return CountViewModel(countReserved) as T
    }
}
//3. acitivity中使用SharePreference保存数据，下次重建activity的时候取出并传递给factory用于初始化：
lateinit var viewModel: CountViewModel
private lateinit var sp: SharedPreferences
sp = getPreferences(Context.MODE_PRIVATE)
val countReserved = sp.getInt("count_reserved", 0)
viewModel = ViewModelProvider(this, CountViewModelFactory(countReserved)).get(CountViewModel::class.java)
```



##### SharedPreference

获取SharedPreference对象：

> 当使用多个SharedPreference时使用。

```kotlin
getSharedPreferences(name : String, mode : Int)
```

> 当使用一个对象时使用。

```
getPreferences(mode : Int)
```

###### mode参数：

> MODE_PRIVATE：默认方式，只能被创建的应用程序或者与创建的应用程序具有相同用户 ID 的应用程序访问。
>
> MODE_WORLD_READABLE：允许其他应用程序对该 SharedPreferences 文件进行读操作。
>
> MODE_WORLD_WRITEABLE：允许其他应用程序对该 SharedPreferences 文件进行写操作。
>
> MODE_MULTI_PROCESS：在多进程应用程序中，当多个进程都对同一个 SharedPreferences 进行访问时，该文件的每次修改都会被重新核对。









