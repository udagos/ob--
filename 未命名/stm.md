F:\anfulai\STM32-V7裸机例程

## 参考
参考手册-对芯片每个外设的具体描述和功能介绍
数据手册-系列芯片的引脚定义、电气特性、机械封装、料号定义等信息。
内核编程手册-对内核的系统控制块的介绍。这个手册有时候也要用到, 比如我们需要了解 NVIC 和 SysTick 相关的寄存器, 就需要使用这个手册
勘误手册
闪存编程手册
应用笔记
用户手册-一般是对某个软件库的说明文档


## SecureCRT 使用方法:
## 输出重定位
[STM32应用开发进阶--UART串口重定向(printf)串口打印-CSDN博客](https://blog.csdn.net/luojuan198780/article/details/138044075)
## 硬件异常
## Event Recorder
## map
### “Memory Map of the image”
### “Image component sizes”

## 虚拟串口 
[【stm32@USB】应用-1：实现USB虚拟串口（CDC\_VPC） - FBshark - 博客园](https://www.cnblogs.com/FBsharl/p/17847962.html)
上位机无需编写专门的 USB 程序，只需要一个下载虚拟串口驱动程序+串口调试助手即可调试，非常实用。

[zhuanlan.zhihu.com/p/371849774](https://zhuanlan.zhihu.com/p/371849774)
通常我们使用 STM32进行[串口通信](https://zhida.zhihu.com/search?q=%E4%B8%B2%E5%8F%A3%E9%80%9A%E4%BF%A1&zhida_source=entity&is_preview=1)会选择其硬件串口，但在某些情况下串口会不够用，这个时候就可以选择 USB 的虚拟串口，这样可以增加一个串口。

虚拟串口与 usb 转串口的区别




带 fifo 的 uart
和 dma 实现的 uart


## 按键 fifo 实现
**getkey 和 putkey 对缓冲区数组的实现**，其中用的 uart 是缓冲区
## 串口hal

## 串口 fifo
![[Pasted image 20241014102944.png]]

 第 1 阶段, 初始化:  
	通过函数 bsp_InitUart 初始化串口结构体, 串口硬件参数。 
 第 2 阶段, 串口中断服务程序:  
	 接收中断是一直开启的。  
	 做了发送空中断和发送完成中断的消息处理。  
 第 3 阶段, 串口数据的收发:  
	 串口发送函数会开启发送空中断。 
	 串口接收中断接收到函数后, 可以使用函数 comGetChar 获取数据。

“**串口中断服务程序是最核心的部分**”
 收到新的数据后, 会将数据压入 RX_FIFO。 
 检测到发送缓冲区空后, 会从 TX_FIFO 中取下一个数据并发送。  
 如果是 RS485 半双工串口, 发送前会设置一个 GPIO=1 控制 RS485 收发器进入发送状态, 当最后一个字节的最后一个 bit 传送完毕后, 设置这个 GPIO=0 让 RS485 收发器进入接收状态。

下面我们分析一下串口中断处理的完整过程。
当产生串口中断后 , CPU 会查找中断向量表 , 获得中断服务程序的入口地址。入口函数为  USART1_IRQHandler, 这个函数在启动文件 startup_stm32f429xx. s 汇编代码中已经有实现。我们在 c  代码中需要重写一个同样名字的函数就可以重载它



**仍然是 uart 缓冲区而不是fifo**
#### 接受中断
if USART_SR_RXNE
	//从串口接收数据寄存器读取数据存放到接收FIFO
	ch = READ_REG(_pUart->uart->DR);
        _pUart->pRxBuf[_pUart->usRxWrite] = ch;

#### 发送 (\_ucaBuf)
//处理发送缓冲区空中断
if USART_SR_TXE
	_pUart->uart->DR = _pUart->pTxBuf[_pUart->usTxRead];
//数据 bit 位全部发送完毕的中断
if USART_SR_TC

所有 bit 和发送缓冲区空的区别？

UartSend (_ucaBuf)
	while 1
		数据已填满缓冲区
			USART_CR 1_TXEIE 置 1
	\_pUart->pTxBuf[_pUart->usTxWrite] = _ucaBuf[i];


UartGetChar
	\*\_pByte = \_pUart->pRxBuf[_pUart->usRxRead];

pRxBuf 是哪个 fifo
## spi 的hal
## flash 读写功能，查询、中断、dma
sf_ReadBuffer（buf, readaddr, size）
	bsp_spiTransfer
		HAL_SPI_TransmitReceive
	
## fmc 的 hal
## fmc

