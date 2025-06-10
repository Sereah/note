#### 生命周期

##### 进入组合
1. compose函数首次被添加到UI树中，类似于onCreateView
2. 使用remember初始化的状态创建
3. 副作用API启动

##### 重组
1. 当compose函数的输入或者读取的state发生变化时触发
2. UI树跳过没有发生变化的compose函数
3. 副作用API根据不同的函数决定是否执行

##### 退出组合
1. compose函数从UI树中移除，类似于onDestroyView
2. remember状态被释放(rememberSaveable除外，不过一般不用，用viewmodel保存数据)
3. 副作用API在此阶段清理资源

##### 协程的生命周期
1. 跟随compose函数，`rememberCoroutineScope()`，这个协程对象会跟随compose的函数。


#### 内边距和外边距

modifier的padding设置在background之前是外边距，否则内边距

#### 嵌套滚动

1. 方向不一致
2. 方向一致，内部列表的滑动方向的长度固定。

#### 减少重组

使用derivedStateOf来增加重组UI的条件，避免每次value发生变化都重组

#### 自定义布局

1. 测量子控件的尺寸
2. 决定自身尺寸
3. 放置子控件

```kotlin
@Composable
fun CustomColumn(modifier: Modifier = Modifier, content: @Composable () -> Unit) {
    Layout(modifier = modifier, content = content, measurePolicy = object : MeasurePolicy {
        override fun MeasureScope.measure(
            measurables: List<Measurable>,
            constraints: Constraints
        ): MeasureResult {
            //第一步
            val placeable = measurables.map {
                it.measure(constraints)
            }
            //第二步
            val layoutWidth = placeable.maxOf { it.width }
            val layoutHeight = placeable.sumOf { it.height }
            //第三步
            return layout(layoutWidth, layoutHeight) {
                var y = 0
                for (p in placeable) {
                    p.placeRelative(x = 0, y = 0)
                    y += p.height
                }
            }
        }
    })
}
```

#### IntrinsicSize

让Row/Column的子组件对齐​（如Text和Button高度一致）。

#### 副作用API

compose中重组是不确定顺序的，避免每次重组导致执行重复代码，副作用API中的代码隔离compose的重组。

##### SideEffect

1. compose重组一次，执行一次。
2. 不提供协程作用域。
3. 无法自动取消或释放资源。
> 适用场景：同步compose状态到view系统，日志打印。

##### LaunchedEffect

1. 参数传一个`key`，依赖key的变化而执行，传入Unit则仅在compose函数组合时执行一次。
2. 提供协程作用域。

##### DisposableEffect

1. 类似于LaunchedEffect，区别是多了一个`onDispose`作用域，当compose函数取消组合时执行内的代码。
2. 不提供协程作用域。
> 适用场景：注册监听，需要回收资源。



