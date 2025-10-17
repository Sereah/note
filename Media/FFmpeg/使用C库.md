## 代码仓库

- https://github.com/Sereah/ffmpegLearn.git

## 引入ffmpeg库

- 直接下载ffmpeg库到系统目录，避免环境配置问题。比如：sudo apt install libavformat-dev

## 获取媒体信息

### 步骤

#### 1.打开媒体文件

- 函数原型： `int avformat_open_input(AVFormatContext **ps, const char *url, const AVInputFormat *fmt, AVDictionary **options);`

- 返回值不为0表示错误

- **ps： 传入二级指针，将定义的AVFormatContext变量指向有效内存。

- *url： 传入媒体源地址，可以是本地的，也可以是网络流。

- *fmt:  输入格式，一般传入nullptr，自动检测。

- **options： 额外参数，一般传入nullptr。

#### 2.查询流

- 函数原型： `int avformat_find_stream_info(AVFormatContext *ic, AVDictionary **options);`

- 返回值不为0表示错误

- *ic： 第一步中指向有效内存的AVFormatContext指针。

- **options： 额外参数，一般传入nullptr。

#### 3.媒体时长

- AVFormatContext结构体中的`int64_t duration`，需要除以`AV_TIME_BASE`，因为是以AV_TIME_BASE大小为单位的。

#### 4.获取流

- 流的数量：AVFormatContext结构体中的`unsigned int nb_streams;`。

- 获取流：根据数量遍历AVFormatContext中的`AVStream **streams;`。

#### 5.流信息

##### 视频流

- 获取流类型：`stream->codecpar->codec_type`，返回AVMediaType枚举。

- 判断是否视频流，和`AVMEDIA_TYPE_VIDEO`作比较。

- 打印流类型名字(video): `const char *av_get_media_type_string(enum AVMediaType media_type);`

- 视频流宽：`stream->codecpar->width`，返回int类型。

- 视频流高：`stream->codecpar->height`，返回int类型。

- 视频流像素格式：`stream->codecpar->format`，返回int类型。

- 像素格式字符串：需要将int类型的值强转为AVPixelFormat，然后`const char *av_get_pix_fmt_name(enum AVPixelFormat pix_fmt);`获取名字。

- 流时长：`static_cast<double>(duration) * (static_cast<double>(stream->time_base.num) / stream->time_base.den)`，需要乘时间基准。

- 视频流帧数：`stream->avg_frame_rate.num << "/" << stream->avg_frame_rate.den`，帧数和时间基准都是用的AVRational表示，一个分数可以避免精度丢失。

##### 音频流

- 获取流类型：`stream->codecpar->codec_type`，返回AVMediaType枚举。

- 判断是否音频流，和AVMEDIA_TYPE_AUDIO作比较。

- 音频流采样存储格式(整数/浮点数，位深，平面/交错)：`stream->codecpar->format`，返回int类型。

- 采样格式的字符串：强转为AVSampleFormat类型，然后使用`const char *av_get_sample_fmt_name(enum AVSampleFormat sample_fmt);`获取名字。

- 采样率：`stream->codecpar->sample_rate`，返回int类型。

- 声道数：`stream->codecpar->ch_layout.nb_channels`，返回int类型。

- 声道布局：`int av_channel_layout_describe(const AVChannelLayout *channel_layout,char *buf, size_t buf_size);`，传入字符数组，因为字符串不固定。

- 流时长：和视频流一样的获取方式。


## 提取YUV数据

### 步骤

#### 1.打开媒体文件

- 使用`avformat_open_input`函数，将AVFormatContext变量指向有效内存。

#### 2.获取视频流

- 遍历`nb_streams`，判断`streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO`。

- 获取视频流`streams[i]`

#### 3.获取解码器

- 获取视频流解码器id：`videoStream->codecpar->codec_id`。

- 使用函数`const AVCodec *avcodec_find_decoder(enum AVCodecID id);`获取解码器。

#### 4.获取解码器上下文

- 使用函数`AVCodecContext *avcodec_alloc_context3(const AVCodec *codec);`。

#### 5.拷贝stream中的AVCodecParameters数据到解码器上下文

- 使用函数`int avcodec_parameters_to_context(AVCodecContext *codec, const struct AVCodecParameters *par);`。

#### 6.打开解码器

- 使用函数`int avcodec_open2(AVCodecContext *avctx, const AVCodec *codec, AVDictionary **options);`。

#### 7.打开存放yuv数据的文件

- 使用fopen函数：`FILE *yuv_file = fopen(yuv_name, "wb");`

#### 8.初始化packet和frame

- 使用`AVPacket *packet = av_packet_alloc();`初始化packet结构体。

- 使用`AVFrame *frame = av_frame_alloc();`初始化frame结构体。

#### 9.读取数据

- 循环读取`while (av_read_frame(fmt_ctx, packet) == 0)`，从AVFormatContext中读取数据到packet。

- 判断数据属于视频流`if (packet->stream_index == videoStream->index)`。

- 将数据包发送到解码器上下文做解码操作(异步)`if (avcodec_send_packet(codec_context, packet) == 0)`。

- 从解码上下文中获取解码后的数据帧`while (avcodec_receive_frame(codec_context, frame) == 0)`。

#### 10.写入YUV数据(YUV420P)

##### Y平面

```c++
// fwrite的参数分别是：起始位置地址，每次写入的字节数，写入多少个字节数，目标文件
// 平面数据就类似于矩阵，存储于二维数组，一行一行写。
// frame->data[0]就是第0行第0列的地址
// 因为每行的字节数不一样，为了对齐，每行的长度用linesize[0]表示，实际数据宽度是frame->width
// YUV420P，Y平面的宽高都是一倍，U和V的宽高都是1/2，其中data数组0代表Y平面的首地址，1表示U，2表示V
for (int i = 0; i < frame->height; i++) {
    fwrite(frame->data[0] + i * frame->linesize[0], 1, frame->width, yuv_file);
}
```

##### U平面

```c++
for (int i = 0; i < frame->height / 2; i++) {
    fwrite(frame->data[1] + i * frame->linesize[1], 1, frame->width / 2, yuv_file);
}
```

##### V平面

```c++
for (int i = 0; i < frame->height / 2; i++) {
    fwrite(frame->data[2] + i * frame->linesize[2], 1, frame->width / 2, yuv_file);
}
```


## 提取PCM数据

### 步骤

#### 1.和YUV提取一样的，找到音频流后依次拿到帧数据

#### 2.读取帧数据写入PCM文件

```c++
//获取每个采样点的内存占用
int data_size = av_get_bytes_per_sample(static_cast<AVSampleFormat>(frame->format));
if (data_size < 0) {
    break;
}
if (av_sample_fmt_is_planar(static_cast<AVSampleFormat>(frame->format))) {
    // 平面格式
    for (int i = 0; i < frame->nb_samples; i++) { //遍历每帧的采样点
        for (int ch = 0; ch < frame->ch_layout.nb_channels; ch++) { //遍历每个采样点的声道
            fwrite(frame->data[ch] + i * data_size, 1, data_size, pcm_file);
        }
    }
} else {
    // 交错格式
    fwrite(frame->data[0], 1, frame->nb_samples * frame->ch_layout.nb_channels * data_size,
           pcm_file);
}
```
