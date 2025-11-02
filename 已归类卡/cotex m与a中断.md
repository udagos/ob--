---
up:
  - "[[../moc/cotex]]"
---


[Linux之ARM Cortex-A7 中断系统详解\_cortex a7-CSDN博客](https://blog.csdn.net/weixin_45309916/article/details/108290225)
## STM32中断系统和 Cortex-M(STM32)中断系统的异同

STM32 的中断系统主要有以下几个关键点：

①、 中断向量表。  
②、 NVIC(内嵌向量中断控制器)。  
③、 中断使能。  
④、中断服务函数。
### 中断向量表
存放的是中断向量。中断服务程序的入口地址或存放中断服务程序的首地址成为中断向量，因此中断向量表是一系列中断服务程序入口地址组成的表。

这些中断服务程序 (函数) 在中断向量表中的位置是由半导体厂商定好的，当某个中断被触发以后就会自动跳转到中断向量表中对应的中断服务程序 (函数) 入口地址处。

中断向量表在整个程序的最前面，比如 STM32F103 的中断向量表如下所示：

```
__Vectors DCD __initial_sp 		 ; Top of Stack
			DCD Reset_Handler	     ; Reset Handler
			DCD NMI_Handler 		 ; NMI Handler
			DCD HardFault_Handler 	 ; Hard Fault Handler

```

我们说 ARM 处理器都是从地址 0X00000000 开始运行的，但是我们学习 STM32 的时候代码是下载到 0X8000000 开始的存储区域中。因此中断向量表是存放到 0X8000000 地址处的
==Cortex-M 架构引入了一个新的概念——中断向量表偏移，通过中断向量表偏移就可以将中断向量表存放到任意地址处==，
中断向量表偏移配置在函数 SystemInit 中完成，通过向 SCB_VTOR 寄存器写入新的中断向量表首地址即可，代码如下所示：
```
void SystemInit (void)
{
	RCC->CR |= (uint32_t)0x00000001;
	
	/* 省略其它代码 */
	
	#ifdef VECT_TAB_SRAM
	SCB->VTOR = SRAM_BASE | VECT_TAB_OFFSET;
	#else
	SCB->VTOR = FLASH_BASE | VECT_TAB_OFFSET;
	#endif
}

```

```
#define FLASH_BASE ((uint32_t)0x08000000) 
#define VECT_TAB_OFFSET 0x0
```
因此第 10 行的代码就是： SCB->VTOR=0X080000000，中断向量表偏移设置完成。


**STM32中断向量表和中断向量偏移和I.MX6U中断向量表和中断向量偏移的关系？**
I.MX6U 所使用的 Cortex-A7 内核也有中断向量表和中断向量表偏移，而且其含义和 STM32 是一模一样的！只是用到的寄存器不同而已，概念完全相同。

### NVIC(内嵌向量中断控制器)
中断系统得有个管理机构，对于 STM32 这种 Cortex-M 内核的单片机来说这个管理机构叫做 NVIC
不过 Cortex-A 内核的中断管理机构不叫做NVIC，而是叫做 GIC
### 中断使能
以 STM32F103 的 PE2 这个 IO 为例，假如我们要使用 PE2 的输入中断肯定要使用如下代码来使能对应的中断：
```
NVIC_InitStructure.NVIC_IRQChannel = EXTI2_IRQn;
NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x02; 	//抢占优先级 2，
NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0x02; 			//子优先级 2
NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE; 				//使能外部中断通道
NVIC_Init(&NVIC_InitStructure);

```
上述代码就是使能 PE2 对应的 EXTI2 中断
### 中断服务函数
同样以 STM32F103 的 PE2 为例，其中断服务函数如下所示：
```
/* 外部中断 2 服务程序 */
void EXTI2_IRQHandler(void)
{
/* 中断处理代码 */
}

```

## Cortex-A7 中断系统详解
跟 STM32 一样， Cortex-A7 也有中断向量表，中断向量表也是在代码的最前面。 CortexA7 内核有 8 个异常中断，这 8 个异常中断的中断向量表如下表所示：

![](../fujian/Pasted%20image%2020250715155440.png)
实际只有 7 个中断。和“示例代码的 STM32F103 中断向量表比起来少了很多！难道一个能跑 Linux 的芯片只有这 7 个中断？明显不可能的！那类似 STM32 中的EXTI9_5_IRQHandler、 TIM2_IRQHandler 这样的中断向量在哪里？ I2C、 SPI、定时器等等的中断怎么处理呢？
这个就是 Cortex-A 和 Cotex-M 在中断向量表这一块的区别，对于 Cortex-M 内核来说，中断向量表列举出了一款芯片所有的中断向量，包括芯片外设的所有中断。对于 CotexA 内核来说并没有这么做，
在上表中有个 IRQ 中断， ==Cortex-A 内核 CPU 的所有外部中断都属于这个 IQR 中断，当任意一个外部中断发生的时候都会触发 IRQ 中断。在 IRQ 中断服务函数里面就可以读取指定的寄存器来判断发生的具体是什么中断==，进而根据具体的中断做出相应的处理。这些外部中断和 IQR 中断的关系如图所示：
![](../fujian/Pasted%20image%2020250715155658.png)
在上面的 7 个中断中，我们常用的就是复位中断和 IRQ 中断，所以我们需要编写这两个中 断的中断服务函数。

首先我们要根据表的内容来创建中断向量表，中断向量表处于程序最开始的地方，比如我们前面例程的 start.S 文件最前面，中断向量表如下：
```
.global _start /* 全局标号 */

_start:
	ldr pc, =Reset_Handler /* 复位中断 */
	ldr pc, =Undefined_Handler /* 未定义指令中断 */
	ldr pc, =SVC_Handler /* SVC(Supervisor)中断 */
	ldr pc, =PrefAbort_Handler /* 预取终止中断 */
	ldr pc, =DataAbort_Handler /* 数据终止中断 */
	ldr pc, =NotUsed_Handler /* 未使用中断 */
	ldr pc, =IRQ_Handler /* IRQ 中断 */
	ldr pc, =FIQ_Handler /* FIQ(快速中断)未定义中断 */

/* 复位中断 */
Reset_Handler:
/* 复位中断具体处理过程 */

/* 未定义中断 */
 Undefined_Handler:
	ldr r0, =Undefined_Handler
	bx r0

/* SVC 中断 */
SVC_Handler:
	ldr r0, =SVC_Handler
	bx r0

/* 预取终止中断 */
PrefAbort_Handler:
	ldr r0, =PrefAbort_Handler
	bx r0

/* 数据终止中断 */
DataAbort_Handler:
	ldr r0, =DataAbort_Handler
	bx r0

/* 未使用的中断 */
NotUsed_Handler:

	ldr r0, =NotUsed_Handler
	bx r0

 /* IRQ 中断！重点！！！！！ */
IRQ_Handler:
/* 复位中断具体处理过程 */

FIQ_Handler:
	ldr r0, =FIQ_Handler
	bx r0

```

第 4 到 11 行是中断向量表，当指定的中断发生以后就会调用对应的中断复位函数，比如复位中断发生以后就会执行第 4 行代码，也就是调用函数 Reset_Handler，函数 Reset_Handler就是复位中断的中断复位函数，其它的中断同理。

第 14 到 50 行就是对应的中断服务函数，中断服务函数都是用汇编编写的，我们实际需要编写的只有复位中断服务函数 Reset_Handler 和 IRQ 中断服务函数 IRQ_Handler，其它的中断本教程没有用到，所以都是死循环。
### GIC 控制器简介
#### GIC 控制器总览
目前 GIC 有 4 个版本:V1~V4， V1 是最老的版本，已经被废弃了。 V2~V4 目前正在大量的使用。 GIC V2 是给 ARMv7-A 架构使用的，比如 Cortex-A7、 Cortex-A9、 Cortex-A15 等，V3 和 V4 是给 ARMv8-A/R 架构使用的，也就是 64 位芯片使用的。

主要讲解 GIC V2。 GIC V2 最多支持 8 个核。 ARM 会根据 GIC 版本的不同研发出不同的 IP 核，那些半导体厂商直接购买对应的 IP 核即可，比如 **ARM 针对 GIC V2 就开发出了 GIC400 这个中断控制器 IP 核。**
**当 GIC 接收到外部中断信号以后就会报给 ARM 内核，但是ARM 内核只提供了四个信号给 GIC 来汇报中断情况： VFIQ、 VIRQ、 FIQ 和 IRQ，他们之间的关系如图所示：**
![](../fujian/Pasted%20image%2020250715160014.png)
在上图中， GIC 接收众多的外部中断，然后对其进行处理，最终就只通过四个信号报给 ARM 内核，这四个信号的含义如下：
- VFIQ:虚拟快速 FIQ。
- VIRQ:虚拟快速 IRQ。
- FIQ:快速中断 IRQ。
- IRQ:外部中断 IRQ

本博文我们只使用 IRQ，所以相当于 GIC 最终向 ARM 内核就上报一个 IRQ信号。那么 GIC 是如何完成这个工作的呢？ GICV2 的逻辑图如图下所示：
![](../fujian/Pasted%20image%2020250715160244.png)
图中左侧部分就是中断源，中间部分就是 GIC 控制器，最右侧就是中断控制器向处理器内核发送中断信息。我们重点要看的肯定是中间的 GIC 部分， GIC 将众多的中断源分为分为三类：
①、 SPI (Shared Peripheral Interrupt), 共享中断，顾名思义，所有 Core 共享的中断，这个是最常见的，那些**外部中断都属于 SPI 中断** (注意！不是 SPI 总线那个中断) 。比如按键中断、串口中断等等，这些中断所有的 Core 都可以处理，不限定特定 Core。
②、 PPI (Private Peripheral Interrupt)，私有中断，我们说了 **GIC 是支持多核的，每个核肯定有自己独有的中断**。这些独有的中断肯定是要指定的核心处理，因此这些中断就叫做私有中断。
③、 SGI (Software-generated Interrupt)，软件中断，由软件触发引起的中断，通过向寄存器GICD_SGIR 写入数据来触发，系统会使用 SGI 中断来完成多核之间的通信。
#### 中断 ID
中断源有很多，为了区分这些不同的**中断源肯定要给他们分配一个唯一 ID，这些 ID 就是中断 ID**。每一个 CPU 最多支持 1020 个中断 ID，中断 ID 号为 ID0~ID1019。这 1020 个 ID 包含了 PPI、 SPI 和 SGI，那么这三类中断是如何分配这 1020 个中断 ID 的呢？这 1020 个 ID 分配如下：
ID0~ID15：这 16 个 ID 分配给 SGI。
ID16~ID31：这 16 个 ID 分配给 PPI。
ID32~ID1019：这 988 个 ID 分配给 SP。


I.MX6U 的总共使用了 128 个中断 ID，加上前面属于 PPI 和 SGI 的 32 个 ID， I.MX6U 的中断源共有 128+32=160个，这 128 个中断 ID 对应的中断在《I.MX6ULL 参考手册》的“3.2 Cortex A7 interrupts”小节，中断源如表所示：
![](../fujian/Pasted%20image%2020250715160436.png)

NXP 官方 SDK中的文件 MCIMX6Y2C.h，在此文件中定义了一个**枚举类型 IRQn_Type**，此枚举类型就枚举出了 I.MX6U 的所有中断，代码如下所示：
```
typedef enum IRQn {
  /* Auxiliary constants */
  NotAvail_IRQn                = -128,             /**< Not available device specific interrupt */

  /* Core interrupts */
  Software0_IRQn               = 0,                /**< Cortex-A7 Software Generated Interrupt 0 */
  Software1_IRQn               = 1,                /**< Cortex-A7 Software Generated Interrupt 1 */
} IRQn_Type;
```

#### GIC 逻辑分块
GIC 架构分为了两个逻辑块： Distributor 和 CPU Interface，也就是分发器端和 CPU 接口端。这两个逻辑块的含义如下：

Distributor (分发器端)： 
从GICV2 的逻辑图中可以看出，此逻辑块负责处理各个中断事件的分发问题，也就是中断事件应该发送到哪个 CPU Interface 上去。
分发器收集所有的中断源，可以控制每个中断的优先级，它总是将优先级最高的中断事件发送到 CPU 接口端。分发器端要做的主要工作如下：
①、全局中断使能控制。
②、控制每一个中断的使能或者关闭。
③、设置每个中断的优先级。
④、设置每个中断的目标处理器列表。
⑤、设置每个外部中断的触发模式：电平触发或边沿触发。
⑥、设置每个中断属于组 0 还是组 1。

CPU Interface (CPU 接口端)： 
CPU 接口端听名字就知道是和 CPU Core 相连接的，因此在图中每个 CPU Core 都可以在 GIC 中找到一个与之对应的 CPU Interface。 CPU 接口端就是分发器和 CPU Core 之间的桥梁， CPU 接口端主要工作如下：
①、使能或者关闭发送到 CPU Core 的中断请求信号。
②、应答中断。
③、通知中断处理完成。
④、设置优先级掩码，通过掩码来设置哪些中断不需要上报给 CPU Core。
⑤、定义抢占策略。
⑥、当多个中断到来的时候，选择优先级最高的中断通知给 CPU Core。

构体里面的寄存器分为了分发器端和 CPU 接口端，寄存器定义如下所示：
```
typedef struct
{
        uint32_t RESERVED0[1024];
  __IOM uint32_t D_CTLR;                 /*!< Offset: 0x1000 (R/W) Distributor Control Register */
  __IM  uint32_t D_TYPER;                /*!< Offset: 0x1004 (R/ )  Interrupt Controller Type Register */
  __IM  uint32_t D_IIDR;                 /*!< Offset: 0x1008 (R/ )  Distributor Implementer Identification Register */
        uint32_t RESERVED1[29];
  __IOM uint32_t D_IGROUPR[16];          /*!< Offset: 0x1080 - 0x0BC (R/W) Interrupt Group Registers */
        uint32_t RESERVED2[16];
  __IOM uint32_t D_ISENABLER[16];        /*!< Offset: 0x1100 - 0x13C (R/W) Interrupt Set-Enable Registers */
        uint32_t RESERVED3[16];
  __IOM uint32_t D_ICENABLER[16];        /*!< Offset: 0x1180 - 0x1BC (R/W) Interrupt Clear-Enable Registers */
        uint32_t RESERVED4[16];
  __IOM uint32_t D_ISPENDR[16];          /*!< Offset: 0x1200 - 0x23C (R/W) Interrupt Set-Pending Registers */
        uint32_t RESERVED5[16];
  __IOM uint32_t D_ICPENDR[16];          /*!< Offset: 0x1280 - 0x2BC (R/W) Interrupt Clear-Pending Registers */
        uint32_t RESERVED6[16];
  __IOM uint32_t D_ISACTIVER[16];        /*!< Offset: 0x1300 - 0x33C (R/W) Interrupt Set-Active Registers */
        uint32_t RESERVED7[16];
  __IOM uint32_t D_ICACTIVER[16];        /*!< Offset: 0x1380 - 0x3BC (R/W) Interrupt Clear-Active Registers */
        uint32_t RESERVED8[16];
  __IOM uint8_t  D_IPRIORITYR[512];      /*!< Offset: 0x1400 - 0x5FC (R/W) Interrupt Priority Registers */
        uint32_t RESERVED9[128];
  __IOM uint8_t  D_ITARGETSR[512];       /*!< Offset: 0x1800 - 0x9FC (R/W) Interrupt Targets Registers */
        uint32_t RESERVED10[128];
  __IOM uint32_t D_ICFGR[32];            /*!< Offset: 0x1C00 - 0xC7C (R/W) Interrupt configuration registers */
        uint32_t RESERVED11[32];
  __IM  uint32_t D_PPISR;                /*!< Offset: 0x1D00 (R/ ) Private Peripheral Interrupt Status Register */
  __IM  uint32_t D_SPISR[15];            /*!< Offset: 0x1D04 - 0xD3C (R/ ) Shared Peripheral Interrupt Status Registers */
        uint32_t RESERVED12[112];
  __OM  uint32_t D_SGIR;                 /*!< Offset: 0x1F00 ( /W) Software Generated Interrupt Register */
        uint32_t RESERVED13[3];
  __IOM uint8_t  D_CPENDSGIR[16];        /*!< Offset: 0x1F10 - 0xF1C (R/W) SGI Clear-Pending Registers */
  __IOM uint8_t  D_SPENDSGIR[16];        /*!< Offset: 0x1F20 - 0xF2C (R/W) SGI Set-Pending Registers */
        uint32_t RESERVED14[40];
  __IM  uint32_t D_PIDR4;                /*!< Offset: 0x1FD0 (R/ ) Peripheral ID4 Register */
  __IM  uint32_t D_PIDR5;                /*!< Offset: 0x1FD4 (R/ ) Peripheral ID5 Register */
  __IM  uint32_t D_PIDR6;                /*!< Offset: 0x1FD8 (R/ ) Peripheral ID6 Register */
  __IM  uint32_t D_PIDR7;                /*!< Offset: 0x1FDC (R/ ) Peripheral ID7 Register */
  __IM  uint32_t D_PIDR0;                /*!< Offset: 0x1FE0 (R/ ) Peripheral ID0 Register */
  __IM  uint32_t D_PIDR1;                /*!< Offset: 0x1FE4 (R/ ) Peripheral ID1 Register */
  __IM  uint32_t D_PIDR2;                /*!< Offset: 0x1FE8 (R/ ) Peripheral ID2 Register */
  __IM  uint32_t D_PIDR3;                /*!< Offset: 0x1FEC (R/ ) Peripheral ID3 Register */
  __IM  uint32_t D_CIDR0;                /*!< Offset: 0x1FF0 (R/ ) Component ID0 Register */
  __IM  uint32_t D_CIDR1;                /*!< Offset: 0x1FF4 (R/ ) Component ID1 Register */
  __IM  uint32_t D_CIDR2;                /*!< Offset: 0x1FF8 (R/ ) Component ID2 Register */
  __IM  uint32_t D_CIDR3;                /*!< Offset: 0x1FFC (R/ ) Component ID3 Register */

  __IOM uint32_t C_CTLR;                 /*!< Offset: 0x2000 (R/W) CPU Interface Control Register */
  __IOM uint32_t C_PMR;                  /*!< Offset: 0x2004 (R/W) Interrupt Priority Mask Register */
  __IOM uint32_t C_BPR;                  /*!< Offset: 0x2008 (R/W) Binary Point Register */
  __IM  uint32_t C_IAR;                  /*!< Offset: 0x200C (R/ ) Interrupt Acknowledge Register */
  __OM  uint32_t C_EOIR;                 /*!< Offset: 0x2010 ( /W) End Of Interrupt Register */
  __IM  uint32_t C_RPR;                  /*!< Offset: 0x2014 (R/ ) Running Priority Register */
  __IM  uint32_t C_HPPIR;                /*!< Offset: 0x2018 (R/ ) Highest Priority Pending Interrupt Register */
  __IOM uint32_t C_ABPR;                 /*!< Offset: 0x201C (R/W) Aliased Binary Point Register */
  __IM  uint32_t C_AIAR;                 /*!< Offset: 0x2020 (R/ ) Aliased Interrupt Acknowledge Register */
  __OM  uint32_t C_AEOIR;                /*!< Offset: 0x2024 ( /W) Aliased End Of Interrupt Register */
  __IM  uint32_t C_AHPPIR;               /*!< Offset: 0x2028 (R/ ) Aliased Highest Priority Pending Interrupt Register */
        uint32_t RESERVED15[41];
  __IOM uint32_t C_APR0;                 /*!< Offset: 0x20D0 (R/W) Active Priority Register */
        uint32_t RESERVED16[3];
  __IOM uint32_t C_NSAPR0;               /*!< Offset: 0x20E0 (R/W) Non-secure Active Priority Register */
        uint32_t RESERVED17[6];
  __IM  uint32_t C_IIDR;                 /*!< Offset: 0x20FC (R/ ) CPU Interface Identification Register */
        uint32_t RESERVED18[960];
  __OM  uint32_t C_DIR;                  /*!< Offset: 0x3000 ( /W) Deactivate Interrupt Register */
} GIC_Type;

```
结构体 GIC_Type 就是 GIC 控制器，列举出了 GIC 控制器的所有寄存器，可以**通过结构体 GIC_Type 来访问 GIC 的所有寄存器**。
第 5 行是 GIC 的分发器端相关寄存器，其相对于 GIC 基地址偏移为 0X1000，因此我们获取到 GIC 基地址以后只需要加上 0X1000 即可访问 GIC 分发器端寄存器。
第 51 行是 GIC 的 CPU 接口端相关寄存器，其相对于 GIC 基地址的偏移为 0X2000，同样的，获取到 GIC 基地址以后只需要加上 0X2000 即可访问 GIC 的 CPU 接口段寄存器。

那么问题来了？ GIC 控制器的寄存器基地址在哪里呢？这个就需要用到 Cortex-A 的 CP15 协处理器了
### CP15 协处理器
CP15 协处理器一般用于存储系统管理，但是在中断中也会使用到， CP15 协处理器一共有16 个 32 位寄存器。 CP15 协处理器的访问通过如下几个指令完成：
![](../fujian/Pasted%20image%2020250715160949.png)
`MCR{cond} p15, <opc1>, <Rt>, <CRn>, <CRm>, <opc2>`
![](../fujian/Pasted%20image%2020250715161013.png)
MRC 的指令格式和 MCR 一样，只不过在 MRC 指令中 Rt 就是目标寄存器，也就是从CP15 指定寄存器读出来的数据会保存在 Rt 中。而 CRn 就是源寄存器，也就是要读取的写处理器寄存器。

假如我们要将 CP15 中 C0 寄存器的值读取到 R0 寄存器中，那么就可以使用如下命令：
`MRC p15, 0, r0, c0, c0, 0`

CP15 协处理器有 16 个 32 位寄存器， c0~c15
#### c0 寄存器
CP15 协处理器有 16 个 32 位寄存器， c0~c15，
在使用 MRC 或者 MCR 指令访问这 16 个 寄存器的时候，**指令中的 CRn、 opc1、 CRm 和 opc2 通过不同的搭配，其得到的寄存器含义是**  
**不同的**。
比如 c0 在不同的搭配情况下含义如下图所示：

####  总结
![](../fujian/Pasted%20image%2020250715161220.png)
### 中断使能
中断使能包括两部分，一个是 IRQ 或者 FIQ 总中断使能，另一个就是 ID0~ID1019 这 1020个中断源的使能。
#### IRQ 和 FIQ 总中断使能
####  ID0~ID1019 中断使能和禁止

### 中断优先级设置
#### 优先级数配置
#### 抢占优先级和子优先级位数设置