```
---
tags: Xilinx Zynq-7000 嵌入式系统设计与实现 基于ARM Cortex-A9双核处理器和Vivado的设计方法
---
```

# 导论 
## Zynq -7000 SoC功能和结构
![](../fujian/Pasted%20image%2020250413102444.png)
![](../fujian/Pasted%20image%2020250413102453.png)
### Zynq - 7000 SoC 的功能 
![](../fujian/Pasted%20image%2020250413102538.png)
### Zynq -7000 SoC处理系统PS的构成
1 .应用处理器单元APU
(13) DMA控制器
(14) 通用的中断控制
2.存储器接口
1) DDR控制器 
2) 四-SPI控制器
3) 静态存储器控制器 (Static Memory Controller, SMC)
3.I /O外设
4) 通用输入/输出端口 GPIO
5) 两个三模式以太网控制器
6) 两个USB控制器
7) 两个SD/SDIO控制器
8) 两个SPI控制器
9) 两个CAN控制器
10) 两个UART控制器
11) ) 两个12c控制器
12) 总共54个PS 一侧的MI0引脚

### Zynq -7000 SoC可编程逻辑PL的构成
### Zynq -7000 SoC内的互联结构
### Zynq -7000 SoC 内 MIO 到 EMIO 的连接
### Zynq-7000 SoC内为PL分配的信号

## Zynq -7000 SoC在嵌入式系统中的优势
### 使用PL实现软件算法
### 降低功耗 
### 实时减负 
### 可重配置计算
# dma
## DMA控制器架构
DMAC能配置为最多8个通道, 每个通道能支持一个单独并发的DMA操作线程。当一个DMA线程执行一个加载或保存指令时, DMA引擎将存储器请求添加到相关的读/写队列中。DMA控制器使用这些队列来缓冲AX1读/写传输:在DMA传输过程中,DMA控制器包含一个多通道先进先出队列 (MultichannelFisrt-in-First-Out, MFIFO), 用于保存数据。运行在DMA引擎处理器上的程序代码, 将MFIFO看作用于DMA读/写交易的一个可变深度的并行FIFO。程序代码必须管理MFIFO, 因为所有DMA的FIFO的总深度不能超过1024字节MFIFO

DMA控制器的系统结构
![](../fujian/Pasted%20image%2020250413093141.png)
DMA控制器的内部结构
![](../fujian/Pasted%20image%2020250413093158.png)
## DMA控制器功能
所有的DMA交易均使用AXI主接口在OCM、DDR存储器和PL内的从设备之间移动数据。PL内的从外设通常连接到DMAC外设请求接口, 用于控制数据流。DMAC能访问PS内的外设, 但是通常这毫无用处, 因为这些路径上没有流控制信号。

DMAC所使用的数据路径如图11.3所示。图中没有给出外设请求接口 (用于流控制)。每个AXI路径均可读/写。它们之间有很多组合, 典型的两个DMA交易如下:
(1) 存储器到存储器交易, 即OCM至DDR存储器; 
(2) 存储器和PL外设之间的交易, 即DDR存储器至PL外设
![](../fujian/Pasted%20image%2020250413093354.png)
## DMA控制器编程指南 
### 启动控制器
### 执行DMA传输
### 中断服务例程
### 寄存器描述 
## DMA引擎编程指南
## 编程限制
## Vivado环境下DMA传输的实现
在Vivado环境下, 实现在xc7z020clg484内PS一侧, 将数据从系统存储器的一个源地址空间搬移到系统存储器的另一个目的地址空间。并且, 对8个DMA通道都进行数据传输的测试和验证。在该设计中, 还包括一个中断句柄, 用于在每个DMA传输结束产生中断时, 对其进行处理。
### DMA控制器初始化流程
![](../fujian/Pasted%20image%2020250413093749.png)
### 中断控制器初始化流程
![](../fujian/Pasted%20image%2020250413093807.png)
### 中断服务句柄处理流程 
中断服务程序对DMA结束时所产生中断事件的处理过程
![](../fujian/Pasted%20image%2020250413093829.png)
### 导出硬件设计到SDK
### 创建新的应用工程
### 运行软件应用工程
# Cortex - A9外设模块结构及功能
本章主要介绍了 Zynq平台的主要外设模块
## DDR存储器控制器
## 静态存储器控制器
## 四-SPI Flash 控制器
## SD/SDIO外设控制器
## USB主机、设备和OTG控制器
## 吉比特以太网控制器
## spi控制器 
![](../fujian/Pasted%20image%2020250413095214.png)
### SPI控制器的接口及功能
SPI控制器的块图如图14.44所示
![](../fujian/Pasted%20image%2020250413095250.png)
## CAN控制器
## UART控制器
## 12c控制器
## ADC转换器接口
## PCI-E 接口
# Zynq -7000 SoC 内  XADC原理及实现
