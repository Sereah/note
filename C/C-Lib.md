### `stdlib.h` 常用函数总结

#### 内存管理
| 函数原型 | 说明 |
| --- | --- |
| `void* malloc(size_t size);` | 分配 `size` 字节的未初始化内存块，返回指向该块的指针。 |
| `void* calloc(size_t num, size_t size);` | 分配 `num * size` 字节的内存块，并初始化为零。 |
| `void* realloc(void* ptr, size_t new_size);` | 调整已分配内存块的大小（可扩大或缩小）。 |
| `void free(void* ptr);` | 释放由 `malloc`、`calloc` 或 `realloc` 分配的内存。 |

#### 字符串转换
| 函数原型 | 说明 |
| --- | --- |
| `int atoi(const char* str);` | 将字符串转换为 `int` 类型整数。 |
| `long atol(const char* str);` | 将字符串转换为 `long` 类型整数。 |
| `double atof(const char* str);` | 将字符串转换为 `double` 类型浮点数。 |
| `long strtol(const char* str, char**​ endptr, int base);` | 将字符串按指定进制转换为 `long`，支持错误检测。 |
| `double strtod(const char* str, char**​ endptr);` | 将字符串转换为 `double`，支持错误检测。 |

#### 随机数生成
| 函数原型 | 说明 |
| --- | --- |
| `int rand(void);` | 生成伪随机数（范围：`0` 到 `RAND_MAX`）。 |
| `void srand(unsigned int seed);` | 设置 `rand()` 的种子值（通常用 `time(NULL)` 初始化）。 |

#### 环境控制
| 函数原型 | 说明 |
| --- | --- |
| `void exit(int status);` | 正常终止程序，`status=0` 表示成功，非零表示错误。 |
| `void abort(void);` | 立即异常终止程序（不执行清理操作）。 |
| `char* getenv(const char* name);` | 获取环境变量 `name` 的值。 |

#### 搜索与排序
| 函数原型 | 说明 |
| --- | --- |
| `void qsort(void* base, size_t num, size_t size, int (*compar)(const void*, const void*));` | 对数组进行快速排序（需自定义比较函数）。 |
| `void* bsearch(const void* key, const void* base, size_t num, size_t size, int (*compar)(const void*, const void*));` | 在已排序数组中二分查找指定元素。 |

#### 其他实用函数
| 函数原型 | 说明 |
| --- | --- |
| `int system(const char* command);` | 执行系统命令（如 `system("pause")`）。 |
| `int abs(int n);` | 返回整数的绝对值。 |
| `long labs(long n);` | 返回 `long` 类型整数的绝对值。 |

---

​**注意事项**​：
- 动态内存分配后需检查返回值是否为 `NULL`（分配失败时返回）。
- `atoi` 系列函数无错误检查，建议优先使用 `strtol` 或 `strtod`。
- `qsort` 和 `bsearch` 需自定义比较函数，返回值为 `负数`、`0` 或 `正数`。


### 