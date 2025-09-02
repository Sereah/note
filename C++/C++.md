# 基础

## 初始化

### 列表初始化

- C++ 11引入列表初始化，示例：`int a{1}; `, `std::string str{"hello"}`

### 注意事项

- C++中变量定义最好赋予初始值，否则默认使用内存中的垃圾值。

### 声明和定义

- C/C++是单独编译每个源文件，想要使用另一个文件的函数或者变量，只有提前声明。
- 声明：extern int a; 一个变量可以多次声明，告诉编译器有这个东西，但未分配内存。
- 定义：int a = 10; 一个变量只能定义一次，分配内存。

------------------------------------------------------------------------------------

## 变量和基本类型

### 引用（左值引用）

#### 使用

- int a = 10; int &b = a; b就是a的引用

#### 核心概念

- 引用就是变量的别名，不具有内存，声明时必须定义，操作引用就是操作绑定的原变量。

#### 引用折叠

- int a = 10; int &b = a; int &c = b; b是a的引用，c是b引用，那么c也是a的引用。


### 指针

#### 使用

- `int a{10}; int *p_a = &a;` p_a是一个指针变量，值等于a的地址，&在这里是取地址符。`*p_a`得到的是原值，*符号为解指针。

#### 核心概念

- 指针是一个变量，有自己的内存，可以赋予不同变量的地址，定义指针是最好初始化为空指针，否则就是野指针。

#### void指针

- void* 指针可以存放任意类型数据的地址，不能使用*来解指针，因为不知道对象的类型，想要解指针需要强转指针类型。

#### 指针的指针

- 指针也是一个变量，有自己的内存，那么指向指针变量的指针就是 `int **pp = &p;`

#### 指针的引用

- 指针不能指向引用，因为引用不是一个对象，但是指针可以有自己的引用，`int *&ref = ptr`，&必须在*的右边，从右往左读，更靠近变量名的符号就是当前变量的类型。


### const

#### 使用

- const 定义的常量只在当前源文件中有效，跨文件需要extend修饰，并在头文件中声明且也用extend修饰。

#### const的指针

- 常量指针：
`int a{10}; int *const a_ptr = &a;`: 指针本身被const修饰，指针不能指向其他变量内存了，但是可以通过*a_ptr修改a的值。

- 指向常量的指针：
`const int a{10}; const int *a_ptr = &a;`: 指针本身可以变，可以指向别的变量内存，但是不能通过*a_ptr修改a的值。

- 常量指针指向常量：
`const int a{10}; const int *const a_ptr = &a;`: 指针本身不能变，也不能通过*a_ptr修改a的值。

- 指向常量的指针可以不指向常量：
`int a{10}; const int *a_ptr = &a;`: 指针可以变，但是不能通过*a_ptr修改a的值，但是a可以自己修改值。

#### const的引用

- 常量的引用：
`const int a{10}; const int &a_ref = a;`: 不能通过a_ref修改a的值。

- 常量的引用不引用常量：
`int a{10}; const int &a_ref =a;`: 不能通过a_ref修改a的值，但是a自己可以变。

- 引用绑定到临时量：
`const int &ref = 20`: 20是一个字面常量（临时量），存在于ref引用的生命周期中。

#### 顶层const和底层const

- 顶层const修饰是对象本身，拷贝时产生的新对象不具有const修饰。

- 底层const修饰的是指向的对象，拷贝时新对象会带有原对象的const修饰。

#### constexpr 

- 表示在编译过程就能确定结果的常量用这个修饰。


### 类型别名

#### typedef修饰

- `typedef double double_t;`: double_t是double类型的别名。

#### using修饰

- `using double_t = double;`: double_t是double类型的别名。


### auto

- 编译器自动推断类型，必须初始化值。

- 会丢失掉顶层const和引用，比如 `int x = 10; const int &ref = x; auto a = ref;`: 推断出a的类型是int，而不是 const int&类型。


### decltype

#### 使用

- `decltype(a) b;`: b的类型和a的类型一样，a如果是表达式，则是表达式的类型，如果是函数，则是返回值类型。

- `decltype((a)) b = a;`: b的类型一定是引用类型，多加了一个括号。

- `decltype(auto) b = a;`: 等价于auto替换了a。

### 自定义类型

#### struct

##### 概念
- 在Cpp中，Struct是类类型，和class的区别是，成员变量默认是public，这和C不一样。

- 类的定义一般放在头文件中。

##### 示例代码

```cpp
#ifndef CPP_PERSON_H
#define CPP_PERSON_H
#include <string>

struct Person {
    std::string name;
    int age = 18;
    bool isMan = false;
};

#endif //CPP_PERSON_H
```

------------------------------------------------------------------------------------

## 字符串，向量和数组

### 命名空间using

#### 每个名字要有独立的声明

- 不建议全局使用`using namespace`，会污染全局，建议使用`using std::cin; using std::cout;`单独定义。

#### 头文件中不使用using

- 头文件中使用using，会污染引用头文件的源文件。

### string

#### 初始化

##### 直接初始化

- `string s("hello"); string s{"hello"};` 在变量后面跟括号的是直接初始化。

- `string s(10, 'c');` 这样可以定义10个连续的c字符。

##### 拷贝初始化

- 使用=的是拷贝初始化，目前cpp推荐列表初始化。

#### 操作string

##### 读写string

```cpp
int main() {
    string s;
    cout << "Input string: " << endl;
    cin >> s;
    cout << "The string is: " << s << endl;
    return 0;
}
```

##### 读取未知数量的字符

- 通过while(cin >> s)判断输入流是否有效，直到遇到结束符。

##### getline读取一整行

###### 定义

- getline参数一个是输入流，一个是字符串变量，当读取到换行符的时候停止读取，但是变量中并不包含换行符。

###### 示例

```cpp
int main() {
    string s;
    cout << "Input string: " << endl;
    while (getline(cin, s)) {
        cout << s << endl;
    }
    return 0;
}
```

##### string.empty

- empty()函数返回字符串是否为空。

##### string.size

- size()函数返回字符串的长度。

- 返回的类型是size_type，这是string特有的类型，无符号类型且能存下足够大的值。不要和有符号的int值作比较。

##### for遍历string

```cpp
int main() {
    const string s{"hello, world"};
    for (const auto &c : s) {
        std::cout << c;
    }
    return 0;
}
```

### vector

#### 概念

- vector是一个集合类模板，模板类似于java的泛型。

#### 初始化


