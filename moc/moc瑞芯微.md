# 3566 orange

## emmc
![](../fujian/file-20250926083427026.png)
![](../fujian/file-20250926083442815.png)
![](../fujian/file-20250926083517024.png)


![](../fujian/file-20250926083530655.png)


![](../fujian/file-20250926083546764.png)


## 使用 RKDevTool 清空 SPIFlash 的方法
![](../fujian/file-20250926083645015.png)
![](../fujian/file-20250926083702610.png)
再擦除所有

## 烧录 Android 镜像到 eMMC 中的方法
![](../fujian/file-20250926083921011.png)
![](../fujian/file-20250926083904512.png)

![](../fujian/file-20250926083939847.png)




## 将 Linux 镜像烧写到 TF 卡的方法
![](../fujian/file-20250926084250013.png)

![](../fujian/file-20250926084309059.png)

![](../fujian/file-20250926084322393.png)


## 烧写 Linux 镜像到 SPIFlash+NVMe SSD 中的方法
![](../fujian/file-20250926084658848.png)

![](../fujian/file-20250926084721970.png)
![](../fujian/file-20250926084732152.png)


# 3588
## 下载 SPI 启动固件
![](../fujian/file-20250926093218333.png)
② : 选择主板对应的 Loader 文件
##  安装系统到 eMMC
![](../fujian/file-20250926093339029.png)


## 安装系统到 MicroSD 卡
将 MicroSD 卡插入到 SD 卡读卡器中，然后将读卡器插入到 PC 的 USB 端口上
![](../fujian/file-20250926093745665.png)

按照上述步骤成功烧录 MicroSD Card 后，将 MicroSD Card 插入到 MicroSD Card 插槽内(如下图所示)，然后上电，电源指示灯显示绿色，系统开始启动，启动正常后，指示灯开始闪烁，一段时间后 HDMI 显示桌面。

## emmc

将 [eMMC Module](https://docs.radxa.com/accessories/emmc_module) 插入到 [eMMC Reader](https://docs.radxa.com/accessories/emmc_reader) 中，然后将 Reader 插入到 PC 的 USB 端口上
![](../fujian/file-20250926093957447.png)
![](../fujian/file-20250926094011945.png)

##  安装系统到 NVME
- 准备一张 MicroSD 卡充当启动盘
    
- 使用系统工具 rsetup 刷 SPI Flash
    
- 将系统镜像刷到 NVME SSD 里面
    
- 拔掉 MicroSD 卡, 从 NVME 启动



### 参考 [制作 MicroSD 启动盘部分](https://docs.radxa.com/rock5/rock5b/getting-started/install-os/boot_from_sd_card) 将系统安装在 MicroSD 卡当中。
这里 MicroSD 卡的作用相当于 x86 的启动盘，目的是拿到 spi.img，将 spi.img 刷到 spi flash 中。
### 从 MicroSD 卡启动后，执行一下命令以更新系统:
	sudo apt-get update  
	sudo apt-get full-upgrade
### 使用系统工具 [rsetup](https://docs.radxa.com/rock5/rock5b/radxa-os/rsetup) 刷 SPI
###  将系统镜像刷到 NVME SSD 里面
将 NVME SSD 插入到板子上，确认 NVME 是否被系统识别，

![](../fujian/file-20250926094218101.png)
如上所示系统已经识别到 NVME SSD 即 nvme0n1（在 Linux 中，NVMe 设备通常被识别为 nvmeXnY）

我这里演示使用 `wget` 命令在主板上下载系统镜像
```
# 安装 wget
sudo apt-get install wget
# 下载系统镜像文件
wget [URL]
```

然后在**主板**上使用 `dd` 命令将系统镜像写入 NVME SSD 中。
  sudo xzcat /path/to/img | sudo dd of=/path/to/nvme bs=1M status=progress
  示例：
  sudo xzcat /home/radxa/rock-5b_xx.img.xz | sudo dd of=/dev/nvme0n1 bs=1M status=progress
  
- xzcat : 解压 xz 格式的系统镜像文件
- dd : 复制并写入到 NVMe SSD 设备（⚠️注意：使用 `dd` 命令时请确认设备名称，错误的设备名可能导致数据丢失）
- of=/dev/nvme0n1 : 指定写入的设备为 nvme0n1（可以根据实际情况修改）
- bs=1M : 指定写入的块大小为 1M，提高写入速度
- status=progress : 显示写入进度，让您了解写入状态

> 1. 直接在主板访问 [资源下载汇总](https://docs.radxa.com/rock5/rock5b/download) 页面，然后通过浏览器下载系统镜像。
> 2. 下载系统镜像在 PC 上，然后使用 U 盘或者在线传输（如 FTP、SCP 等）的方式将系统镜像文件复制到主板上。

## usb刷机
![](../fujian/file-20250926094913539.png)
![](../fujian/file-20250926094925588.png)- 选择 Loader (详见上文文件下载部分)
- 点击右键，选择添加项，选择储存介质为 eMMC
- 选择系统镜像(详见上文文件下载部分，下载完后需要解压成 .img 格式)
- 点击执行，开始烧录

# 野火


## nvme 
``
![](../fujian/file-20250926102537470.png)


## emmc
刷入EMMC：
使用当前目录的烧录工具
打开RKDevTool. exe工具，进入maskrom模式，
1. 选择“下载镜像”下面有名字写着：boot  system
2.“boot”选择当前目录工具文件夹里面自带名是“rk3588_MiniLoaderAll. bin”点击右边“...”选择bin
3.“sysem”选择下载好的镜像，ubuntu**. xz压缩包，进行解压出镜像. img，点击右边“...”选择镜像. img
2. 下方打勾“强制按地址写”
3. 最后点击“执行”正在刷入，等待结束。


## 网络
电脑有 USB 接口且具有可以通讯数据的 TYPE-C 线, 电脑有网络, 可以通过 USB 共享网络
手机支持 usb 共享网络, 通过 usb 线连接手机和板卡, 手机开启 usb 网络共享

### 网线连接电脑和板卡
#### pc

选择有网络的网卡共享到要共享的网卡
pc端要共享的
	![](../fujian/file-20250926213210197.png)

测试 
	ping 办卡IP

#### 板卡端
网关为
	![](../fujian/file-20250926213331745.png)
nmtui
	IP 网段一直
	dns和pc一致
测试
	ping 192.168.137.1
	ping 8.8.8.8
	ping www.baidu.com
### 手机 USB 共享网络
### 电脑 USB 共享网络-Windows

