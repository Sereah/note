###自定义尺寸 OnMeasure()

1. 参数：widthMeasureSpec，heightMeasureSpec

> 由父布局传递给子视图的可以使用的空间和测量模式。

```
MeasureSpec.getMode(int measureSpec)
MeasureSpec.getSize(int measureSpec)
```

2. 测量模式

> MeasureSpec.UNSPECIFIED: 父布局对子视图没有限制，子视图可以任意尺寸，通常是特殊场景（ListView滚动测量）。
> MeasureSpec.EXACTLY: 父布局已经确定了视图的精确大小，子视图应将自身的大小设置为给定的尺寸。
> MeasureSpec.AT_MOST: 父布局允许子视图使用的最大尺寸（getSize里获取），子视图可以选择小于等于这个值的尺寸。

3. 自定义view的尺寸代码

```
    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        //父布局给的尺寸和模式
        val widthSize = MeasureSpec.getSize(widthMeasureSpec)
        val widthMode = MeasureSpec.getMode(widthMeasureSpec)
        //自己想要设置的尺寸
        val expectSize = 200
        //根据父布局的模式确定最终的尺寸
        val width = when(widthMode) {
            MeasureSpec.EXACTLY -> widthSize
            MeasureSpec.UNSPECIFIED -> expectSize
            MeasureSpec.AT_MOST -> expectSize.coerceAtMost(widthSize)
            else -> 0
        }
        //将确定的尺寸设置出去
        setMeasuredDimension(width, width)
    }
```
> 上面的模式switch代码可以使用resolveSize(expectSize, widthMeasureSpec)替代。

4. 自定义构造测绘规范

使用MeasureSpec.makeMeasureSpec可以构造测绘规范传递给子view，控制子view的大小。

```
        for (i in 0 until childCount) {
            val child = getChildAt(i)
            val childWidthSpec = MeasureSpec.makeMeasureSpec(viewWidth, MeasureSpec.EXACTLY)
            val childHeightSpec = MeasureSpec.makeMeasureSpec(viewHeight, MeasureSpec.EXACTLY)
            child.measure(childWidthSpec, childHeightSpec)
        }
```


