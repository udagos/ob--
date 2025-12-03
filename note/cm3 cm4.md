加载存储架构
	例如，==要增加SRAM中存储的数据值，处理器需要使用一条指令从SRAM中读出数据，并且将数据放到处理器的寄存器中，然后使用第二条指令增加寄存器中的数据值，最后使用第三条指令将数值写回存储器


外设经过了存储器映射，这也就意味着**寄存器可以从系统存储器映射中访问**==
一般来说，==**外设在使用前需要初始化，一般包括以下几步**==：
- 设置时钟控制回路使能连接到外设和对应引脚的时钟。
- 可能还需要配置I/o引脚的操作模式。大多数微控制器都有复用的i/o 引脚
- 外设配置。多数外设中包含多个可编程寄存器, 它们需要在使用前进行配置
- 中断配置


加载域运行域
	==因为MCU没上电时RAM中没有数据，所以此时所有的东西（包括代码、变量、初始值等）都是存放在flash中的，当上电后又要把变量等复制到RAM中才能正常运行。这就涉及到程序的加载时域和运行时域。==
	![](../fujian/Pasted%20image%2020250314104427.png)



![](../../fujian/Pasted%20image%2020250302111852.png)

基于Cortex-M3或Cortex-M4的简单系统 ([pdf](zotero://open-pdf/library/items/UID4KR72?page=166&annotation=KHEMSDN3))

![](../../fujian/Pasted%20image%2020250302112642.png)
Cortex-M3总线连接样板范例 ([pdf](zotero://open-pdf/library/items/HCL636HZ?page=105&annotation=GCC837XY))


![](../fujian/Pasted%20image%2020250302111933.png)
总线矩阵


![](../../fujian/Pasted%20image%2020250717150756.png)

![](../fujian/Pasted%20image%2020250314112033.png)
**Cortex-M3 内核的总线接口:** Cortex-M3 内核本身提供了多个总线接口，用于连接到系统总线：
- **I-Code 总线 (Instruction Code Bus):** **指令总线**，用于 **取指令 (Instruction Fetch)**。<span style="background:#ff4d4f"> CPU 通过 I-Code 总线从指令存储器 (通常是 Flash 或 指令 Cache) 读取指令。</span>
- **D-Code 总线 (Data Code Bus):** **数据总线**，主要用于 **<span style="background:#ff4d4f">获取字面量数据</span> (literal data)**，<span style="background:#ff4d4f">例如指令中内嵌的常数</span>。 虽然名字也叫 "Code"，但它==<span style="background:#ff4d4f">主要服务于指令执行过程中的数据需求</span>==。
- **System 总线 (System Bus 或 Data Bus):** ==**主要的数据总线**==，也常被称为 **D-Bus (Data Bus)**。用于 **数据访问 (Data Access)**，==例如 **加载数据 (Load) 和存储数据 (Store)** 操作，以及访问外设寄存器。这是 CPU 进行数据读写操作的主要通道==。
对比[数据总线 系统总线](../已归类卡/数据总线%20系统总线.md)的数据指令总线

[[../book/cm3cm4书]]

# 架构
**包括编程模型、异常（如中断）如何处理、存储器映射**、如何使用外设
## 编程模型
### 操作模式和状态
#### 操作状态
![](../fujian/Pasted%20image%2020250717152320.png)
==**由于Cortex-M处理器不支持ARM指令集. 因此, ARM状态并不存在。**==
#### 操作模式
处理模式
线程模式
### 寄存器
==**对于ARM架构, 若处理的是存储器中的数据, 就需要将其从存储器加载到寄存器组中的寄存器里。在处理器内处理完后, 若有必要, 还要写回存储器, 这种方式一般被称作加载一存储架构**==
#### 特殊寄存器
定义了操作状态和中断/异常屏蔽
![](../fujian/Pasted%20image%2020250717151919.png)
==**特殊寄存器未经过存储器映射，可以使用MSR和MRS等特殊寄存器访问指令来进行访问**==


![](../fujian/Pasted%20image%2020250305200133.png)

CONTROL寄存器 (见图4.9) 定义了
	•**栈指针的选择** (主栈指针/进程栈指针)。
	**线程模式的访问等级** (特权/非特权)。






## 中断

![](../fujian/Pasted%20image%2020250305212126.png)


![](../fujian/Pasted%20image%2020250314141120.png)
NVIC为Cortex-M处理器的一部分, 它是可编程的,==**且寄存器位于存储器映射的系统控制空间 (SCS)**==


![](../fujian/Pasted%20image%2020250314142554.png)
## 复位
==在**复位后以及处理器开始执行程序前, Cortex-M处理器会从存储器中读出头两个字,** 如图4. 30所示。**向量表位于存储器的开头部分, 它的头两个字为主栈指针 (MSP) 的初始值, 以及代表复位处理起始地址的复位向量** (参考本书图4. 26和4. 5. 3节)。**处理器读出这两个字后, 就会将这些数值赋给MSP和程序计数器 (PC)。**==
![](../fujian/Pasted%20image%2020250305213929.png)

![](../fujian/Pasted%20image%2020250314142854.png)


# 存储器系统


![](../fujian/Pasted%20image%2020250305194357.png)
![](../fujian/Pasted%20image%2020250314143459.png)