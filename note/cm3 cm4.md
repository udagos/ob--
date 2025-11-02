![](../fujian/Pasted%20image%2020250717150804.png)



![](../../fujian/Pasted%20image%2020250302111852.png)

基于Cortex-M3或Cortex-M4的简单系统 ([pdf](zotero://open-pdf/library/items/UID4KR72?page=166&annotation=KHEMSDN3))

![](../../fujian/Pasted%20image%2020250302112642.png)
Cortex-M3总线连接样板范例 ([pdf](zotero://open-pdf/library/items/HCL636HZ?page=105&annotation=GCC837XY))


![](../fujian/Pasted%20image%2020250302111933.png)
总线矩阵


![](../../fujian/Pasted%20image%2020250717150756.png)
**Cortex-M3 内核的总线接口:** Cortex-M3 内核本身提供了多个总线接口，用于连接到系统总线：

- **I-Code 总线 (Instruction Code Bus):** **指令总线**，用于 **取指令 (Instruction Fetch)**。<span style="background:#ff4d4f"> CPU 通过 I-Code 总线从指令存储器 (通常是 Flash 或 指令 Cache) 读取指令。</span>
- **D-Code 总线 (Data Code Bus):** **数据总线**，主要用于 **<span style="background:#ff4d4f">获取字面量数据</span> (literal data)**，<span style="background:#ff4d4f">例如指令中内嵌的常数</span>。 虽然名字也叫 "Code"，但它==<span style="background:#ff4d4f">主要服务于指令执行过程中的数据需求</span>==。
- **System 总线 (System Bus 或 Data Bus):** **主要的数据总线**，也常被称为 **D-Bus (Data Bus)**。用于 **数据访问 (Data Access)**，==例如 **加载数据 (Load) 和存储数据 (Store)** 操作，以及访问外设寄存器。这是 CPU 进行数据读写操作的主要通道==。
对比[数据总线 系统总线](../已归类卡/数据总线%20系统总线.md)的数据指令总线

[[../book/cm3cm4书]]

# 架构
**包括编程模型、异常（如中断）如何处理、存储器映射**、如何使用外设
## 编程模型
### 操作模式和状态
#### 操作状态
![](../fujian/Pasted%20image%2020250717152320.png)
#### 操作模式
处理模式
线程模式
### 寄存器
==**对于ARM架构, 若处理的是存储器中的数据, 就需要将其从存储器加载到寄存器组中的寄存器里。在处理器内处理完后, 若有必要, 还要写回存储器, 这种方式一般被称作加载一存储架构**==
#### 特殊寄存器
定义了操作状态和中断/异常屏蔽
![](../fujian/Pasted%20image%2020250717151919.png)==**特殊寄存器未经过存储器映射，可以使用MSR和MRS等特殊寄存器访问指令来进行访问**==