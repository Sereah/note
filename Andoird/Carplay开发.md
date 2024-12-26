#### 阅读须知

> 本文档是开发Carplay过程中涉及到的知识个人总结，包含android相关，系统相关，文档相关等等，持续更新

#### GLSurfaceView

```java
mGlSurfaceView = (GLSurfaceView)mView;
//设置版本
mGlSurfaceView.setEGLContextClientVersion(2);
//设置GLSurfaceView.Render
mGlSurfaceView.setRenderer(new CarplayScreenRender());
//设置渲染模式
mGlSurfaceView.setRenderMode(GLSurfaceView.RENDERMODE_WHEN_DIRTY);
//添加SurfaceHolder的callback
mGlSurfaceView.getHolder().addCallback(new SurfaceHolderCallback());
```

###### 渲染模式

RENDERMODE_WHEN_DIRTY

> `Renderer` 的 `onDrawFrame()` 方法只有在视图明确请求时才会被调用。通常是在调用 `requestRender()` 方法时触发。

RENDERMODE_CONTINUOUSLY

> `onDrawFrame()` 方法会不断地被调用，频率尽可能地快。这会导致显示内容持续更新，类似于游戏循环。



##### SurfaceHolder

`SurfaceHolder` 是 `SurfaceView` 的核心组件，提供了对底层 `Surface` 的控制，允许在 `SurfaceView` 上进行高效的绘图和视频处理操作。

###### SurfaceHolder.Callback

管理SurfaceView的生命周期，在主线程

```Java
    private final SurfaceHolder.Callback callback = new SurfaceHolder.Callback() {
        @Override
        public void surfaceCreated(@NonNull SurfaceHolder surfaceHolder) {
            //做一些初始化的工作，比如保持屏幕打开
        }

        @Override
        public void surfaceChanged(@NonNull SurfaceHolder surfaceHolder, int format, int width, int height) {
			//SurfaceView的格式和大小发生变化时调用，在这里请求视频流。
        }

        @Override
        public void surfaceDestroyed(@NonNull SurfaceHolder surfaceHolder) {
			//通知停止推流
        }
    };
```



##### Render

渲染

###### GLSurfaceView.Render

```java
    private class ScreenRender implements GLSurfaceView.Renderer {
        
        private GLDirectDrawer mDirectDrawer = null;
        
        private int genTextureID()  {
            int[] texture = new int[1];
            GLES20.glGenTextures(1, texture, 0);
            GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, texture[0]);
            return texture[0];
        }

        @Override
        public void onSurfaceCreated(GL10 gl, EGLConfig config) {
            LogPrint.Info(TAG, "GL onSurfaceCreated");
            //1.构建SurfaceTexture
            
            mDirectDrawer = new GLDirectDrawer();
            mDirectDrawer.SetCropArea(0, 0,
                    mRemoteScrWidth, mRemoteScrHeight);
            mSurfaceTexture.attachToGLContext(genTextureID());
        }

        @Override
        public void onSurfaceChanged(GL10 gl, int width, int height) {
            LogPrint.Info(TAG, "GL onSurfaceChanged width ="+ width + " height =" + height);
            GLES20.glViewport(0, 0, width, height);
        }

        @Override
        public void onDrawFrame(GL10 gl) {
            if (mCodecScrHeight > 0 || mCodecScrWidth > 0) {
                mDirectDrawer.setCodecCropArea(
                        mCodecScrWidth, mCodecScrHeight);
                mCodecScrHeight = 0;
                mCodecScrWidth = 0;
            }
            try {
                mSurfaceTexture.updateTexImage();
                mDirectDrawer.DrawTexture();
            } catch (Exception e) {
                LogPrint.Error("onDrawFrame Error !");
                e.printStackTrace();
            }
        }
    }
```



##### SurfaceTexture

`SurfaceTexture` 通常与 `GLSurfaceView` 一起使用，用于在 GLSurfaceView 上渲染动态的图像内容。例如，从摄像头获取的实时视频流可以通过 `SurfaceTexture` 渲染到 GLSurfaceView 上。

```java
mSurfaceTexture = new SurfaceTexture(false);
mSurfaceTexture.setOnFrameAvailableListener(surfaceTexture -> {
	if (mGlSurfaceView != null) {
		mGlSurfaceView.requestRender();
	}
});
```

###### 函数-updateTexImage

在更新内部图像缓冲区的时候调用，作用是绑定最新的图像数据到OpenGL纹理中，在渲染循环中（如在 `GLSurfaceView.Renderer` 的 `onDrawFrame()` 方法中）调用。

###### 函数-attachToGLContext

用于将 `SurfaceTexture` 绑定到一个现有的 OpenGL ES 纹理对象中，使得图像数据可以通过该纹理对象进行渲染。

> TextureID

```java
private int genTextureID() {
	int[] texture = new int[1];
	//生成一个纹理id，放到texture数组里，0代表偏移量，从0个元素开始存储id
	GLES20.glGenTextures(1, texture, 0);
    //将纹理ID绑定到纹理目标上，GL_TEXTURE_EXTERNAL_OES用于从外部资源获取图像信息
	GLES20.glBindTexture(GLES11Ext.GL_TEXTURE_EXTERNAL_OES, texture[0]);
	return texture[0];
}
```



#### MediaSession

> 这部分主要用在Carplay的音乐信息与播放状态传递给系统测，比如桌面媒体卡片等。Demo：https://github.com/Sereah/MediaSessionDemo

##### 概念和用法

###### 服务端（Carplay）

`MediaSession` 是 Android 中一个核心组件，负责管理和处理与媒体播放控制相关的交互。它是媒体应用和外部控制器的中介，提供了一种标准化的方式来同步播放状态和响应用户的操作（如播放、暂停、快进等）。

```java
private MediaSession mMediaSession;
mMediaSession = new MediaSession(context, context.getPackageName());
mMediaSession.setActive(active);//激活media session，开始播放/拿到媒体焦点的时候
```



`MediaSession.Callback` 是一个用于接收媒体控制命令的回调接口，媒体播放器必须实现这个回调来处理系统发送的播放命令。

```java
//media session设置callback	
mMediaSession.setCallback(mSessionCallback, new Handler(Looper.getMainLooper()));

    private final MediaSession.Callback mSessionCallback = new MediaSession.Callback() {
        //处理方控下发的命令，比如input keyevent 87
        @Override
        public boolean onMediaButtonEvent(@NonNull Intent intent) {
            if (Intent.ACTION_MEDIA_BUTTON.equals(intent.getAction())) {
                KeyEvent keyEvent = intent.getParcelableExtra(
                        Intent.EXTRA_KEY_EVENT);
                if (keyEvent != null) {
                    switch (keyEvent.getKeyCode()) {
                        case KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE:
                            CarplaySessionProxy.getInstance().notifyFlashMedia(
                                    keyEvent.getAction() == KeyEvent.ACTION_DOWN);
                            break;
                        case KeyEvent.KEYCODE_MEDIA_PLAY:
                            CarplaySessionProxy.getInstance().notifyStartMedia(
                                    keyEvent.getAction() == KeyEvent.ACTION_DOWN);
                            break;
                        case KeyEvent.KEYCODE_MEDIA_PAUSE:
                            CarplaySessionProxy.getInstance().notifyStopMedia(
                                    keyEvent.getAction() == KeyEvent.ACTION_DOWN);
                            break;
                        case KeyEvent.KEYCODE_MEDIA_PREVIOUS:
                            CarplaySessionProxy.getInstance().notifyPreviousTrack(
                                    keyEvent.getAction() == KeyEvent.ACTION_DOWN);
                            break;
                        case KeyEvent.KEYCODE_MEDIA_NEXT:
                            CarplaySessionProxy.getInstance().notifyNextTrack(
                                    keyEvent.getAction() == KeyEvent.ACTION_DOWN);
                            break;
                        default:
                            break;
                    }
                    return true;
                }
            }
            return false;
        }

        //处理mediasession中通过mediaController.transportControls控制播放的行为
        @Override
        public void onSkipToNext() {
            LogPrint.Debug(TAG, "onSkipToNext");
            CarplaySessionProxy.getInstance().notifyNextTrack(true);
            CarplaySessionProxy.getInstance().notifyNextTrack(false);
        }

        @Override
        public void onSkipToPrevious() {
            LogPrint.Debug(TAG, "onSkipToPrevious");
            CarplaySessionProxy.getInstance().notifyPreviousTrack(true);
            CarplaySessionProxy.getInstance().notifyPreviousTrack(false);
        }

        @Override
        public void onPause() {
            LogPrint.Debug(TAG, "onPause");
            CarplaySessionProxy.getInstance().notifyStopMedia(true);
            CarplaySessionProxy.getInstance().notifyStopMedia(false);
        }

        @Override
        public void onPlay() {
            LogPrint.Debug(TAG, "onPlay");
            CarplaySessionProxy.getInstance().notifyStartMedia(true);
            CarplaySessionProxy.getInstance().notifyStartMedia(false);
        }
    };
```



`MediaMetadata` 用于封装当前正在播放的媒体的详细信息。它包含如标题、艺术家、专辑、播放时长、封面等媒体元数据。这些信息通常被展示在外部控制界面中。

```java
//将当前播放的媒体信息，歌名，歌手，专辑等放到MediaMetadata中，然后通过mediasession的setMetadata传递出去
public void setMediaMetaInfo(int duration, String title, String album, String artist, String artwork) {
        if (mSession != null) {
            MediaMetadata.Builder builder = new MediaMetadata.Builder();
            builder.putLong(MediaMetadata.METADATA_KEY_DURATION, duration);
            builder.putString(MediaMetadata.METADATA_KEY_TITLE, title);
            builder.putString(MediaMetadata.METADATA_KEY_ALBUM, album);
            builder.putString(MediaMetadata.METADATA_KEY_ARTIST, artist);
            builder.putString(MediaMetadata.METADATA_KEY_ALBUM_ART_URI, "file://" + artwork);
            mSession.setMetadata(builder.build());
        }
    }
```



`PlaybackState` 描述了当前媒体的播放状态（如播放中、暂停、快进、后退等）以及播放的具体进度。这是 `MediaSession` 和外部控制器同步播放状态的方式。

```java
public void playbackInformation(byte status, int milliSeconds) {
        int playState = PlaybackState.STATE_STOPPED;
        switch (status) {
            case 1:
                playState = PlaybackState.STATE_PLAYING;
                break;
            case 2:
                playState = PlaybackState.STATE_PAUSED;
                break;
            case 0:
            default:
                break;
        }
    	//这段代码是让客户端有控制上一曲，下一曲，播放暂停的能力
    	mPlaybackStateBuilder.setActions(PlaybackState.ACTION_PLAY_PAUSE
                | PlaybackState.ACTION_SKIP_TO_NEXT
                | PlaybackState.ACTION_SKIP_TO_PREVIOUS);
    	//往playback中放入当前的播放状态和播放毫秒数，1表示当前播放速度和正常播放速度一样（1倍）
        mPlaybackStateBuilder.setState(playState, milliSeconds, 1);
    	//通过meidasession传递出去
        if (mMediaSession != null) {
            mMediaSession.setPlaybackState(mPlaybackStateBuilder.build());
        }
    }
```



`MediaBrowserService` 是媒体应用的服务，用于提供媒体内容树给系统。它允许系统获取Carplay的媒体内容，并进行控制。`onLoadChildren` 是服务中用于提供媒体内容的回调方法，Carplay用不到，一般用于回调媒体列表，Carplay只会传递当前正在播放的内容。

```java
public class CustomMediaService extends MediaBrowserService {
    private static final String MY_MEDIA_ROOT_ID = "carplay_media_id";

    @Override
    public void onCreate() {
        super.onCreate();
        //从前面构建的mediasession对象中获取token，然后设置到服务中去，让客户端可以通过token连接
        MediaSession session = CustomMediaManager
                .getInstance().getMediaSession(this);
        setSessionToken(session.getSessionToken());
    }

    @Nullable
    @Override
    public BrowserRoot onGetRoot(@NonNull String clientPackageName,
                                 int clientUid, @Nullable Bundle rootHints) {
        //返回一个非空的对象，包含媒体id，表示允许客户端连接
        return new BrowserRoot(MY_MEDIA_ROOT_ID, null);
    }

    @Override
    public void onLoadChildren(@NonNull String parentId,
                               @NonNull Result<List<MediaBrowser.MediaItem>> result) {
        //这里传一些媒体列表，carplay用不到
    }
}

//在manifest中添加自定义的服务
        <service android:name=".CustomMediaService"
            android:exported="true"
            android:enabled="true">
            <intent-filter>
                //固定的action
                <action android:name="android.media.browse.MediaBrowserService"/>
            </intent-filter>
        </service>
```



###### 客户端（比如媒体卡片）

`MediaBrowser` 是用于连接 `MediaBrowserService` 并获取媒体内容树的客户端。

```kotlin
private lateinit var mediaBrowser: MediaBrowser        
mediaBrowser = MediaBrowser(
    requireContext(),
    ComponentName(""/*service app package name*/,""/*service app media session service name*/),
    mediaBrowserConnectCallback,
    null
)
mediaBrowser.connect()
```



`MediaController` 代表一个客户端，它用来控制 `MediaSession`。`MediaController` 可以向 `MediaSession` 发送播放命令（如播放、暂停、跳转等）并获取当前的播放状态。

```kotlin
    private val mediaBrowserConnectCallback = object : MediaBrowser.ConnectionCallback() {
        override fun onConnected() {
            //从mediaBrowser服务中获取mediasession的token
            var sessionToken = mediaBrowser.sessionToken
            //通过这个token构建mediacontroller
            mediaController = MediaController(requireContext(), sessionToken)

            //回调中包含playstate和metadata信息
            mediaController.registerCallback(object : MediaController.Callback() {
                override fun onPlaybackStateChanged(state: PlaybackState?) {
                    val playState = state?.state
                    val millSecond = state?.position
                    val extraBundle = state?.extras
                }

                override fun onMetadataChanged(metadata: MediaMetadata?) {
                    val durationMs = metadata?.getLong(METADATA_KEY_DURATION)
                    val title = metadata?.getString(METADATA_KEY_TITLE)
                    val album = metadata?.getString(METADATA_KEY_ALBUM)
                    val artist = metadata?.getString(METADATA_KEY_ARTIST)
                    val pic = metadata?.getString(METADATA_KEY_ALBUM_ART_URI)
                }
            })
        }
    }

//上一曲
mediaController.transportControls.skipToPrevious()
//下一曲
mediaController.transportControls.skipToNext()
//暂停
mediaController.transportControls.pause()
//播放
mediaController.transportControls.play()
```

