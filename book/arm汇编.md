
# arm 汇编的特点
## **LDR/STR 架构**
==<span style="background:#ff4d4f">**ARM 采用 RISC 架构，CPU 本身不能直接读取内存，而需要先将内存中内容加载入 CPU 中通用寄存器中才能被 CPU 处理**</span>==
2). ldr（**load register**）指令将内存内容加载入通用寄存器。
3). str（**store register**）指令将寄存器内容存入内存空间中。
## **至此8种寻址方式**


1). 寄存器寻址 mov r1, r2。@**放在 r1**
2).立即 (立即数)寻址 mov r0, \#0xFF00 。
3). 寄存器移位寻址 mov r0, r1, lsl #3 。         **LSL r0, r1, #3  将寄存器 `r1` 的值左移 3 位，并将结果存储在寄存器 `r0` 中**
	- **LSL**（logic shift left）
	- **ASL**（arithmatic shift left） 
	- **ROL**（rotate shift left）
4). 寄存器间接寻址 ldr r1,\[r2]    **从寄存器 `R2` 指向的内存地址中加载数据，并将加载的数据存储到寄存器 `R1` 中**
5). 基址变址寻址 ldr r1,\[r2, #4 ]内存地址在 r2+4里面。
6). **多寄存器寻址** **一次访问多个寄存器**。
	==`LDM(load much)：` 多数据加载==,将地址上的**值**加载到[寄存器](https://so.csdn.net/so/search?q=%E5%AF%84%E5%AD%98%E5%99%A8&spm=1001.2101.3001.7020)上  
	`STM(store much)：` 多数据存储,将寄存器的值存到地址上  
	主要用途：现场保护、数据复制、参数传送等，共有8种模式（前面4种用于数据块的传输，后面4种是[堆栈](https://so.csdn.net/so/search?q=%E5%A0%86%E6%A0%88&spm=1001.2101.3001.7020)操作）如下：\
- 1、`IA:（Increase After）` 每次传送后**地址加4，其中的寄存器从左到右执行**，例如：`STMIA R0,{R1,LR}` ，先存R1、再存LR
- 2、`IB:（Increase Before）`每次传送前地址加4，同上
- 3、`DA:（Decrease After）`每次传送后**地址减4，其中的寄存器从右到左执行**，例如：`STMDA R0,{R1,LR}` ，先存LR，再存R1
- 4、`DB：（Decrease Before）`每次传送前地址减4，同上
- 5、`FD：`满递减堆栈 (每次传送前地址减4)
- 6、`FA：`满递增堆栈 (每次传送后地址减4)
- 7、`ED：`空递减堆栈 (每次传送前地址加4)
- 8、`EA：` 空递增堆栈 (每次传送后地址加4\
注意：其中在数据块的传输中是 `STMMDB` 和 `LDMIA` 对应，`STMMIA` 和 `LDMDB` 对应，而在堆栈操作是 `STMFD` 和 `LDMFD` 对应，`STMFA` 和 `LDMFA` 对应，格式如下：
```c
LDM{cond} mode Rn{!}, reglist{^}
STM{cond} mode Rn{!}, reglist{^}
```
其中
```c
Rn：基址寄存器，装有传送数据的起始地址，Rn不允许为R15；
！：表示最后的地址写回到Rn中；
reglist：可包含多于一个寄存器范围，用“，”隔开，如{R1，R2，R6-R9}，寄存器由小到大顺序排列；
^：不允许在用户模式和系统模式下运行
```
数据块的传输实例：
```c
Ldr R1,=0x10000000          //传送数据的起始地址0x10000000     

LDMIB R1!,{R0,R4-R6}      //从左到右加载,相当于 LDR R0,10000004  LDR R4,10000008... ...

/*传送前地址加+4,

所以地址加4,R0=0X1000004地址里的内容，

地址加4,R4=0X10000008地址里的内容，

地址加4,R5=0X1000000C地址里的内容，

地址加4,R6=0X10000010 地址里的内容，

由于!, 最后的地址写回到R1中,R1=0X10000010   */
```

```c
Ldr R1,=0x10000000          //传送数据的起始地址0x10000000        

LDMIA R1!,{R0,R4-R6}         //从左到右加载,相当于 LDR R0,10000000  LDR R4,10000004... ...

/*传送后地址加+4,

所以R0=0X10000000地址里的内容，地址加4,

R4=0X10000004地址里的内容，地址加4,

R5=0X10000008地址里的内容，地址加4,

R6=0X1000000C 地址里的内容，地址加4,

由于!,最后的地址写回到R1中,所以R1=0X10000010   */
```

```c
LDR R1,=0x10000000          //传送数据的起始地址0x10000000        

LDR R4,=0X10

LDR R5,=0X20

LDR R6,=0X30

STMIB R1,{R4-R6}          //从左到右加载,相当于STR [R4],0X10000004    STR [R5],0X10000008 .....

/*传送前地址加+4,所以0X10000004地址=0X10，0X10000008地址=0X20，0X1000000C地址=0X30 */
```

```c
Ldr R1,=0x10000000        //传送数据的起始地址0x10000000  

LDR R4,=0X10

LDR R5,=0X20

LDR R6,=0X30           

STMIA R1!,{R4-R6 }     

/*传送后地址加+4,所以0X10000000地址=0X10，0X10000004地址=0X20，0X10000008地址=0X30，由于!,最后的地址写回到R1中,所以R1=0X1000000C  */
```
中断实例（利用 `STMDB` 和 `LDMIA` 保护现场，然后通过 LR 寄存器返回）
- 先设置栈 `sp`，用于后面使用 `stmdb` 存储寄存器数据
- 当产生异常时，便进入中断
```c
sub lr, lr, #4                  

 //首先将lr-4,因为arm流水线,lr=当前pc+8,由于pc+4段没有执行，所以lr=(当前pc+8)-4;
stmdb sp!, { r0-r12,lr }  

//每次传送前-4,由于递减,所以从右往左存储寄存器

//所以sp-4=lr,sp-8=r12,... sp-56=r0; 由于!，所以最后的地址写回到sp中,sp=sp-56;
 

ldr lr, =int_return  //设置返回地址

ldr pc, =EINT_Handle //进入中断服务函数,如果中途返回就会调用pc=lr,即可执行int_return;

int_return:
ldmia sp!, { r0-r12,pc }^  

//每次传送后+4,所以从左往右加载数据到寄存器

//所以r0=sp, r1=sp+4,...pc=sp+52;由于!，所以最后地址写回到sp中,sp=sp+56;

//此时,sp=sp+56就等于最初栈顶值,pc=lr,然后返回到异常发生前的相应位置继续执行。

//^  ^表示将spsr的值复制到cpsr,因为异常返回后需要恢复异常发生前的工作状态
```
7). **堆栈寻址** stmfd sp!,{r2-r7, lr}。
8). **相对寻址** beq flag。
## 指令后缀
经常使用的后缀有：
B（byte）功能不变，操作长度变为 8 位, 默认的32位
	LDR、STR（加载/存储半字）等。
H（halfword）功能不变，长度变为 16 位
S（signed）功能不变，**操作数变为有符号**
	如 ldr ldrb ldrh ldrsb ldrsh
S（S 标志）功能不变，**影响 CPSR 标志位**（N, Z, C, V）
	几乎所有算术/逻辑指令（如 ADDS、SUBS、ANDS）。
	如 mov 和 movs movs r0, #0


N（Negative）：结果为负时置 1。
Z（Zero）：结果为零时置 1。
C（Carry）：发生进位/借位时置 1。
V（Overflow）：有符号溢出时置 1。

**cpsr程序状态寄存器**
	条件标志位（N, Z, C, V）
	中断控制位（I, F 用于屏蔽 IRQ/FIQ 中断）
	处理器模式位（如 User、IRQ、FIQ、SVC 等）
	执行状态位（T 位，指示 Thumb/ARM 指令集）
## 条件执行后缀
**{cond}**

**常见条件码**：

| 条件码     | 英文全称                   | 中文解释    | 标志位条件（CPSR） |     |
| ------- | ---------------------- | ------- | ----------- | --- |
| `EQ`    | Equal                  | 相等      | Z=1         |     |
| `NE`    | Not Equal              | 不相等     | Z=0         |     |
| `GT`    | Greater Than           | 有符号大于   | Z=0 且 N=V   |     |
| `LT`    | Less Than              | 有符号小于   | N≠V         |     |
| `CS/HS` | Carry Set/High or Same | 无符号大于等于 | C=1         |     |
| `CC/LO` | Carry Clear/Lower      | 无符号小于   | C=0         |     |
## 多级指令流水线
# 数据传输
数据传输指令 mov mvn (Move Not)
	MVN  r1 ,  # 0xFF  ；r1 ← 0x FFFF FF00,将被传送的对象先**按位取反**，再传送到目的寄存器。
算术指令 add sub rsb (Reverse Subtract) adc (Add with Carry) sbc (Subtract with Carry) rsc ( Reverse Subtract with Carry)

逻辑指令 
	and (Bitwise AND) 
		AND Rd, Rn, Rm
		`AND Rd, Rn, #<immediate>`
	orr （Bitwise OR）
		对两个操作数执行按位或操作，并将结果存储到目标寄存器中。
	eor (Bitwise Exclusive OR)异或
		对两个操作数执行按位异或操作，并将结果存储到目标寄存器中。
	bic{条件}{S} Rd,Rn,operand    (Bitwise AND with Inverted second operand)
		对两个操作数执行按位与操作，但第二个操作数先进行按位取反，然后将结果存储到目标寄存器中。这相当于 Rd = Rn & ~Rm
	 	bic  根据 operand 哪个位为1，清除 Rn 对应的位
比较指令 
	cmp (Compare) 对两个操作数执行减法操作，并根据结果设置状态标志，但不将结果写回到任何寄存器
		CMP Rn, Rm
		`CMP Rn, #<immediate>`
	cmn (Compare Negative) 对两个操作数执行加法操作，并根据结果设置状态标志，但不将结果写回到任何寄存器。这通常用于检查负数。
	tst (Test)对两个操作数执行按位与操作，并根据结果设置状态标志，但不将结果写回到任何寄存器。这通常用于检查特定的位是否被设置。
	teq (Test Equivalence) 对两个操作数执行按位异或操作，并根据结果设置状态标志，但不将结果写回到任何寄存器。这通常用于检查两个操作数是否相等。
乘法指令 
	mul(Multiply)
		将 Rn 和 Rm 的值相乘，结果存储在 Rd 中。
		MUL Rd, Rn, Rm
	mla(Multiply and Accumulate)
		执行两个寄存器的乘法操作，并将结果累加到另一个寄存器中
		MLA Rd, Rn, Rm, Ra
		将 Rn 和 Rm 的值相乘，然后将结果与 Ra 的值相加，最终结果存储在 Rd 中。
	umull（Unsigned Multiply Long）
		执行两个寄存器的无符号乘法操作，结果为64位，存储在两个寄存器中
		UMULL RdLo, RdHi, Rn, Rm
		将 Rn 和 Rm 的值相乘，结果的低32位存储在 RdLo 中，高32位存储在 RdHi 中。
	umlal(Unsigned Multiply Long and Accumulate)
		执行两个寄存器的无符号乘法操作，并将结果累加到两个寄存器中。
		UMLAL RdLo, RdHi, Rn, Rm
		将 Rn 和 Rm 的值相乘，然后将结果与 RdLo 和 RdHi 的值相加，最终结果的低32位存储在 RdLo 中，高32位存储在 RdHi 中。
	smull
	smlal
前导零计数 clz（Count Leading Zeros）
	CLZ Rd, Rm
	计算 Rm 中的值的前导零的数量，并将结果存储到 Rd 中。
		前导零：从最高位（MSB）开始，连续的零的数量。

# cpsr 访问指令 程序状态寄存器传输指令
**ARM 中有两条指令用于在状态寄存器和通用寄存器之间传送数据。程序不能通过直接修改 CPSR 中的 T 控制位直接将程序状态切换到 thumb 状态，必须通过 BX 等指令完成程序状态的切换。通常程序状态寄存器修改是通过读->改->写的方式来实现的。**
mrs（Move to Register from System register）&msr（**Move to System register from Register**）

CPSR 寄存器比较特殊，需要专门的指令访问，这就是 mrs 和 msr。

cps ( Change Processor State)
	CPS 指令可以在特权模式下直接修改 CPSR（Current Program Status Register）寄存器的某些位，从而改变处理器的模式或使能/禁用中断
	`CPS #mode`
	`CPSIE iflags{, #mode}`
	`CPSID iflags{, #mode}`
	更改处理器模式：通过设置 \#mode ，可以切换处理器到不同的模式。
	使能或禁用中断：通过 CPSIE 和 CPSID 指令，可以分别使能或禁用中断。
	CPS \#0x12   进入irq模式
	CPSIE I  使能IRQ
	CPSID I  禁用IRQ
	CPSIE F  使能FIQ
	CPSID F
# **跳转(分支)指令**
b & bl & bx
	- b 直接跳转（就没打开算返回）
	- bl branch and link，**跳转前把返回地址放入 lr 中**，以便返回，以便用于函数调用
	- bx **跳转同时切换到 ARM 模式**，一般用于异常处理的跳转。
blx   `BLX` 会切换处理器的指令集，并将返回地址（即下一条指令的地址）保存到链接寄存器 `LR` 中
# **访存指令**
ldr/str&ldm/stm&swp
**单个字/半字/字节**访问ldr/str
**多字**批量访问 ldm/stm
**使用 SWP 可实现信号量操作**。
	swp r1,r2,[r0]
	swp r1,r1,[r0]

`swp{<cond>}<Rd>,<Rm>,[<Rn>]` 执行的结果是把 Rn 的内容读取到 Rd 中，同时将 Rm 寄存器的内容写入到 Rn 中。

stmiasp,{r 0-r 12}
将 r 0 存入 sp 指向的内存处（假设为 0 x 30001000）；然后地址+4（即指向 0 x 30001004），将 r 1 存入该地址；然后地址再+4（指向 0 x 30001008），将 r 2 存入该地址······直到 r 12 内容放入（0 x 3001030），指令完成。
## **后缀的种类：**  

ia（increase after）先传输，再地址+4  
ib（increase before）先地址+4，再传输  
da（decrease after）先传输，再地址-4  
db（decrease before）先地址-4，再传输 

fd（full decrease）满递减堆栈  
ed（empty decrease）空递减堆栈  
fa（·······） 满递增堆栈  
ea（·······）空递增堆栈




**!的作用:**
	ldmiar 0,{r 2-r 3}
	ldmiar 0！,{r 2-r 3}
	感叹号的作用就是 r 0 的值在 ldm 过程中发生的增加或者减少最后写回到 r 0 去，也就是说 **ldm 时会改变 r0的值**。
**^的作用:**
	ldmfdsp!,{r 0-r 6, pc}
	ldmfdsp!,{r 0-r 6, pc}^
	^的作用：在目标寄存器中有 pc 时，会同时将 spsr 写入到 cpsr，一般用于从异常模式返回。
	总结：批量读取或写入内存时要用 ldm/stm 指令。
	各种后缀以理解为主，不需记忆，最常见的是 stmia 和 stmfd。
	谨记：操作栈时使用相同的后缀就不会出错，不管是满栈还是空栈、增栈还是减栈。

# 软中断
** ARM 有 7 种模式，可以分为用户模式和特权模式。在特权模式中可以访问系统的所有资源以及任意切换到别的模式**
swi（softwareinterrupt）软中断指令用来实现 OS 中系统调用

# 协处理器 CP 15
ARM 设计上支持多达 16 个协处理器，**但是一般 SoC 只实现其中的 CP 15.**（cp：coprocessor）
协处理器和 MMU、cache、TLB 等处理有关，功能上和操作系统的虚拟地址映射、cache 管理等有关。


ARM 协处理器指令包括以下 3 类：
	用于 ARM 处理器初始化 ARM 协处理器的数据处理操作。CDP
	用于 ARM 处理器的寄存器和 ARM 协处理器的寄存器间的数据传送操作。MCR、MRC
	用于在 ARM 协处理器的寄存器和内存单元之间传送数据。LDC、STC

**CDP 指令让 ARM 处理器能够通知 ARM 协处理器执行特定的操作，该操作由协处理器完成。**

# VFP（Vector Floating-Point）媒体寄存器
VFP（Vector Floating-Point）是 ARM 架构中的一种浮点运算扩展
VFP 提供了一组专门的浮点寄存器和指令集

VMRS (VFP Media Register to System Register)
	用于将数据从系统寄存器移动到普通寄存器
	VMRS Rn, <system_register>
VSTM (VFP Store Multiple)
	将一组 VFP（Vector Floating-Point）寄存器的值存储到内存中
	VSTM Rn!, {D0-D15}
		存储多个 VFP 寄存器：将指定的 VFP 寄存器的值存储到内存中。
		更新基址寄存器：根据存储操作的结果更新基址寄存器的值。


#  ARM 中的指令执行条件码
![[Pasted image 20240525095139.png]]
立即数是 32 bit，但是**并不是所有的操作数都是立即数**。立即数=8 位数据>>偶数陪（最多是移位 30 位，有些地方说是 32 位，右移 32 位其实就是没有移位），立即数的构成是使用移位最少的那个方式，所以数据宽度超多了 8 bit 肯定就不是立即数了。在 ARM 指令集中立即数使用#标记。
**算术右移是带有符号位**，即最高位的值保留；逻辑右移是用 0 填充左边被移走的位；循环右移是用右边移出的位填充左边的位；带拓展的循环右移是使用 CPSR 中的 C 位填充最高位。
F (full)、E (empty)：栈指针指向栈顶元素（最后一个入栈的数据）时称为 full 栈，栈指针指向与栈顶元素相邻的一个可用数据单元时称为 empty 栈。D（descending）：数据栈向内存地址减少的方向增长，A (ascending)数据栈向内存地址增加的方向增长。

# **ARM 汇编器支持的[[../已归类卡/伪操作]]**
伪指令是一种在汇编语言中使用的特殊指令，它们不会被处理器执行，而是由汇编器处理。**伪操作是一种在汇编语言中用来定义数据、符号或控制汇编过程的指令****
**

**告诉编译器怎么去编译指令，而==它本身不生成机器码（类似于 C 中的宏==）**

特殊指令助记符，这些助记符与指令系统的助记符不同，没有相对应的操作码，通常称这些特殊指令助记符为伪操作标识符，**它们所完成的操作称为伪操作**。
## 符号定义的伪操作
符号定义伪操作用于定义 ARM 汇编程序中的变量、对变量赋值及定义寄存器的别名等操作。
（1）用于定义全局变量的 GBLA、GBLL 和 GBLS。
（2）用于定义局部变量的 LCLA、LCLL 和 LCLS。
（3）用于对变量赋值的 SETA、SETL 和 SETS。
（4）为通用寄存器列表定义名称的 RLIST。

## 数据定义的伪操作
数据定义伪操作一般用于为特定的数据分配存储单元，同时可完成已分配存储单元的初始化。常见的数据定义伪操作有如下几种：
（1）DCB 用于分配一片连续的字节存储单元并用指定的数据初始化
（2）DCW（DCWU）用于分配一片连续的半字存储单元并用指定的数据初始化
（3）DCD（DCDU）用于分配一片连续的字存储单元并用指定的数据初始化
（4）DCFD（DCFDU）用于为双精度的浮点数分配一片连续的字存储单元并用指定的数据初始化
（5）DCFS（DCFSU）用于为单精度的浮点数分配一片连续的字存储单元并用指定的数据初始化
（6）DCQ（DCQU）用于分配一片以 8 字节为单位的连续的存储单元并用指定的数据初始化
（7）SPACE 用于分配一片连续的存储单元
（8）MAP 用于定义一个结构化的内存表首地址
（9）FIELD 用于定义一个结构化的内存表的数据域

## 汇编控制伪操作
（1）IF、ELSE、ENDIF  
 （2）WHILE、WEND  
 （3）MACRO、MEND
 （4）MEXIT
## 杂项伪操作
（1）AREA 用于定义一个代码段或数据段
（2）ALIGN 用于使程序当前位置满足一定的对齐方式
（3）ENTRY 用于指定程序入口点
（4）END 用于指示源程序结束
（5）EQU 用于定义字符名称
（6）EXPORT（或 GLOBAL）用于声明符号可以被其他文件引用
（7）EXPORTAS 用于向目标文件引入符号
（8）IMPORT 用于通知编译器当前符号不在本文件中
（9）EXTERN 用于通知编译器要使用的标号在其他的源文件中定义，但要在当前源文件中引用
（10）GET（或 INCLUDE）用于将一个文件包含到当前源文件
（11）INCBIN 用于将一个文件包含到当前源文件




# **[[../已归类卡/伪指令]]**  
**而伪指令可以有很多一条机器码，也可以理解为==伪指令是有很多一条汇编指令组合而成==。**


**伪指令的意义在于指导汇编过程**。
**伪指令是和具体的汇编器有关的，我们使用 gnu 工具链，因此学习 gnu 下的汇编伪指令**







## **伪指令 vs 伪操作**

|特性|伪指令（Pseudo-instructions）|伪操作（Pseudo-ops/Directives）|
|---|---|---|
|**是否生成机器码**|是（转换为真实指令）|否（仅指导汇编器）|
|**用途**|简化编程（如 `LDR =value`）|控制汇编过程（如 `.data`）|
|**示例**|`PUSH {R0-R3}`, `NOP`|`.word`, `.global`, `.if`|