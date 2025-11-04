---
up:
  - "[[../moc/MocCotex|MocCotex]]"
---

## Debug外设工作原理

![](../fujian/Pasted%20image%2020250616101824.png)
DBG支持模块（红框标注部分，也可以看作一个外设）通过一条专用的**AHB-AP总线**和调试接口相连（Jtag或swd），并且有与**数据**和**外设**总线直接相连的**桥接器**。
它还同时连接了中断嵌套管理器（因此同样可以**捕获中断并进行debug**）和**ITM、DWT、FPB这些调试支持模块**。因此DBG可以直接获取内存或片上外设内的数据而不需要占用CPU的资源，并将这些数据通过专用外设总线发送给调试器，进而在上位机中读取。

FPB是flash patch breakpoint闪存指令断点的缩写，用于**提供代码断点插入的支持**，当CPU的指令寄存器读取到某一条指令时，FPB会监测到它的动作，并通知TPIU暂停CPU进行现场保护。

DWT是data watch trace数据观察与追踪单元的缩写，**用于比较debug变量的大小，并追踪变量值的变化**。当你设定了比较断点规则（当某个数据大于/小于某个值时暂停程序）或将变量加入watch进行查看，DWT就会开始工作。DWT还提供了一个额外的计时器，即所有可见的TIM资源之外的另一个硬件计时器（因为调试其他硬件定时器的计时由于时钟变化可能定时不准，而DWT定时器是始终正常运行的）。它用于给自身和其他调试器模块产生的信息打上时间戳。我们的bsp中也封装了dwt计时器，你可以使用它来计时。

ITM是instrument trace macrocell**指令追踪宏单元的缩写，它用于提供非阻塞式的日志发送支持**（相当于大家常用的串口调试），SEGGER RTT就可以利用这个模块，向上位机发送日志和信息。这个硬件还可以追踪CPU执行的所有指令，这也被称作**trace**（跟踪），并将执行过的指令全部通过调试器发送给上位机。当debug无法定位bug所在的时候，逐条查看cpu执行的指令是一个绝佳的办法，特别是你有大量的中断或开启了实时系统时。

以上三个模块都需要通过TPIU（trace port interface unit）和外部调试器（j-link等）进行连接，TPIU会将三个模块发来的数据进行封装并通过DWT记录时间，发送给上位机。
## GDB调试MCU原理
![](../fujian/Pasted%20image%2020250616102222.png)
不论使用MDK（KEIL）还是VSCode还是Ozone，实际上背后的流程相同。
首先GDB会建立TCP/IP端口并提供接口，调试服务器（Server）作为硬件调试器和GDB软件的桥梁，将硬件调试器的相关功能（也就是DBG外设支持的那些功能）映射到GDB的接口上（通过连接到GDB建立的端口）。
之后启动调试，将可执行文件下载到目标MCU上，然后从main开始执行
	而对于直接运行在电脑上的程序（.exe），就不需要GDBserver和物理调试器，GDB程序可以直接访问电脑上运行的程序和CPU的寄存器等。



MinGW、Arm GNU toolchain和OpenOCD也可以通过**MSYS2**使用pacman包管理器（和apt/yum类似）直接安装，这种方法一步到位，**==这是更推荐使用的方式==**，请参看[附录5](https://gitee.com/hnuyuelurm/basic_framework/blob/master/.Doc/VSCode%2BOzone%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95.md##%E9%99%84%E5%BD%955%EF%BC%9A%E5%88%A9%E7%94%A8MSYS2%E5%AE%89%E8%A3%85%E4%BE%9D%E8%B5%96%E7%8E%AF%E5%A2%83)。