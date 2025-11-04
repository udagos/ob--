---
up:
  - "[[../moc/mocwork]]"
---
```
---
tags: 
---
```
## rt_hw_vector_init
```
static void rt_hw_vector_init(void)
{
    int sctrl;
    unsigned int *src = (unsigned int *)&system_vectors;
  

    /* C12-C0 is only active when SCTLR.V = 0 */
    asm volatile ("mrc p15, #0, %0, c1, c0, #0"
                  :"=r" (sctrl));
    sctrl &= ~(1 << 13);
    asm volatile ("mcr p15, #0, %0, c1, c0, #0"
                  :
                  :"r" (sctrl));


    asm volatile ("mcr p15, #0, %0, c12, c0, #0"
                  :
                  :"r" (src));
}
```

这段代码是一个初始化硬件向量表的函数，通常用于嵌入式系统或实时操作系统（RTOS）中，以设置异常和中断向量表。以下是对这段代码的详细解释：

### 函数定义
```c
static void rt_hw_vector_init(void)
{
    int sctrl;
    unsigned int *src = (unsigned int *)&system_vectors;
```
- 定义了一个静态函数 `rt_hw_vector_init`，该函数没有参数，也不返回任何值。
- 定义了一个整型变量 `sctrl`，用于存储从协处理器读取的值。
- 定义了一个指向无符号整型的指针 `src`，它指向 `system_vectors` 的地址。`system_vectors` 是一个数组，包含了异常和中断处理程序的地址。

### 修改SCTLR寄存器
```c
    /* C12-C0 is only active when SCTLR.V = 0 */
    asm volatile ("mrc p15, #0, %0, c1, c0, #0"
                  :"=r" (sctrl));
    sctrl &= ~(1 << 13);
    asm volatile ("mcr p15, #0, %0, c1, c0, #0"
                  :
                  :"r" (sctrl));
```
- 使用内联汇编读取SCTLR寄存器的值。SCTLR寄存器控制处理器的各种功能，如缓存、分支预测等。
- 清除SCTLR寄存器的第13位（即禁用C12-C0），因为C12-C0只有在SCTLR. V = 0时才有效。
- 将修改后的值写回SCTLR寄存器。

### 设置向量表
```c
    asm volatile ("mcr p15, #0, %0, c12, c0, #0"
                  :
                  :"r" (src));
```
- 使用内联汇编将 `src` 指向的地址写入C12寄存器。C12寄存器用于设置向量表的基地址。
- 这行代码将 `system_vectors` 的地址设置为向量表的基地址，从而初始化异常和中断向量表。

### 总结
这段代码的主要目的是初始化硬件向量表，通过修改SCTLR寄存器和设置C12寄存器来完成。这是在嵌入式系统或RTOS中常见的操作，用于配置处理器的异常和中断处理机制。通过这种方式，系统可以在发生异常或中断时跳转到正确的处理程序。



这段代码是一个初始化ARM Generic Interrupt Controller (GIC) 分布器的函数。GIC是ARM架构中用于处理中断和异常的硬件组件。以下是对这段代码的详细解释：
## arm_gic_dist_init
```
int arm_gic_dist_init(rt_uint32_t index, rt_uint32_t dist_base, int irq_start)

{

    unsigned int max_irq, i;

    rt_uint32_t cpumask = 1 << 0;

  

    RT_ASSERT(index < ARM_GIC_MAX_NR);

  

    _gic_table[index].dist_hw_base = dist_base;

    _gic_table[index].offset = irq_start;

  

#ifndef RT_PRETENT_AS_CPU0

    /* If we are run on the second core, the GIC should have already been setup

     * by BootStrapProcessor. */

    if ((rt_cpu_get_smp_id() & 0xF) != 0)

        return 0;

#endif

  

    cpumask |= cpumask << 8;

    cpumask |= cpumask << 16;

  

    GIC_DIST_CTRL(dist_base) = 0x0;

  

    /* Find out how many interrupts are supported. */

    max_irq = GIC_DIST_CTR(dist_base) & 0x1f;

    max_irq = (max_irq + 1) * 32;

  

    /*

     * The GIC only supports up to 1020 interrupt sources.

     * Limit this to either the architected maximum, or the

     * platform maximum.

     */

    if (max_irq > 1020)

        max_irq = 1020;

    if (max_irq > ARM_GIC_NR_IRQS)

        max_irq = ARM_GIC_NR_IRQS;

  

    /* Set all global interrupts to be level triggered, active low. */

    for (i = 32; i < max_irq; i += 16)

        GIC_DIST_CONFIG(dist_base, i) = 0x0;

  

    /* Set all global interrupts to this CPU only. */

    for (i = 32; i < max_irq; i += 4)

        GIC_DIST_TARGET(dist_base, i) = cpumask;

  

    /* Set priority on all interrupts. */

    for (i = 0; i < max_irq; i += 4)

        GIC_DIST_PRI(dist_base, i) = 0xa0a0a0a0;

  

    /* Disable all interrupts. */

    for (i = 0; i < max_irq; i += 32)

        GIC_DIST_ENABLE_CLEAR(dist_base, i) = 0xffffffff;

  

    GIC_DIST_CTRL(dist_base) = 0x01;

  

    return 0;

}
```
### 函数定义
```c
int arm_gic_dist_init(rt_uint32_t index, rt_uint32_t dist_base, int irq_start)
```
- 定义了一个函数 `arm_gic_dist_init`，它接受三个参数：
  - `index`：GIC表的索引。
  - `dist_base`：GIC分布器的基地址。
  - `irq_start`：中断号的起始值。

### 变量定义
```c
    unsigned int max_irq, i;
    rt_uint32_t cpumask = 1 << 0;
```
- 定义了两个无符号整型变量 `max_irq` 和 `i`，用于循环计数和存储最大中断数。
- 定义了一个32位无符号整型变量 `cpumask`，并初始化为 `1 << 0`，表示CPU 0。

### 断言
```c
    RT_ASSERT(index < ARM_GIC_MAX_NR);
```
- 使用断言确保 `index` 在有效范围内。

### 设置GIC表
```c
    _gic_table[index].dist_hw_base = dist_base;
    _gic_table[index].offset = irq_start;
```
- 设置GIC表中对应索引的分布器硬件基地址和中断偏移量。

### 多核处理
```c
#ifndef RT_PRETENT_AS_CPU0
    if ((rt_cpu_get_smp_id() & 0xF) != 0)
        return 0;
#endif
```
- 如果定义了 `RT_PRETENT_AS_CPU0`，则跳过以下代码。否则，如果当前CPU不是CPU 0（通过 `rt_cpu_get_smp_id()` 获取），则返回0，表示不需要再次初始化GIC。

### 设置CPU掩码
```c
    cpumask |= cpumask << 8;
    cpumask |= cpumask << 16;
```
- 将 `cpumask` 扩展到所有CPU（假设最多8个CPU），以便所有CPU都能处理中断。

### 初始化GIC分布器
```c
    GIC_DIST_CTRL(dist_base) = 0x0;
```
- 禁用GIC分布器。

### 查找最大中断数
```c
    max_irq = GIC_DIST_CTR(dist_base) & 0x1f;
    max_irq = (max_irq + 1) * 32;
```
- 从GIC分布器的控制寄存器中读取最大中断数，并计算实际的中断数量。

### 限制最大中断数
```c
    if (max_irq > 1020)
        max_irq = 1020;
    if (max_irq > ARM_GIC_NR_IRQS)
        max_irq = ARM_GIC_NR_IRQS;
```
- 将最大中断数限制在1020或平台定义的最大值 `ARM_GIC_NR_IRQS` 之间。

### 设置中断触发类型和目标CPU
```c
    for (i = 32; i < max_irq; i += 16)
        GIC_DIST_CONFIG(dist_base, i) = 0x0;

    for (i = 32; i < max_irq; i += 4)
        GIC_DIST_TARGET(dist_base, i) = cpumask;
```
- 将所有全局中断设置为电平触发，低电平有效。
- 将所有全局中断设置为目标CPU（即所有CPU）。

### 设置中断优先级
```c
    for (i = 0; i < max_irq; i += 4)
        GIC_DIST_PRI(dist_base, i) = 0xa0a0a0a0;
```
- 为所有中断设置优先级（假设优先级为0xa0）。

### 禁用所有中断
```c
    for (i = 0; i < max_irq; i += 32)
        GIC_DIST_ENABLE_CLEAR(dist_base, i) = 0xffffffff;
```
- 禁用所有中断。

### 启用GIC分布器
```c
    GIC_DIST_CTRL(dist_base) = 0x01;
```
- 启用GIC分布器。

### 返回值
```c
    return 0;
```
- 函数返回0，表示初始化成功。

### 总结
这段代码初始化了ARM GIC分布器，设置了中断的触发类型、目标CPU、优先级，并禁用了所有中断。这是在多核系统中配置中断处理机制的重要步骤。

## arm_gic_cpu_init
```
int arm_gic_cpu_init(rt_uint32_t index, rt_uint32_t cpu_base)

{

    RT_ASSERT(index < ARM_GIC_MAX_NR);

  

    _gic_table[index].cpu_hw_base = cpu_base;

  

    GIC_CPU_PRIMASK(cpu_base) = 0xf0;

    /* Enable CPU interrupt */

    GIC_CPU_CTRL(cpu_base) = 0x01;

  

    return 0;

}
```
这段代码是一个初始化ARM Generic Interrupt Controller (GIC) CPU接口的函数。GIC是ARM架构中用于处理中断的硬件组件，它包含一个分布器（负责管理中断源）和一个或多个CPU接口（负责管理特定CPU上的中断）。以下是对这段代码的详细解释：

### 函数定义
```c
int arm_gic_cpu_init(rt_uint32_t index, rt_uint32_t cpu_base)
```
- 定义了一个函数 `arm_gic_cpu_init`，它接受两个参数：
  - `index`：GIC表的索引。
  - `cpu_base`：GIC CPU接口的基地址。

### 断言
```c
    RT_ASSERT(index < ARM_GIC_MAX_NR);
```
- 使用断言确保 `index` 在有效范围内，即不超过系统中GIC的最大数量。

### 设置GIC表
```c
    _gic_table[index].cpu_hw_base = cpu_base;
```
- 设置GIC表中对应索引的CPU接口硬件基地址。

### 设置中断屏蔽和使能
```c
    GIC_CPU_PRIMASK(cpu_base) = 0xf0;
```
- 设置CPU接口的中断屏蔽寄存器。这里将屏蔽寄存器设置为 `0xf0`，表示屏蔽所有中断，直到设置优先级低于这个值的中断才会被处理。

```c
    GIC_CPU_CTRL(cpu_base) = 0x01;
```
- 设置CPU接口的控制寄存器。这里将控制寄存器设置为 `0x01`，表示启用CPU接口，允许中断被处理。

### 返回值
```c
    return 0;
```
- 函数返回0，表示初始化成功。

### 总结
这段代码的主要目的是初始化GIC的CPU接口，设置中断屏蔽和使能。这是在配置中断处理机制时的重要步骤，确保CPU能够正确地响应和处理中断。通过设置中断屏蔽寄存器，可以控制哪些中断可以被CPU处理，而通过设置控制寄存器，可以启用或禁用CPU接口。

## 向量表 gic表
- **向量表**负责定义处理器异常的处理程序入口地址，当处理器遇到异常时，它会根据向量表中的地址跳转到相应的处理程序。
    
- **GIC表**负责管理GIC中断，包括中断的使能、禁用、优先级设置、目标CPU设置等。当处理器通过GIC接收到中断时，它会根据GIC表中的信息来处理中断。

## rt_components_board_init
```
void rt_components_board_init(void)
{
#ifndef _MSC_VER
#if RT_DEBUG_INIT
    int result;
    const struct rt_init_desc *desc;
    for (desc = &__rt_init_desc_rti_start; desc < &__rt_init_desc_rti_board_end; desc ++)
    {
        rt_kprintf("initialize %s", desc->fn_name);
        result = desc->fn();
        rt_kprintf(":%d done\n", result);
    }
#else
    const init_fn_t *fn_ptr;
  
    for (fn_ptr = &__rt_init_rti_start; fn_ptr < &__rt_init_rti_board_end; fn_ptr++)
    {
        (*fn_ptr)();
    }
#endif
#endif
}
```
这个函数的目的是初始化所有在板级初始化阶段需要配置的组件。以下是对这段代码的详细解释：

## 1
```
* initialization export */
#ifdef RT_USING_COMPONENTS_INIT
typedef int (*init_fn_t)(void);
#ifdef _MSC_VER /* we do not support MS VC++ compiler */
    #define INIT_EXPORT(fn, level)
#else
    #if RT_DEBUG_INIT
        struct rt_init_desc
        {
            const char* fn_name;
            const init_fn_t fn;
        };
        #define INIT_EXPORT(fn, level)          \
            const char __rti_##fn##_name[] = #fn; \
            const struct rt_init_desc __rt_init_desc_##fn SECTION(".rti_fn."level) = \
            { __rti_##fn##_name, fn};
    #else
        #define INIT_EXPORT(fn, level)  \
            const init_fn_t __rt_init_##fn SECTION(".rti_fn."level) = fn
    #endif
#endif
#else
#define INIT_EXPORT(fn, level)
#endif
  

/* board init routines will be called in board_init() function */
#define INIT_BOARD_EXPORT(fn)           INIT_EXPORT(fn, "0")
/* device/component/fs/app init routines will be called in init_thread */
/* device initialization */
#define INIT_DEVICE_EXPORT(fn)          INIT_EXPORT(fn, "2")
/* components initialization (dfs, lwip, ...) */
#define INIT_COMPONENT_EXPORT(fn)       INIT_EXPORT(fn, "3")
/* file system initialization (dfs-elm, dfs-rom, ...) */
#define INIT_FS_EXPORT(fn)              INIT_EXPORT(fn, "4")
/* environment initialization (mount disk, ...) */
#define INIT_ENV_EXPORT(fn)             INIT_EXPORT(fn, "5")
/* appliation initialization (rtgui application etc ...) */
#define INIT_APP_EXPORT(fn)             INIT_EXPORT(fn, "6")

```

```·
INIT_BOARD_EXPORT(rt_hw_timer_init);
```

## rt_console_set_device
```
rt_device_t rt_console_set_device(const char *name)
{
    rt_device_t new, old;

    /* save old device */
    old = _console_device;
  
    /* find new console device */
    new = rt_device_find(name);
    if (new != RT_NULL)
    {
        if (_console_device != RT_NULL)
        {
            /* close old console device */
            rt_device_close(_console_device);
        }

        /* set new console device */
        _console_device = new;
        rt_device_open(_console_device, RT_DEVICE_OFLAG_RDWR);
    }
  
    return old;
}
```

## rt_system_heap_init
```
void rt_system_heap_init(void *begin_addr, void *end_addr)

{

    struct heap_mem *mem;

    rt_uint32_t begin_align = RT_ALIGN((rt_uint32_t)begin_addr, RT_ALIGN_SIZE);

    rt_uint32_t end_align = RT_ALIGN_DOWN((rt_uint32_t)end_addr, RT_ALIGN_SIZE);

  

    RT_DEBUG_NOT_IN_INTERRUPT;

  

    /* alignment addr */

    if ((end_align > (2 * SIZEOF_STRUCT_MEM)) &&

        ((end_align - 2 * SIZEOF_STRUCT_MEM) >= begin_align))

    {

        /* calculate the aligned memory size */

        mem_size_aligned = end_align - begin_align - 2 * SIZEOF_STRUCT_MEM;

    }

    else

    {

        rt_kprintf("mem init, error begin address 0x%x, and end address 0x%x\n",

                   (rt_uint32_t)begin_addr, (rt_uint32_t)end_addr);

  

        return;

    }

  

    /* point to begin address of heap */

    heap_ptr = (rt_uint8_t *)begin_align;

  

    RT_DEBUG_LOG(RT_DEBUG_MEM, ("mem init, heap begin address 0x%x, size %d\n",

                                (rt_uint32_t)heap_ptr, mem_size_aligned));

  

    /* initialize the start of the heap */

    mem        = (struct heap_mem *)heap_ptr;

    mem->magic = HEAP_MAGIC;

    mem->next  = mem_size_aligned + SIZEOF_STRUCT_MEM;

    mem->prev  = 0;

    mem->used  = 0;

  

    /* initialize the end of the heap */

    heap_end        = (struct heap_mem *)&heap_ptr[mem->next];

    heap_end->magic = HEAP_MAGIC;

    heap_end->used  = 1;

    heap_end->next  = mem_size_aligned + SIZEOF_STRUCT_MEM;

    heap_end->prev  = mem_size_aligned + SIZEOF_STRUCT_MEM;

  

    rt_sem_init(&heap_sem, "heap", 1, RT_IPC_FLAG_FIFO);

  

    /* initialize the lowest-free pointer to the start of the heap */

    lfree = (struct heap_mem *)heap_ptr;

}
```

这段代码是RT-Thread操作系统中用于初始化系统堆的函数。系统堆是用于动态内存分配的内存区域。以下是对这段代码的详细解释：

### 函数定义
```c
void rt_system_heap_init(void *begin_addr, void *end_addr)
```
- 定义了一个名为 `rt_system_heap_init` 的函数，用于初始化系统堆。该函数接受两个参数：`begin_addr` 和 `end_addr`，分别表示堆内存区域的起始地址和结束地址。

### 变量定义
```c
struct heap_mem *mem;
rt_uint32_t begin_align = RT_ALIGN((rt_uint32_t)begin_addr, RT_ALIGN_SIZE);
rt_uint32_t end_align = RT_ALIGN_DOWN((rt_uint32_t)end_addr, RT_ALIGN_SIZE);
```
- 定义了一个指向 `heap_mem` 结构体的指针 `mem`。
- 使用 `RT_ALIGN` 宏对起始地址进行对齐，确保起始地址是 `RT_ALIGN_SIZE` 的倍数。
- 使用 `RT_ALIGN_DOWN` 宏对结束地址进行对齐，确保结束地址是 `RT_ALIGN_SIZE` 的倍数。

### 调试检查
```c
RT_DEBUG_NOT_IN_INTERRUPT;
```
- 确保当前不在中断上下文中执行。

### 计算对齐后的内存大小
```c
if ((end_align > (2 * SIZEOF_STRUCT_MEM)) &&
    ((end_align - 2 * SIZEOF_STRUCT_MEM) >= begin_align))
{
    mem_size_aligned = end_align - begin_align - 2 * SIZEOF_STRUCT_MEM;
}
else
{
    rt_kprintf("mem init, error begin address 0x%x, and end address 0x%x\n",
               (rt_uint32_t)begin_addr, (rt_uint32_t)end_addr);

    return;
}
```
- 检查对齐后的起始地址和结束地址之间的距离是否足够大（至少可以容纳两个 `heap_mem` 结构体）。
- 如果不满足条件，打印错误信息并返回。

### 初始化堆指针
```c
heap_ptr = (rt_uint8_t *)begin_align;
```
- 将 `heap_ptr` 指向对齐后的起始地址。

### 打印调试信息
```c
RT_DEBUG_LOG(RT_DEBUG_MEM, ("mem init, heap begin address 0x%x, size %d\n",
                            (rt_uint32_t)heap_ptr, mem_size_aligned));
```
- 打印堆的起始地址和大小。

### 初始化堆的起始和结束
```c
mem        = (struct heap_mem *)heap_ptr;
mem->magic = HEAP_MAGIC;
mem->next  = mem_size_aligned + SIZEOF_STRUCT_MEM;
mem->prev  = 0;
mem->used  = 0;

heap_end        = (struct heap_mem *)&heap_ptr[mem->next];
heap_end->magic = HEAP_MAGIC;
heap_end->used  = 1;
heap_end->next  = mem_size_aligned + SIZEOF_STRUCT_MEM;
heap_end->prev  = mem_size_aligned + SIZEOF_STRUCT_MEM;
```
- 初始化堆的起始 `heap_mem` 结构体，设置其 `magic`、`next`、`prev` 和 `used` 字段。
- 初始化堆的结束 `heap_mem` 结构体，设置其 `magic`、`used`、`next` 和 `prev` 字段。

### 初始化堆信号量
```c
rt_sem_init(&heap_sem, "heap", 1, RT_IPC_FLAG_FIFO);
```
- 初始化一个信号量 `heap_sem`，用于保护堆内存区域的访问。

### 初始化最低空闲指针
```c
lfree = (struct heap_mem *)heap_ptr;
```
- 将 `lfree` 指向堆的起始 `heap_mem` 结构体，用于跟踪最低的空闲内存块。

### 总结
这段代码通过初始化系统堆的起始和结束 `heap_mem` 结构体，设置堆指针和最低空闲指针，并初始化一个信号量来保护堆内存区域的访问。这样可以确保系统堆能够正确地管理动态内存分配和释放。


## RTM_EXPORT
这段代码定义了一个宏 `RTM_EXPORT`，用于在不同编译器环境下导出符号，以便在运行时模块（RT-Thread的模块系统）中解析和使用这些符号。这个宏根据不同的编译器环境（Microsoft Visual C++、MinGW 或其他）定义了不同的实现方式。以下是对这段代码的详细解释：

### Microsoft Visual C++ 编译器
```c
#if defined(_MSC_VER)
#pragma section("RTMSymTab$f",read)
#define RTM_EXPORT(symbol)                                            \
__declspec(allocate("RTMSymTab$f"))const char __rtmsym_##symbol##_name[] = "__vs_rtm_"#symbol;
#pragma comment(linker, "/merge:RTMSymTab=mytext")
```
- 使用 `#pragma section` 指令定义一个名为 `"RTMSymTab$f"` 的内存段，该段用于存储符号表。
- 定义 `RTM_EXPORT` 宏，使用 `__declspec(allocate("RTMSymTab$f"))` 将符号名称分配到指定的内存段中。符号名称前缀为 `"__vs_rtm_"`。
- 使用 `#pragma comment(linker, "/merge:RTMSymTab=mytext")` 指令将所有 `RTMSymTab$f` 段合并到一个名为 `mytext` 的段中。

### MinGW 编译器
```c
#elif defined(__MINGW32__)
#define RTM_EXPORT(symbol)
```
- 对于 MinGW 编译器，当前不导出符号，因此 `RTM_EXPORT` 宏为空。

### 其他编译器
```c
#else
#define RTM_EXPORT(symbol)                                            \
const char __rtmsym_##symbol##_name[] = #symbol;                      \
const struct rt_module_symtab __rtmsym_##symbol SECTION("RTMSymTab")= \
{                                                                     \
    (void *)&symbol,                                                  \
    __rtmsym_##symbol##_name                                          \
};
#endif
```
- 对于其他编译器，定义 `RTM_EXPORT` 宏，创建一个包含符号名称和符号地址的结构体，并将其放置在名为 `"RTMSymTab"` 的内存段中。
- 使用 `SECTION("RTMSymTab")` 属性将符号表项放置在指定的内存段中。

### 总结
这个宏 `RTM_EXPORT` 的目的是在不同编译器环境下导出符号，以便在运行时模块中解析和使用这些符号。通过这种方式，可以在模块系统中动态加载和解析模块中的符号，从而实现模块的动态链接和运行时绑定。这种机制对于模块化设计和动态加载模块非常有用。