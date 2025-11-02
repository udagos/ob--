

sudo get update
sudo -i
hostname -I   看ip
# wsl 
安装Ubuntu lts只需要电机ubuntu lts，卸载应用重置数据
安装ssh server和client
sudo service ssh --full-restart

后台得开着ubuntu才能用第三方链接，账户和密码为普通用户的账户和密码


# 交叉编译开发环境搭建
## 安装工具
芯片厂家SDK中, 进行工程构建、编译、打包等各种操作中, 往往需要两类工具

1. “通过 apt-get install 命令安装的工具。比如: make、gcc、python 等,以及各种命令”
	![](../fujian/Pasted%20image%2020250613190703.png)
	“上述1)中,一般采用一般缺什么补什么的方法,但是需要用户花时间不断地尝试”
	“1) 命令 pat1”
		sudo apt-get install -y sed make binutils build-essential gcc g++ bash patch gzip bzip2 perl tar cpio unzip rsync file  bc wget python cvs git mercurial rsync subversion android-tools-mkbootimg vim libssl-dev android-tools-fastboot  net-tools vsftpd bison
	2) 命令 pat2
		sudo apt-get install build-essential subversion git libncurses5-dev zlib1g-dev gawk flex quilt libssl-dev xsltproc  libxml-parser-perl mercurial bzr ecj cvs unzip lib32z1 lib32z1-dev lib32stdc++6 libstdc++6 libc6: i386  libstdc++6: i386 lib32ncurses5 lib32z1 -y
2. 编译工具链等。此类工具一般已经放在了芯片SDK中,无需用户自行安装
## 解压厂商sdk包
![](../fujian/Pasted%20image%2020250613191013.png)
![](../fujian/Pasted%20image%2020250613191035.png)
阅读文档学习sdk使用方法


目前大部分厂商都会提供SDK, SDK中包含各种交叉编译工具链以及厂商的linux、uboot等源码以及各种打包工具, 对于全志的**T113系列芯片的内核组成比较复杂, 包括arm、riscv、dsp三个不同的核心, 因此一般的开发者必须使用其SDK**。

**对于一些发烧级开发者也可以尝试自己下载并搭建交叉编译工具链，比如**
	![](../fujian/Pasted%20image%2020250613191146.png)
## 编译验证
### 编译linux
 ![](../fujian/Pasted%20image%2020250613191426.png)
 ![](../fujian/Pasted%20image%2020250613191444.png)
### 编译risc-v
![](../fujian/Pasted%20image%2020250613191531.png)
![](../fujian/Pasted%20image%2020250613191539.png)
![](../fujian/Pasted%20image%2020250613191603.png)


详细的SDK使用方法, 需仔细阅读厂商提供的SDK使用手册等文档。
## 使用 FTP 进行文件互传
“使用VirtualBox的文件共享功能可以很方面的进行宿主机与Ubuntu的文件互传,另外,使用FTP服务也可以很方便的互传文件”
### 虚拟机设置
首先在关闭虚机的情况下, 设置桥接网卡, 可以设置双网卡。
![](../fujian/Pasted%20image%2020250613191806.png)
![](../fujian/Pasted%20image%2020250613191825.png)
第二个网卡的ip用于ftp访问
![](../fujian/Pasted%20image%2020250613191834.png)
![](../fujian/Pasted%20image%2020250613191850.png)
### ftp 客户端 filezilla
## 导出虚拟机
导出之前, 一定需要取消双网卡, 且将网卡设置为NAT模式, 由于桥接模式网卡依赖于本机的网卡硬件,  如果使用桥接模式, 当换一台电脑时, 很容易由于网卡硬件信息不匹配, 导致导入的虚机无法启动。
## 导入虚拟机
# 全志T113-i
## 代码编译及烧录
### linux编译
进入全志SDK根目录==T113_Tina目录下, 可以看到此目录下有build. sh脚本文件==
![](../fujian/Pasted%20image%2020250613192240.png)

1) 配置: 终端中执行 sudo ./build. sh config 命令选择整体平台方案
2) 编译: 终端执行 sudo ./build. sh 编译Linux
3) 3) 打包: 终端执行 sudo ./build. sh pack 打包固件, 如果打包成功, 可以生成一个img镜像,  该镜像即最终生成的固件, 可用于烧录。若已编译完成RISC-V, 则打包时会将RISC-V固件一起打包。

### risc-v编译
进入==T113_Tina下级目录rtos下, 可以看到此目录下有envsetup. sh脚本文件==
1) 配置: 终端执行 source envsetup. sh 使环境变量生效
	执行 lunch_rtos 选择编译方案
		![](../fujian/Pasted%20image%2020250613192633.png)
2) 编译: 进入rtos上级目录==T113_Tina, 终端执行 sudo ./build. sh rtos 编译RISC-V==。
	编译完成后, 生成的镜像文件会自动拷贝到对应平台方案中, 并且rt_system. elf  重命名为amp_rv0. bin, ==amp_rv0. bin即为RISC-V编译生成固件==。
3) 重新编译: 当RISC-V代码有更改重新编译时, 一方面编译生成的中间件过多可能导致编译报错, 另一方面部分更改可能无法触发重新编译, 建议编译前先执行 sudo ./build. sh rtos clean 清除编译中间件, 再进行编译。

### 整体镜像烧录
全志提供的烧写工具很多，本次介绍PhoenixSuit一种工具
	![](../fujian/Pasted%20image%2020250613192844.png)
### RISC-V单独烧录
“若Linux部分不需更改,可单独烧录RISC-V相关固件”
可采用两种方式: 
	1、通过adb push将新生成的镜像文件amp_rv0. bin 推到/lib/firmware 目录下; 
	2、通过nfs拷贝新生成的镜像文件amp_rv0. bin  到/lib/firmware 目录下。
#### adb push方式
- 设置环境变量
- 链接开发板
	- 通过USB连接开发板与Windows主机,开发板中会出现连接成功log
	- 在命令提示符中输入 adb shell 即可进入开发板目录
- 使用adb推送固件
	- 将编译完成的RISC-V固件拷贝至Windows下,启动PowerShell。注意:由于新北洋安全助手限制,  使用adb传输文件时不可使用命令提示符,需使用PowerShell
	- 执行 adb push amp_rv0.bin /lib/firmware 即可将固件推送至开发板。
	- 开启开发板并进入开发板Linux控制台,在Linux控制台执行如下命令:
	`echo stop > /sys/class/remoteproc/remoteproc1/state #关闭RV   echo amp_rv0.bin > /sys/class/remoteproc/remoteproc1/firmware echo start > /sys/class/remoteproc/remoteproc1/state #启动RV`
#### 直接拷贝

通过挂载nfs实现开发板与Linux主机间共享文件, 首先需要保证烧录进开发板的镜像文件已开启  nfs支持, 其次需要确保开发板与Linux主机能互相ping通, 开发板IP可通过Linux控制台执行 ifconfig  eth0 192.168.2.3 指令设置, 或者修改开发板/etc/目录下的 interfaces 文件, 二者区别为前者每次启动开发板都需要重新设置, 后者设置一次即可。

在开发板Linux控制台执行 mount -t nfs -o nolock, vers=3 192.168.2.2:/home/snbc/nfs  /mnt 挂载nfs, 其中指令中IP为Linux主机IP, 挂载成功后, 开发板通过访问/mnt路径即可访问Linux主机的/home/snbc/nfs路径, 实现文件共享。

将编译完成的amp_rv0. bin固件拷贝至/home/snbc/nfs路径下, 在开发板Linux控制台下执行 cp  /mnt/amp_rv0. bin /lib/firmware/ 即可实现RISC-V烧录。注意在拷贝时RISC-V应处于关闭状态, 若开启RISC-V, 需先关闭RISC-V
## RISC-V配置
进入SDK根目录T113_Tina下, 终端执行 ==sudo ./build. sh rtos menuconfig== 即可进入RISC-V配置界面
![](../fujian/Pasted%20image%2020250613193958.png)


Architecture Options内包含RISC-V起始地址, 内存大小, FPU、Cache等配置, 
Kernel  Options包含Freertos相关配置, 
Drivers Options内可配置各外设及其相关测试demo。

根据需求完成配置后保存退出, 重新编译即可将相关配置编译进固件。**此配置界面配置后会更改对应平台方案下的defconfig文件,** 如目前选择的平台方案, 当更改此界面配置后, 路径T113_Tina/rtos/lichee/rtos/projects/t113_i_c906/evb1_auto/defconfig文件会随之发生更改。  
defconfig文件内容如图3.2所示。此文件中配置选中项会取消注释, 
![](../fujian/Pasted%20image%2020250613194225.png)

志SDK中部分文件编译时会有warning, 而SDK中默认开启-Werror编译属性, 会将编译时的  warning按error处理, 导致编译时若有warning会编译失败, 因此需将此编译属性注释。进入目录  T113_Tina/rtos/lichee/rtos下找到. config. mk文件, 注释如图3.3所示部分代码。
![](../fujian/Pasted%20image%2020250613194315.png)

**在增加部分外设文件编译时,此部分外设可能含有DMA相关使用,若未同时增加DMA相关文件,可能导致编译报错,建议在增加有DMA支持外设时同时增加DMA相关文件 (Drivers Options内使能  DMA)。**

## RISC-V使用
### RISC-V启动
**在将正确的镜像烧录进开发板后**, 通过**u转串**连接开发板**CON3**处uart至电脑的USB口, 
打开串口调试助手, 可以**使用MobaXterm, 配置波特率115200**, 给板子上电, 串口会打印系统启动的log 信息。
启动成功log如图4.1所示。此时输入账户名: root, 回车后输入密码: root, 即可以**正常进入linux控制台**
![](../fujian/Pasted%20image%2020250613194659.png)
				Linux启动成功log
通过**u转串**连接开发板**CON4**处uart至电脑的USB口, 打开串口调试助手, 配置波特率115200, 
在上述Linux控制台中执行指令 `echo start > /sys/class/remoteproc/remoteproc1/state` 
,**Linux 控制台**中有如图4.2所示启动成功日志。**RISC-V控制台**有如图4.3所示启动成功日志。
![](../fujian/Pasted%20image%2020250613195024.png)
			RISC-V启动成功**Linux控制台**日志
![](../fujian/Pasted%20image%2020250613195238.png)
				RISC-V启动成功**RISC-V控制台**日志
### RISC-V运行
启动RISC-V指令后, RISC-V启动运行, 全志在SDK中已配置部分代码, 初始化中断控制器、时钟、串口日志等并启动操作系统。
在RISC-V控制台中执行 help 命令即可显示目前RISC-V烧录固件中可运行demo, 此部分demo为全志提供的用于测试验证示例, 如图4.4所示。
	![](../fujian/Pasted%20image%2020250613200548.png)

**此部分demo运行时可能需要传参,** 具体传参需查看代码, 

以 hal_gpio_output 为例, 此命令代码如下:
```
int cmd_test_gpio_output(int argc, char **argv)  
{  
	gpio_pin_t pin;  
	gpio_data_t data;  
	if (argc != 3) 
	{ 
		printf("Usage: Control IO output high and low levels\r\n");  	printf("\thal_gpio_output PC 1\r\n"); 
		printf("\thal_gpio_output PC 0\r\n");  
		return 0;  
	}  
	if (str2pin(argv[1], &pin) != 0)
	{  
		printf("undown arg=%s\r\n", argv[1]); 
		return 0; 
	}  
	data = atoi(argv[2]);  
	if (data != 0 && data != 1) 
	{  
		printf("undown arg=%s\r\n", argv[2]);  
		return 0;  
	}  
	hal_gpio_pinmux_set_function(pin, GPIO_MUXSEL_OUT); 
	hal_gpio_set_pull(pin, GPIO_PULL_UP); 
	hal_gpio_set_direction(pin, GPIO_DIRECTION_OUTPUT);
	hal_gpio_set_data(pin, data);
	return 0;  
} 
FINSH_FUNCTION_EXPORT_CMD(cmd_test_gpio_output, hal_gpio_output, gpio hal output  tests);
```

查看代码可以知道, **此接口需传入两个参数**, 第一个为需配置引脚, 第二个为高电平或低电平, **在  RISC-V控制台执行命令 hal_gpio_output PB0 1 即可控制PB0引脚输出高电平**。

注意运行全志提供的spi**测试demo时需配置RISC-V开启FPU支持, 否则代码跑飞**。若需关闭RISC-V, 可在Linux控制台执行 `echo stop > /sys/class/remoteproc/remoteproc1/state` 。
## 使用Makefile增加文件
为便于代码管理及维护, 需要将我们自己编写的代码进行管理, 会涉及到增加文件夹及文件等操作, 此时即需要修改  Makefile。

通过查看全志SDK层级, **决定在T113_Tina/rtos/lichee/rtos目录下增加SNBC文件夹用于统一管理 RISC-V代码**, 目录内容如图5.1所示。此目录下包含全志提供的内核、驱动、头文件及操作系统等文件。
	![](../fujian/Pasted%20image%2020250613201928.png)

首先需要**将新建的SNBC文件夹增加至编译路径**, **进入  T113_Tina/rtos/lichee/rtos/. dbuild/dbuild. mk文件内, 此文件内定义了rtos文件夹内编译的文件路径, 在图5.2所示处增加SNBC。**
![](../fujian/Pasted%20image%2020250613202044.png)


目前平台组已增加部分模块 (日志、RingBuffer等), 操作系统及SNBC驱动, 此部分可直接到SVN  检出使用。注意: 由于整个SDK较大, 目前SVN中仅上传RISC-V相关代码且由于Linux与Windows命名规则不同, SVN中上传代码相对SDK有缺失, 拷贝时仅需拷贝SNBC文件夹, 其余文件按照SVN日志在SDK  中作对应更改, 不可使用SVN中代码整体替换SDK中代码。SVN路径: `https://fwsvn.byintra.com:82/sv  n/FW_LIB_PLATFORM/FW_LIB_TEMPLATE/tags/T113i-lvdecai-20240520-rtos`。若在当前已建立文件夹中增加文件, 则不需更改Makefile, Makefile可根据设置的路径利用foreach函数自动寻找路径下的. c  文件添加进编译, 若需继续增加文件夹, 此处以增加Application文件夹为例说明。

进入SNBC目录下, 新建Application文件夹, 并打开SNBC目录下Makefile, 添加代码 obj-y +=  Application/ ,将Application文件夹增加至SNBC编译路径, 如图5.3所示。

/////


## 使用sys_config配置引脚
全志SDK中提供两种引脚配置方式: 1、使用sys_config文件配置; 2、使用头文件配置。
	目前SNBC驱动中涉及引脚复用配置处均采用sys_config配置。注意: 若调用全志提供的测试  demo, 部分demo引脚复用采用sys_config配置, 部分demo引脚复用在头文件配置, 具体需查看代码。
配置方法如下: 进入T113_Tina/rtos/board/t113_i_c906/evb1auto/configs/sys_config. fex文件, **在此文件内增加引脚配置**。其基本格式如下:
	[外设+id]
	引脚说明:port: 端口< 复用功能>< 上下拉>< 驱动能力>< 输出值>

例如配置spi1引脚时, 其配置如下:
```
[spi1]  
spi1_clk = port:PD11<4><1><default><default>  
spi1_cs = port:PD10<4><1><default><default>  
spi1_mosi = port:PD12<4><1><default><default>  
spi1_miso = port:PD13<4><1><default><default>  
spi1_wp = port:PD15<4><1><default><default>  
spi1_hold = port:PD14<4><1><default><default>
```

复用功能值可查看手册9.7.3.2 GPIO Multiplex Function章节传入正确值。如图6.1所示根据红框内容确定, 配置引脚PD10-PD15为spi1时复用功能为4。
	![](../fujian/Pasted%20image%2020250613201757.png)

# linux应用开发过程
## 交叉编译工具链
![](../fujian/Pasted%20image%2020250614092955.png)

编译完成之后, SDK中的out目录也存放着交叉编译工具链, 路径为:
`/home/snbc/T113_Tina/out/toolchain/gcc-linaro-5.3.1-2016.05-x86_64_arm-linux-gnueabi/bin`
![](../fujian/Pasted%20image%2020250614093109.png)



为方便使用, 一般需要将交叉编译工具链的路径设置到环境变量中, 否则在使用arm-gcc编译命令时需要输出很长的文件路径
![](../fujian/Pasted%20image%2020250614093148.png)
![](../fujian/Pasted%20image%2020250614093156.png)
`export PATH=$PATH:/home/snbc/T113_Tina/out/toolchain/gcc-linaro-5.3.1-2016.05-x86_64_arm-linux-gnueabi/bin`
## makefile模板介绍
Linux环境下没有像keil一样的开发环境, 一般采用makefile进行编译, 下面为makefile的内容, 一般开发者仅需掌握如何进行少量调整即可
一个完整的工程包括顶层目录、子目录, 于是对应着顶层makefile、各个子目录的makefile
### 顶层makefile
“Makefile”文件

“Makefile. build”文件

### “makefile” (子目录)
## makefile 的修改

### 设置交叉编译工具链
![](../fujian/Pasted%20image%2020250614093717.png)
### 设置文件包含路径
![](../fujian/Pasted%20image%2020250614093746.png)
### 加入源码文件
![](../fujian/Pasted%20image%2020250614093754.png)
## 应用程序开发
### 共享工程文件
可以在Windows下编写代码, 在Ubuntu  中编译代码, 比较方便。当然也可以根据自己的喜好使用其他方式 (比如使用ftp互传等、ssh远程等)。注: 如果使用虚拟机可以采用此方法, 如果使用服务器需要使用vscode远程代码编辑、及ssh的方式。
### 编写代码并调整 makefile 文件
![](../fujian/Pasted%20image%2020250614093852.png)
![](../fujian/Pasted%20image%2020250614093859.png)
### 编译代码
![](../fujian/Pasted%20image%2020250614093911.png)