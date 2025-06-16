### main函数

```C
#include <stdio.h>

int main(int argc, char *argv[])
{
    printf("---%d, %s \n", argc, argv[0]);
    return 0;
}
```
- argc: 表示传递给程序的参数个数，最小值1，第一个参数是程序名称。
- argv: 传递给程序的所有参数数组，第一个参数argv[0]是程序名称。

1. 从main函数返回时，将返回到shell进程，也就是程序的父进程。
2. main的返回值将临时保存在shell的变量`?`中，通过`echo $?`可以打印返回值。


### man手册

> sudo apt install manpages-posix-dev

1. 第一章节：用户命令，比如`man 1 ls`
2. 第二章节：系统调用，比如`man 2 open`
3. 第三章节：库函数，比如`man 3 printf`
4. 第四章节：设备驱动程序，位于/dev中的
5. 第五章节：文件格式和规范，位于/etc
6. 后续还有其他的，可以通过`man man`查看帮助信息

man手册使用分页查看器, 快捷键有：
- 上下键：一行一行滚动
- 空格键：向下一页（一个屏幕）滚动
- b键：向上一页滚动
- /键：开启关键字搜索
- n键：搜索后跳转到下一个关键字
- q键：退出

#### apropos命令

快速查找man手册中需要的关键字：`apropos [选项] 关键字`

常用选项：
1. -a：与，同时满足所有关键字
2. -s：在指定章节搜索

#### whatis命令

快速查看指定关键字的描述：`whatis getopt`


### 使用程序的返回值

`test -e 文件夹名`可以测试是否存在某个文件夹，存在时返回0，否则返回1，可以写出下列脚本去使用返回的结果`$?`然后打印信息。

```shell
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "has not argument."
    exit 1
fi

test -e "$1"
if [ "$?" -eq 0 ]; then
    echo "exist!!!"
elif [ "$?" -eq 1 ]; then
    echo "not exist..."
    exit 3
else 
    echo "unknow result from test."
    exit 1
fi

exit 0
```

- `$#`表示传入shell脚本的命令行参数个数，类似于main函数的argc，**但是不包含shell本身，最小值是0**。
- `$1`表示传入shell脚本的第一个参数，其中$0代表shell本身。


### 标准输入输出，标准错误

1. 标准输出：`stdout`, 文件描述符1。
```shell
ls /home 1> result.text //将标准输出结果重定向到文本里，其中1可以不写，默认是1
```
2. 标准错误：`stderr`, 文件描述符2。
```shell
ls /homew 2> result.text //将标准错误结果重定向到文本里
```
3. 标准输入：`stdin`, 文件描述符0。
```shell
wc 0< result.text //将标准输入重定向，0可以不写，默认是0
```
> 使用`&>`可以将标准输出和标准错误一起重定向

#### printf和fprint和dprintf

```c
int printf(const char *format, ...);
int fprintf(FILE *stream, const char *format, ...);
int dprintf(int fd, const char *format, ...);
```
- printf函数会将字符串打印到标准输出
- fprintf函数可以打印到指定的文件流
- dprintf函数传入的就不是文件流的名字，而是文件描述符

> /dev/null 是一个特殊的文件，类似于黑洞，重定向到这里的内容都消失了，可以用来过滤
> 引入unistd.h，则可以用`STDIN_FILENO`, `STDOUT_FILENO`, `STDERR_FILENO`三个宏传入dprintf

#### fgets

```c
#include <stdio.h>

int main(int argc, char *argv[])
{
    char input[1024];
    if(fgets(input, 1024, stdin) != NULL) 
    {
        printf("your input is: \n");
        printf("%s\n", input);
    }
    return 0;
}
```

fgets标准输入函数：`char *fgets(char *s, int size, FILE *stream)` 

1. `*s`传入存储输入字符的数组
2. `size`传入字符的最大个数
3. `*stream`传入输入流stdin
4. 如果读取到了字符则返回指针，否则返回NULL


### GCC编译链接库

1. 定义头文件
```c
int myLib(int num);
```

2. 实现函数
```c
int myLib(int num)
{
    if(num == 18)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}
```

3. 使用`gcc -fPIC -c myLib.c`生成无关位置的.o文件
4. 打包为链接库：`gcc -shared -Wl,-soname,libmyLib.so -o libmyLib.so myLib.o`
5. 使用链接库：`gcc -L${LD_LIBRARY_PATH} main.c -o main -lmyLib`,其中-L后面跟链接库的位置，结尾-l后面跟链接库的名字

> 使用`ldd 执行文件`可以查看使用了哪些链接库


### 编译切换C标准

1. 使用`gcc -std<参数>`切换编译C标准
2. 始终使用`gcc -Wall -Wextra -pedantic`选项参与编译


### 系统调用

1. 头文件`unistd.h`
2. 举例使用系统函数`write`: ssize_t write(int fd, const void *buf, size_t count);

> `size_t`参数表示字符的缓冲区大小，不能超出，否则警告，比如`hello, world\n`的长度是13
```c
#include <unistd.h>

int main(void)
{
    write(1, "hello, world\n", 13);
    return 0;
}
```

3. 其他头文件：`sys/types.h`包含用户id的uid_t等, `sys/sysinfo.h`用于sysinfo函数，非linux的unix不可用，比如macos。`

> `man sys_types.h`查看types。
> 系统调用出错时都返回-1
> POSIX头文件手册是手册的一个特殊部分，没有在man man中列出。在Fedora和CentOS下，这部分称为0p；在Debian和Ubuntu下，它被称为7posix。


### 功能测试宏
一种编译时机制，用于控制头文件暴露的API范围，确保程序在不同标准或环境下能正确访问所需的系统接口。它们通过定义特定的宏来声明程序依赖的标准或扩展功能（如POSIX、GNU扩展等），从而影响头文件中的函数、变量和常量的可见性。

- 举例：strdup函数需要定义功能测试宏`_XOPEN_SOURCE >= 500`
    - 在头文件之前写上`#define _XOPEN_SOURCE 700`
    - 或者在编译的时候加上参数`-D_XOPEN_SOURCE=700`

> 当编译时不指定编译标准以及功能测试宏时会默认有编译标准和测试宏，当指定了编译标准时，默认的测试宏就没有了。
> _XOPEN_SOURCE设置成700或更大与_POSIX_C_STANARD设置为200809或更大的效果相同, GCC默认设置_POSIX_C_STANARD
> `man 7 feature_test_macros`手册阅读功能测试宏信息


### 编译的4个步骤

#### 预处理
`gcc -E -P unistd.c -o unistd.i`
- -E选项使GCC在对文件进行预处理之后停止，即只创建预处理文件。
- -P选项是使预处理器不在预处理文件中包含行标记。我们想要干净的文件。
- 所有的#include语句都被对应的头文件内容替换。任何宏也都会被实际的数字替换。
- 预处理文件通常以.i作为扩展名。

#### 编译
`gcc -S unistd.c -o unistd.s`
- -S选项，告诉GCC在编译过程完成后停止。
- 汇编文件通常以.s作为扩展名。

#### 汇编
`gcc -c unistd.s -o unistd.o`

#### 链接
`gcc -o unistd.o -o unistd`


### Makefile

1. 默认make编译：`make unistd`执行的命令是`cc unistd.c -o unistd`
2. 编写Makefile后，make执行的命令则是Makefile里的，Makefile适用于同一目录下的所有程序。
> 默认情况下make假定传入的名称是源文件的名称，也是编译后二进制的文件名
3. Makefile编写：
    - 包含target（目标，比如文件或者伪命令），dependencies（依赖），commands（命令）
    ```C
    target: dependencies
        commands
    ```
    - 变量替代重复命令，`NAME = value`，使用`$(NAME)`
    - 内置变量，`$@`表示目标，`$^`表示所有依赖文件，`$<`表示第一个依赖文件
    - 建议将编译和链接拆分开
    ```c
    CC=gcc
    CFLAGS=-Wall -Wextra -pedantic -std=c9
    TARGET=demo
    OBJS=demo1.o demo2.o

    $(TARGET): $(OBJS)
        $(CC) $^ -o $@

    demo1.o: demo1.c
        $(CC) -c demo1.c -o demo1.o

    demo2.o: demo2.c
        $(CC) -c demo2.c -o demo2.o

    ```

4. 模式匹配方式编写
    ```C
    %.o: %.c
        $(CC) -c $< -o $@
    ```
> `OBJS = $(SRCS:.c=.o)`可以将SRCS变量里的.c文件替换为.o文件。


### 错误处理

大多数系统调用会在错误时设置`errno`宏，在系统调用返回-1时去检查error的值可以确定具体的错误信息，使用errno需要引入`errno.h`。

#### strerror函数

使用strerror函数可以替代人为遍历error宏，直接获得错误信息。

```C
int errnonum = errno;
fprintf(stderr, "%s\n", strerror(errnonum));
```

#### perror函数

perror会将错误信息直接打印到stderr流，只需要要传入通用错误字符串，函数会在传入的字符串后紧跟`:`，空格和错误信息。

```C
perror("Error");
```

> ubuntu中下载moreutils然后通过`errno -l`可以列出所有的错误宏。


### 文件系统

> 使用stat <file>可以查看文件的索引节点信息
```C
#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<unistd.h>
#include<string.h>
#include<errno.h>

int main(int argc, char *argv[])
{
        struct stat file_stat;

        if(argc != 2) {
                fprintf(stderr, "Please use: %s <file>\n", argv[0]);
                return 1;
        }
        if( stat(argv[1], &file_stat) == -1 ){
                perror("Stat file error");
                return errno;
        }

        printf("Inode: %lu\n", file_stat.st_ino);
        return 0;
}
```

#### 文件名

linux中文件名是指向文件索引节点的指针。文件索引节点包含文件的元数据(创建时间等信息)和指向数据块的指针。

#### 链接

硬链接就是文件名，软链接就是文件名的快捷方式。
- 创建硬链接：
    1. 可以使用系统调用`link`, `int link(const char *oldpath, const char *newpath);`。
    2. 可以使用命令`ln`
- 创建软链接：
    1. 使用系统调用`symlink`, `int symlink(const char *target, const char *linkpath);`
    2. 使用命令`ln -s`

> 文件的硬链接默认是1，也就是这个文件名。文件夹的硬链接默认是2，除了自己`.`还有父目录`..`。

#### 创建文件

使用系统调用`int creat(const char *pathname, mode_t mode);`

#### 更新文件时间戳

使用系统调用`int utime(const char *filename, const struct utimbuf *times);`
- 第二个参数传入NULL则更新为当前系统时间，否则更新为传入的结构体里的时间。

#### 删除文件

使用系统调用`int unlink(const char *pathname);`

> unlink本质是解除文件的硬链接，当文件没有硬链接且在进程中没有打开时会释放内存，不可以删除文件夹。

#### 文件模式

文件的完整模式是由6个八进制数组成，比如100755：
- 10代表文件类型，可以用`man 7 inode`查看其他类型。
- 0代表特殊权限位(SUID/SGID/Sticky Bit)没有任何值。
    1. SUID: 4或者s，文件执行时以所有者身份运行。
    2. SGID: 2或者s，文件执行时以所属组身份运行，文件夹中新建文件继承父目录组。
    3. Sticky: 1或者t，目录内的文件仅允许文件所有者删除。
- 755代表基本权限位，分别是所属用户权限，组权限和其他用户权限。

修改权限使用系统调用`int chmod(const char *pathname, mode_t mode);`

修改文件所有权使用系统调用`int chown(const char *pathname, uid_t owner, gid_t group);`
> 传入的用户id和组id需要通过`getpwnam`和`getgrnam`系统调用获取

#### 写入文件

##### 用文件描述符写入
1. 打开文件
`int open(const char *pathname, int flags, mode_t mode);`
- 第一个参数是文件名，第二个参数是带有模式位的宏，比如`O_CREAT|O_RDWR`表示如果不存在就创建它，以及允许读写操作，第三个参数是文件模式，当flags带有O_CREAT时需要传入文件的模式，返回值是文件描述符。

2. 写入文件 
` ssize_t write(int fd, const void *buf, size_t count);`
- 第一个参数是文件描述符，第二个参数是写入的内容，第三个参数是内容的长度。

3. 关闭文件
`int close(int fd);`
- 文件写入后会自动关闭，如果显示关闭文件，使用`close`函数。

##### 用文件流写入
1. 打开文件
` FILE *fopen(const char *pathname, const char *mode);`
- 传入文件路径和打开文件模式，模式是字符，比如`'w'`表示写入，返回值是FILE类型的指针，打开时判断指针是否为NULL。

2. while循环读取输入的每行内容
`char *fgets(char *s, int size, FILE *stream);`
- 第一个参数定义的每行字符的缓冲来存储读取的字符串，比如`char linebuff[1024] = {0}`, 第二个参数是缓冲大小`sizeof(linebuff)`, 第三个参数是文件流，fopen的返回值，当fgets返回为NULL时表示读取完毕，退出循环。

3. 写入文件
`int fprintf(FILE *stream, const char *format, ...);`
- 第一个参数是文件流，第二个传入每行的字符串`linebuff`

4. 关闭流
`int fclose(FILE *stream);`


#### 读取文件

##### 用文件描述符读取
1. 打开文件
- 同样使用`open`函数打开文件，此时flags使用`O_RDONLY`表示只读，不需要传入文件模式，文件模式传入会被忽略。

2. 获取文件大小
`int fstat(int fd, struct stat *statbuf);`
- 传入打开的文件的描述符和stat结构体对象，通过`stat中的st.size`获取文件大小，单位字节。

3. 读取文件
`ssize_t read(int fd, void *buf, size_t count);`
- 第一个参数是文件描述符，第二个是存储文件内容的字符数组，第三个是读取文件的大小，一般设定一个最大值，比较文件实际的大小来避免溢出。

##### 用流读取文件

1. 打开文件
- 使用`fopen`函数，这次传入的mode是`'r'`

2. 循环获取每一行并打印
- 使用`fgets`函数读取每一行得到linebuff,然后`printf`打印出来。

3. 关闭流

> 拓展：某些场景需要使用二进制文件写入和读取来避免精度损失。


### 进程

#### bash命令

1. `ptree`查看进程树
> ubuntu 下载：sudo apt install psmisc
- `ptree -A -p -s $$`查看当前进程的父进程和子进程

2. `echo $$`查看当前进程号

3. `jobs`显示后台进程

4. `bg`/`fg`将进程带到后台/前台，后面跟jobs展示的进程序号。

#### 控制和终止进程



