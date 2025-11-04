---
up:
  - "[[../moc/MocZynq|MocZynq]]"
---


## 系统配置
增加的IP系统ZYNQ

双击该IP系统, 进行配置,。在该界面中, 需要分别对引脚功能、系统时钟、DDR时钟及外设时钟, 以及DDR参数进行配置, 同时要对DMA、PS与PL的接口、中断等进行配置。
## 导出硬件配置 ([pdf](zotero://open-pdf/library/items/L6IL93XD?page=6&annotation=7FABWUZD))
会在工程目录下生成一个名称为“HW”的文件夹
![](../fujian/Pasted%20image%2020250715101221.png)
在这几个文件中, 进行了系统功能引脚、系统时钟、DDR时钟、外设时钟以及DDR参数等的配置, 在我们后面创建SDK工程时需要用到。
## 创建FSBL
BootROM: 处理器从CPU0片内ROM开始启动, 根据BOOT引脚的硬件配置, 首先从QSPIFLASH加载FSBL至OCM中, 然后运行FSBL代码。
FSBL:在FSBL中,主要完成PLL以及DDRIII的初始化,MIO (多功能IO) 的配置, 以及各个外设的频率设置, 然后加载SD卡中的FPGA配置文件, 以及UBOOT代码, 跳转至UBOOT代码的运行地址, 执行UBOOT。
u-boot: u-boot部分主要功能为初始化linux运行环境, 将ramdisk文件系统、devicetree读入RAM, 将linux内核读入RAM。并将启动参数传递给内核, 引导内核启动。该部分设计采用xilinx开发包提供的u-boot, 并修改引导模式为从SD卡加载内核等文件。
Linux内核: 该部分在xilinx开发包提供的内核源码上进行配置修改。
文件系统: 根文件系统使用Ramdisk, sd卡分为FAT32及ext文件系统, FAT32文件系统存储FPGA配置文件、u-boot、内核、ramdisk、devietree文件。ext文件系统存放应用程序及图像数据, 挂载到Ramdisk文件系统上。ext3文件系统最高支持16T存储空间, 满足应用需求。
应用程序: 主要包括人机界面及部分外设控制、纸币数据处理功能 (冠字号识别、图像压缩存储) 与系统软件交互程序。人机界面程序通过串口与控制液晶、按键的处理器通讯。
CPU1实时控制部分:CPU1运行在RTT实时操作系统下, 完成喂钞、测厚、纸币在通道中的运行控制、图像数据采集控制、出钞控制, 以及纸币的清分、面值面向识别、鉴伪等工作, 以及与CPU0的相互、与FPGA的交互等相关工作。

### FSBL创建
打开“Xilinx SDK

选择我们创建工程所对应的处理器
如果选择  ps7_cortexa9_0, 则程序运行在CPU0中; 如果选择ps7_cortexa9_1, 则程序运行在CPU1中。由于我们创建的是FSBL工程, 因此程序需要运行在CPU0中, 我们在此选择ps7_cortexa9_0。

我们选择Zynq FSBL选项, 然后点击Finish按钮

需要进行修改, 以便生成适合我们的FSBL, 主要是修改加载方式等

## 创建应用程序
在CPU0中运行的Linux程序加载的CPU1应用程序。

在选择处理器时 , 由于我们的程序运行在 CPU1 中 , 因此我们选择  ps7_cortexa9_1, 然后在创建应用工程时, 我们选择创建一个空工程, 即Empty  Application


我们将我们的应用程序的三个文件夹放置在该目录下
![](../fujian/Pasted%20image%2020250715101843.png)

## 底层库函数修改
在SDK中, 当创建一个工程时, 该工程将会根据硬件平台设置, 自动生成一套底层库函数, 并将底层库函数编译后, 生成为名称为libxil. a库文件, 加载在工程中, 如下图所示:
![](../fujian/Pasted%20image%2020250715101921.png)
## 程序运行在不同CPU中的注意事项
程序可能在CPU核0中运行, 也可能在CPU核1中运行。由于两个CPU核公用L2Cache、内存、中断、定时器、外设等, 因此在开发过程中需要注意。

在CPU0中, 会进行L2 Cache及中断分配的初始化, 在CPU1不进行L2 Cache及中断分配的初始化 , 因此需要做一些处理。在工程目录的 BSP 目录里面有个  system. mss文件, 双击后有个“Modfiy this BSP's Settings”, 双击后, 在下面的界面中增加 –g -DUSE_AMP=1, 如下图所示:
![](../fujian/Pasted%20image%2020250715102132.png)
## 工程配置 
### 自定义数据段添加及使用
在实际开发过程中, 有时候需要自定义一些数据段, 将部分数据放置在我们指定的位置, 比如将部分数据放置在RAM中。

该分散加载文件的名称为  lscript. ld

定义一个名称为l1_data  数据段:
```
.l1_data :  
{
	  __l1_data_start = .;  
	  *(.l1_data)  
	  *(.l1_data.*)  
	  __l1_data_end = .;
  } > ps7_ram_1_S_AXI_BASEADDR
```
其中, ps7_ram_1_S_AXI_BASEADDR为已经在前面定义的内存名称。

在SDK工程中使用定义数据段举例如下:  
`int __attribute__((section (". l1_data"))) Ocmdata[10] = {0, 1, 2, 3,  4, 5, 6, 7, 8, 9};  `
这样, 数组Ocmdata在编译时就会放置在内存ps7_ram_1_S_AXI_BASEADDR中。
### 函数、变量地址查看
在SDK工程中, 在编译后不会像keil编译器一样会生成一个类似内存map的文件。在SDK中, 如果要查看函数、变量等编译后的地址, 可以通过下面的方式进行查看。

每个工程编译后在SDK中可以看到编译好的elf文件, 如下图所示 
![](../fujian/Pasted%20image%2020250715102650.png)
### 更改硬件平台
硬件平台生成的**xml文件**
## 仿真
...
### 内存数据查看
### 内存数据导入导出
## 生成可执行文件并烧写
### 可执行文件生成
通过Release模式生成的升级文件, 存储在工程目录下的Release目录下, 文件格式为elf格式。

由于固化在处理器内部的ROM加载程序在加载时有一定的格式, 因此需要将  elf格式的文件转换为可加载的bin文件, 需要使用SDK中的Xilinx Tools工具进行转换。

单击SDK下的Xilinx Tools->Create Zynq Boot Image
	![](../fujian/Pasted%20image%2020250715103616.png)
第一部分为创建BIF文件或者导入已经存在的BIF文件.在第一次生成可执行文件时, 需要新建一个BIF文件。如果下次在生成可执行文件时, 如果文件列表未变化, 只是文件内容变化了, 可以导入之前已经创建的BIF文件。

第二部分为文件列表, 点击Add按钮
	![](../fujian/Pasted%20image%2020250715103807.png)
	Partition type: 分区类型
	我们主要使用bootloader以及datafile类型。当==添加第一个文件时, 其类型必须为bootloader, 也就是说, 我们添加的第一个文件必须为FSBL生成的文件==。==之后, 我们添加的FPGA加载文件、UBOOT、CPU应用程序等, 都属于datafile==  类型的文件。

由于我们方案是从QSPIFLASH加载FSBL, 然后FSBL从SD卡加载FPGA程序、UBOOT、应用程序等, 因此我们需要制作两个可执行文件, 一个烧写在QSPIFLASH中, 只包括FSBL; 另外一个放置在SD卡中,包括FSBL (该FSBL不用于加载, 只是由于工具生成可执行文件需要)、FPGA程序、UBOOT、应用程序等。
### 可执行文件烧写
可执行文件烧写主要时是QSPIFLASH的烧写, 由于我们使用的FLASH与SDK中提供的FLASH烧写工具支持的FLASH不兼容, 因此我们自己制作了一个FLASH烧写模块
![](../fujian/Pasted%20image%2020250715104425.png)

![](../fujian/Pasted%20image%2020250715104503.png)


点击右上角NEW, 浏览选择文件夹zynqsdk