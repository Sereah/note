#### 一、JVM与Java体系结构	

> JVM: Java Virtual Machine

Java7后，通过JSR-292规范基本实现Java虚拟机平台上运行非Java语言编写的程序。

##### JVM整体结构

![第02章_JVM架构-简图](png/第02章_JVM架构-简图.jpg)

##### JVM架构模型

1. 基于栈式架构，采用零地址指令。

> 不同CPU的架构不同，所以不使用寄存器架构。优点是易实现，指令集小，可跨平台，缺点是性能下降。

##### JVM的生命周期

1. 虚拟机的启动

通过引导类加载器（bootstrap class loader）创建一个初始类（initial class）来完成。

2. 虚拟机的执行

执行java程序也就是执行虚拟机进程。

3. 虚拟机的退出

正常执行结束、异常终止、OS错误终止、线程调用Runtime类/System类的exit方法，或Runtime类的halt方法。



#### 二、类加载子系统

##### 类加载器与类加载的过程

![第02章_JVM架构-英](png/第02章_JVM架构-英.jpg)

![第02章_JVM架构-中](png/第02章_JVM架构-中.jpg)

###### 类加载器的作用

1. 加载class文件，是否可运行，由执行引擎决定。
2. 加载的类信息放在**方法区**中。

###### 类的加载过程

![第02章_类的加载过程](png/第02章_类的加载过程.jpg)

> 加载

1. 通过一个类的全限定名获取定义此类的二进制字节流。
2. 将这个字节流代表的静态存储结构转化为方法区的运行时数据结构。
3. 在内存中生成一个代表这个类的java.lang.Class对象，作为方法区中这个类的访问入口。

> 链接

1. **验证**，确保class文件中的字节流中包含信息符合当前虚拟机要求，包括文件格式验证、元数据验证、字节码验证、符号引用验证。
2. **准备**，为**类变量**分配内存地址并初始化值。（不包含final修饰的变量，因为final是在编译的时候分配了内存，也不包含实例变量，实例变量随对象分配在堆中，而不是方法区中）
3. **解析**，将常量池中的符号引用转换为直接引用。（直接引用，即执行目标的指针，相对偏移量等）

> 初始化

执行类构造器方法<clinit>()，此方法是javac编译器自动收集类中的所有**类变量的赋值动作和静态代码块**合并而来，此方法会同步加锁。



##### 类加载器的分类

**Java虚拟机规范定义两类**：

1. 引导类加载器（Bootstrap ClassLoader）
2. 自定义加载器：派生于ClassLoader的类加载器



**虚拟机自带的加载器**：

1. **引导类加载器 Bootstrap ClassLoader**	

使用C/C++实现，嵌套在JVM中。

用来加载Java核心库，用于提供JVM自身需要的类。(JAVA_HOME/jre/lib/rt.jar、resources.jar或sun.boot.class.path)

```java
URL[] urLs = Launcher.getBootstrapClassPath().getURLs();
        for (URL ele: urLs) {
            System.out.println(ele.toExternalForm());
        }
```

```
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/lib/resources.jar
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/lib/rt.jar
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/lib/sunrsasign.jar
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/lib/jsse.jar
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/lib/jce.jar
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/lib/charsets.jar
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/lib/jfr.jar
file:/C:/Program%20Files/Java/jdk1.8.0_301/jre/classes
```

并不继承于java.lang.ClassLoader，没有父加载器。

加载扩展类和应用程序类加载器，并指定为它们的父加载器。

2. **扩展类加载器 Extension ClassLoader**

Java语言编写，由sun.misc.Launcher$ExtClassLoader实现。

从**java.ext.dirs系统属性**所指定的路径加载类库，或从jdk安装目录的jre/lib/ext子目录下加载类库。

```java
        String property = System.getProperty("java.ext.dirs");
        for (String path: property.split(";")) {
            System.out.println(path);
        }
```

```
C:\Program Files\Java\jdk1.8.0_301\jre\lib\ext
C:\windows\Sun\Java\lib\ext
```

派生于ClassLoader类，父加载器为引导类加载器。

3. **应用程序类加载器 AppClassLoader**（系统类加载器）

Java语言编写，由sun.misc.Launcher$AppClassLoader实现。

加载环境变量classpath或系统属性**java.class.path**指定路径下的类库。

派生于ClassLoader类，父加载器为扩展类加载器。

是程序默认的类加载器，通过ClassLoader#getSystemClassLoader()方法获取该类加载器。

4. **自定义加载器**

   目的：隔离加载类，修改类加载的方式，扩展加载源，防止源码泄露。

###### 获取ClassLoader的途径

> 获取当前类的classloader：clazz.getClassLoader()
>
> 获取当前线程上下文的classloader：Thread.currentThread().getContextClassLoader()
>
> 获取系统的classloader：ClassLoader.getSystemClassLoader()
>
> 获取调用者的classloader：DriverManager.getCallerClassLoader()

##### 双亲委派机制

![image-20221025171920108](png/双亲委派机制)



##### 其他

###### 在JVM中，表示两个class对象是否为同一个类的条件：

1. 类名含包名一致。
2. 加载此类的classloader一样。

###### Java程序对类的使用：主动和被动

> 主动：

1. 创建类的实例
2. 访问类或接口的静态变量，以及赋值
3. 调用类的静态方法
4. 反射
5. 初始化一个类的子类
6. Java虚拟机启动时被标明为启动类的类
7. jdk 7开始提供的动态语言支持：java.lang.invoke.MethodHandle实例的解析结果，REF_getStatic、REF_putStatic、REF_invokeStatic句柄对应的类没有初始化，则初始化

> 被动

others
