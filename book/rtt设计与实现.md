RT-Thread 可通过方便易用的工具，裁剪出仅需要 3 KBFlash、1.2 KBRAM 内存资源的 NANO 版本

RT-Thread 与其他很多 RTOS（如 FreeRTOS、uC/OS）的主要区别之一是，它不仅仅是一个实时内核，还具备丰富的中间层组件
“它具体包括以下部分。”
![[Pasted image 20240424155744.png]]


3.1.0 版的基础上进行了裁剪
源码的目录结构。“各个目录所包含的文件类型的描述如表2-1所示。”
![[Pasted image 20240424155933.png]]
在工程主窗口左侧的 Project 栏里可以看到该工程的文件列表，这些文件被分别存放到如表 2-2 中所示的几个组内。

仿真运行
“View — Serial Windows  -> UART #1 "命令, 打开串口 1窗口, 可以看到串口输出了 RT-Thread的Log
RT-Thread提供==FinSH==功能, 用于调试或查看系统信息
# 0 内核
# 内核基础
“内核的组成 部分、系统如何启动、内存分布情况以及内核配置方法。”
## 内核介绍
内核架构图，内核处于硬件层之上，内核部分包括内核库、实时内核实现。!![[Pasted image 20240424160444.png]]
内核库是为了保证内核能够独立运行的一套小型的类似 C 库©的函数实现子集

定时器
	“**通常使用定时器定时回调函数**（即超时函数），完成定时服务”

线程同步
	“线程同步机制支持线程按优先级等待或按先进先出方式获取信号量或互斥量”
	线程通过对信号量、互斥量的获取与释放进行同步。线程通过对事件的发送与接收进行同步
	互斥量采用优先级继承的方式解决了实时系统常见的优先级翻转问题

线程通信
	通信机制支持线程按优先级等待或按先进先出方式获取。

设备管理
	**RT-Thread 将 PIN、iic、SPI、USB、UART 等作为外设设备，统一通过设备注册完成。**
	实现了按名称访问的设备管理子系统，可按照统一的 API 界面访问硬件设备
	**对不同的设备可以挂接相应的事件。当设备事件触发时，由驱动程序通知给上层的应用程序。**
## 启动流程 
我们使用了 MDK 的扩展功能 `$Sub$$和$Super$$`   
![[Pasted image 20240424162604.png]]
![[Pasted image 20240424162609.png]]

![[Pasted image 20240424162835.png]] 中 rtthread_startup ()

> 在某些情况下，编译器可能会生成多个版本的函数，以支持不同的硬件特性或优化目标。`$Sub$$` 标记的函数是这些版本中的一个。

==其中 rtthread_startup ()函数==的代码：
![[Pasted image 20240424163104.png]]
部分启动代码大致可以分为 4 个部分：
(1)初始化与系统相关的硬件；(2)初始化系统内核对象，例如定时器、调度器、信号；(3)创建 main 线程，在 main 线程中对各类模块依次进行初始化；(4)初始化定时器线程、空闲线程，并启动调度器。
	在 rt_hw_board_init ()中完成系统时钟设置，为系统提供心跳、串口初始化，将系统输人输出终端绑定到这个串口，后续系统运行信息就会从串口打印出来。
## 内存分布
上面提到的 ProgramSize 包含以下几个部分。
(1) Code：代码段，存放程序的代码部分。
(2) RO-data：只读数据段，存放程序中定义的常量。
(3) RW-data：读写数据段，存放初始化为非 0 值的全局变量。
(4) ZI-data：0 数据段，存放未初始化的全局变量及初始化为 0 的变量。

**编译完工程后会生成一个. map 文件**，该文件说明了各个函数占用的尺寸和地址
![[Pasted image 20240424163717.png]]
**程序运行之前，需要有文件实体被烧录到 STM 32 的 Flash 中，一般是 bin 或者 hex 文件，该被烧录文件称为可执行映像文件**

图 3-3 中**左图是可执行映像文件烧录到 STM 32 后的内存分布，它包含 RO 段和 RW 段两个部分**：其中 RO 段中保存了 Code、RO-data 的数据, RW 段中保存了 RW-data 的数据，由于 **ZI-data 都是0,所以未包含在映像文件中**。
![[Pasted image 20240424164744.png]]
STM 32 在上电启动之后默认从 Flash 启动，**启动之后会将 RW 段中的 RW-data (初始化的全局变量)搬运到 RAM 中，但不会搬运 RO 段，即 CPU 的执行代码从 Flash 中读取，另外根据编译器给出的 ZI 地址和大小分配出 ZI 段，并将这块 RAM 区域清零。**

**其中动态内存堆为未使用的 RAM 空间，应用程序申请和释放的内存块都来自该空间。**
而一些全局变量则存放于 RW 段和 ZI 段中，RW 段存放的是具有初始值的全局变量 (而**常量形式的全局变量**则放置在 RO段中，是只读属性的)，ZI 段存放的系统未初始化的全局变量
## 自动初始化机制
**自动初始化机制是指初始化函数不需要被显式调用，只要在函数定义处通过宏定义的方式进行声明，就会在系统启动过程中被执行。**
## 内核对象模型
### 静态动态对象
内核对象分为两类，即静态内核对象和动态内核对象，静态内核对象通常放在 RW 段和 ZI 段中，系统启动后在程序中初始化；动态内核对象则是从内存堆中创建的，而后进行手工初始化。

thread 1对象的内存空间，包括线程控制块 thread 1 与栈空间 thread 1_stack, 都是编译时决定的，因为代码中都不存在初始值，统一放在未初始化数据段中。

静态对象会占用 RAM 空间，不依赖于内存堆管理器，内存分配时间确定。动态对象则依赖于内存堆管理器，运行时申请 RAM 空间，当对象被删除后，占用的 RAM 空间被释放。
### 内核对象管理系统
**对象容器**给每类**内核对象分配了一个链表**
![[Pasted image 20240424165840.png]]
![[Pasted image 20240424165916.png]]
### 对象控制块
**内核对象控制块数据结构**
![[Pasted image 20240428105930.png]]
### 内核对象管理方式
内核**对象容器**数据结构
![[Pasted image 20240428110029.png]]
一类对象由一个 rt_object_information 结构体来管理，==这类对象的每个具体实例都通过链表的形式挂接在 object_list 上==

#### 初始化 
![[Pasted image 20240428111030.png]]
**当调用该函数进行==对象初始化时，系统会把这个对象放置到对象容器中进行管理==**
#### 脱离
![[Pasted image 20240428111232.png]]
可使得一个**静态内核对象从内核对象容器中脱离出来，即从内核对象容器链表上删除相应的对象节点**
“对象脱离后，对象**占用的内存并不会被释放**。”
#### 分配
上述描述的都是对象初始化、脱离的接口，**都是在面向对象内存块已经有的情况下，而动态对象则可以在需要时申请**
![[Pasted image 20240428111338.png]]
#### 删除
当不再使用一个**动态对象**时，可以调用如下接口删除该对象，并释放相应的系统资源:
![[Pasted image 20240428111433.png]]
首先从对象容器**链表中脱离对象，然后释放对象所占用的内存**。
#### 辨别、
判断指定对象是否是系统对象 (**静态内核对象**)
![[Pasted image 20240428111555.png]]
调用 rt_object_is_systemobject 接口可判断一个对象是否是系统对象，在 RT-Thread 操作系统中，一个系统对象就是一个静态对象，对象类型标识上 RT_Object_Class_Static 位置位。通常，使用 rt_object_init ()方式初始化的对象都是系统对象
## 内核配置示例
可裁剪性，支持对内核进行精细调整, 其配置主要通过修改工程目录下的 rtconfig. h 文件来进行
用户可以通过打开/关闭该文件中的宏定义来对代码进行条件编译，最终达到系统配置和裁剪的目的
( 1 ) RT-Thread 内核部分。
![[Pasted image 20240428100428.png]]
(2)线程间同步与通信部分，该部分会用到的对象有信号量、互斥量、事件、邮箱、消息队列、信号等。
![[Pasted image 20240428100527.png]]
![[Pasted image 20240428100536.png]]
(3 )内存管理部分。
![[Pasted image 20240428100839.png]]
(4)内核设备对象。
![[Pasted image 20240428101047.png]]
(5)自动初始化方式。
(6 ) FinSH
![[Pasted image 20240428101436.png]]
(7)关于 MCU

系统配置文件 rtconfig. h 是由配置工具自动生成的，无须手动更改。
## 常见宏
“Keil 编译环境下一些常见的宏定义”
(1 ) rt_inline, 定义如下，static 关键字的作用是令函数只能在当前的文件中使用; inline 表示内联，用 static 修饰后，在调用函数时会建议编译器进行内联展开。
> [[内联函数]]

(2)RT_USED, 定义如下，该宏的作用是向编译器说明这段代码有用，即使函数中没有调用也要保留编译。
(3 ) RT_UNUSED, 定义如下，表示函数或变量可能不使用，这个属性可以避免编译器产生警告信息。
(4) RT_WEAK, 定义如下，常用于定义函数，编译器在链接函数时会优先链接没有该关键字前缀的函数
(5） ALIGN (n), 定义如下，其作用是在给某对象分配地址空间时，将其存放的地址按照 n 字节对齐
RT_ALIGN (size, align), 定义如下，其作用是将 size 提升为 align 定义的整数的倍数，例如，RT_ALIGN (13,4)将返回 16。
# 线程管理
“RT-Thread 线程管理的主要功能是对线程进行管理和调度”
系统线程和用户线程，系统线程是由 RT-Thread 内核创建的线程，用户线程是由应用程序创建的线程。这两类线程都会从内核对象容器中分配线程对象
**每个线程都有重要的属性**，如线程控制块、线程栈、入口函数等。
![[Pasted image 20240428111907.png]]
## 线程工作机制
**线程控制块**由结构体 struct rt_thread 表示。线程控制块是操作系统用于管理线程的数据结构

![[Pasted image 20240428113037.png]]
![[Pasted image 20240428113109.png]]
...
cleanup 会在线程退出时被空闲线程回调一次，以执行用户设置的清理现场等工作。
最后一个成员 use_data 可由用户挂接一些数据信息到线程控制块中，以提供类似线程私有数据的实现。
### 重要属性
#### 线程栈
“第一次运行线程时，可以以手工的方式构造上下文来设置一些初始环境：”入口函数（PC 寄存器）、入口参数（R 0 寄存器）、返回位置（LR 寄存器）、当前机器运行状态（CPSR 寄存器）。

“线程栈的增长方向是与芯片构架密切相关的”
“对于 ARM Cortex M 架构，线程栈的构造如图4-3 所示。”
![[Pasted image 20240428112711.png]]

#### 线程状态
线程状态：在就绪状态下，线程按照优先级排队，等待被执行
#### 线程入口函数 
“线程控制块中的 entry 是线程的入口函数，它是线程实现预期功能的函数。线程的人口函数由用户设计实现，一般有以下两种代码模式。”
“无限循环模式：在实时系统中，线程通常是被动式的”
“顺序执行或有限次循环模式”
### 线程状态切换
![[Pasted image 20240428113403.png]]
> RT-Thread 中，实际上线程并不存在运行状态，就绪状态和运行状态是等同的。

### 系统线程 
**在 RT-Thread 内核中的系统线程有空闲线程和主线程。**
#### 空闲线程 
空闲线程是系统创建的最低优先级的线程，线程状态永远为就绪状态。
当系统中无其他就绪线程存在时，调度器将调度到空闲线程
它通常是一个死循环，且永远不能被挂起。

若某线程运行完毕，系统将自动删除线程：自动执行 rt_thread_exit ()函数，先将该线程从系统就绪队列中删除，再将该线程的状态更改为关闭状态，不再参与系统调度，然后挂入 rt_thread_defunct 僵尸队列 (资源未回收、处于关闭状态的线程队列)中，最后空闲线程会回收被删除线程的资源。

空闲线程也提供了接口来运行用户设置的钩子函数，在空闲线程运行时会调用该钩子函数，适合钩入功耗管理、看门狗、喂狗等工作。
#### 主线程
在系统启动时，系统会创建 main 线程，它的入口函数为 main_thread_entry (), 用户的应用入口函数 main。就是从这里真正开始的
![[Pasted image 20240428113753.png]]
## 线程的管理方式 
![[Pasted image 20240428113837.png]]
### 创建和删除线程
![[Pasted image 20240428150027.png]]
“调用这个函数时，系统会从动态堆内存中分配一个线程句柄并按照参数中指定的栈大小从动态堆内存中分配相应的空间。分配出来的栈空间按照 rtconfig.h 中配置的 RT_ ALIGN_SIZE 方式对齐。线程创建接口的参数和返回值如表4-2所示”
![[Pasted image 20240428150045.png]]
![[Pasted image 20240428150102.png]]

![[Pasted image 20240428150121.png]]
实际上，用 rt_thread_delete。函数删除线程接口，仅仅是把相应的线程状态更改为 RT_THREAD_CLOSE 状态，然后放入 rt_thread_defunct 队列中；而真正的删除动作 (释放线程控制块和释放线程栈)需要到下一次执行空闲线程时，由参数描述空闲线程完成最后的线程删除动作
这个函数仅在使能了系统动态堆时才有效 (即 RT_USNG_HEAP 宏定义已经完成)。
### 初始化和脱离线程
![[Pasted image 20240428150424.png]]
![[Pasted image 20240428150431.png]]
### 启动线程
![[Pasted image 20240428150442.png]]
进入就绪状态
### 获得当前线程
![[Pasted image 20240428150519.png]]

### 使线程让出处理器资源
rt_err_t rt_thread_yield (void);
调用该函数后，当前线程首先把自己从所在的就绪优先级线程队列中删除，然后把自己挂到该优先级队列链表的尾部，然后激活调度器进行线程上下文切换 (如果当前优先级只有这一个线程，则线程继续执行，不进行上下文切换动作)。

rt_thread_yield ()函数和 rt_schedule ()函数比较相像，但在有相同优先级的其他就绪状态线程存在时，系统的行为却完全不一样。执行 rt_thread_yield ()函数后，当前线程被换出，相同优先级的下一个就绪线程将被执行。而执行 reschedule。函数后，当前线程并不一定被换出，即使被换出，也不会被放到就绪线程链表的尾部，而是在系统中选取就绪的优先级最高的线程执行 (如果系统中没有比当前线程优先级更高的线程存在，那么执行完 reschedule。函数后，系统将继续执行当前线程)。
### 使线程睡眠
![[Pasted image 20240428150719.png]]
调用它们可以使当前线程挂起一段指定的时间，时间过后，线程会被唤醒并再次进入就绪状态
### 挂起和恢复线程
![[Pasted image 20240428150813.png]]
通常不应该使用这个函数来挂起线程本身，如果确实需要采用 rt_thread_suspend ()函数挂起当前任务，需要在调用 rt_thread_suspend ()函数后立刻调用 rt_schedule ()函数进行手动的线程上下文切换。用户只需要了解该接口的作用，不推荐使用该接口。
![[Pasted image 20240428150926.png]]
### 控制线程
当需要对线程进行一些其他控制时，例如动态更改线程的优先级
![[Pasted image 20240428181616.png]]
指示控制命令 cmd 当前支持的命令如下。
□ RT_THREAD_CTRL_CHANGE_ PRIORITY ：动态更改线程的优先级。 
□ RT_THREAD_CTRL_STARTUP ： 开始运行一个线程，等同于 rt_ thread_startup ()函数调用。
RT_THREAD_CTRL_CLOSE：关闭一个线程，等同于 rt_thread_delete ()函数调用。
### 设置和删除空闲钩子
空闲钩子函数是空闲线程的钩子函数，如果设置了空闲钩子函数，就可以在系统执行空闲线程时自动执行空闲钩子函数来做一些其他事情 
![[Pasted image 20240428181755.png]]
设置的钩子函数必须保证空闲线程在任何时刻都不会处于挂起状态，例如 rt_thread_delay () rt_sem_take ()等可能会导致线程挂起的函数都不能使用。
### 设置调度器钩子 
系统的上下文切换是系统中最普遍的事件。有时用户可能会想知道在某个时刻发生了什么样的线程切换，可以通过调用下面的函数接口设置一个相应的钩子函数。在系统线程切换时，这个钩子函数将被调用：
![[Pasted image 20240428182226.png]]
钩子函数声明如下
![[Pasted image 20240428182239.png]]
在这个钩子函数中，基木上不允许调用系统 API, 更不应该导致当前运行的上下文挂起
## 线程应用示例
### 创建线程示例
![[Pasted image 20240428183922.png]]
![[Pasted image 20240428183943.png]]

![[Pasted image 20240428184034.png]]
线程 2 计数到一定值时会执行完毕，并被系统自动删除，计数停止。线程 1 一直打印计数。

大多数线程都是循环执行的，无须删除；而对于能运行完毕的线程，RT-Thread 在线程运行完毕后自动删除线程，在 rt_thread_exit ()里完成删除动作。用户只需要了解删除线程接口的作用，不推荐使用该接口 (可以由其他线程调用此接口或在定时器超时函数中调用此接口删除一个线程，但是这种用法非常少)。
### 线程时间片轮转调度示例
![[Pasted image 20240428184335.png]]
![[Pasted image 20240428184348.png]]
![[Pasted image 20240428184357.png]]
“由运行的计数结果可以看出，线程2的运行时间是线程1的一半。”

### 线程调度器钩子示例
下面的例子是在调度器钩子函数中打印线程间的切换信息，如代码清单 4-3 所示。
![[Pasted image 20240428184957.png]]
![[Pasted image 20240428185007.png]]
“由仿真结果可以看出，对线程进行切换时，设置的调度器钩子函数是在正常工作的, 即一直在打印线程切换的信息，包括切换到空闲线程。”

为什么有空闲？

## 总结
由于能执行完毕的线程会被系统自动删除，所以不推荐用户使用删除/脱离线程接口。
线程调度基于优先级抢占的方式进行，优先级相同的线程通过时间片轮询执行。
# 时钟管理
## 时钟节拍
时钟节拍率越快，系统的额外开销就越大，
**从系统启动开始计数的时钟节拍数称为系统时间。**

RT-Thread 中，时钟节拍的长度可以根据 RT_TICK_PER_SECOND 的定义来调整
### 实现方式
**时钟节拍由配置为中断触发模式的硬件定时器产生**

**当中断到来时，将调用一次 void rt_tick_increase (void)**, 通知操作系统已经过去一个系统时钟
下面的中断函数以 STM 32 定时器作为示例。
![[Pasted image 20240428185635.png]]
“在中断函数中调用 rt_tick_increase()对全局变量 rt tick 进行自加”
![[Pasted image 20240428185703.png]]
此外，每经过一个时钟节拍时，都会检查当前线程的时间片是否用完，以及是否有定时器超时
> 中断中的 rt_timer_check ()用于检查系统硬件定时器链表，如果有定时器超时，将调用相应的超时函数。所有定时器在定时超时后都会从定时器链表中被移除，而周期性定时器会在它再次启动时被加入定时器链表。

### 获取时钟节拍
![[Pasted image 20240428185536.png]]

## 定时器管理
(1)硬件定时器是芯片本身提供的定时功能。一般是由外部晶振提供给芯片输入时钟
“中断触发方式。”
(2)软件定时器是由操作系统提供的一类系统接口，它构建在硬件定时器基础之上, 使系统能够提供不受数目限制的定时器服务。
### 介绍
根据超时函数执行时所处的上下文环境，RT-Thread 的定时器可以分为 HARD_TIMER 模式与 SOFT_TIMER 模式
![[Pasted image 20240428185940.png]]
### 工作机制
### 管理方式
## 示例

# 线程间同步 
**在多线程实时系统中, 一项工作往往可以通过多个线程协调的方式来共同完成,**

**同步是指按预定的先后次序运行**，线程同步是指多个线程通过特定的机制（如互斥量、事件对象、临界区）来控制线程之间的执行顺序，**也可以说是在线程之间通过同步建立起执行顺序的关系，如果没有同步，那么线程之间将是无序的**

线程的同步方式有很多种，其核心思想都是在访问临界区的时候只允许一个（或一类线程运行。
进入/退出临界区的方式如下。
(1 )调用 rt_hw_interrupt_disable ()进入临界区，调用 rt_hw_interrupt_enable ()退出临界区；详见 9.3 节的内容。 
(2 )调用 rt_enter_critical ()进入临界区，调用 rt_exit_critical ()退出临界区。
## 信号量
### 信号量的工作机制 
线程可以获取或释放它，从而达到同步或互斥的目的。

每个信号量对象都有一个信号量值和一个线程等待队列
信号量的值对应信号量对象的实例数目、资源数目，假如信号量值为 5, 则表示共有 5 个信号量实例 (资源)可以被使用
![[Pasted image 20240429182816.png]]

### 控制块
![[Pasted image 20240429182353.png]]
rt semaphore 对象从 rt ipc object 中派生，由 IPC 容器所管理
### 管理方式
![[Pasted image 20240429182305.png]]
初始化flag ![[Pasted image 20240429182607.png]]
### 实现
```
rt_err_t rt_sem_init(rt_sem_t    sem,
                     const char *name,
                     rt_uint32_t value,
                     rt_uint8_t  flag)
{
	rt_object_init(&(sem->parent.parent), RT_Object_Class_Semaphore, name);
		 rt_list_insert_after(&(information->object_list), &(object->list));
	rt_ipc_object_init(&(sem->parent));
	
	sem->value = value;
	sem->parent.parent.flag = flag;
}


rt_err_t rt_sem_take(rt_sem_t sem, rt_int32_t time)
	temp = rt_hw_interrupt_disable();	
	if (sem->value > 0)
		sem->value --;
		rt_hw_interrupt_enable(temp);	
	else
		if (time == 0)
			rt_hw_interrupt_enable(temp);
			return 
		else
			thread = rt_thread_self();
			/* suspend thread */
            rt_ipc_list_suspend(&(sem->parent.suspend_thread),
                                thread,
                                sem->parent.parent.flag);
                                
            /* has waiting time, start thread timer */
            if (time > 0)
            
            /* enable interrupt */
            rt_hw_interrupt_enable(temp);
            
            /* do schedule */
            rt_schedule();
```
### 实例
本例程将使用2个线程、3个信号量实现生产者与消费者的例子。  3个信号量分别为:1lock: 因为2个线程都会对同一个数组array进行操作, 所以该数组是一个共享资源, 信号量锁用来保护这个共享资源。2empty: 空位个数, 初始化为5  个空位。3fidl: 满位个数, 初始化为。个满位。  2个线程分别为:1生产者线程: 获取到空位后, 产生一个数字, 循环放入数组中,  然后释放一个满位。2消费者线程: 获取到满位后, 读取数组内容并相加, 然后释放一个空位。

```
#include <rtthread.h>
# define THREAD_PRIORITY 6 
# define THREAD_STACK_SIZE 512 

# define THREAD_TIMESLICE 5  

/ * 定义最大能够产生5个元素*/ 
#define MAXSEM 5 
 / * 用于放置生产的整数数组*/  
rt_uint32__t array [MAXSEM]; 
 
/ * 指向生产者、消费者在array数组中的读写位置*/ 
static rt_uint32_t set, get;  

/ * 指向线程控制块的指针*/  
static rt_thread__t producer_tid = RT_NULL; 
static rt_thread__t consumer_tid = RT_NULL;  

struct rt_semaphore sem_lock; 
struct rt_semaphore sem_empty, sem_full;  / * 生产者线程入口 */
  
void producer_thread_entry(void *parameter) 
{  
	int ent = 0;  
	
	/ * 运行10次*/  
	while (ent < 10) 
	{
		 / * 获取一个空位*/  
		rt_sem_take(&sem_empty, RT_WAITING__FOREVER); 
		
		 / * 修改array内容,上锁*/  
		rt_sem_take(&sem_lock, RT_WAITING__FOREVER); 
		array[set % MAXSEM] = ent + 1; 
		rt_kprintf("the producer generates a number: %d\nM, array [set % MAXSEM]); 
		set++; 
		rt_sem_release(&sem_lock);
		
		/ * 发布一个满位*/  
		rt_sem_release(&sem_full); 	
		cnt++; 
		
		 / * 暂停一段时间*/  
		rt thread mdelay(20);  
	} 
	rt_kprintf("the producer exit I\n"); 
}  

/ * 消费者线程入口 */ 
void consumer_thread_entry(void *parameter)  
{ 
	rt_uint32_t sum = 0;  
	while (1) 
	{  
		/ * 获取一个满位*/ 
		rt_sem_take(&sem_full, RT_WAITING_FOREVER); 
		
		/ * 临界区,上锁进行操作*/  
		rt__sem_take (&sem_lock, RT_WAITING_FOREVER); 
		sum += array [get % MAXSEM]; 
		rt_kprintf("the consumer[%d] get a number: %d\n", (get % MAXSEM), array [get % MAXSEM]);
	 	get++; 一 
		rt_sem_release(&sem_lock); 
		
		 / * 释放一个空位*/  
		rt_sem_release(&sem_empty); 
		 
		/ * 生产者生产到10个数目,停止,消费者线程相应停止*/ 
		if (get = = 10) break; 
		
		/ * 暂停一小会时间*/  
		rt_thread_mdelay(50); 
	} 
	rt_kprintf("the consumer sum is: %d\n", sum);
	rt_kprintf '(*the consumer exit! \nH); 
}

int producer_consumer(void) 
{ 
	set = 0; 
	get = 0;  
	/* 初始化3个信号量 */  
	rt__sem_init (&sem_ lock, "lock”, 1, RT_IPC_FLAG_FIFO); 
	rt__sem_init (&sem_ empty, "empty", MAXSEM, RT_IPC_FLAG_FIFO); 
	rt__sem_init (&sem "full", 0, RT_IPC_FLAG_FIFO);
	
	/ * 创建生产者线程*/  
	producer_tid = rt_thread_create("producer", producer_thread_entry, RT_NULL, THREAD_STACK_SIZE, THREAD_PRIORITY - 1, THREAD_TIMESLICE); 
	if (producer__tid != RT__NULL)  
	{  
		rt_thread_startup(producer_tid); 
	}  
	else 
	{  
		rt_kprintf("create thread producer failed"); 
		return -1; 
	}
	 
	/ * 创建消费者线程*/  
	consumer_tid = rt_thread_create("consumer", consumer_thread__entry, THREAD_STACK_SIZE/ THREAD_PRIORITY + 1, THREAD_TIMESLICE); 
	if (consumer_tid 1= RT_NULL) 
	{  
		rt_thread__startup (consumer_tid);  
	}  
	else 
	{  
		rt_kprintf("create thread consumer failed");
		return -1; 
	} 
	return 0; 
}
  
/ * 导出到msh命令列表中*/  
MSH CMD EXPORT(producer consumer, producer consumer sample);
```

本例程可以理解为生产者生产产品并将其放入仓库, 消费者从仓库中取走产品。
(1) 生产者线程:  
	1获取1个空位 (放产品number), 此时空位减1;  
	2上锁保护; 本次产生的number值为cnt+1, 把值循环存入数组array中; 开锁;  
	3释放1个满位 (给仓库中放置一个产品, 仓库就多一个满位), 满位加1; 

(2) 消费者线程:  
	1获取1个满位 (取产品number), 此时满位减1 ;  
	2上锁保护; 将本次生产者产生的number值从array中读出来, 并与上次number值相加; 开锁;  
	3释放1个空位 (从仓库上取走一个产品, 仓库就多一个空位), 空位加1。

生产者依次产生10个number ,消费者依次取走, 并将10个number的值求和。信号量锁lock保护array临界区资源: 保证了消费者每次取number值的排他性, 实现了线程间同步。
### 使用场合
可以运用在多种场合中，形成锁、同步、资源计数等关系，, 也能方便地用于线程与线程、中断与线程间的同步。
#### 线程同步 
当持有信号量的线程完成它处理的工作时，释放该信号量，可以把等待在该信号量上的线程唤醒，让它执行下一部分工作，此时可以把信号量看成工作完成标志：持有信号量的线程完成它自己的工作，然后通知等待该信号量的线程继续下一部分工作。


例如,使用信号量进行两个线程之间的同步,  **信号量的值初始化成0**,表示具备0个信号量资源实例;而尝试获得该信号量的线程,将直接在该信号量上进行等待。 ,  当持有信号量的线程完成它处理的工作时,释放该信号量
	此时可以**把信号量看成工作完成标志: 持有信号量的线程完成它自己的工作, 然后通知等待该信号量的线程继续下一部分工作。**
#### 锁 
单一的锁常应用于多个线程间对同一共享资源（即临界区）的访问。信号量在作为锁来使用时，**通常应将信号量资源实例初始化成 1**

这类锁也叫二值信号量

==它需要先获得这个资源锁。==
![[Pasted image 20240429184111.png]]
#### 中断与线程的同步 
![](../fujian/Pasted%20image%2020250623152116.png)

“信号量的值初始为0,当 FinSH线程试图取得信号量时， 因为信号量值是0,所以它会被 挂起。当console设备有数据输入时，产生中断，从而进入中断服务例程。在中断服务例程中，它会读取console设备的数据，并把读取的数据放入UART buffer中进行缓冲，而后释放信号量，释放信号量的操作将唤醒FinSH线程。在中断服务例程运行完毕后，如果系统中没有比FinSH线程优先级更高的就绪线程存在，FinSH线程将持有信号量并运行，从 UART buffer缓冲区中获取输入的数据。”

> “中断与线程间的互斥不能采用信号量（锁）的方式实现，而应采用开关中断的方式实现。”
#### 资源计数 
“也可以认为信号量是一个递增或递减的计数器”

“例如, 初始化一个信号量的值为5,则这个信号量可最大连续减少5次,直到计数器减为0”

“计数适合线程间**工作处理速度不匹配的场合,这个时候信号量可以作为前一线程工作完成个数的计数,而当调度到后一线程时,它也可以以一种连续的方式一次处理多个事件**。
	例如,生产者与消费者问题中,**生产者可以对信号量进行多次释放,而后消费者被调度时能够一次处理多个信号量资源**。”

## 互斥量
互斥量又叫相互排斥的信号量，是一种特殊的二值信号量

“互斥量和信号量的不同是：拥有互斥量的线程拥有互斥量的所有权，互斥量支持递归访问且能**防止线程优先级翻转**；互斥量只能由持有线程释放，而信号量则可以由任何线程释放。”

**避免死锁**
当有线程持有它时,互斥量处于闭锁状态,由该线程获得它的所有权。相反,当该线程释放它时,将对互斥量进行开锁,  失去它的所有权。
当一个线程持有互斥量时,其他线程将不能对它进行开锁或持有它,持有该互斥量的线程也能够再次获得这个锁而不被挂起,如图6-6所示。
这个特性与一般的二值信号量有很大的不同:  在信号量中,因为已经不存在实例,线程**递归持有**会发生主动挂起(最终形成死锁)。
![](../fujian/Pasted%20image%2020250623153109.png)
**避免优先级反转**
所谓优先级翻转, 是指当一个高优先级线程试图通过信号量机制访问共享资源时, 如果该信号量已被低优先级线程持有, 而这个低优先级线程在运行过程中可能又被其他一些中等优先级的线程抢占, 从而造成高优先级线程被许多具有较低优先级的线程阻塞, 实时性难以得到保证


![](../fujian/Pasted%20image%2020250623153619.png)
“线程C开始使用某一**共享资源M**。在使用过程中,线程A等待的事件到来,线程A转为就绪状态,因为它比线程C优先级高,所以立即执行。
但是**当线程A要使用共享资源M时**, 由于其正在被线程C使用,因此线程A被挂起切换到线程C运行。
如果此时线程B等待的事件到来,则线程B转为就绪状态。由于线程B的优先级比线程C高,因此线程B开始运行,直到其运行完毕,线程C才开始运行。只有当线程C释放共享资源M后,线程A才得以执行”

![](../fujian/Pasted%20image%2020250623153920.png)
**==互斥量可以解决优先级翻转问题==**
“**优先级继承**是通过**在线程A尝试获取共享资源而被挂起的期间内,将线程C的优先级提升到线程A的优先级别**,从而解决优先级翻转引起的问题。这样能够防止C (间接地防止A)被B抢占,如图6-8所示”
优先级继承是指, 提高某个占有某种资源的低优先级线程的优先级, 使之与所有等待该资源的线程中优先级最高的那个线程的优先级相等, 然后执行, 
而当这个低优先级线程释放该资源时, 优先级重新回到初始设定。
因此, 继承优先级的线程避免了系统资源被任何中间优先级的线程抢占。

### 实例
有两个线程, 线程1和线程2, 线程1对两个number分别进行加1操作; 线程2也对两个number分别进行加1操作, 使用互斥量保证线程改变两个number值的操作不被打断



创建3个动态线程以检查持有互斥量时, 持有的线程优先级是否被调整到等待线程优先级中的最高优先级。
```
#include <rtthread.h>
  / * 指向线程控制块的指针*/
static  rt thread t tid1		 = RT NULL; 
static  rt thread t tid2		 = RT NULL; 
static  rt thread t tid3		 = RT NULL; 
static rt_mutex_t mutex			 = RT NULL; 

# define THREAD_PRIORITY 10
# define THREAD_STACK_SIZE 512 
#define THREAD_TIMESLICE 5  

/ * 线程1入口 */  
static void threadl_entry(void *parameter) 
{
	 / * 先让低优先级线程运行*/
	  rt_thread_mdelay(100);  
	 
	 /* 此时 thread3 持有 mutex,而 thread2 等待持有 mutex /*  
	 
	 / * 检查thread2与thread3的优先级情况*/ 
	 if (tid2->current_priority != tid3->current_priority)  
	{  
		/ * 优先级不相同,测试失败*/ 
		rt_kprintf("the priority of thread2 is: %d\n", tid2->current_priority);
		rt_kprintf(Hthe priority of threads is: %d\nM, tid3->current_priority); 
		rt_kprintf("test failed.\nM); return;
	}
	else
	 { 
		rt_kprintf("the priority of thread2 is: %d\n”, tid2->current_priority); 
		rt_kprintf("the priority of thread3 is: %d\n", tid3->current_priority);
		rt_kprintf(Htest OK.\n"); 
	 } 
}
  


/ * 线程2入口 */  
static void thread2_entry(void *parameter) 
{ 
	 rt err t result;  
	 rt_kprintf("the priority of thread2 is: %d\n", tid2->current_priority); 
	 
	/ * 先让低优先级线程运行*/
	 rt_thread_mdelay(50); 
	 
	/*  
	* 试图持有互斥锁,此时thread3持有互斥锁,应把threads的优先级提升
	* 到与thread2相同的优先级
	*/ 
	result = rt_mutex_take(mutex, RT_WAITING_FOREVER);  
	if (result == RT_EOK) 
	{  
		/ * 释放互斥锁*/  
		rt__mutex_release (mutex);
	}
}

/ * 线程3入口 */  
static void thread3_entry(void *parameter)
{ 
	rt_tick_t tick;
	rt_err_t result;  
	
	rt_kprintf(the priority of thread3 is: %d\n", tid3->current_priority); 
	 
	result = rt_mutex_take(mutex, RT_WAITING_FOREVER);
	if (result != RT_EOK)  
	{
		rt_kprintf("thread3 take a mutex, failed.\n"); 
	}  
	
	/ * 做一个长时间的循环,500ms /* 
	tick = rt_tick_get(); 
	while (rt_tick_get 0 - tick < (RT^TICK_PER_SECOND / 2));
	 
	rt_mutex_release(mutex); 
} 

int pri_inversion(void)
{
	/ * 创建互斥锁*/  
	mutex = rt_mutex_create("mutex", RT_IPC_FLAG_FIFO); 
	if (mutex == RT_NULL) ,  
	(
	  rt_kprintf ('c*reate dynamic mutex failed. \n"); 
	  return -1; 
	} 
	
	/ * 创建线程1 /* 
	tidl = rt__thread_create ("threadl", threadl_entry, RT_NULL, THREAD_STACK__SIZE, THREAD__PRIORITY - 1, THREAD_TIMESLICE); 
	if (tidl 1= RT_NULL) 
		rt_thread_startup(tidl);
	
	/ * 创建线程2 /*  
	tid2 = rt__thread_create ("thread2 ", thread2_entry, RT_NULL, THREAD_STACK_SIZE, THREAD_PRIORITY, THREAD_TIMESLICE); 
	if (tid2 1= RT_NULL)
 		rt_thread_startup(tid2);
	  
	/ * 创建线程3 /*  
	tid3 = rt_thread__create ("threads ", thread3_entry, RT_NULL, THREAD_STACK_SIZE, THREAD_PRIORITY + 1, THREAD_TIMESLICE);
	if (tid3 ]= RT_NULL) 
		rt_thread_startup(tid3);  
		
	return 0; 
} 

  / * 导出到msh命令列表中*/  
  MSH CMD EXPORT(pri inversion, prio inversion sample);

```
上面的例程演示了互斥量的使用方法。**线程3先持有互斥量, 而后线程2试图持有互斥量, 此时线程3的优先级被提升为和线程2的优先级相同。**
### 工作机制 
互斥量和信号量的不同是：拥有互斥量的线程拥有互斥量的所有权，互斥量支持递归访问且能防止线程优先级翻转；互斥量只能由持有线程释放，而信号量则可以由任何线程释放。
### 实现
```
struct rt_mutex
{
    struct rt_ipc_object parent;                        /**< inherit from ipc_object */

    rt_uint16_t          value;                         /**< value of mutex */

    rt_uint8_t           original_priority;             /**< priority of last thread hold the mutex */
    rt_uint8_t           hold;                          /**< numbers of thread hold the mutex */

    struct rt_thread    *owner;                         /**< current owner of mutex */
};
typedef struct rt_mutex *rt_mutex_t;


rt_err_t rt_mutex_init(rt_mutex_t mutex, const char *name, rt_uint8_t flag)
	rt_object_init(&(mutex->parent.parent), RT_Object_Class_Mutex, name);
	rt_ipc_object_init(&(mutex->parent));
	
	mutex->value = 1;
    mutex->owner = RT_NULL;
    mutex->original_priority = 0xFF;
    mutex->hold  = 0;
    
    mutex->parent.parent.flag = flag;
    
    
    
rt_err_t rt_mutex_take(rt_mutex_t mutex, rt_int32_t time)
	temp = rt_hw_interrupt_disable();
	
	thread = rt_thread_self();
	
	if (mutex->owner == thread)
		/* it's the same thread */
		 mutex->hold ++;
	else
		/* The value of mutex is 1 in initial status. Therefore, if the
         * value is great than 0, it indicates the mutex is avaible.
         */
		if (mutex->value > 0)
			/* mutex is available */
			mutex->value --;
			
			/* set mutex owner and original priority */
			mutex->owner             = thread;
			mutex->original_priority = thread->current_priority;
			mutex->hold ++;
		else
			/* no waiting, return with timeout */
            if (time == 0)
                /* enable interrupt */
                rt_hw_interrupt_enable(temp);
                return 
            else
            	/* mutex is unavailable, push to suspend list */
            	
            	/* change the owner thread priority of mutex */
                if (thread->current_priority < mutex->owner->current_priority)
                {
                    /* change the owner thread priority */
                    rt_thread_control(mutex->owner,
                                      RT_THREAD_CTRL_CHANGE_PRIORITY,
                                      &thread->current_priority);
                }

                /* suspend current thread */
                rt_ipc_list_suspend(&(mutex->parent.suspend_thread),
                                    thread,
                                    mutex->parent.parent.flag);

                /* has waiting time, start thread timer */
                if (time > 0)
                {
                    RT_DEBUG_LOG(RT_DEBUG_IPC,
                                 ("mutex_take: start the timer of thread:%s\n",
                                  thread->name));

                    /* reset the timeout of thread timer and start it */
                    rt_timer_control(&(thread->thread_timer),
                                     RT_TIMER_CTRL_SET_TIME,
                                     &time);
                    rt_timer_start(&(thread->thread_timer));
                }

                /* enable interrupt */
                rt_hw_interrupt_enable(temp);

                /* do schedule */
                rt_schedule();
		
	
```


if检查当前线程是否已经持有该互斥量，如果是，增加持有计数。
else
	if检查互斥量是否可用，如果可用，当前线程获取互斥量和设置互斥优先级，增加持有计数。
	else如果互斥量不可用
		if且超时时间为0，设置线程错误为 -RT_ETIMEOUT 并返回，开启中断。
		else如果互斥量不可用如果互斥量不可用且超时时间大于0，
			如果当前线程的优先级高于互斥量持有者的优先级，提升持有者的优先级以避免优先级倒置问题。
			将当前线程挂起到互斥量的挂起线程列表中。
			如果指定了超时时间，启动线程定时器。
			启用中断并触发调度器。
			如果线程错误不是 RT_EOK，返回线程错误。
			如果成功获取互斥量，再次禁用中断。
### 使用场合
(1) **线程多次持有互斥量的情况。这样可以避免[[../已归类卡/同一线程多次递归持有而造成死锁]]的问题。**  lizi?
(2) 可能会由于多线程同步而造成优先级翻转的情况。

## 事件集
利用事件集可以完成一对多、多对多的线程间同步


事件无排队性,即多次向线程发送同一事件 (如果线程还未来得及读走), 其效果等同于只发送一次。
### 使用场合
“它能够在一定程度上代替信号量,用于线程间同步”

“但是它与信号量不同的是，**事件的发送操作在事件未清除前是不可累计的;，而信号量的释放动作是累计的**”
### 实现
```
struct rt_event
{
    struct rt_ipc_object parent;                        /**< inherit from ipc_object */

    rt_uint32_t          set;                           /**< event set */
};


rt_err_t rt_event_init(rt_event_t event, const char *name, rt_uint8_t flag)
	rt_object_init(&(event->parent.parent), RT_Object_Class_Event, name);
	rt_ipc_object_init(&(event->parent));
	event->parent.parent.flag = flag;
	event->set = 0;		
	
	
	
rt_err_t rt_event_send(rt_event_t event, rt_uint32_t set)
	level = rt_hw_interrupt_disable();
	
	/* set event */
    event->set |= set;
    
    if (!rt_list_isempty(&event->parent.suspend_thread))
    	/* search thread list to resume thread */
        n = event->parent.suspend_thread.next;
        while (n != &(event->parent.suspend_thread))
        	/* get thread */
            thread = rt_list_entry(n, struct rt_thread, tlist);
            if (thread->event_info & RT_EVENT_FLAG_AND)
            	if ((thread->event_set & event->set) == thread->event_set)
            		/* received an AND event */
                    status = RT_EOK;
            else if (thread->event_info & RT_EVENT_FLAG_OR)
            	if (thread->event_set & event->set)
            		 /* save recieved event set */
                    thread->event_set = thread->event_set & event->set;
                    /* received an OR event */
                    status = RT_EOK;
                    
            /* move node to the next */
            n = n->next;

			/* condition is satisfied, resume thread */
            if (status == RT_EOK)
            	/* clear event */
                if (thread->event_info & RT_EVENT_FLAG_CLEAR)
                	event->set &= ~thread->event_set;
                
                /* resume thread, and thread list breaks out */
                rt_thread_resume(thread);
                
                /* need do a scheduling */
                need_schedule = RT_TRUE;
    
     /* enable interrupt */
    rt_hw_interrupt_enable(level);
    
    if (need_schedule == RT_TRUE)
        rt_schedule();   
            
```


设置事件
	- 将发送的事件集与事件对象的当前事件集进行位或操作，更新事件对象的事件集。

if 检查是否有线程因等待该事件而挂起。
	while遍历挂起线程列表，检查每个线程的等待条件是否满足。
		 如果线程的等待条件是 `AND`，检查发送的事件集是否包含线程等待的所有事件。
		 如果线程的等待条件是 `OR`，检查发送的事件集是否包含线程等待的任意一个事件。
		 n = n->next;
		 如果条件满足，恢复线程，并设置 `need_schedule` 为 `RT_TRUE`。
		 如果线程的等待条件包含 `RT_EVENT_FLAG_CLEAR`，清除事件对象中已接收的事件。
启用中断
如果恢复了线程，调用 `rt_schedule` 触发调度器，重新调度线程
# 线程间通信 
==**在裸机编程中, 经常会使用全局变量进行功能间的通信, 如某些功能可能由于一些操作而改变全局变量的值, 另一个功能对此全局变量进行读取, 根据读取到的全局变量值执行相应的动作, 达到通信协作的目的**==
## 邮箱
### 工作方式 
非阻塞方式的邮件发送过程能够安全地应用于中断服务中，是线程、中断服务、定时器向线程发送消息的有效手段
邮件收取过程**可能是阻塞的**，这取决于邮箱中是否有邮件，以及收取邮件时设置的超时时间。**当邮箱中不存在邮件且超时时间不为0时, 邮件收取过程将变成阻塞方式。在这类情况下，只能由线程进行邮件的收取。**
![](../fujian/Pasted%20image%2020250513082923.png)
### 实现
```
struct rt_mailbox
{
    struct rt_ipc_object parent;                        /**< inherit from ipc_object */

    rt_uint32_t         *msg_pool;                      /**< start address of message buffer */

    rt_uint16_t          size;                          /**< size of message pool */

    rt_uint16_t          entry;                         /**< index of messages in msg_pool */
    rt_uint16_t          in_offset;                     /**< input offset of the message buffer */
    rt_uint16_t          out_offset;                    /**< output offset of the message buffer */

    rt_list_t            suspend_sender_thread;         /**< sender thread suspended on this mailbox */
};
typedef struct rt_mailbox *rt_mailbox_t;



rt_err_t rt_mb_init(rt_mailbox_t mb,
                    const char  *name,
                    void        *msgpool,
                    rt_size_t    size,
                    rt_uint8_t   flag)
	rt_object_init(&(mb->parent.parent), RT_Object_Class_MailBox, name);
	rt_ipc_object_init(&(mb->parent));
	mb->parent.parent.flag = flag;
 
	/* init mailbox */
	mb->msg_pool   = msgpool;
	mb->size       = size;
	mb->entry      = 0;
	mb->in_offset  = 0;
	mb->out_offset = 0;
	
	 /* init an additional list of sender suspend thread */
    rt_list_init(&(mb->suspend_sender_thread));
    
    
    
rt_err_t rt_mb_send(rt_mailbox_t mb, rt_uint32_t value)
{
    return rt_mb_send_wait(mb, value, 0);
}

rt_err_t rt_mb_send_wait(rt_mailbox_t mb,
                         rt_uint32_t  value,
                         rt_int32_t   timeout)
	thread = rt_thread_self();
	temp = rt_hw_interrupt_disable();
	
	/* for non-blocking call */
    if (mb->entry == mb->size && timeout == 0)
	    rt_hw_interrupt_enable(temp);	
	    return -RT_EFULL;
	
	 /* mailbox is full */
    while (mb->entry == mb->size)
	    /* no waiting, return timeout */
		if (timeout == 0)
			rt_hw_interrupt_enable(temp);
			return -RT_EFULL;
			
		/* suspend current thread */
		rt_ipc_list_suspend(&(mb->suspend_sender_thread),
							thread,
							mb->parent.parent.flag);
		
	 	if (timeout > 0)
	 		/* get the start tick of timer */
            tick_delta = rt_tick_get();
            
        rt_hw_interrupt_enable(temp);
        rt_schedule();
        
        /* resume from suspend state */
        if (thread->error != RT_EOK)
        	return thread->error;
        	
        temp = rt_hw_interrupt_disable();	
        
        /* if it's not waiting forever and then re-calculate timeout tick */
        if (timeout > 0)
        ...
		 
		 
rt_err_t rt_mb_recv(rt_mailbox_t mb, rt_uint32_t *value, rt_int32_t timeout)
```
#### 检查邮箱是否已满
- 如果邮箱已满且超时时间为0，返回 `-RT_EFULL`。
#### 等待邮箱空间可用
如果邮箱已满，进入等待循环。
	如果超时时间为0，返回 -RT_EFULL。开中断
	将当前线程挂起到邮箱的发送等待列表中。
	如果指定了超时时间，启动线程定时器。
	启用中断并触发调度器。
	如果线程错误不是 RT_EOK，返回线程错误。
	关闭中断
	如果超时时间大于0，重新计算超时时间。
#### 发送消息
将消息值写入邮箱的消息池。mb->msg_pool[mb->in_offset] = value;
更新输入偏移量。++ mb->in_offset;
如果输入偏移量超出邮箱大小，将其重置为0。
增加邮箱中的消息数量。mb->entry ++;
#### 唤醒等待的线程
如果有线程因等待消息而挂起，恢复这些线程。
启用中断并触发调度器。
#### 开启中断





#### 禁用中断
#### 检查邮箱是否为空
如果邮箱为空且超时时间为0，返回 -RT_ETIMEOUT。
#### 等待消息可用
如果邮箱为空，进入等待循环。
	如果超时时间为0，返回 -RT_ETIMEOUT。
	将当前线程挂起到邮箱的接收等待列表中。
	如果指定了超时时间，启动线程定时器。
	启用中断并触发调度器。
	如果线程错误不是 RT_EOK，返回线程错误。
	关闭中断
	如果超时时间大于0，重新计算超时时间。
#### 接收消息
从邮箱的消息池中读取消息值。\*value = mb->msg_pool[mb->out_offset];
更新输出偏移量。++ mb->out_offset
如果输出偏移量超出邮箱大小，将其重置为0。
减少邮箱中的消息数量。mb->entry --;
#### 唤醒等待的线程
如果有线程因等待发送消息而挂起，恢复这些线程。
启用中断并触发调度器。
#### 启用中断
启用中断，结束临界区保护。

### 使用场合
“一次传递一个4字节大小的邮件,并且具备一定的存储功能, 能够缓存一定数量的邮件数(邮件数由创建、初始化邮箱时指定的容量决定)”

“由于在32系统上 4字节的内容恰好可以放置一个指针,因此当需要在线程间传递比较大的消息时,可以把指向一个缓冲区的指针作为邮件发送到邮箱中,即邮箱也可以传递指针”
例如
struct msg 
(  rt uint8 t \*data ptr;
rt__uint32_t data_size; },  
当一个线程需要把这个消息发送给另外一个线程时, 可以采用如下的操作:
```
struct *msg msg_ptr;  

msg_ptr = (struct msg*)rt_malloc(sizeof(struct msg)); 
msg_ptr->data_ptr = ...; /* 指向相应的数据块地址*/ 
msg_ptr->data_size = len; /* 数据块的长度 */ 
/* 妥送这个消息招针给mb邮箱*/  
rt_mb_send (mb, (rt_uint32_t) msg_ptr);
```
而在接收线程中, 因为收取过来的是指针, 而msg_ptr是一个新分配出来的内存块, 所以在接收线程处理完毕后, 需要释放相应的内存块:
```
struct *msg msg_ptr; 
if (rt_mb_recv(mb, (*rt_uint32_t*)&msg_ptr == RT_EOK)  
{
	/ * 在接收线程处理完毕后,需要释放相应的内存块*/ 
	rt_free(msg_ptr); 
}
```
## 消息队列
“,线程或中断服务例程可以将一条或多条消息放入消息队列中。同样,一 个或多个线程也可以从消息队列中获得消息。当有多个消息发送到消息队列时,通常将先进入消息队列的消息先传给线程”

“也就是说,线程先得到的是最先进入消息队列的消息, 即**先进先出(FIFO)原则**。”

![](../fujian/Pasted%20image%2020250624110811.png)
消息队列对象由多个元素组成, 当消息队列被创建时, 它就被分配了消息队列控制块: 消息队列名称、内存缓冲区、消息大小以及队列长度等。
同时每个消息队列对象中包含多个消息框, 每个消息框可以存放一条消息; 
消息队列中的第一个和最后一个消息框分别被称为消息链表头和消息链表尾, 对应于消息队列控制块中的msg_  queue_head和msg_queue_tail ;

有些消息框可能是空的, 它们通过msg_queue_free形成一个空闲消息框链表

。所有消息队列中的消息框总数即消息队列的长度, 这个长度可在消息队列创建时指定。


### 实现
```
struct rt_messagequeue
{
    struct rt_ipc_object parent;                        /**< inherit from ipc_object */

    void                *msg_pool;                      /**< start address of message queue */

    rt_uint16_t          msg_size;                      /**< message size of each message */
    rt_uint16_t          max_msgs;                      /**< max number of messages */

    rt_uint16_t          entry;                         /**< index of messages in the queue */

    void                *msg_queue_head;                /**< list head */
    void                *msg_queue_tail;                /**< list tail */
    void                *msg_queue_free;                /**< pointer indicated the free node of queue */
};
typedef struct rt_messagequeue *rt_mq_t;


rt_err_t rt_mq_init(rt_mq_t     mq,
                    const char *name,
                    void       *msgpool,
                    rt_size_t   msg_size,
                    rt_size_t   pool_size,
                    rt_uint8_t  flag)
	rt_object_init(&(mq->parent.parent), RT_Object_Class_MessageQueue, name);
	mq->parent.parent.flag = flag;
	rt_ipc_object_init(&(mq->parent));
	
	/* set messasge pool */
    mq->msg_pool = msgpool;
    
    /* get correct message size */
    mq->msg_size = RT_ALIGN(msg_size, RT_ALIGN_SIZE);
    mq->max_msgs = pool_size / (mq->msg_size + sizeof(struct rt_mq_message));
    
   /* init message list */
    mq->msg_queue_head = RT_NULL;
    mq->msg_queue_tail = RT_NULL;
    
     /* init message empty list */
    mq->msg_queue_free = RT_NULL;
    for (temp = 0; temp < mq->max_msgs; temp ++)
    	head = (struct rt_mq_message *)((rt_uint8_t *)mq->msg_pool +
            temp * (mq->msg_size + sizeof(struct rt_mq_message)));
        head->next = mq->msg_queue_free;
        mq->msg_queue_free = head;
    
     /* the initial entry is zero */
    mq->entry = 0; 
    
    
    
rt_err_t rt_mq_send(rt_mq_t mq, void *buffer, rt_size_t size)
	/* greater than one message size */
	if (size > mq->msg_size)
		return -RT_ERROR;
	
	temp = rt_hw_interrupt_disable();
	
	/* get a free list, there must be an empty item */
    msg = (struct rt_mq_message*)mq->msg_queue_free;
	/* message queue is full */
    if (msg == RT_NULL)	
		
```
rt_mq_send(rt_mq_t mq, void \*buffer, rt_size_t size)
#### 禁用中断
#### 获取空闲消息节点
从消息队列的空闲链表中获取一个空闲消息节点。msg = (struct rt_mq_message*)mq->msg_queue_free;
如果空闲链表为空，表示消息队列已满，返回 -RT_EFULL。开启中断
更新空闲链表的头指针。mq->msg_queue_free = msg->next;
#### 启用中断
#### 准备消息内容
将消息节点的 next 指针设置为 NULL。
将消息内容从缓冲区复制到消息节点中。rt_memcpy(msg + 1, buffer, size);
#### 禁用中断
#### 将消息链接到消息队列
如果消息队列的**尾指针不为空，将新消息链接到队列的尾部**。 ((struct rt_mq_message \*)mq->msg_queue_tail)->next = msg;
更新消息队列的尾指针。mq->msg_queue_tail = msg;
如果消息队列的头指针为空，将新消息设置为队列的头部。mq->msg_queue_head = msg;
增加消息队列中的消息数量。mq->entry ++;
#### 唤醒等待的线程
如果有线程因等待消息而挂起，恢复这些线程。
启用中断并触发调度器。
#### 启用中断







rt_mq_recv(rt_mq_t mq, void \*buffer, rt_size_t size,rt_int32_t timeout)
#### 禁用中断
#### 检查消息队列是否为空
- 如果消息队列为空且超时时间为0，返回 `-RT_ETIMEOUT`。
#### 等待消息可用
如果消息队列为空，进入等待循环。
	如果超时时间为0，返回 -RT_ETIMEOUT。开启中断
	将当前线程挂起到消息队列的接收等待列表中。
	如果指定了超时时间，启动线程定时器。
	启用中断并触发调度器。
	如果线程错误不是 RT_EOK，返回线程错误。
	关闭中断
	如果超时时间大于0，重新计算超时时间。
#### 获取消息
从消息队列的**头部获取一条消息**。msg = (struct rt_mq_message \*)mq->msg_queue_head;
更新消息队列的头部指针。mq->msg_queue_head = msg->next;
如果消息队列的尾指针指向当前消息，将尾指针设置为 NULL。if (mq->msg_queue_tail == msg) mq->msg_queue_tail = RT_NULL;
减少消息队列中的消息数量。mq->entry --;
#### 启用中断
#### 复制消息内容
将消息内容从消息节点复制到缓冲区。如果缓冲区大小大于消息大小，只复制消息大小的内容  
rt_memcpy(buffer, msg + 1, size > mq->msg_size ? mq->msg_size : size);
#### 禁用中断
#### 将消息节点放回空闲链表
msg->next = (struct rt_mq_message \*)mq->msg_queue_free;
mq->msg_queue_free = msg;
#### 启用中断
### 使用场合
“下面以发送消息和同步消息两部芬来介绍消息队列的使用。”
#### 发送消息
“是类似邮箱的代码:”
```
struct msg 
{
	rt_uint8_t *data_ptr; /* 数据块首地址 */  
	rt uint32 t data size; /* 数据块大小 */
}
```
假设依然需要发送这样一个消息给接收线程。在邮箱的例子中,这个结构只能够发送指向该结构的指针 (在函数指针被发送过去后, 接收线程能够正确地访问指向这个地址的内容, 通常这块数据需要留给接收线程来释放)

而使用消息队列的方式则大不相同:
```
void send_op(void *data, rt_size_t length) 
{  
	struct msg msg_ptr; 
	
	msg_ptr.data_ptr = data; / * 指向相应的数据块地址*/ 
	msg_ptr.data_size = length; /* 数据块的长度 */  
	
	/ * 发送这个消息指针给mq消息队列*/ 
	rt_mq_send(mq, (void*)&msg_ptr, sizeof(struct msg));
}
```
上面的代码中是把一个**局部变量的数据内容发送到了消息队列**中。
在接收线程中, 同样也**采用局部变量进行消息接收的结构体**:
```
void message_handler()
{
	struct msg msg_ptr; / * 用于放置消息的局部变量*/ 
	
	/ * 从消息队列中接收消息到msg_ptr中*/ 
	if (rt__mq_recv (mq, (*void) &msg_ptr, sizeof (struct msg) ) == RT_EOK) 
	{ 
		 / * 成功接收到消息,进行相应的数据处理*/ 
	}
}
```
“**因为消息队列是直接的数据内容复制**,所以在上面的例子中,**都采用了局部变量的方式保存消息结构体,这样也就免去了动态内存分配的烦恼**(也就不用担心,接收线程在接收 到消息时,消息内存空间已经被释放)。”
#### [[../已归类卡/同步消息]]
发送同步消息的问题, 这时就可以根据当时状态的不同选择相应的实现: 
两个线程间可以采用[消息队列+信号量或邮箱]的形式实现。
发送线程**通过消息发送的形式发送相应的消息给消息队列**, **发送完毕后希望获得接收线程的收到确认**, 工作示意图如图7-5所示。
![](../fujian/Pasted%20image%2020250624112909.png)
根据消息确认的不同, 可以把消息结构体定义成:
```
struct msg
{  
	/ * 消息结构其他成员*/  
	struct rt_mailbox ack;  
};  
  
  / * 或者*/ 
  
struct msg 
{ 
	/ * 消息结构其他成员*/ 
	 struct rt_semaphore ack;  
};
```

**第一种类型的消息使用了邮箱来作为确认标志,** 
**而第二种类型的消息采用了信号量来作为确认标志。**

邮箱作为确认标志, 代表着接收线程能够通知一些状态值给发送线程;
而信号量作为确认标志时只能够单一地通知发送线程, 消息已经确认接收。
## 信号（nano没有）
信号(又称为软中断信号)
在软件层次上是对中断机制的一种模拟, 在原理上, 一个线程收到一个信号与处理器收到一个中断请求是类似的。


“一个线程不必通过任何操作来等待信号的到达”
“线程之间可以通过互相调用rt_thread_kill()发送软中断信号。”

“收到信号的线程对各种信号有不同的处理方法”
	第一种是类似中断的处理程序,对于需要处理的信号,线程可以指定处理函数,由该函数来处理。  
	第二种方法是,忽略某个信号,对该信号不做任何处理,就像未发生过一样。  
	第三种方法是,对该信号的处理保留系统的默认值。


“如图7-6所示，假设线程1需要对信号进行处理，
	首先线程1安装一个信号并解除阻塞，并在安装的同时设定对信号的异常处理方式；
	然后其他线程可以给线程1发送信号, 触发线程1对该信号的处理。”
![](../fujian/Pasted%20image%2020250624134806.png)
当信号被传递给线程1时, 如果它正处于挂起状态, 那会把状态改为就绪状态去处理对应的信号。
如果它正处于运行状态, 那么会在它当前的线程栈基础上建立新栈帧空间去处理对应的信号, 需要注意的是, 使用的线程栈大小也会相应增加。
# **内存管理** 
## 内存堆管理

**内存堆配置和初始化**
	“在使用内存堆时，必须要在系统初始化的时候进行堆的初始化”
	void rt_system_heap_init(void \*begin_addr, void \*end_addr)
	这个函数会把参数begin_addr、end addr区域的内存空间作为内存堆来使用

	在使用memheap堆内存时
	rt_err_t rt_memheap_init(struct rt__memheap \*memheap, const char \*name, void s\*tart_addr , rt_uint32_t size)
	如果有多个不连续的memheap, 可以多次调用该函数将其初始化并加入memheap item  链表

**接口**
	![](../fujian/Pasted%20image%2020250624141942.png)
### 小内存管理算法
### [[../已归类卡/slab管理算法]]
![](../fujian/Pasted%20image%2020250624142909.png)

```·
void rt_system_heap_init(void *begin_addr, void *end_addr)
{
    rt_uint32_t limsize, npages;

    RT_DEBUG_NOT_IN_INTERRUPT;

    /* align begin and end addr to page */
    heap_start = RT_ALIGN((rt_ubase_t)begin_addr, RT_MM_PAGE_SIZE);
    heap_end   = RT_ALIGN_DOWN((rt_ubase_t)end_addr, RT_MM_PAGE_SIZE);

    if (heap_start >= heap_end)
    {
        rt_kprintf("rt_system_heap_init, wrong address[0x%x - 0x%x]\n",
                   (rt_ubase_t)begin_addr, (rt_ubase_t)end_addr);

        return;
    }

    limsize = heap_end - heap_start;
    npages  = limsize / RT_MM_PAGE_SIZE;

    /* initialize heap semaphore */
    rt_sem_init(&heap_sem, "heap", 1, RT_IPC_FLAG_FIFO);

    RT_DEBUG_LOG(RT_DEBUG_SLAB, ("heap[0x%x - 0x%x], size 0x%x, 0x%x pages\n",
                                 heap_start, heap_end, limsize, npages));

    /* init pages */
    rt_page_init((void *)heap_start, npages);

    /* calculate zone size */
    zone_size = ZALLOC_MIN_ZONE_SIZE;
    while (zone_size < ZALLOC_MAX_ZONE_SIZE && (zone_size << 1) < (limsize / 1024))
        zone_size <<= 1;

    zone_limit = zone_size / 4;
    if (zone_limit > ZALLOC_ZONE_LIMIT)
        zone_limit = ZALLOC_ZONE_LIMIT;

    zone_page_cnt = zone_size / RT_MM_PAGE_SIZE;

    RT_DEBUG_LOG(RT_DEBUG_SLAB, ("zone size 0x%x, zone page count 0x%x\n",
                                 zone_size, zone_page_cnt));

    /* allocate memusage array */
    limsize  = npages * sizeof(struct memusage);
    limsize  = RT_ALIGN(limsize, RT_MM_PAGE_SIZE);
    memusage = rt_page_alloc(limsize / RT_MM_PAGE_SIZE);

    RT_DEBUG_LOG(RT_DEBUG_SLAB, ("memusage 0x%x, size 0x%x\n",
                                 (rt_ubase_t)memusage, limsize));
}
```



```
void *rt_malloc(rt_size_t size)
{
    slab_zone *z;
    rt_int32_t zi;
    slab_chunk *chunk;
    struct memusage *kup;

    /* zero size, return RT_NULL */
    if (size == 0)
        return RT_NULL;

    /*
     * Handle large allocations directly.  There should not be very many of
     * these so performance is not a big issue.
     */
    if (size >= zone_limit)
    {
        size = RT_ALIGN(size, RT_MM_PAGE_SIZE);

        chunk = rt_page_alloc(size >> RT_MM_PAGE_BITS);
        if (chunk == RT_NULL)
            return RT_NULL;

        /* set kup */
        kup = btokup(chunk);
        kup->type = PAGE_TYPE_LARGE;
        kup->size = size >> RT_MM_PAGE_BITS;

        RT_DEBUG_LOG(RT_DEBUG_SLAB,
                     ("malloc a large memory 0x%x, page cnt %d, kup %d\n",
                      size,
                      size >> RT_MM_PAGE_BITS,
                      ((rt_ubase_t)chunk - heap_start) >> RT_MM_PAGE_BITS));

        /* lock heap */
        rt_sem_take(&heap_sem, RT_WAITING_FOREVER);

#ifdef RT_MEM_STATS
        used_mem += size;
        if (used_mem > max_mem)
            max_mem = used_mem;
#endif
        goto done;
    }

    /* lock heap */
    rt_sem_take(&heap_sem, RT_WAITING_FOREVER);

    /*
     * Attempt to allocate out of an existing zone.  First try the free list,
     * then allocate out of unallocated space.  If we find a good zone move
     * it to the head of the list so later allocations find it quickly
     * (we might have thousands of zones in the list).
     *
     * Note: zoneindex() will panic of size is too large.
     */
    zi = zoneindex(&size);
    RT_ASSERT(zi < NZONES);

    RT_DEBUG_LOG(RT_DEBUG_SLAB, ("try to malloc 0x%x on zone: %d\n", size, zi));

    if ((z = zone_array[zi]) != RT_NULL)
    {
        RT_ASSERT(z->z_nfree > 0);

        /* Remove us from the zone_array[] when we become empty */
        if (--z->z_nfree == 0)
        {
            zone_array[zi] = z->z_next;
            z->z_next = RT_NULL;
        }

        /*
         * No chunks are available but nfree said we had some memory, so
         * it must be available in the never-before-used-memory area
         * governed by uindex.  The consequences are very serious if our zone
         * got corrupted so we use an explicit rt_kprintf rather then a KASSERT.
         */
        if (z->z_uindex + 1 != z->z_nmax)
        {
            z->z_uindex = z->z_uindex + 1;
            chunk = (slab_chunk *)(z->z_baseptr + z->z_uindex * size);
        }
        else
        {
            /* find on free chunk list */
            chunk = z->z_freechunk;

            /* remove this chunk from list */
            z->z_freechunk = z->z_freechunk->c_next;
        }

#ifdef RT_MEM_STATS
        used_mem += z->z_chunksize;
        if (used_mem > max_mem)
            max_mem = used_mem;
#endif

        goto done;
    }

    /*
     * If all zones are exhausted we need to allocate a new zone for this
     * index.
     *
     * At least one subsystem, the tty code (see CROUND) expects power-of-2
     * allocations to be power-of-2 aligned.  We maintain compatibility by
     * adjusting the base offset below.
     */
    {
        rt_int32_t off;

        if ((z = zone_free) != RT_NULL)
        {
            /* remove zone from free zone list */
            zone_free = z->z_next;
            -- zone_free_cnt;
        }
        else
        {
            /* unlock heap, since page allocator will think about lock */
            rt_sem_release(&heap_sem);

            /* allocate a zone from page */
            z = rt_page_alloc(zone_size / RT_MM_PAGE_SIZE);
            if (z == RT_NULL)
            {
                chunk = RT_NULL;
                goto __exit;
            }

            /* lock heap */
            rt_sem_take(&heap_sem, RT_WAITING_FOREVER);

            RT_DEBUG_LOG(RT_DEBUG_SLAB, ("alloc a new zone: 0x%x\n",
                                         (rt_ubase_t)z));

            /* set message usage */
            for (off = 0, kup = btokup(z); off < zone_page_cnt; off ++)
            {
                kup->type = PAGE_TYPE_SMALL;
                kup->size = off;

                kup ++;
            }
        }

        /* clear to zero */
        rt_memset(z, 0, sizeof(slab_zone));

        /* offset of slab zone struct in zone */
        off = sizeof(slab_zone);

        /*
         * Guarentee power-of-2 alignment for power-of-2-sized chunks.
         * Otherwise just 8-byte align the data.
         */
        if ((size | (size - 1)) + 1 == (size << 1))
            off = (off + size - 1) & ~(size - 1);
        else
            off = (off + MIN_CHUNK_MASK) & ~MIN_CHUNK_MASK;

        z->z_magic     = ZALLOC_SLAB_MAGIC;
        z->z_zoneindex = zi;
        z->z_nmax      = (zone_size - off) / size;
        z->z_nfree     = z->z_nmax - 1;
        z->z_baseptr   = (rt_uint8_t *)z + off;
        z->z_uindex    = 0;
        z->z_chunksize = size;

        chunk = (slab_chunk *)(z->z_baseptr + z->z_uindex * size);

        /* link to zone array */
        z->z_next = zone_array[zi];
        zone_array[zi] = z;

#ifdef RT_MEM_STATS
        used_mem += z->z_chunksize;
        if (used_mem > max_mem)
            max_mem = used_mem;
#endif
    }

done:
    rt_sem_release(&heap_sem);
    RT_OBJECT_HOOK_CALL(rt_malloc_hook, ((char *)chunk, size));

__exit:
    return chunk;
}
```

```
rt_inline int zoneindex(rt_size_t *bytes)
{
    /* unsigned for shift opt */
    rt_ubase_t n = (rt_ubase_t)(*bytes);

    if (n < 128)
    {
        *bytes = n = (n + 7) & ~7;

        /* 8 byte chunks, 16 zones */
        return (n / 8 - 1);
    }
    if (n < 256)
    {
        *bytes = n = (n + 15) & ~15;

        return (n / 16 + 7);
    }
    if (n < 8192)
    {
        if (n < 512)
        {
            *bytes = n = (n + 31) & ~31;

            return (n / 32 + 15);
        }
        if (n < 1024)
        {
            *bytes = n = (n + 63) & ~63;

            return (n / 64 + 23);
        }
        if (n < 2048)
        {
            *bytes = n = (n + 127) & ~127;

            return (n / 128 + 31);
        }
        if (n < 4096)
        {
            *bytes = n = (n + 255) & ~255;

            return (n / 256 + 39);
        }
        *bytes = n = (n + 511) & ~511;

        return (n / 512 + 47);
    }
    if (n < 16384)
    {
        *bytes = n = (n + 1023) & ~1023;

        return (n / 1024 + 55);
    }

    rt_kprintf("Unexpected byte count %d", n);

    return 0;
}
```
### memheap管理算法
![](../fujian/Pasted%20image%2020250624143115.png)
## 内存池
![](../fujian/Pasted%20image%2020250624141510.png)



“内存堆管理器可以分配任意大小的内存块，非常灵活和方便，但其也存在明显的缺点： 一是分配效率不高，在每次分配时，都要空闲内存块查找；二是容易产生内存碎片”
“提高内存分配的效率，并且避免内存碎片，RT-Thread提供了另外一种内存管理方法：内存池(Memory Pool)”


内存池用于分配大量**大小相同**的小内存块

“RT-Thread的**内存池支持线程挂起功能**，当内存池中无空闲内存块时，申请线程会被挂起，直到内存池中有新的可用内存块，再将挂起的申请线程唤醒。”
“内存池的线程**挂起功能非常适合需要通过内存资源进行同步的场景**，例如播放音乐时，播放器线程会对音乐文件进行解码，然后发送到声卡驱动，从而驱动硬件播放音乐。”
如图8-8所示,当播放器线程需要解码数据时,就会向内存池请求内存块,如果内存块已经用完,线程将被挂起,否则它将获得内存块以放置解码的数据;
而后播放器线程把包含解码数据的内存块写入到声卡抽象设备中(线程会立刻返回,继续解码出更多的数据);  
当声卡设备写入完成后,将调用播放器线程设置的回调函数,释放写入的内存块,如果在此之前,播放器线程因为把内存池里的内存块都用完而被挂起的话,那么这次它将被将唤醒,并继续进行解码。
![](../fujian/Pasted%20image%2020250624143953.png)
### 实现
```
struct rt_mempool
{
    struct rt_object parent;                            /**< inherit from rt_object */

    void            *start_address;                     /**< memory pool start */
    rt_size_t        size;                              /**< size of memory pool */

    rt_size_t        block_size;                        /**< size of memory blocks */
    rt_uint8_t      *block_list;                        /**< memory blocks list */

    rt_size_t        block_total_count;                 /**< numbers of memory block */
    rt_size_t        block_free_count;                  /**< numbers of free memory block */

    rt_list_t        suspend_thread;                    /**< threads pended on this resource */
};
typedef struct rt_mempool *rt_mp_t;



rt_err_t rt_mp_init(struct rt_mempool *mp,
                    const char        *name,
                    void              *start,
                    rt_size_t          size,
                    rt_size_t          block_size)
{
    /* initialize object */
    rt_object_init(&(mp->parent), RT_Object_Class_MemPool, name);

    /* initialize memory pool */
    mp->start_address = start;
    mp->size = RT_ALIGN_DOWN(size, RT_ALIGN_SIZE);

    /* align the block size */
    block_size = RT_ALIGN(block_size, RT_ALIGN_SIZE);
    mp->block_size = block_size;

    /* align to align size byte */
    mp->block_total_count = mp->size / (mp->block_size + sizeof(rt_uint8_t *));
    mp->block_free_count  = mp->block_total_count;

    /* initialize suspended thread list */
    rt_list_init(&(mp->suspend_thread));

    /* initialize free block list */
    block_ptr = (rt_uint8_t *)mp->start_address;
    for (offset = 0; offset < mp->block_total_count; offset ++)
    {
        *(rt_uint8_t **)(block_ptr + offset * (block_size + sizeof(rt_uint8_t *))) =
            (rt_uint8_t *)(block_ptr + (offset + 1) * (block_size + sizeof(rt_uint8_t *)));
    }

    *(rt_uint8_t **)(block_ptr + (offset - 1) * (block_size + sizeof(rt_uint8_t *))) =
        RT_NULL;

    mp->block_list = block_ptr;

    return RT_EOK;
}




void *rt_mp_alloc(rt_mp_t mp, rt_int32_t time)
{
    /* disable interrupt */
    level = rt_hw_interrupt_disable();

    while (mp->block_free_count == 0)
    {
        /* memory block is unavailable. */
        if (time == 0)
        {
            rt_hw_interrupt_enable(level);

            rt_set_errno(-RT_ETIMEOUT);

            return RT_NULL;
        }

        thread->error = RT_EOK;

        /* need suspend thread */
        rt_thread_suspend(thread);
        rt_list_insert_after(&(mp->suspend_thread), &(thread->tlist));

        if (time > 0)
        {
            /* get the start tick of timer */
            before_sleep = rt_tick_get();

            /* init thread timer and start it */
            rt_timer_control(&(thread->thread_timer),
                             RT_TIMER_CTRL_SET_TIME,
                             &time);
            rt_timer_start(&(thread->thread_timer));
        }


        rt_hw_interrupt_enable(level);
        rt_schedule();

        if (thread->error != RT_EOK)
            return RT_NULL;

        if (time > 0)
        {
            time -= rt_tick_get() - before_sleep;
            if (time < 0)
                time = 0;
        }
        level = rt_hw_interrupt_disable();
    }

    /* memory block is available. decrease the free block counter */
    mp->block_free_count--;

    /* get block from block list */
    block_ptr = mp->block_list;
    RT_ASSERT(block_ptr != RT_NULL);

    /* Setup the next free node. */
    mp->block_list = *(rt_uint8_t **)block_ptr;

    /* point to memory pool */
    *(rt_uint8_t **)block_ptr = (rt_uint8_t *)mp;

    /* enable interrupt */
    rt_hw_interrupt_enable(level);


    return (rt_uint8_t *)(block_ptr + sizeof(rt_uint8_t *));
}
```

rt_err_t rt_mp_init(struct rt_mempool \*mp,
                    const char        \*name,
                    void              \*start,
                    rt_size_t          size,
                    rt_size_t          block_size)
#### 初始化对象
- 使用 `rt_object_init` 初始化内存池对象，设置对象类型为 `RT_Object_Class_MemPool`，并设置对象名称。
#### 初始化内存池
设置内存池的起始地址。 mp->start_address = start;
对内存池的总大小进行对齐，确保大小满足硬件对齐要求。
#### 对齐内存块大小
对内存块大小进行对齐，确保每个内存块的大小满足硬件对齐要求。
设置内存池的内存块大小。
#### 计算内存块总数
计算内存池中可以容纳的内存块总数。mp->block_total_count = mp->size / (mp->block_size + sizeof(rt_uint8_t \*));
初始化空闲内存块计数为总内存块数。mp->block_free_count  = mp->block_total_count;
#### 初始化挂起线程列表
rt_list_init(&(mp->suspend_thread));
#### 初始化空闲内存块链表
初始化空闲内存块链表，将所有内存块链接到一个链表中。
每个内存块的指针指向下一个内存块，最后一个内存块的指针设置为 RT_NULL。
设置内存池的空闲内存块链表头指针。


代码更详细解释如下：
block_ptr = (rt_uint8_t \*)mp->start_address;

**初始化内存块链表**：
```c
for (offset = 0; offset < mp->block_total_count; offset++)
{
    *(rt_uint8_t **)(block_ptr + offset * (block_size + sizeof(rt_uint8_t *))) =
        (rt_uint8_t *)(block_ptr + (offset + 1) * (block_size + sizeof(rt_uint8_t *)));
}
```
第一个内存块的指针（位于 0x1000）指向第二个内存块的起始位置（0x1044）。
第二个内存块的指针（位于 0x1044）指向第三个内存块的起始位置（0x1088）。
第三个内存块的指针（位于 0x1088）在循环结束后设置为 RT_NULL。

**设置最后一个内存块的指针**：
```
*(rt_uint8_t **)(block_ptr + (offset - 1) * (block_size + sizeof(rt_uint8_t *))) =
    RT_NULL;
```

mp->block_list = block_ptr;



void \*rt_mp_alloc(rt_mp_t mp, rt_int32_t time)

```
thread = rt_thread_self();
level = rt_hw_interrupt_disable();

while (mp->block_free_count == 0)
{
	/* memory block is unavailable. */
	if (time == 0)
	{
		/* enable interrupt */
		rt_hw_interrupt_enable(level);

		rt_set_errno(-RT_ETIMEOUT);

		return RT_NULL;
	}

	RT_DEBUG_NOT_IN_INTERRUPT;

	thread->error = RT_EOK;

	/* need suspend thread */
	rt_thread_suspend(thread);
	rt_list_insert_after(&(mp->suspend_thread), &(thread->tlist));

	if (time > 0)
	{
		/* get the start tick of timer */
		before_sleep = rt_tick_get();

		/* init thread timer and start it */
		rt_timer_control(&(thread->thread_timer),
						 RT_TIMER_CTRL_SET_TIME,
						 &time);
		rt_timer_start(&(thread->thread_timer));
	}

	rt_hw_interrupt_enable(level);
	rt_schedule();

	if (thread->error != RT_EOK)
		return RT_NULL;

	if (time > 0)
	{
		time -= rt_tick_get() - before_sleep;
		if (time < 0)
			time = 0;
	}
	level = rt_hw_interrupt_disable();
}

/* memory block is available. decrease the free block counter */
mp->block_free_count--;

/* get block from block list */
block_ptr = mp->block_list;
RT_ASSERT(block_ptr != RT_NULL);

/* Setup the next free node. */
mp->block_list = *(rt_uint8_t **)block_ptr;

/* point to memory pool */
*(rt_uint8_t **)block_ptr = (rt_uint8_t *)mp;

rt_hw_interrupt_enable(level);


return (rt_uint8_t *)(block_ptr + sizeof(rt_uint8_t *));
```


#### 禁用中断
#### 检查内存池是否有空闲内存块
如果内存池中没有空闲内存块，进入等待循环。
	如果超时时间为0，返回 RT_NULL。开启中断
	将当前线程挂起到内存池的挂起线程列表中。
	如果指定了超时时间，启动线程定时器。
	启用中断并触发调度器。
	如果线程错误不是 RT_EOK，返回 RT_NULL。
	如果超时时间大于0，重新计算超时时间。
#### 分配内存块
从内存池的空闲内存块链表中取出一个内存块：
1. 减少空闲内存块计数。 mp->block_free_count--;
2. 获取当前空闲内存块链表的第一个内存块。block_ptr = mp->block_list;   
3. 更新空闲内存块链表的头指针，将当前内存块从链表中移除。mp->block_list = \*(rt_uint8_t \*\*)block_ptr;
4. 将内存块的指针设置为指向内存池的起始地址，以便后续的释放操作可以找到内存池的元数据
	 \*(rt_uint8_t \*\*)block_ptr = (rt_uint8_t \*)mp;
#### 设置内存块的指针
将内存块的指针设置为指向内存池的起始地址，以便后续的释放操作可以找到内存池的元数据。
```
/* point to memory pool */
*(rt_uint8_t **)block_ptr = (rt_uint8_t *)mp;
```
#### 启用中断
#### 返回分配的内存块
返回分配的内存块的指针，跳过内存块的指针部分，直接返回内存块的起始地址。
```
return (rt_uint8_t *)(block_ptr + sizeof(rt_uint8_t *));
```
![](../fujian/Pasted%20image%2020250624152733.png)
# 中断管理 
## Cortex-M CPU 架构基础
不同于老的经典 ARM 处理器（例如 ARM 7、ARM 9 ）, ARM Cortex-M 处理器有一个非常不同的架构
### 寄存器介绍
通用寄存器组和若干特殊功能寄存器
![[Pasted image 20240429184856.png]]
通用寄存器组里的 R13作为堆栈指针寄存器（Stack Pointer, SP）; R14作为连接寄存器（Link Register, LR）,用于在调用子程序时，存储返回地址；R15作为程序计数器 （Program Counter, PC）,其中堆栈指针寄存器可以是主堆栈指针（MSP）,也可以是进程堆栈指针（PSP）

**可以通过 MSR/MRS 指令来访问特殊功能寄存器**
![[Pasted image 20240429185158.png]]

程序状态字寄存器里保存算术与逻辑标志。
控制寄存器用来定义特权级别和当前使用哪个堆栈指针
### 操作模式和特权级别
分别为线程模式和处理模式，如果进入异常或中断处理则进入处理模式，其他情况则为线程模式。
可通过 CONTROL 特殊寄存器控制
Cortex-M 有两个运行级别，分别为特权级和用户级，**线程模式可以工作在特权级或者用户级，而处理模式总工作在特权级**
![[Pasted image 20240429185345.png]]
处理模式总是使用 MSP 作为堆栈，线程模式可以选择使用 MSP 或 PSP 作为堆栈
### 嵌套向量中断控制器
**Cortex-M 中断控制器名为 NVIC** （嵌套向量中断控制器）

中断触发并且系统进行响应时，处理器硬件会将当前运行位置的上下文寄存器**自动**压入中断栈中，这部分的寄存器包括 PSR、 PC、LR、R 12、R 3 ~ RO 寄存器。
![[Pasted image 20240429185723.png]]
### PendSV 系统调用
PendSV 也称为可悬起的系统调用，它是一种异常
它是专门用来辅助操作系统进行上下文切换的
PendSV 异常会被初始化为最低优先级的异常。每次需要进行上下文切换的时候，会手动触发 PendSV 异常，在 PendSV 异常处理函数中进行上下文切换
## RTT 中断控制机制
### 中断向量表
即当一个中断触发时，处理器将直接判定是哪个中断源，然后直接**跳转到相应的固定位置**进行处理

**中断服务程序必须排列在一起放在统一的地址上**（该地址必须要设置到 NVIC 的中断向量偏移寄存器中）。
中断向量表一般由一个数组定义或在起始代码中给出，默认采用起始代码给出：
![[Pasted image 20240429190032.png]]
![[Pasted image 20240429190125.png]]
### 中断处理过程
在 RT-Thread 中断管理中，将中断处理程序分为中断前导程序、用户中断服务程序、中断后续程序 3 部分，如图 9-6 所示。、
![[Pasted image 20240429190419.png]]
#### 中断前导
(1 )保存 CPU 中断现场。对于 Cortex-M 来说，该工作由硬件自动完成
(2)通知内核进入中断状态。调用 rt_interrupt_enter ()函数，其作用是把全局变量仁 interrupt_nest 加 1, 用它来记录中断嵌套的层数
![[Pasted image 20240429190614.png]]

#### 用户中断服务
在中断处理过程中需要进行线程切换时，会调用 rt_hw_context_ switch_interrupt ()函数进行上下文切换
在 Cortex-M 架构中，**rt_hw_context_switch_interrupt** ()的函数实现流程如图 9-7所示
![[Pasted image 20240507161324.png]]
#### 中断后续程序 
1通知内核离开中断状态，通过调用 rt_interrupt_leave ()函数
![[Pasted image 20240507161521.png]]
![[Pasted image 20240507161528.png]]
2 恢复上下文
如果在中断处理过程中未进行线程切换，那么恢复 from 线程的 CPU 上下文，如果在中断中进行了线程切换，那么恢复 to 线程的 CPU 上下文。
在 Cortex-M 架构中实现流程如图 9-8 所示。
![[Pasted image 20240507161642.png]]
### 中断栈
在中断处理过程中，在系统响应中断前，软件代码（或处理器）需要把当前线程的上下文保存下来（通常保存在当前线程的**线程栈**中），再调用中断服务程序进行中断响应、处理。在进行中断处理时（实际上是调用用户的中断服务程序函数），中断处理函数中很可能会有自己的局部变量，这些都需要相应的栈空间来保存，所以**中断响应依然需要一个栈空间**作为上下文，运行中断处理函数。

**中断栈可以保存在打断线程的栈中，当从中断中退出时，返回相应的线程继续执行。**
**中断栈也可以与线程栈完全分离开来，即每次进入中断时，在保存完打断线程上下文后，切换到新的中断栈中独立运行。在中断退出时，再做相应的上下文恢复**


RT-Thread 采用的方式是提供独立的中断栈，即中断发生时，**中断的前期处理程序会将用户的栈指针更换到系统事先留出的中断栈空间中，等中断退出时再恢复用户的栈指针。这样中断就不会占用线程的栈空间，从而提高内存空间的利用率**，且随着线程的增加，这种减少内存占用的效果也越明显。

在 Cortex-M 处理器内核里有两个堆栈指针，一个是主堆栈指针（MSP）, 它是默认的堆栈指针，在运行第一个线程之前以及中断和异常服务程序里使用；另一个是线程堆栈指针（PSP）, 在线程里使用。在中断和异常服务程序退出时，**修改 LR 寄存器第 2 位的值为 1, 线程的 SP 就由 MSP 切换到 PSP**
### 中断的底半处理
**中断服务程序在取得硬件状态或数据以后，还需要进行一系列更耗时的处理**，通常需要将该中断分割为两部分，即上半部分（TopHalf）和底半部分（BottomHalf）。在上半部分中，取得硬件状态和数据后，打开被屏蔽的中断，给相关线程发送一条通知（可以是 RT-Thread 所提供的信号量、事件、邮箱或消息队列等方式）, 然后结束中断服务程序；而接下来，相关的线程在接收到通知后，接着对状态或数据进行进一步的处理，这一过程称为底半处理。


我们以一个虚拟的网络设备接收网络数据包作为范例（见代码清单 9-1）, 并假设接收到数据报文后，系统对报文的分析和处理是一个相对耗时的、比外部中断源信号重要性小许多的而且在不屏蔽中断源信号情况下也能处理的过程。
示例中的程序创建了一个 nwt 线程，该线程在启动运行后，将阻塞在 nw_bh_sem 信号上，一旦这个信号量被释放，将执行接下来的 nw_packet_parser 过程，开始 BottomHalf 的事件处理。
![[Pasted image 20240508105545.png]]
![[Pasted image 20240508105754.png]]
**在 demo_nw_isr 中是如何处理 TopHalf 并开启 BottomHalf 的，如下所示。**\
![[Pasted image 20240508105829.png]]
中断服务程序通过对一个信号量对象的等待和释放，来完成中断 BottomHalf 的起始和终结。将中断处理划分为 Top 和 Bottom 两个部分后，中断处理过程变为异步过程
这部分系统开销需要用户在使用 RT-Thread 时，必须认真考虑中断服务的处理时间是否大于给 BottomHalf 发送通知并处理的时间。

## rtt 中断管理接口
![[Pasted image 20240507163352.png|825]]
### 中断服务程序挂接
系统把用户的**中断服务程序 (handler)和指定的中断号关联**起来
![[Pasted image 20240508110812.png]]
![[Pasted image 20240508110955.png]]
通常 Cortex-M 0/M 3/M 4 的移植分支中就没有该 API

### 中断源管理
通常在 ISR 准备处理某个中断信号之前，我们需要先屏蔽该中断源，在 ISR 处理完状态或数据以后，及时打开之前被屏蔽的中断源。

### 全局中断开关
是禁止多线程访问临界区最简单的一种方式

使用中断锁来操作临界区的方法可以应用于任何场合，**且其他几类同步方式都是依赖于中断锁而实现的**
不能响应外部的事件。所以中断锁对系统的实时性影响非常巨大
当使用不当的时候会导致系统完全无实时性可言 (可能导致系统完全偏离要求的时间需求)；而使用得当，则会变成一种快速、高效的同步方式。



例如，为了保证一行代码 (例如赋值)的互斥运行，最快速的方法是使用中断锁而不是信号量或互斥量：
![[Pasted image 20240508111738.png]]
在使用中断锁时，需要确保关闭中断的时间非常短，例如上面代码中的 a=a+value, 也可换成另外一种方式，例如使用信号量：
![[Pasted image 20240508111752.png]]
这段代码在 rt_sem_take、rt_sem_release 的实现中，已经存在使用中断锁保护信号量内部变量的行为，所以对于简单如 a=a+value; 的操作，使用中断锁将更为简洁和快速。




在 RT-Thread 中，开关全局中断的 API 支持多级嵌套使用
![[Pasted image 20240508111919.png]]
这个特性可以给代码的开发带来很大的便利，例如，在某个函数里关闭了中断，然后调用某些子函数，再打开中断。**这些子函数里面也可能存在开关中断的代码。由于全局中断的 API 支持嵌套使用，用户无须为这些代码做特殊处理**。
### 中断通知
**当整个系统被中断打断，进入中断处理函数时，需要通知内核当前已经进入中断状态**

这两个接口分别用于中断前导程序和中断后续程序中，均会**对 rt_interrupt_nest (中断嵌套深度)的值进行修改**。

## 中断与轮询
当驱动外设工作时采用中断模式触发还是轮询模式触发

例如一些携带 FIFO (包含一定数据量的先进先出队列)的串口外设, 其写入过程如图 9-11 所示。
线程先向串口的 FIFO 中写入数据, 当 FIFO 满时，线程主动挂起。串口控制
器持续地从 FIFO 中取出数据并以配置的波特率 (例如 115200 bps)发送出去。当 FIFO 中所有数据都发送完成时，将向处理器触发一个中断；当中断服务程序得到执行时，可以唤醒这个线程
![[Pasted image 20240508104852.png]]

对于低速设备来说，运用这种模式非常好，因为在串口外设把 FIFO 中的数想发送出去前，处理器可以运行其他的线程，这样就提高了系统的整体运行效率 (甚至对才分时系统来说，这样的设计也非常必要)

但是对于一些高速设备，例如传输速度达到 10 Mbps 的时候，假设一次发送的数据量是 32 字节，我们可以计算出发送这样一段数据量需要的时间是：(32 x 8) xl/10 Mbps=25 us。当数据需要持续传输时，系统将在 25 us 后触发一个中断以唤醒上层线程继续下次传递。假设系统的线程切换时间是 8 us (通常实时操作系统的线程上下文切换时间只有几 us), 那么当整个系统运行时，对于数据带宽利用率将只有 25/(25+8)=75.8%。但是采用轮询模式，数据带宽的利用率则可能达到100%

这也是大家普遍认为实时系统中数据吞吐量不足的缘故，系统开销消耗在了线程切换上 (如本章前面所介绍的，有些实时系统甚至会采用底半处理，分级的中断处理方式，相当于又拉长了中断到发送线程的时间开销，效率会进一步下降)。

发送数据量越小，发送速度越快，对于数据吞吐量的影响也将越大。归根结底，取决于系统中产生中断的频度如何。当一个实时系统想要提升数据吞吐量时，可以考虑以下几种方式：(1)增加每次数据量发送的长度，每次让外设尽量多地发送数据；(2)必要情况下更改中断模式为轮询模式。同时，为了解决轮询方式一直抢占处理机, 其他低优先级线程得不到运行的情况，可以把轮询线程的优先级适当降低。

# 内核移植
能够具备线程管理和调度、内存管理、线程间同步和通信、定时器管理等功能
移植可分为 CPU 架构移植和 BSP（BoardSupportPackage, 板级支持包）移植两种。
## CPU 架构移植 

为了使 RT-Thread 能够在不同 CPU 架构的芯片上运行，RT-Thread 提供了一个 **libcpu 抽象层来适配不同的 CPU 架构**。libcpu 层向上对内核提供统一的接口，**包括全局中断的开关、线程栈的初始化、上下文切换等。**
RT-Thread 的 **libcpu 抽象层向下提供了一套统一的 CPU 架构移植接口**，这部分接口包含全局中断开关函数、线程上下文切换函数、时钟节拍的配置和中断函数、Cache 等内容。
表 10-1 是-CPU 架构移植需要实现的接口和变量
![[Pasted image 20240508113252.png]]
![[Pasted image 20240508142319.png]]
### 实现全局中断开关
下面介绍在 Cortex・M 架构上如何实现这两个函数
Cortex・M 为了快速开关中断，实现了 CPS 指令，可以用在此处。![[Pasted image 20240508113427.png]]
1.关闭全局中断
在 rt_hw_interrupt_disable ()函数中需要依序完成的功能是：
(1 )保存当前的全局中断状态，并把状态作为函数的返回值。 (2)关闭全局中断。
![[Pasted image 20240508113549.png]]
最后使用 BX 指令返回。r 0 中存储的数据就是函数的返回值
**关于寄存器在函数调用时和在中断处理程序里是如何管理的**，不同的 CPU 架构有不同的约定。在 ARM 官方手册《ProcedureCallStandardfortheARM®Architecture》里可以找到关于 Cortex-M 对寄存器使用的约定的更详细介绍。

2. 打开全局中断
Cortex-M 内核上的实现打开全局中断
![[Pasted image 20240508113757.png]]
首先使用 MSR 指令将 r 0 的值寄存器写入 PRIMASK 寄存器，从而恢复之前的中断状态。
### 实现线程栈初始化
在动态创建线程和初始化线程的时候，会用到内部的线程初始化函数_rt_thread_init (), 该函数会调用栈初始化函数 rt_hw_stack_init (), 在栈初始化函数中会手动构造一个上下文内容，这个上下文内容将作为每个线程第一次执行的初始值
![[Pasted image 20240508132638.png]]
![[Pasted image 20240508132714.png]]
![[Pasted image 20240508132730.png]]
### 实现上下文切换
**在 Cortex-M 中上下文切换都是统一使用 PendSV 异常来完成**
**但是为了能适应不同的 CPU 架构，RT-Thread 的 libcpu 抽象层还是需要实现三个线程切换相关的函数**

在线程环境下，如果调用 rt_hw_context_switch。函数，那么可以马上进行上下文切换；而在中断环境下，需要等待中断处理函数完成之后才能进行切换。由于这种差异，在 ARM 9 等平台，rt_hw_context_switch ()和 rt_hw_context_switch_ interrupt。的实现并不一样

在中断处理程序里如果触发了线程的调度，调度函数中会调用 **==rt_hw_context_switch_interrupt ()触发上下文切换。中断处理程序里处理完中断事务之后，中断退出之前，检查 rt_thread_switch_interrupt_flag 变量**，如果**该变量的值为 1, 就根据 rt_interrupt_from_thread 变量和 rt_interrupt_to_thread 变量，完成线程的上下文切换。**==

在 Cortex-M 处理器架构里，基于**自动部分压栈**和 PendSV 的特性，上下文切换可以实现得更加简洁。



线程之间的上下文切换
![[Pasted image 20240508133228.png]]
硬件在进入 PendSV 中断之前自动保存了 from 线程的 PSR、PC、LR、R 12、R 3~R 0 寄存器，
然后 **PendSV 里保存 from 线程的 R 11〜R 4 寄存器**，以及恢复 to 线程的 R 4〜RI 11 寄存器，
最后硬件在退出 PendSV 中断之后，自动恢复 to 线程的 R 0〜R 3、R12、LR、PC、PSR 寄存器。

中断到线程的上下文切换
![[Pasted image 20240508133306.png]]
硬件在进入中断之前自动保存了 from 线程的 PSR、PC、LR、R 12、R 3〜R 0 寄存器, 
然后 **PendSV 里保存 from 线程的 R 11〜R 4 寄存器**，以及恢复 to 线程的 R 4〜R11 寄存器，
最后硬件在退出 PendSV 中断之后，自动恢复 to 线程的 R 0〜R 3、R 12、LR、PC、 PSR 寄存器。

在 Cortex-M 内核中 rt_hw_context_switch ()和 rt_hw_context_switch_interrupt ()功能一致，即都是在 PendSV 中完成剩余上下文的保存和回复。所以我们仅仅需要夔现一段代码，简化移植的工作。
####     实现 rt_hw_context_switch_to ()
![[Pasted image 20240508142345.png]]
这个函数实现切换到指定线程的功能

![[Pasted image 20240508142606.png]]
![[Pasted image 20240508142622.png]]
#### .实现 rt_hw_context_switch ()和 rt_hw_context_switch_interrupt 

![[Pasted image 20240508142402.png]]
![[Pasted image 20240508142700.png]]
![[Pasted image 20240508142716.png]]
#### 实现 PendSV 中断
完成线程切换的实际工作
![[Pasted image 20240508142820.png]]
![[Pasted image 20240508142926.png]]
![[Pasted image 20240508142941.png]]
### 实现时钟节拍
## BSP 移植
其主要任务是建立让操作系统运行的基本环境，需要完成的主要工作是：
(1 )初始化 CPU 内部寄存器，设定 RAM 工作时序。 
(2)实现时钟驱动及中断控制器驱动，完善中断管理。 
(3 )实现串口和 GPIO 驱动。
(4)初始化动态内存堆，实现动态内存堆管理。
## 内核移植示例
# 1 组件 
# I/O 设备管理
## I/O 设备介绍
### I/O 设备管理框架
I/O 设备管理框架
从上到下分别是 ==**I/O 设备管理层、设备驱动框架层、设备驱动层**==
![[Pasted image 20240429102140.png]]
应用程序通过 I/O 设备管理接口获得正确的设备驱动 .I/O 设备管理层实现了对设备驱动程序的封装
设备驱动框架层是对同类硬件设备驱动的抽象，它将不同厂家的同类硬件设备驱动中相同的部分抽取出来


设备驱动层:==对于操作逻辑简单的设备，可以不经过设备驱动框架层，直接将设备注册到 I/O 设备管理器中==
序列图如图 13-2 所示
(1)设备驱动根据设备模型定义，**创建出具备硬件访问能力的设备实例**，将该设备通过 rt_device_register ()接口**注册到** I/O 设备管理器中。
(2)应用程序通过 rt_device_find ()接口查找到设备，然后使用 I/O 设备管理接口来访问硬件。
![[Pasted image 20240429102640.png]]
> ==序列图用于表示多层体系的层次关系，即上层方法的底层实现和下层传递到上传上层==

对于另一些设备，如看门狗等，则会将创建的设备实例先注册到对应的设备驱动框架中，再由设备驱动框架向 I/O 设备管理器进行注册
(2)看门狗设备驱动框架通过 rt_device_register ()接口将看门狗**设备注册到** I/O 设备管理器中。
(3)**应用程序通过 I/O 设备管理接口**来访问看门狗设备硬件。
![[Pasted image 20240429102726.png]]
### I/O 设备模型
RT-Thread 的==设备模型是建立在内核对象模型基础之上==
![[Pasted image 20240429103012.png]]
**设备对象的定义**
![[Pasted image 20240614164729.png]]
### I/O 设备类型
![[Pasted image 20240429111628.png]]
其中字符设备、块设备是常用的设备类型
字符模式设备允许非结构的数据传输，即通常数据传输采用串行的形式, 每次一个字节。字符设备通常是一些简单设备，如串口、按键。
块设备每次传输一个数据块，例如每次传输 512 个字节数据。这个数据块是硬件强制性的，数据块要使用某类数据接口或某些强制性的传输协议
当系统服务于一个具有大量数据的写操作时，设备驱动程序必须首先将数据划分为多个包。每个包采用设备指定的数据尺寸。


而在实际过程中，最后一部分数据尺寸有可能小于正常的设备块尺寸
通常情况下，设备驱动程序需要首先执行相对应的设备块的读操作，然后把写入数据覆盖到读出数据上，然后再把这个合成的数据块作为一整个块写回到设备中
例如图 13-5 中的块 4, 驱动程序需要先把块 4 所对应的设备块读出来，然后将需要写入的数据覆盖至从设备块读出的数据上，使其合并成一个新的块，最后再写回到块设备中。
![[Pasted image 20240429143852.png]]
## 操作
### 创建和注册 IO 设备
**驱动层负责创建设备实例，并注册到 I/O 设备管理器中，可以通过==静态声明的方式创建==设备实例**，
**也可以用如下接口进行动态创建**
![[Pasted image 20240614182023.png]]



**设备被创建后，==需要实现它访问硬件的操作方法==**，操作方法原型如下所示：
![[Pasted image 20240614164930.png]]
![[Pasted image 20240614164941.png]]



当一个动态创建的设备不需要再使用时，可以通过如下的函数来销毁
![[Pasted image 20240429103516.png]]



**设备被创建后，需要注册到 I/O 设备管理器中**，**应用程序才能够访问**，注册设备的函数如下所示
![[Pasted image 20240614165037.png]]
#### 实例
##### 看门狗 
**要注册**
![[Pasted image 20240614170415.png]]
![[Pasted image 20240614170427.png]]

##### iic
![[Pasted image 20240614170635.png]]
不一样????
### 访问 io 设备 
==应用程序通过 i/o 设备管理接口来访问硬件设备==
I/O 设备管理接口与 I/O 设备的操作方法的映射关系如图 13-6所示。
![[Pasted image 20240429103743.png]]
#### 查找
**应用程序根据设备名称获取设备句柄**
![[Pasted image 20240429103816.png]]
#### 初始化设备
![[Pasted image 20240429103827.png]]
#### 打开和关闭设备 
**打开设备时，会检测设备是否已经初始化，没有初始化则会默认调用初始化接口初始化设备**
![[Pasted image 20240429103837.png]]
oflags 支持以下参数
![[Pasted image 20240429103917.png]]
![[Pasted image 20240429103929.png]]
> 如果上层应用程序需要设置设备的接收回调函数，则必须以 RT_DEVICE_FLAG_ INT RX 或者 RT DEVICE FLAG DMA RX 的方式打开设备，否则不会回调函数。


应用程序打开设备并完成读写等操作后，如果不需要再对设备进行操作则可以关闭设备
![[Pasted image 20240429104041.png]]
#### 控制设备
![[Pasted image 20240429104106.png]]
参数 cmd 的通用设备命令可取如下宏定义:
![[Pasted image 20240429104116.png]]

#### 读写设备
![[Pasted image 20240429104222.png]]
“pos 读取数据偏移量根据不同的设备类别有不同的意义”
![[Pasted image 20240429110308.png]]
#### 数据收发回调
“当硬件设备收到数据时，可以通过如下函数回调另一个函数来设置数据接收指示，通知上层应用线程有数据到达
![[Pasted image 20240429104430.png]]
该函数的**回调函数由调用者提供**。**当硬件设备接收到数据时，会回调这个函数并把收到的数据长度放在 size 参数中传递给上层应用。上层应用线程应在收到指示后，立刻从设备中读取数据。**

在应用程序**调用 rt_device_write ()写入数据时，如果底层硬件能够支持自动发送，那么上层应用可以设置一个回调函数。这个回调函数会在底层硬件数据发送完成后** (例如 DMA 传送完成或 FIFO 已经写入完毕产生中断时)**调用**。可以通过如下函数设置设备发送完成指示
![[Pasted image 20240429111257.png]]
调用该函数时，回调函数由调用者提供，**当硬件设备发送完数据时，由驱动程序回调这个函数并把发送完成的数据块地址 buffer 作为参数传递给上层应用。上层应用 (线程)在收到指示时会根据发送 buffer 的情况，释放 buffer 内存块或将其作为下一个写数据的缓存。**
#### 设备访问示例
应用程序访问设备的示例
首先通过 rt_device_find ()接口查找看门狗设备，获得设备句柄，然后通过 rt_device_init ()接口初始化设备，通过 rt_device_control ()接口设置看门狗设备溢出时间。
![[Pasted image 20240614182200.png]]
![[Pasted image 20240429141613.png]]
> 这里没有打开设备？
# 通用外设
，现在许多芯片在制造时已经能够将部分接口电路和总线集成到 MCU 内部，如 UART 总线、SPI 总线、12 c 总线、GPIO 等, 这类用于与外部设备连接的接口电路和总线称为片内外设。
RT-Thread 对常用的片内外设做了抽象，为同一类外设提供了通用接口，对于不同 MCU 的片内外设，都可以使用同一套外设接口进行访问
## UART
通用的串行数据总线，异步收发传输器
UART 串口通信有 4 个重要的参数，分别是波特率、数据位、停止位和奇偶检验位
UART 串口传输的数据格式为：1 个起始位、1〜8 个数据位、1 个奇/偶/非极性位、 1〜2 个结束位。没有检验位也可以
![[Pasted image 20240429111746.png]]
### 串口设备管理
在 RT-Thread 中，应用程序可通过通用 I/O 设备管理接口来访问串口硬件
可以按照轮询、中断或 DMA 等方式进行串口数据收发，也可以设置串口的波特率、数据位等。
**串口设备驱动框架中定义了串口的设备模型**，**它从设备对象派生而来**
![[Pasted image 20240429132251.png]]
“串口设备使用序列如图14-2所示，主要有以下几点：
![[Pasted image 20240429132029.png]]
### 创建和注册串口设备
“串口设备驱动程序负责根据串口模型定义来创建和注册串口设备。”
**创建串口设备主要是**实现串口设备 structrt_serial_device 的数据结构定义，也就是实例化串口设备，
并实现串口设备的操作方法 struct rt_uart_ops
![[Pasted image 20240429113024.png]]
![[Pasted image 20240429135746.png]]
串口设备被创建后，使用如下接口**注册到串口设备驱动框架**中
![[Pasted image 20240429113045.png]]
串口设备一般配置为可读写和中断接收的模式，注册串口设备时参数 flag 取值为 RT_ DEVICE_FLAG_RDWR 或 RT_DEVICE_FLAG_INT_RX 
### 访问串口设备
==应用程序通过 I/O 设备管理接口来访问串口硬件==
图 14-3 所示为使用 I/O 设备管理接口操作串口设备的函数调用层次关系
应用程序使用 rt_device_read ()接口读取串口设备接收到的数据，首先会使用串口设备驱动框架的操作方法 rt_serial_read (), **最终会使用串口设备驱动提供的串口设备的操作方法 getc ()接口，如果使用 DMA 模式收发数据**，则会调用 dma_transmit()接口。
![[Pasted image 20240429135935.png]]
### 示例
![[Pasted image 20240429141800.png]]
![[Pasted image 20240429141819.png]]
![[Pasted image 20240429141846.png]]
> 应用层只是调用 rt_device, 本节都是底层包装的实现

## GPIO
芯片上的引脚一般分为 4 类：电源、时钟、控制与 I/O
I/O 口在使用模式上又分为通用输出输出 (简称 GPIO)与功能复用 I/O (如 SPI、I 2 C、 UART 等)。

通用 I/O 口主要特性如下：
(1）可编程控制中断。中断触发模式可配置，一般有图 14-4 所示的 5 种中断触发模式。
(2)**输入输出模式可控制**。**输出模式**一般包括推挽、开漏、上拉、下拉，**输入模式**一般包括浮空、上拉、下拉、模拟。
### pin 设备管理 
**应用程序可通过 PIN 设备接口来操作 GPIO** ,如设置引脚模式和输出电平、读取引脚输入电平、配置引脚外部中断等。

==PIN 设备驱动框架中定义了 PIN 设备模型，它从设备对象派生而来==
![[Pasted image 20240429142329.png]]

PIN 设备使用序列如
![[Pasted image 20240429142354.png]]
### 创建和注册 pin 设备 
pin 设备驱动程序负责根据 pin 设备模型定义来创建和注册 pin 设备。
**创建 PIN 设备**主要是实现 PIN 设备 struct rt_device_pin 的数据结构定义，并实现 PIN 设备的操作方法 struct rt_pin_ops, 也就是实例化 PIN 设备。
![[Pasted image 20240429142613.png]]
PIN 设备的操作方法描述如表 14-3 所示。
![[Pasted image 20240429142629.png]]
PIN 设备被创建后，使用如下接口**注册到 PIN 设备驱动框架中**
![](../fujian/Pasted%20image%2020250719131844.png)
### 访问
==**应用程序通过 PIN 设备接口来访问 GPIO 引脚**==，图 14-6 所示为使用 PIN 设备接口的函数调用层次关系。
![[Pasted image 20240429142802.png]]
#### 绑定引脚中断回调函数
将某个引脚配置为某种中断触发模式并绑定一个中断回调函数到对应引脚，当引脚中断发生时，就会执行回调函数
![[Pasted image 20240429143204.png]]
#### 使能引脚中断
![[Pasted image 20240429143300.png]]
#### 脱离引脚中断函数
![[Pasted image 20240429143324.png]]
### 示例 
![[Pasted image 20240429143418.png]]
![[Pasted image 20240429143440.png]]
## spi
SPI (SerialPeripheralInterface, 串行外设接口)是一种高速、全双工、同步通信总线, 常用于短距离通信，主要应用于 EEPROM、FLASH、实时时钟、AD 转换器以及数字信号处理器和数字信号解码器之间
SPI 一般使用 4 根线通信

SPI 以主从方式工作，通常有一个主设备和一个或多个从设备。通信由主设备发起

从设备的时钟由主设备通过 SCLK 提供
SPI 的工作时序模式由 CPOL (ClockPolarity, 时钟极性)和 CPHA (ClockPhase, 时钟相位)之间的相位关系决定，

CPOL 表示时钟信号的初始电平的状态：CPOL 为 0表示时钟信号初始状态为低电平，CPOL 为 1 表示时钟信号的初始电平是高电平
CPHA 表示在哪个时钟沿采样数据：CPHA 为 0 表示在首个时钟变化沿采样数据，而 CPHA 为 1 则表示在第二个时钟变化沿采样数据
**根据 CPOL 和 CPHA 的不同组合共有 4 种工作时序模式**
![[Pasted image 20240613162250.png]]
### spi 设备管理 
在 RT-Thread 中，将 SPI 控制器抽象成 SPI 总线设备
并且提供了一组 SPI 设备接口来访问 SPI 从设备器件

**SPI 设备驱动框架中定义了 SPI 总线设备模型和从设备模型，它们从设备对象派生而来**

SPI **总线设备模型定义**如下面的代码所示。
SPI **从设备模型定义**如下面的代码所示:
![[Pasted image 20240613163124.png]]
==SPI 设备使用序列如图 14-10 所示==
![[Pasted image 20240613164044.png]]
### 创建和注册 spi 总线设备 
**==SPI 总线设备驱动程序负责==**根据 SPi 总线设备模型定义来创建和注册 SPI 总线设备。

**创建 SPI 总线设备**主要是实现 SPI 总线设备 struct rt_spi_bus 的数据结构定义，并实现操作方法 struct rt_spi_ops, 也就是**实例化 SPI 总线设备**。
![[Pasted image 20240613163343.png]]
![[Pasted image 20240613163353.png]]
**SPI 总线设备被创建后，使用如下接口注册到 SPI 设备驱动框架中**，函数参数及返回值见表 14-12
![[Pasted image 20240613163442.png]]
![[Pasted image 20240613163453.png]]
### 创建和挂载 spi 从设备 
SPI 总线用**于操作 SPI 从设备器件**，比如 SPIFlash 等。
==SPI 从机驱动程序负责==根据 SPI 从设备模型定义来创建 SPI 从设备，将从设备挂载到 SPI 总线设备上，并对从设备进行配置。

创建 SPI 从设备主要是实现 SPI 从设备 struct  rt_spi_device 的数据结构定义，然后使用 rt_spi_bus_attach_device ()接口将 **SPI 从设备挂载到 SPI 总线设备上**
![[Pasted image 20240613164637.png]]
![[Pasted image 20240613164700.png]]



为满足不同 SPI 从设备的时钟、数据宽度等要求，通常需要配置 SPI 模式、频率参数。SPI 从设备的模式决定主设备的模式，所以 SPI 主设备的模式必须和从设备一样两者才能正常通信, 可以使用 rt_spi_configure 接口**设置 SPI 从设备的相关参数**
![[Pasted image 20240613164851.png]]
![[Pasted image 20240613164858.png]]




配置参数的结构体 struct rt spi configuration 原型如下。
![[Pasted image 20240613164920.png]]


配置 SPI 从设备的示例代码如下所示：
### 访问 spi 从设备 
SPI 从设备被成功挂载和配置后，就可以使用 SPI 设备接口来访问 SPI 从机器件了

图 14-11 所示为 SPI 设备接口的调用层次关系，SPI **从设备驱动**使用 **SPI 设备接口**，会调**用到 SPI 总线设备驱动提供的操作方法**，最终访问 SPI 从设备硬件。
![[Pasted image 20240613165605.png]]
#### 自定义传输 
![[Pasted image 20240614081051.png]]
![[Pasted image 20240614081057.png]]
此函数可以传输一连串消息，用户可以**自定义每个待传输的 message 结构体各参数的数值，从而可以很方便地控制数据传输方式**。
struct rt_spi_message 原型如下：
![[Pasted image 20240614081139.png]]
![[Pasted image 20240614081150.png]]
send_buf 为发送缓冲区指针，其值为 RT_NULL 时，表示本次传输为**只接收状态**，不需要发送数据。
recv_buf 为接收缓冲区指针，其值为 RT_NULL 时，表示本次传输为**只发送状态**，不需要保存接收到的数据，所以收到的数据直接丢弃。
length 的单位为 word, 即数据长度为 8 位时，每个 length 占用 1 个字节；当数据长度为 16 位时，每个 length 占用 2 个字节。
**参数 next 是指向继续发送的下一条消息的指针，若只发送一条消息，则此指针值为 RT_NULL** 。多个待传输的消息通过 next 指针以单向链表的形式连接在一起。cs_take 值为 1 时，表示在传输数据前，设置对应的 CS 为有效状态。cs_release 值为 1时，表示在数据传输结束后，释放对应的 CS。
> 注意：当 send_buf 或 recv_buf 不为空时，两者的可用空间都不得小于 length。若使用此函数传输消息，**传输的第一条消息 cs_take 需置为 1, 设置片选为有效，最后一条消息的 cs_release 需置为1,释放片选。**
#### 传输一次
如果只传输一次数据可以使用如下函数
![[Pasted image 20240614081622.png]]
等同于
![[Pasted image 20240614081934.png]]
![[Pasted image 20240614081941.png]]
#### 发送一次
![[Pasted image 20240614081850.png]]
此函数**等同于调用 rt_spi_transfer_ message ()传输一条消息，开始发送数据时片选选中，函数返回时释放片选， message 参数配置如下**
![[Pasted image 20240614081920.png]]
#### 接受一次 
![[Pasted image 20240614081721.png]]
#### 连续两次发送
如果需要先后连续发送 2 个缓冲区的数据，并且中间片选不释放
![[Pasted image 20240614082022.png]]
本函数适合向 SPI 从设备中写入一块数据，第一次先发送命令和地址等数据，第二次再发送指定长度的数据。
**之所以分两次发送而不是合并成一个数据块发送或调用两次 rt_spi_send ()**,是因为在大部分的数据写操作中，都需要先发命令和地址，长度一般只有几个字节。如果与后面的数据合并在一起发送，将需要进行内存空间申请和大量的数据搬运。
而如果**调用两次 rt_spi_send (), 那么在发送完命令和地址后，片选会被释放，大部分 SPI 从设备都依靠设置片选一次有效为命令的起始, 所以片选在发送完命令或地址数据后被释放，则此次操作被丢弃。**

此函数等同于调用 rt_spi_transfer_message ()传输 2 条消息，message 参数配置如下：
![[Pasted image 20240614082520.png]]
![[Pasted image 20240614082525.png]]
#### 先发送后接收
如果需要向从设备先发送数据，然后接收从设备发送的数据，并且中间片选不释放，
![[Pasted image 20240614082544.png]]
**本函数适合从 SPI 从设备中读取一块数据，第一次会先发送一些命令和地址数据，然后再接收指定长度的数据。**
此函数等同于调用 rt_spi_transfer_message。传输 2 条消息，message 参数配置如下：
![[Pasted image 20240614082552.png]]

SPI 设备管理模块还提供 rt_spi_sendrecv 8 ()和 rtspisendrecv 16 ()函数，这两个函数都是对此函数的封装，rt_spi_sendrecv 8 ()发送一个字节数据的同时收到一个字节数据，rt_spi_sendrecvl 6 ()发送 2 个字节数据的同时收到 2 个字节数据。
### 特殊使用场景 
在一些特殊的使用场景，**某个设备希望独占总线一段时间，且期间要保持片选一直有效, 期间数据传输可能是间断的，则可以按照如所示步骤使用相关接口**
传输数据函数**必须使用 rt_spi_transfer_message ()**，并且此函数每个待传输消息的片选控制域 **cs_take 和 cs_release 都要设置为 0 值，因为片选已经使用了其他接口控制，不需要在数据传输的时候控制。**
#### 获取总线 
在**多线程**的情况下，可能会在不同的线程中使用同一个 SPI 总线，为**了防止 SPI 总线正在传输的数据丢失，从设备在开始传输数据前需要先获取 SPI 总线的使用权**，获取成功才能够使用总线传输数据
![[Pasted image 20240614083035.png]]
#### 选中片选 
从设备**获取总线的使用权后，需要设置自己对应的片选信号为有效**，可使用如下函数选中片选
![[Pasted image 20240614083117.png]]
#### 增加一条信息
使用 rt_spi_transfer_message ()传输消息时，所有**待传输的消息都是以单向链表的形式连接起来的，可使用如下函数往消息链表里增加一条新的待传输消息**
![[Pasted image 20240614083154.png]]
![[Pasted image 20240614083212.png]]
#### 释放片选 
![[Pasted image 20240614083223.png]]
#### 释放总线 
![[Pasted image 20240614083230.png]]

### spi 设备使用示例 

![[Pasted image 20240614083958.png]]
![[Pasted image 20240614084010.png]]
## i 2 c 总线
12 c 总线传输数据时只需两根信号线，一根是双向数据线 SDA (serialdata), 另一根是双向时钟线 SCL (serialclock)

12 c 和 SPI 一样以**主从的方式**工作，**不同于 SPI 一主多从的结构，它允许同时有多个主设备存在**，每个连接到总线上的**器件都有唯一的地址**，
**主设备启动数据传输并产生时钟信号，从设备被主设备寻址，同一时刻只允许有一个主设备。**

I 2 C 总线主要的数据传输格式如图 14-13 所示。
![[Pasted image 20240614084310.png]]
当总线**空闲时，SDA 和 SCL 都处于高电平状态**，
当主机要和某个从机通信时，会先发送一个开始条件，然后发送从机地址和读写控制位，接下来传输数据 (主机发送或者接收数据)，数据传输结束时主机会发送停止条件传输的每个字节为 8 位，**高位在前，低位在后。**
(1)开始条件：**SCL 为高电平时，主机将 SDA 拉低**，寿示数据传输即将开始。
(2)从机地址：
![[Pasted image 20240614084752.png]]
(3)应答信号：每传输完成**一个字节的数据，接收方就需要回复一个 ACK** (acknowledge) o 写数据时由从机发送 ACK, 读数据时由主机发送 ACK。当**主机读到最后一个字节数据时，可发送 NACK** (NegativeAcknowledgement), 然后**跟停止条件。**
(5)重复开始条件：在一次通信过程中, **主机可能需要和不同的从机传输数据或者需要切换读写操作时，主机可以再发送一个开始条件**。
(6)停止条件：**在 SDA 为低电平时，主机将 SCL 拉高并保持高电平，然后再将 SDA 拉高**，表示传输结束。
### i 2c 设备管理  
在 RT-Thread 中，**12 c 从机驱动通过 12 c 设备接口来访问 12 c 从设备器件**，12 c 设备设备驱动框架中定义了 12 c 总线设备模型，它从设备对象派生而来
![[Pasted image 20240614084921.png]]
**12 c 设备使用序列**如图 14-15 所示
![[Pasted image 20240614084940.png]]
### 创建和注册 i2 c 总线设备
### 访问 i 2c 设备
### i 2c 设备应用实例
## 运行设备应用实例

## 总结
io设备管理及通用外设的框架r10没有使用 
==**框架做的是把底层的操作接口绑定到上层的函数指针而已**==

# 网络框架 
## RT-Thread网络框架介绍
T-Thread为了能够支持各种网络协议栈, 开发了SAL组件, 全称为SocketAbstractionLayer, 即套接字抽象层, RT-Thread通过它可以无缝接入各类协议栈, 包括几种常用的TCP/IP协议栈, 例如嵌入式开发中常用的LwIP协议栈

网络框架向用户应用程序提供标准BSD Socket接口, 开发者使用BSD Socket接口进行操作, 无须关心网络底层如何实现, 也无须关心网络数据通过的是哪个网络协议栈, 套接字抽象层为上层应用层提供的接口有accept、connect、send、recv等。
![](../fujian/Pasted%20image%2020250719134110.png)

将复杂的设备通信方式转换成简单的串口编程, 大大简化了产品的硬件设计和软件开发成本, 这使得几乎所有的网络模组如GPRS、3G/4G、NB-IoT, 蓝牙、WiFi、GPS等模组都很方便地接入RT-Thread网络框架

总体来说, RT-Thread网络框架使开发者只需要关心和使用标准BSD Socket网络接口进行网络应用开发, 而无须关心底层具体网络协议栈类型和实现
## 网络框架工作流程
使用RT-Thread网络框架, 首先需要初始化SAL, 然后注册各类网络协议簇, 确保应用程序能够使用socket网络套接字接口进行通信

### 网络协议簇注册
首先使用sal_init () 接口对组件中使用的互斥锁等资源进行初始化
	![](../fujian/Pasted%20image%2020250719134301.png)
SAL初始化后, 通过sal_proto_family_register () 接口来注册网络协议簇, 将LwIP网络协议簇注册到SAL中
	![](../fujian/Pasted%20image%2020250719134319.png)
	![](../fujian/Pasted%20image%2020250719134328.png)
	
### 网络数据接收流程
==LwIP注册到SAL之后==, 应用程序可通过网络套接字接口进行网络数据收发
在LwIP中，创建了几个主要线程，分别是tcpip线程、erx接收线程和etx发送线程，
网络数据接收流程如图16-3所示
![](../fujian/Pasted%20image%2020250719134821.png)
### 网络数据发送流程
![](../fujian/Pasted%20image%2020250719134842.png)
## 网络套接字编程
使得应用程序无须关注协议本身，直接使用socket提供的接口来进行互联以实现不同主机间的通信
### TCP socket 通信流程
![](../fujian/Pasted%20image%2020250719142224.png)
### 创建套接字
在进行通信前, 通信双方首先使用socket。接口创建套接字, 根据指定的地址族、数据类型和协议来分配一个套接字描述符及其所用的资源
![](../fujian/Pasted%20image%2020250719134955.png)
### 绑定套接字
绑定套接字用于将端口号和IP地址绑定到指定套接字上。当使用socket。创建一个套接字时, 只是给定了协议族, 并没有分配地址, 在套接字接收来自其他主机的连接前, 必须用bind。给它绑定一个地址和端口号
![](../fujian/Pasted%20image%2020250719135027.png)
### 建立TCP连接
对于服务器端程序, 使用bind。绑定套接字后, 还需要使用listen。函数让套接字进入被动监听状态, 再调用accept。函数, 就可以随时响应客户端的请求了。
### 数据传输
TCP需要建立连接后才能进行数据传输, 使用  send () 函数进行数据发送, 使用recv函数进行数据接收, 而UDP则不需要建立连接, 使用  sendto () 函数进行数据发送, 使用recvfromO函数进行数据接收。

### 关闭网络连接
