---
up:
  - "[[../moc/MocCotex|MocCotex]]"
---
**开启该外设时钟**
**配置 GPIO_InitTypeDef**
GPIO_Init(GPIO_TypeDef* **GPIOx**,  **GPIO_InitTypeDef*** GPIO_InitStruct)
	GPIOx->BRR


**GPIOx 是外设映射的地址**


**存储器映射**
也是我们最关心的三个块 Block 0 用来设计成内部 FLASH，Block 1 用来设计成内部 RAM，Block 2 用来设计成片上的外设
**寄存器映射**
Block 2 这块区域，设计的是片上外设，它们以四个字节为一个单元
![[Pasted image 20240724164822.png]]
![[Pasted image 20240724164829.png]]
![[Pasted image 20240724164838.png]]


![[Pasted image 20240724182750.png]]
寄存器组起始地址
![[Pasted image 20240724183004.png]]
![[Pasted image 20240724183013.png]]
stm 已经固定好了

SRAM 的起始地址是 0 x 20000000。
flash 的起始地址为


DMA_Init(DMA_CHANNEL, &DMA_InitStructure);
## 总线 
![[Pasted image 20240724184625.png]]
ICode 总线
	闪存
DCode 总线
	闪存
系统总线
	链接内核的系统总线 (外设总线)到总线矩阵
	总线矩阵协调着内核和 DMA 间的访问
DMA 总线
	将 DMA 的 AHB 主控接口与总线矩阵相联
	总线矩阵协调着DCode和DMA到SRAM、闪存和外设的访问
总线矩阵
	协调**内核系统总线和 DMA 主控总线之间的访问仲裁**
AHB 外设通过总线矩阵与系统总线相连, 允许 DMA 访问。