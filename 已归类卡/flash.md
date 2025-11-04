---
up:
  - "[[../moc/MocCotex|MocCotex]]"
---
Nor-Flash 中的 Nor 是或非门的缩写。

Nor-Flash 每个 Bit Line 中的存储单元是并联的, 当某个 Word Line 被选中后, 就可以实现对该 Word 的读取, 即可以进行字节读取。

Nand-Flash
Nand-Flash 中的 Nand 是与非门的缩写。
==Nand-Flash无法进行字节读取, 也就无法在Nand-Flash上直接执行程序。==
## flash分类 
按组成结构
#### Nor-Flash 
Nor-Flash通常使用SPI接口 (串行口) 与MCU连接。
![|725](../附件/Pasted%20image%2020250303153130.png)
#### Nand Fla sh
Nand-Flash通常使用FSMC接口 (并行口) 与MCU连接。
![|675](../附件/Pasted%20image%2020250303153215.png)

### 依据使用方法分类
#### eFlash 
仅有片内Flash。代码和数据 (字库、EEP等) 全部存放到片内Flash; ==程序在片内Flash中执行。==
#### Flash + SPI-Flash
片内Flash + 片外Flash。片外Flash通过普通SPI接口连接, ==MCU通过直接发送命令的方式操作Flash==。==程序在片内Flash  中执行, 片外Flash只存放数据, 不能执行程序。==
#### QSPI-Flash
无片内Flash, 必须外挂片外串行Nor-Flash
通常该类MCU==有QSPIFlash存储控制器 (例如RT10xx的FlexSPI), 它可以将总线地址读取访问转化为对Flash的SPI控制时序。==

==该类MCU的代码和数据全部存放到Spi Flash; 程序在Spi Flash中执行。==

==SNBC2201定制芯片目前采用方式 (三), 通过SSI外设挂接片外Flash。==
## SPI Nor-Flash介绍
最常用的是SPINor-Flash
### SFDP
==每家厂商Flash用法各不相同==
JEDEC联合几家规模较大的厂商制定了SFDP (SerialFlashDiscoverableParameter) 标准, 厂商会使用==统一的标准, 将Flash相关信息固定到SFDP信息区中==, 仅供读取
### 状态寄存器 
SPINor-Flash提供三个状态/配置寄存器用于==对Flash进行配置==

常用的状态位有:QuadSPI设置、3/4字节地址设置 (最高有效字节)、BUSY状态位、写保护使能位等。
可以通过 (01h/31h/11h) 指令==写Flash状态寄存器==,通过 (05h/35h/15h) 指令==读Flash状态寄存器。==
![](../fujian/Pasted%20image%2020250303154510.png)
### QE位
SPI-Flash==若使用四线模式, 需要将Flash状态寄存器的QE位置 1==, 此时 WP、HOLD 引脚会被复用为IO2、IO3。
![](../fujian/Pasted%20image%2020250303154551.png)
### 三/四字节地址
==Flash上电后==, 通过==读取状态寄存器的ADP位, 确认当前字节地址模式==。当ADP=0, 进入三字节地址模式; 当ADP=0, 进入四字节地址模式。
![](../fujian/Pasted%20image%2020250303154651.png)

“在Flash==初始化完成之后,还可以通过发送命令切换三/四字节地址模式”==
![](../fujian/Pasted%20image%2020250303154909.png)
### 单双四线
==通常我们说的单线 (Std), 双线 (Dual), 四线 (Quad), 指的是操作Flash时, 用于SPI传输数据的I/O数量。==
单线：
	**一个时钟周期内**，只通过 **一根数据线 (MISO)** 向 MCU 传输 **1 bit** 的数据。
双线：
	 **一个时钟周期内**，同时通过 **两根数据线 (IO0 和 IO1)** 向 MCU 传输 **2 bits** 的数据。
四线：
	**一个时钟周期内**，同时通过 **四根数据线 (IO0, IO1, IO2, IO3)** 向 MCU 传输 **4 bits** 的数据。

- **SPI Flash 读取操作 (单线、双线、四线)： 在 _实际应用_ 和 _数据传输阶段_，更偏向于 _半双工_ 或 _更接近半双工_ 的工作方式。** ==虽然 SPI 协议有全双工的能力==，但在典型的 Flash 读取操作中，并没有被充分利用来进行并发的双向数据传输。 ==数据流的主要方向是单向的 (命令和地址: Master -> Slave; 数据读取: Slave -> Master)。==
![](../fujian/Pasted%20image%2020250303155558.png)
![](../fujian/Pasted%20image%2020250303155604.png)
![](../fujian/Pasted%20image%2020250303155612.png)
### XIP
XIP (eXecuteInPlace), 即芯片内执行。
CPU的基本功能是取指、译码、运行。
==<span style="background:#ff4d4f">能在Nor-Flash中XIP, 指的是CPU能够直接从Nor-flash中取指令, 供后面的译码器和执行器来使用, 而不用再读到内存中。</span>==
## 221 flash介绍 
### 结构框图和总线地址映射
SNBC2201共有3个==SSI外设==, 均可以外挂串行Nor-Flash。最终芯片选择SSI1外挂串行Nor-Flash, 并将Flash合封到芯片封装中。SSI2、SSI3可以在MCU外部挂接串行Nor-Flash, ==并且同样支持XIP和AHB总线读数据==。
![](../fujian/Pasted%20image%2020250303155956.png)


其总线地址映射如表2.1所示:
![](../fujian/Pasted%20image%2020250303160024.png)
![](../fujian/Pasted%20image%2020250303160031.png)

### 支持XIP
### 支持Cache
## 221 flash应用
### 启动引导
==221芯片上电后, 默认会先进入芯片厂商在ROM中烧录的Bootloader。==此时SSI为初始单线模式, Flash读写效率低, 需要重新初始化。==在Bootloader中会从合封Flash起始地址处 (0x10000000), 读取4K大小的数据。==

==该4K区域为Flash配置信息区 (Config Page), 用于配置SSI外设的一系列参数, Boot loader读取后会根据配置信息, 将SSI重新初始化。==
### 配置信息
目前ConfigPage作为一个4K大小的数组, 存放在<FlashInfoConfig.c>中,

==Config Page需要放到合封Flash的起始地址处, 我们需要通过Keil的分散加载将Config Page链接到固定的地址, 代码如下。==
![](../fujian/Pasted%20image%2020250303160946.png)
### 烧写算法
由于总共有3个SSI外设, 并且SSI2有两组引脚复用, 因此共计12个烧写算法。
### ini文件
==Keil调试时是通过ini脚本文件启动, 没有经过ROM的引导启动, 由于在ROM中会初始化SSI XIP功能, 因此需要在ini文件中使能SSI XIP功能==, 才能在片外Flash执行程序。所以调试时需要根据实际情况选择相应的ini文件。
![](../fujian/Pasted%20image%2020250303161119.png)
由于总共有3个SSI外设、大于16MFlash时需要4Bytes地址访问、XIP读命令支持Dual和Quad模式, 因此共计有12个ini文件。