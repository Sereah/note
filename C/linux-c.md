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

`test -e 文件夹名`可以测试是否存在某个文件夹，存在时返回0，否则返回1，可以写出下列脚本去使用返回的结果然后打印信息。

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

