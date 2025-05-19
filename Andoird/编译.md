#### enableJetifier
问题：三方库仍然使用support-v4，导致和androidx编译冲突。
解决：`gradle.properties`中加入`android.enableJetifier=true`，会将support-v4转换为androidx相同的库。

#### namespace和applicationId
- namespace: 资源路径，每个lib都有一个，R类的引用。
- applicationId: app唯一id，系统中显示的package名字。
- applicationIdSuffix：可以根据构建类型区分applicationId。
```kotlin
buildTypes {
        debug {
            applicationIdSuffix = ".debug"
        }
    }
```

#### 使用签名
- 在signingConfigs中引入jks文件，在构buildType中引用。
```kotlin
    signingConfigs {
        create("keystore") {
            storeFile = file("../../keystore/debug.jks")
            keyPassword = "123456"
            storePassword = "123456"
            keyAlias = "debug"
        }
    }

    buildTypes {
        release {
            signingConfig = signingConfigs.findByName("keystore")
        }

        debug {
            signingConfig = signingConfigs.findByName("keystore")
        }
    }
```

#### ABI架构(app依赖so库时)
1. 在defaultConfig中写ndk配置，指定编译的apk包含的架构，不写默认全部。
```kotlin
ndk {
    abiFilters.addAll(listOf("arm64-v8a", "x86_64"))
}
```
2. 在buildTypes中的各个编译类型中写则覆盖前面的。
```kotlin
release {
    ndk {
        abiFilters.clear()
        abiFilters.addAll(listOf("arm64-v8a"))
    }
}
```
3. 前面的都是将所有架构的so库放在同一个apk，下面将不同的架构分包编译成apk。
```kotlin
splits {
    abi {
        isEnable = true
        reset()
        include("arm64-v8a", "x86_64")
        isUniversalApk = true
    }
}
```

#### apk重命名
```kotlin
    applicationVariants.all {
        outputs.all {
            val variantOutput = this as com.android.build.gradle.internal.api.BaseVariantOutputImpl
            val abi = variantOutput.filters.find { it.filterType == "ABI" }?.identifier ?: "global"
            variantOutput.outputFileName = "Demo-$abi.apk"
        }
    }
```

#### 自定义构建变体
- flavorDimensions: 构建维度
- productFlavors： 构建不同的风味
- 在buildTypes中设置signingConfig = null避免默认签名影响
```kotlin
    flavorDimensions += "platform"
    productFlavors {
        create("emulator") {
            dimension = "platform"
            signingConfig = signingConfigs.getByName("emulator_platform")
        }
        create("XXXX") {
            dimension = "platform"
            signingConfig = signingConfigs.getByName("platform_xxxx")
        }
    }
```

#### 导入framework.jar编译
设置bootstrapClasspath
例如：

```java
gradle.projectsEvaluated {
    tasks.withType(JavaCompile).tap {
        configureEach {
            List<File> newFileList = new ArrayList<>()
            newFileList.add(rootProject.file(branch_path + '/ext/framework-bluetooth.jar'))
            newFileList.add(rootProject.file(branch_path + '/ext/framework-wifi.jar'))
            newFileList.addAll(options.bootstrapClasspath.getFiles())
            options.bootstrapClasspath = files(newFileList.toArray())
        }
    }
}
```