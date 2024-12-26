### 性能优化

#### 三级缓存

1. Scrap缓存

> 存储位置：AttachedScrap(暂时不可见), CachedScrap(被回收，但是数据仍绑定)
> 高优先级服用，因为数据仍然绑定，无需bind数据。

2. Recycler缓存

> 存储位置：RecyclerView.Recycler
> 按viewHolder类型分类存储，默认5个。

#### 优化方向

1. 稳定的id

> 适用于item的大小固定，这样避免item重新绘制view。

```
recyclerView.setHasFixedSize(true);

override fun getItemId(position: Int): Long {}
```

2. 将item点击监听器等放到createViewHolder中，bindViewHolder频繁触发。

3. 重写OnScroll事件
> 对于大量图片的RecyclerView，滑动暂停后再加载；RecyclerView中存在几种绘制复杂，占用内存高的楼层类型，但是用户只是快速滑动到底部，并没有必要绘制计算这几种复杂类型，所以也可以考虑对滑动速度，滑动状态进行判断，满足条件后再加载这几种复杂的。

4. 加大ViewHolder缓存数量
> 默认缓存ViewHolder为2个，可以更改，利用空间换时间，缓存的viewholder只能是相同位置，即同一个item使用，适用场景是来回滑动的时候，避免一直bind。

```
setItemViewCacheSize(int )
```

