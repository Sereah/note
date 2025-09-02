## ffmpeg的使用

### ffprobe命令

#### 查看视频文件详细信息

- ffprobe -v quiet -print_format json -show_format -show_streams target

#### 命令解释

- `-v quiet`: 设置输出日志级别，quiet表示不输出日志，只输出指定的信息。

- `-print_format json`: 设置输出内容的格式为json。

- `-show_format`: 设置输出信息包含视频容器信息。

- `-show_streams`: 设置输出视频文件中的流信息（视频流，音频流，字母流等）。

- `rarget`: 设置目标文件。

#### 结果展示

##### 容器信息

```json
"format": {
        "filename": "test.mp4", //文件名
        "nb_streams": 2, //流的数量
        "nb_programs": 0, //节目的数量，在MPEG-TS 等传输流容器中可以同时包含多个节目，每个节目又有自己的音频视频流。
        "nb_stream_groups": 0, //流组数量，描述流之间的逻辑分组。
        "format_name": "mov,mp4,m4a,3gp,3g2,mj2", //容器的短名
        "format_long_name": "QuickTime / MOV", //容器的完整描述
        "start_time": "0.000000", //开始时间
        "duration": "8.337188", //时长
        "size": "8866051", //大小，单位Byte。
        "bit_rate": "8507473", //比特流，单位bps。
        "probe_score": 100, //探测分数，越高说明越准确。
        "tags": {
            "major_brand": "mp42", //容器主品牌
            "minor_version": "0", //次版本号
            "compatible_brands": "isommp42", //兼容的容器品牌
            "creation_time": "2025-09-02T03:11:42.000000Z", //文件创建时间
            "com.android.version": "13" //android设备创建的视频文件
        }
    }
```

##### 视频流信息

```json
"streams": [
        {
            "index": 0, //流索引
            "codec_name": "h264", //视频编码器
            "codec_long_name": "H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10", //编码器全称
            "profile": "Baseline", //编码档次
            "codec_type": "video", //编码类型
            "codec_tag_string": "avc1", //编码标识，四字符编码，人类可读
            "codec_tag": "0x31637661",  //16进制表示四字符编码
            "width": 720, //视频分辨率
            "height": 1280, 
            "coded_width": 720, //编码宽高
            "coded_height": 1280,
            "has_b_frames": 0, //是否含有B帧
            "pix_fmt": "yuvj420p", //像素格式，yuv=色彩空间，j=0-255全幅色彩范围（视频标准16-235），色度下采样420，平面存储（YUV分开存储）
            "level": 10, //H.264编码等级，越高表示支持的分辨率/码率越高
            "color_range": "pc", //颜色范围（pc=全范围，tv=有限范围）
            "color_space": "bt709", //色彩空间
            "color_transfer": "smpte170m", //色彩传递特性
            "color_primaries": "bt709", //色彩基准
            "chroma_location": "left", //色度位置
            "field_order": "progressive", //扫描方式（progressive=逐行，tt=隔行）
            "refs": 1, //参考帧数量
            "is_avc": "true", 
            "nal_length_size": "4", 
            "id": "0x1", 
            "r_frame_rate": "30/1", //容器声明的帧率30fps
            "avg_frame_rate": "1875000/62431", //平均帧率
            "time_base": "1/90000", //时间基（时间戳换算比例，单位秒）
            "start_pts": 0, //开始时间
            "start_time": "0.000000",
            "duration_ts": 749172, //结束时间（基于时间基）
            "duration": "8.324133", //结束时间，单位秒
            "bit_rate": "8417372", //视频流码率，bps
            "bits_per_raw_sample": "8", //原始采样位深，8bit
            "nb_frames": "250", //总帧数
            "extradata_size": 38, //编码器附加信息大小
            "disposition": { //流属性标志
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
                "non_diegetic": 0,
                "captions": 0,
                "descriptions": 0,
                "metadata": 0,
                "dependent": 0,
                "still_image": 0,
                "multilayer": 0
            },
            "tags": {
                "creation_time": "2025-09-02T03:11:42.000000Z",
                "language": "eng",
                "handler_name": "VideoHandle", //处理器名称
                "vendor_id": "[0][0][0][0]"
            }
        },
    ],
```

##### 音频流信息

```json
{
            "index": 1,
            "codec_name": "aac",
            "codec_long_name": "AAC (Advanced Audio Coding)",
            "profile": "LC", //编码档次
            "codec_type": "audio",
            "codec_tag_string": "mp4a",
            "codec_tag": "0x6134706d",
            "sample_fmt": "fltp", //采样数据格式（如 fltp=浮点 planar）
            "sample_rate": "48000", //采样率
            "channels": 1, //声道
            "channel_layout": "mono", //声道布局
            "bits_per_sample": 0,
            "initial_padding": 0,
            "id": "0x2",
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/48000",
            "start_pts": 1843,
            "start_time": "0.038396",
            "duration_ts": 398342,
            "duration": "8.298792",
            "bit_rate": "96120", //码率
            "nb_frames": "389",
            "extradata_size": 2,
            "disposition": {
                "default": 1,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0,
                "timed_thumbnails": 0,
                "non_diegetic": 0,
                "captions": 0,
                "descriptions": 0,
                "metadata": 0,
                "dependent": 0,
                "still_image": 0,
                "multilayer": 0
            },
            "tags": {
                "creation_time": "2025-09-02T03:11:42.000000Z",
                "language": "eng",
                "handler_name": "SoundHandle",
                "vendor_id": "[0][0][0][0]"
            }
        }
```


### ffmpeg命令

#### 转码

- ffmpeg -i input.mp4 -c:v libx265 -c:a aac output.mp4

#### 转封装

- ffmpeg -i input.mp4 -c copy output.ts

#### 抽取分离

##### 抽取音频流

- ffmpeg -i input.mp4 -vn -c:a copy audio.aac 

- `-vn`表示video none，去掉视频流

- `-c:a copy`表示音频编解码器设置为直接拷贝，不重新编码

##### 抽取视频流

- ffmpeg -i input.mp4 -an -c:v copy video.h264

- `-an`表示audio none，去掉音频流

- `-c:v copy`表示视频编解码器设置为直接拷贝，不重新编码

#### 处理

##### 裁剪

- ffmpeg -i input.mp4 -t 10 -ss 00:01:30 output.mp4

- `-t 10` 输出10s的视频。

- `-ss 00:01:30` 从1分30秒还是裁剪。

##### 缩放

- ffmpeg -i input.mp4 -vf "scale=1280:720" output_720p.mp4

- `-vf "scale=1280:720"` 视频缩放到1280x720，可能会拉伸画面，将宽/高换成-1可以保持比例，比如`scale=1280:-1`

##### 添加水印

- ffmpeg -i input.mp4 -i logo.png -filter_complex "[0:v][1:v] overlay=10:10" output_watermarked.mp4

- `-filter_complex "[0:v][1:v] overlay=10:10"`: `[0:v]`代表视频，`[1:v]`代表水印图片，10:10表示距离上和左10px。

#### 解码

##### 解码出yuv

- ffmpeg -i input.mp4 -c:v rawvideo -pix_fmt yuv420p output.yuv

##### 解码出pcm

- ffmpeg -i input.mp4 -c:a pcm_s16le -ar 44100 -ac 2 output.pcm
