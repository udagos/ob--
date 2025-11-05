---
up:
  - "[[../moc/MocRtos|MocRtos]]"
same:
  - "[[../note/信号量锁和信号量实例]]"
  - "[[事件集]]"
---



# 链表
## 1
```
struct rt_list_node
{
    struct rt_list_node *next;                          /**< point to next node. */
    struct rt_list_node *prev;                          /**< point to prev node. */
};
typedef struct rt_list_node rt_list_t;                  /**< Type for lists. */
```
没有元素？
	![](../fujian/Pasted%20image%2020250621150955.png)
```
rt_inline void rt_list_init(rt_list_t *l)
{
    l->next = l->prev = l;
}

rt_inline void rt_list_insert_after(rt_list_t *l, rt_list_t *n)//插入的是n
{
    l->next->prev = n;
    n->next = l->next;

    l->next = n;
    n->prev = l;
}

rt_inline void rt_list_remove(rt_list_t *n)
{
    n->next->prev = n->prev;
    n->prev->next = n->next;

    n->next = n->prev = n;
}
```
不分配内存？
	![](../fujian/Pasted%20image%2020250621151159.png)
	这里插入是元素和位置。rtt则是直接插入的节点，所以没有元素

```
rt_object_init(struct rt_object *object,)
	information = rt_object_get_information(type);
	rt_list_insert_after(&(information->object_list), &(object->list));

rt_err_t rt_sem_init(rt_sem_t    sem)
	rt_object_init(&(sem->parent.parent))	
	rt_ipc_object_init(&(sem->parent));
	
shell = &_shell;	
rt_sem_init(&(shell->rx_sem),


struct finsh_shell _shell;

struct finsh_shell
{
    struct rt_semaphore rx_sem;
    
struct rt_semaphore
{
    struct rt_ipc_object parent;                        /**< inherit from ipc_object */

    rt_uint16_t          value;                         /**< value of semaphore. */
    rt_uint16_t          reserved;                      /**< reserved field */
};

struct rt_ipc_object
{
    struct rt_object parent;                            /**< inherit from rt_object */

    rt_list_t        suspend_thread;                    /**< threads pended on this resource */
};


struct rt_object
{
    char       name[RT_NAME_MAX];                       /**< name of kernel object */
    rt_uint8_t type;                                    /**< type of kernel object */
    rt_uint8_t flag;                                    /**< flag of kernel object */

    rt_list_t  list;                                    /**< list node of kernel object */
};
```

rt_list_insert_after (&(information->object_list), &(object->list)); 的 (object->list) 实体在哪
	struct finsh_shell \_shell;
```
#ifdef RT_USING_HEAP
	shell = (struct finsh_shell *)rt_calloc(1, sizeof(struct finsh_shell));
#else
	shell = &_shell;		
```


rtt没有头节点
如果单链表
“几处地方可能会出问题首先.并不存在从所给定义出发在表的前面插入元素的真正显性的方法。
第二,从表的前面实行删除是一个特殊情况,因为它改变了表的起始端;编程中的疏忽将会造成表的丢失。
第三 个问题涉及一般的删除。虽然上述指针的移动很简单,但是删除算法要求我们记住被删除元 素前面的表元。”

如果双向
“它可以有表头,也可以g有表 头(若有表头,则最后的单元就指向它)”
## 2
```
typedef struct PAPERMANAGE_MAIN
{
    struct STD_LIST_NODE mList;
	U32 mPaperId;
	...
}PAPER;

static PAPER sPaperManage[TRACK_NOTE_NUM_MAX];

NewMainPaper(GATE_INDEX SrcGateNo)
	U8 PaperIndex = MallocPaperManageUnit(); 申请介质单元
	PaperUnitInit(SrcGateNo, PaperIndex); 介质单元初始化
	OsListInsertAfter(&sMainPaperListHead,&sPaperManage[PaperIndex].mList);
```

```
#define STD_LIST_ENTRY(node, type, member) \
    ((type *)((U8 *)(node) - (U32)(&((type *)0)->member)))


#define WALK_BRAN_LIST_FROM_FIRST(Paper, Head)\
        BRAN_PAPER *Paper = STD_LIST_ENTRY((Head)->prev, BRAN_PAPER, mList);\
        for(struct STD_LIST_NODE *Node = (Head)->prev; Node != (Head); Node = Node->prev,Paper = STD_LIST_ENTRY(Node, BRAN_PAPER, mList))
        
WALK_BRAN_LIST_FROM_FIRST(BranPaper, BranHead)


BranPaper->mTrackNodeNum
```

结构体是链表元素了，链表应该只是一个标记作用



# 对象容器
![](../fujian/Pasted%20image%2020250622100212.png)
```
struct rt_object_information
{
    enum rt_object_class_type type;                     /**< object class type */
    rt_list_t                 object_list;              /**< object list */
    rt_size_t                 object_size;              /**< object size */
};

#define _OBJ_CONTAINER_LIST_INIT(c)     \
    {&(rt_object_container[c].object_list), &(rt_object_container[c].object_list)}

static struct rt_object_information rt_object_container[RT_Object_Info_Unknown] =
{
    /* initialize object container - thread */
    {RT_Object_Class_Thread, _OBJ_CONTAINER_LIST_INIT(RT_Object_Info_Thread), sizeof(struct rt_thread)},
```

这类对象的每个具体实例都通过链表的形式挂接在 object_list 上



```
void rt_object_init(struct rt_object         *object,
                    enum rt_object_class_type type,
                    const char               *name)
{
	//get object information
	information = rt_object_get_information(type);
		return &rt_object_container[index];
		
	//find object
	for (node  = information->object_list.next;
            node != &(information->object_list);
            node  = node->next)
    	obj = rt_list_entry(node, struct rt_object, list);
    	RT_ASSERT(obj != object);
    	
    //initialize object's parameters
    RT_OBJECT_HOOK_CALL(rt_object_attach_hook, (object));//可能没有用hook
    rt_list_insert_after(&(information->object_list), &(object->list));
}

```

对象初始化时，系统会把这个对象放置到对象容器中进行管理


# 线程
![](../fujian/Pasted%20image%2020250622100138.png)


![](../fujian/Pasted%20image%2020250623085943.png)
RT-Thread 中，实际上线程并不存在运行状态，就绪状态和运行状态是等同的。
1 
	rt_thread_suspend(thread);
		/* change thread stat \*/
	    **rt_schedule_remove_thread** (thread);
	    thread->stat = RT_THREAD_SUSPEND | (thread->stat & ~RT_THREAD_STAT_MASK);
	rt_schedule ();
2
	/* remove from suspend list \*/
    rt_list_remove(&(thread->tlist));
    /* insert to schedule ready list \*/
    **rt_schedule_insert_thread**(thread);


```
struct rt_thread
{
	/* rt object */
    rt_list_t   list;                                   /**< the object list */
    rt_list_t   tlist;                                  /**< the thread list */
    
    /* stack point and entry */
    void       *sp;                                     /**< stack point */
    void       *entry;                                  /**< entry */
    void       *parameter;                              /**< parameter */
    void       *stack_addr;                             /**< stack address */
    rt_uint32_t stack_size;                             /**< stack size */
     void (*cleanup)(struct rt_thread *tid);             /**< cleanup function when thread exit */
}
```
cleanup 会在线程退出时被空闲线程回调一次，以执行用户设置的清理现场等工作

```
static struct rt_thread idle;
static rt_uint8_t rt_thread_stack[IDLE_THREAD_STACK_SIZE];

void rt_thread_idle_init(void)
{
    /* initialize thread */
    rt_thread_init(&idle,
                   "tidle",
                   rt_thread_idle_entry,
                   RT_NULL,
                   &rt_thread_stack[0],
                   sizeof(rt_thread_stack),
                   RT_THREAD_PRIORITY_MAX - 1,
                   32);

    /* startup */
    rt_thread_startup(&idle);
}

rt_err_t rt_thread_init(struct rt_thread *thread,
                        const char       *name,
                        void (*entry)(void *parameter),
                        void             *parameter,
                        void             *stack_start,
                        rt_uint32_t       stack_size,
                        rt_uint8_t        priority,
                        rt_uint32_t       tick)
{
	rt_object_init((rt_object_t)thread, RT_Object_Class_Thread, name);
	
	return _rt_thread_init(thread,
                           name,
                           entry,
                           parameter,
                           stack_start,
                           stack_size,
                           priority,
                           tick);
}

_rt_thread_init
{
	/* init thread list */
	rt_list_init(&(thread->tlist));
	 thread->entry = (void *)entry;
    thread->parameter = parameter;
    
    /* stack init */
    thread->stack_addr = stack_start;
    
    /* init thread stack */
    rt_memset(thread->stack_addr, '#', thread->stack_size);
    thread->sp = (void *)rt_hw_stack_init(thread->entry, thread->parameter,
                                          (rt_uint8_t *)((char *)thread->stack_addr + thread->stack_size - sizeof(rt_ubase_t)),
                                          (void *)rt_thread_exit)
}



rt_uint8_t *rt_hw_stack_init(void *tentry, void *parameter,
                             rt_uint8_t *stack_addr, void *texit)
{
    rt_uint32_t *stk;

    stack_addr += sizeof(rt_uint32_t);
    stack_addr  = (rt_uint8_t *)RT_ALIGN_DOWN((rt_uint32_t)stack_addr, 8);
    stk      = (rt_uint32_t *)stack_addr;
    *(--stk) = (rt_uint32_t)tentry;         /* entry point */
    *(--stk) = (rt_uint32_t)texit;          /* lr */
    *(--stk) = 0xdeadbeef;                  /* r12 */
    *(--stk) = 0xdeadbeef;                  /* r11 */
    *(--stk) = 0xdeadbeef;                  /* r10 */
    *(--stk) = 0xdeadbeef;                  /* r9 */
    *(--stk) = 0xdeadbeef;                  /* r8 */
    *(--stk) = 0xdeadbeef;                  /* r7 */
    *(--stk) = 0xdeadbeef;                  /* r6 */
    *(--stk) = 0xdeadbeef;                  /* r5 */
    *(--stk) = 0xdeadbeef;                  /* r4 */
    *(--stk) = 0xdeadbeef;                  /* r3 */
    *(--stk) = 0xdeadbeef;                  /* r2 */
    *(--stk) = 0xdeadbeef;                  /* r1 */
    *(--stk) = (rt_uint32_t)parameter;      /* r0 : argument */

    /* cpsr */
    if ((rt_uint32_t)tentry & 0x01)
        *(--stk) = SVCMODE | 0x20;          /* thumb mode */
    else
        *(--stk) = SVCMODE;                 /* arm mode   */

#if defined(__TI_VFP_SUPPORT__) || (defined (__VFP_FP__) && !defined(__SOFTFP__))
#ifndef RT_VFP_LAZY_STACKING
    {
        int i;

        for (i = 0; i < VFP_DATA_NR; i++)
        {
            *(--stk) = 0;
        }
        /* FPSCR TODO: do we need to set the values other than 0? */
        *(--stk) = 0;
        /* FPEXC. Enable the FVP if no lazy stacking. */
        *(--stk) = 0x40000000;
    }
#else
    /* FPEXC. Disable the FVP by default. */
    *(--stk) = 0x00000000;
#endif
#endif

    /* return task's current stack address */
    return (rt_uint8_t *)stk;
}
                        
```



## rt_hw_stack_init
![](../fujian/Pasted%20image%2020250622104734.png)

1. **栈地址对齐**
   ```c
   stack_addr += sizeof(rt_uint32_t);
   stack_addr  = (rt_uint8_t *)RT_ALIGN_DOWN((rt_uint32_t)stack_addr, 8);
   ```
   - 将栈地址向上调整一个 `rt_uint32_t` 的大  小，确保栈空间有足够的空间存储后续的数据。
   - 将栈地址向下对齐到8字节边界，确保栈地址满足硬件对齐要求。

2. **初始化栈内容**
   ```c
   stk      = (rt_uint32_t *)stack_addr;
   *(--stk) = (rt_uint32_t)tentry;         /* entry point */
   *(--stk) = (rt_uint32_t)texit;          /* lr */
   *(--stk) = 0xdeadbeef;                  /* r12 */
   *(--stk) = 0xdeadbeef;                  /* r11 */
   *(--stk) = 0xdeadbeef;                  /* r10 */
   *(--stk) = 0xdeadbeef;                  /* r9 */
   *(--stk) = 0xdeadbeef;                  /* r8 */
   *(--stk) = 0xdeadbeef;                  /* r7 */
   *(--stk) = 0xdeadbeef;                  /* r6 */
   *(--stk) = 0xdeadbeef;                  /* r5 */
   *(--stk) = 0xdeadbeef;                  /* r4 */
   *(--stk) = 0xdeadbeef;                  /* r3 */
   *(--stk) = 0xdeadbeef;                  /* r2 */
   *(--stk) = 0xdeadbeef;                  /* r1 */
   *(--stk) = (rt_uint32_t)parameter;      /* r0 : argument */
   ```
   - 将栈指针 `stk` 指向栈地址。
   - 依次将线程的入口函数地址、退出函数地址以及一些寄存器的初始值（如 `r12` 到 `r1`）压入栈中。
   - 将线程入口函数的参数 `parameter` 压入栈中，作为 `r0` 寄存器的值。

3. **设置处理器状态寄存器（CPSR）**
   ```c
   if ((rt_uint32_t)tentry & 0x01)
       *(--stk) = SVCMODE | 0x20;          /* thumb mode */
   else
       *(--stk) = SVCMODE;                 /* arm mode   */
   ```
   - 检查线程入口函数地址是否为奇数（即是否为Thumb模式指令）。
   - 如果是Thumb模式，设置CPSR为 `SVCMODE | 0x20`，表示线程将以Thumb模式运行。
   - 如果是ARM模式，设置CPSR为 `SVCMODE`，表示线程将以ARM模式运行。

4. **浮点支持（可选）**
   ```c
   #if defined(__TI_VFP_SUPPORT__) || (defined (__VFP_FP__) && !defined(__SOFTFP__))
   #ifndef RT_VFP_LAZY_STACKING
       {
           int i;

           for (i = 0; i < VFP_DATA_NR; i++)
           {
               *(--stk) = 0;
           }
           /* FPSCR TODO: do we need to set the values other than 0? */
           *(--stk) = 0;
           /* FPEXC. Enable the FVP if no lazy stacking. */
           *(--stk) = 0x40000000;
       }
   #else
       /* FPEXC. Disable the FVP by default. */
       *(--stk) = 0x00000000;
   #endif
   #endif
   ```
   - 如果编译器支持浮点运算（VFP），并且没有启用延迟栈模式（`RT_VFP_LAZY_STACKING`），则初始化浮点寄存器和状态寄存器。
   - 如果启用了延迟栈模式，则禁用浮点运算单元（FVP）。

5. **返回栈顶地址**
   ```c
   return (rt_uint8_t *)stk;
   ```
   - 返回初始化后的栈顶地址，即线程当前的栈地址。

## 设置和删除空闲钩子
空闲钩子函数是空闲线程的钩子函数，如果设置了空闲钩子函数，就可以在系统执行空闲线程时自动执行空闲钩子函数来做一些其他事情 

## 设置调度器钩子 
系统的上下文切换是系统中最普遍的事件。有时用户可能会想知道在某个时刻发生了什么样的线程切换，可以通过调用下面的函数接口设置一个相应的钩子函数。在系统线程切换时，这个钩子函数将被调用：
```
void rt_schedule(void)
	RT_OBJECT_HOOK_CALL(rt_scheduler_hook, (from_thread, to_thread));

rt_scheduler_sethook(void (*hook)(struct rt_thread *from, struct rt_thread *to))
{
    rt_scheduler_hook = hook;
}
```

## rt_thread_startup
```
rt_err_t rt_thread_startup(rt_thread_t thread)
{
	/* change thread stat \*/
    thread->stat = RT_THREAD_SUSPEND;
    
    /* then resume it *// 恢复
    rt_thread_resume(thread);//放入就绪队列
    if (rt_thread_self() != RT_NULL)//获得当前线程
    	rt_schedule();

}
```

# 上下文切换
```
rt_schedule
{
	/* get switch to thread */
	to_thread = rt_list_entry(rt_thread_priority_table[highest_ready_priority].next,
                                  struct rt_thread,
                                  tlist);
                                  
    //如果目标线程与当前线程不同时，执行线程切换                                
 	if (to_thread != rt_current_thread)   
 		RT_OBJECT_HOOK_CALL(rt_scheduler_hook, (from_thread, to_thread));//切换回调，上面有解释                             
		if (rt_interrupt_nest == 0)	
			rt_hw_context_switch((rt_ubase_t)&from_thread->sp,
	                                     (rt_ubase_t)&to_thread->sp);
		else//在中断中
			rt_hw_context_switch_interrupt((rt_ubase_t)&from_thread->sp,
	                                               (rt_ubase_t)&to_thread->sp);
}
```
## 1
m3-gcc

==因为m核心有pendsv中断可以自动保存部分寄存器，而a核没有该中断==

rt_hw_context_switch
rt_hw_context_switch_interrupt
m
```m
/*
 * void rt_hw_context_switch(rt_uint32 from, rt_uint32 to);
 * R0 --> from
 * R1 --> to
 */
    .global rt_hw_context_switch_interrupt
    .type rt_hw_context_switch_interrupt, %function
    .global rt_hw_context_switch
    .type rt_hw_context_switch, %function
rt_hw_context_switch_interrupt:
rt_hw_context_switch:
    /* set rt_thread_switch_interrupt_flag to 1 */
    LDR     R2, =rt_thread_switch_interrupt_flag
    LDR     R3, [R2]
    CMP     R3, #1
    BEQ     _reswitch
    MOV     R3, #1
    STR     R3, [R2]

    LDR     R2, =rt_interrupt_from_thread   /* set rt_interrupt_from_thread */
    STR     R0, [R2]

_reswitch:
    LDR     R2, =rt_interrupt_to_thread     /* set rt_interrupt_to_thread */
    STR     R1, [R2]

    LDR     R0, =ICSR           /* trigger the PendSV exception (causes context switch) */
    LDR     R1, =PENDSVSET_BIT
    STR     R1, [R0]
    BX      LR


```

a
```
*
 * void rt_hw_context_switch(rt_uint32 from, rt_uint32 to);
 * r0 --> from
 * r1 --> to
 */
.globl rt_hw_context_switch
rt_hw_context_switch:
    stmfd   sp!, {lr}       @ push pc (lr should be pushed in place of PC)
    stmfd   sp!, {r0-r12, lr}   @ push lr & register file

    mrs r4, cpsr
    tst lr, #0x01
    beq _ARM_MODE
    orr r4, r4, #0x20       @ it's thumb code

_ARM_MODE:
    stmfd sp!, {r4}         @ push cpsr

    vmrs    r4, fpexc
    vmrs    r5, fpscr
    vstmdb  sp!, {d16-d31}
    vstmdb  sp!, {d0-d15}
    @ TODO: add support for Common VFPv3.
    @       Save registers like FPINST, FPINST2
    stmdb   sp!, {r5}
    stmdb   sp!, {r4}

    str sp, [r0]            @ store sp in preempted tasks TCB
    ldr sp, [r1]            @ get new task stack pointer

    ldmia   sp!, {r0}       @ get fpexc
    vmsr    fpexc, r0       @ restore fpexc
    ldmia   sp!, {r1}       @ get fpscr
    vmsr    fpscr, r1
    vldmia  sp!, {d0-d15}
    vldmia  sp!, {d16-d31}

    ldmfd sp!, {r4}         @ pop new task cpsr to spsr
    msr spsr_cxsf, r4

    ldmfd sp!, {r0-r12, lr, pc}^  @ pop new task r0-r12, lr & pc, copy spsr to cpsr
```
rt_hw_context_switch_to:
m
```
/*
 * void rt_hw_context_switch_to(rt_uint32 to);
 * R0 --> to
 */
    .global rt_hw_context_switch_to
    .type rt_hw_context_switch_to, %function
rt_hw_context_switch_to:
    LDR     R1, =rt_interrupt_to_thread
    STR     R0, [R1]

    /* set from thread to 0 */
    LDR     R1, =rt_interrupt_from_thread
    MOV     R0, #0
    STR     R0, [R1]

    /* set interrupt flag to 1 */
    LDR     R1, =rt_thread_switch_interrupt_flag
    MOV     R0, #1
    STR     R0, [R1]

    /* set the PendSV and SysTick exception priority */
    LDR     R0, =SHPR3
    LDR     R1, =PENDSV_PRI_LOWEST
    LDR.W   R2, [R0,#0]             /* read */
    ORR     R1, R1, R2              /* modify */
    STR     R1, [R0]                /* write-back */

    LDR     R0, =ICSR               /* trigger the PendSV exception (causes context switch) */
    LDR     R1, =PENDSVSET_BIT
    STR     R1, [R0]

    /* restore MSP */
    LDR     r0, =SCB_VTOR
    LDR     r0, [r0]
    LDR     r0, [r0]
    NOP
    MSR     msp, r0

    /* enable interrupts at processor level */
    CPSIE   F
    CPSIE   I

    /* never reach here! */

```
a
```
/*
 * void rt_hw_context_switch_to(rt_uint32 to, struct rt_thread *to_thread);
 * r0 --> to (thread stack)
 * r1 --> to_thread
 */
.globl rt_hw_context_switch_to
rt_hw_context_switch_to:
    ldr sp, [r0]            @ get new task stack pointer

#ifdef RT_USING_SMP
    mov     r0, r1
    bl      rt_cpus_lock_status_restore
#endif /*RT_USING_SMP*/
    b       rt_hw_context_switch_exit

.section .bss.share.isr
_guest_switch_lvl:
    .word 0

.globl vmm_virq_update

.section .text.isr, "ax"
```

rt_hw_interrupt_thread_switch: 没有用到
```

/* compatible with old version */
    .global rt_hw_interrupt_thread_switch
    .type rt_hw_interrupt_thread_switch, %function
rt_hw_interrupt_thread_switch:
    BX      LR
    NOP

    .global HardFault_Handler
    .type HardFault_Handler, %function
HardFault_Handler:
    /* get current context */
    MRS     r0, msp                 /* get fault context from handler. */
    TST     lr, #0x04               /* if(!EXC_RETURN[2]) */
    BEQ     _get_sp_done
    MRS     r0, psp                 /* get fault context from thread. */
_get_sp_done:

    STMFD   r0!, {r4 - r11}         /* push r4 - r11 register */
    STMFD   r0!, {lr}               /* push exec_return register */

    TST     lr, #0x04               /* if(!EXC_RETURN[2]) */
    BEQ     _update_msp
    MSR     psp, r0                 /* update stack pointer to PSP. */
    B       _update_done
_update_msp:
    MSR     msp, r0                 /* update stack pointer to MSP. */
_update_done:

    PUSH    {LR}
    BL      rt_hw_hard_fault_exception
    POP     {LR}

    ORR     LR, LR, #0x04
    BX      LR
```

## 解释
==Cortex-M 中上下文切换都是统一使用 PendSV 异常来完成==



![](../fujian/Pasted%20image%2020250622111244.png)
==m核 硬件在进入 PendSV 中断之前自动保存了 from 线程的 PSR、PC、LR、R 12、R 3~R 0 寄存器，==
然后 **PendSV 里保存 from 线程的 R 11〜R 4 寄存器**，以及恢复 to 线程的 R 4〜RI 11 寄存器，
最后硬件在退出 PendSV 中断之后，自动恢复 to 线程的 R 0〜R 3、R12、LR、PC、PSR 寄存器。

![](../fujian/Pasted%20image%2020250622111257.png)

### rt_hw_context_switch
![](../fujian/Pasted%20image%2020250623082839.png)
==在 Cortex-M 内核中 rt_hw_context_switch () 和 rt_hw_context_switch_interrupt () 功能一致==，
即都是在 PendSV 中完成剩余上下文的保存和回复。所以我们仅仅需要夔现一段代码，简化移植的工作。

- 初始化线程的栈空间。
    
- 设置线程的入口函数和参数。
    
- 将线程插入到就绪队列中。
    
- 触发调度器，使线程开始执行。
### rt_hw_context_switch_to
这个函数实现切换到指定线程的功能
![](../fujian/Pasted%20image%2020250622111348.png)
- 初始化内核对象，如线程、信号量、互斥锁等。
    
- 初始化中断系统。
    
- 初始化调度器。
    
- 启动第一个线程，通常是 `main` 线程。

## 实现 PendSV 中断
完成线程切换的实际工作
![](../fujian/Pasted%20image%2020250623084444.png)
```
    .global PendSV_Handler
    .type PendSV_Handler, %function
PendSV_Handler:
    /* disable interrupt to protect context switch */
    MRS     R2, PRIMASK
    CPSID   I

    /* get rt_thread_switch_interrupt_flag */
    LDR     R0, =rt_thread_switch_interrupt_flag
    LDR     R1, [R0]
    CBZ     R1, pendsv_exit         /* pendsv aLReady handled */

    /* clear rt_thread_switch_interrupt_flag to 0 */
    MOV     R1, #0
    STR     R1, [R0]

    LDR     R0, =rt_interrupt_from_thread
    LDR     R1, [R0]
    CBZ     R1, switch_to_thread    /* skip register save at the first time */

    MRS     R1, PSP                 /* get from thread stack pointer */
    STMFD   R1!, {R4 - R11}         /* push R4 - R11 register */
    LDR     R0, [R0]
    STR     R1, [R0]                /* update from thread stack pointer */

switch_to_thread:
    LDR     R1, =rt_interrupt_to_thread
    LDR     R1, [R1]
    LDR     R1, [R1]                /* load thread stack pointer */

    LDMFD   R1!, {R4 - R11}         /* pop R4 - R11 register */
    MSR     PSP, R1                 /* update stack pointer */

pendsv_exit:
    /* restore interrupt */
    MSR     PRIMASK, R2

    ORR     LR, LR, #0x04
    BX      LR
```

# 问
##  rt_hw_context_switch与rt_hw_context_switch_to
rt_thread_startup//start a thread and put it to system ready queue
	rt_schedule
		rt_hw_context_switch
main
		rtthread_startup //startup RT-Thread RTOS 
		rt_system_scheduler_start
			rt_hw_context_switch_to((rt_uint32_t)&to_thread->sp);


## rt_hw_interrupt_thread_switch 与 rt_hw_context_switch_interrupt
### rt_hw_interrupt_thread_switch
硬件中断上下文切换函数，通常在中断服务例程（ISR）中调用。它的作用是在线程切换时保存当前线程的上下文，并准备切换到新的线程。

- 保存当前线程的上下文。
    
- 更新当前线程指针。
    
- 准备切换到新的线程。
### rt_hw_context_switch_interrupt
硬件上下文切换中断函数，通常在 PendSV 异常处理程序中调用。它的作用是通过 PendSV 异常触发上下文切换。

- 设置中断标志，触发 PendSV 异常。
    
- 保存当前线程的上下文。
    
- 更新当前线程指针。
    
- 恢复目标线程的上下文。

### 区别

1. **触发机制**
    
    - **`rt_hw_interrupt_thread_switch`**：通常在中断服务例程（ISR）中调用，直接进行上下文切换。
        
    - **`rt_hw_context_switch_interrupt`**：通过 PendSV 异常触发上下文切换，适用于需要在中断上下文中进行线程切换的场景。
        
2. **应用场景**
    
    - **`rt_hw_interrupt_thread_switch`**：适用于在中断服务例程中直接切换线程，例如在中断处理过程中需要切换到高优先级线程。
        
    - **`rt_hw_context_switch_interrupt`**：适用于需要通过 PendSV 异常进行上下文切换的场景，例如在调度器中触发线程切换。
        
3. **实现细节**
    
    - **`rt_hw_interrupt_thread_switch`**：直接调用上下文保存和恢复函数，不涉及中断标志的设置。
        
    - **`rt_hw_context_switch_interrupt`**：设置中断标志，触发 PendSV 异常，然后在 PendSV 异常处理程序中完成上下文切换。
        

#### 总结

- **`rt_hw_interrupt_thread_switch`**：在中断服务例程中直接进行上下文切换，适用于需要立即切换线程的场景。
    
- **`rt_hw_context_switch_interrupt`**：通过 PendSV 异常触发上下文切换，适用于需要在中断上下文中进行线程切换的场景。
    

这两个函数在 RT-Thread 操作系统中都用于线程切换，但触发机制和应用场景有所不同

## [[../note/信号量锁和信号量实例]]

# 线程同步
一项工作往往可以通过多个线程协调的方式来共同完成

线程的同步方式有很多种，其核心思想都是在访问临界区的时候只允许一个（或一类线程运行。
进入/退出临界区的方式如下。
	(1 ) 调用 rt_hw_interrupt_disable () 进入临界区，调用 rt_hw_interrupt_enable () 退出临界区；详见 9.3 节的内容。 
	(2 ) 调用 rt_enter_critical () 进入临界区，调用 rt_exit_critical () 退出临界区。//lock the thread scheduler
## 信号量

rt_sem_take
```

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
            
			rt_hw_interrupt_enable(temp);
			rt_schedule();
```

rt_sem_release
```
temp = rt_hw_interrupt_disable();

if (!rt_list_isempty(&sem->parent.suspend_thread))
	rt_ipc_list_resume(&(sem->parent.suspend_thread));
	need_schedule = RT_TRUE;
else
	if(sem->value < RT_SEM_VALUE_MAX)
		sem->value ++;
	else
		 rt_hw_interrupt_enable(temp);
		 return
		 
	rt_hw_interrupt_enable(temp);
	
	 /* resume a thread, re-schedule */
	if (need_schedule == RT_TRUE)
		rt_schedule();	

```
- 检查是否有线程因等待该信号量而挂起。
    - 如果有挂起的线程，调用 `rt_ipc_list_resume` 恢复这些线程，并设置 `need_schedule` 为 `RT_TRUE`。
    - 如果没有挂起的线程，检查信号量值是否小于最大值 `RT_SEM_VALUE_MAX`。
        - 如果小于最大值，增加信号量值。
        - 如果等于最大值，启用中断并返回 `-RT_EFULL`，表示信号量值溢出。

每个信号量对象都有一个信号量值和一个线程等待队列
号量的值对应信号量对象的实例数目
![](../fujian/Pasted%20image%2020250623102252.png)

控制块
	![](../fujian/Pasted%20image%2020250623092404.png)

使用场合：
线程同步 
	信号量的值初始化成o, 表示具备o个信号量资源实例; 而尝试获得该信号量的线程, 将直接在该信号量上进行等待。
	“此时可以把信号量看成工作完成标志”
锁
	锁常应用于多个线程间对同一共享资源（即临界区）的访问。**信号量在作为锁来使用时，通常应将信号量资源实例初始化成 1**，代表系统默认有一个资源可用
	当线程需要访问共享资源时, 它需要先获得这个资源锁
	![](../fujian/Pasted%20image%2020250623102331.png)
中断与线程同步 
	信号量也能够方便地应用于中断与线程间的同步
	信号量的值初始为0, 当  FinSH线程试图取得信号量时,  因为信号量值是0, 所以它会被挂起。当console设备有数据输入时,  产生中断，从而进入中断服务例程。在中断服务例程中, 它会读取console设备的数据, 并把读取的数据放入UART buffer中进行缓冲, 而后释放信号量, 释放信号量的操作将唤醒FinSH线程。在中断服务例程运行完毕后, 如果系统中没有比FinSH线程优先级更高的就绪线程存在, FinSH线程将持有信号量并运行, 从  UART buffer缓冲区中获取输入的数据。
		![](../fujian/Pasted%20image%2020250719100732.png)
资源计数
	例如,  初始化一个信号量的值为5, 则这个信号量可最大连续减少5次, 直到计数器减为0
	适合线程间工作处理速度不匹配的场合, 这个时候信号量可以作为前一线程工作完成个数的计数, 而当调度到后一线程时, 它也可以以一种连续的方式一次处理多个事件。例如, 生产者与消费者问题中, 生产者可以对信号量进行多次释放, 而后消费者被调度时能够一次处理多个信号量资源。
## 互斥量
使用信号量会导致的另一个潜在问题图6-6互斥量工作示意图是线程优先级翻转
在RT-Thread操作系统中, 互斥量可以解决优先级翻转问题, 使用优先级继承算法实现
![](../fujian/Pasted%20image%2020250719104240.png)
互斥量又叫相互排斥的信号量，**是一种特殊的二值信号量**
```
struct rt_mutex
{
    struct rt_ipc_object parent;                        /**< inherit from ipc_object */
  
    rt_uint16_t          value;                         /**< value of mutex */

    rt_uint8_t           original_priority;             /**< priority of last thread hold the mutex */
    rt_uint8_t           hold;                          /**< numbers of thread hold the mutex */

    struct rt_thread    *owner;                         /**< current owner of mutex */

};
```

rt_mutex_init
	mutex->value = 1;
rt_mutex_take
```
if (mutex->owner == thread)
{
	/* it's the same thread */
	mutex->hold ++;
}
else
	if (mutex->value > 0)
		/* mutex is available */
		mutex->value --;	
		/* set mutex owner and original priority */
		mutex->owner             = thread;
		mutex->original_priority = thread->current_priority;
		mutex->hold ++;
	else
		if (time == 0)	
		else
			/* change the owner thread priority of mutex */
			if (thread->current_priority < mutex->owner->current_priority)
				/* change the owner thread priority */
				rt_thread_control(mutex->owner,
								  RT_THREAD_CTRL_CHANGE_PRIORITY,
								  &thread->current_priority);
			/* suspend current thread */
			rt_ipc_list_suspend(&(mutex->parent.suspend_thread),
								thread,
								mutex->parent.parent.flag);

			/* has waiting time, start thread timer */
			if (time > 0)
			rt_hw_interrupt_enable(temp);
			rt_schedule();
	
```

rt_mutex_release
```

 mutex->hold --;
if (mutex->hold == 0)
	/* change the owner thread to original priority */
	if (mutex->original_priority != mutex->owner->current_priority)
	{
		rt_thread_control(mutex->owner,
						  RT_THREAD_CTRL_CHANGE_PRIORITY,
						  &(mutex->original_priority));
	}

	/* wakeup suspended thread */
	if (!rt_list_isempty(&mutex->parent.suspend_thread))
	{
		/* get suspended thread */
		thread = rt_list_entry(mutex->parent.suspend_thread.next,
							   struct rt_thread,
							   tlist);

		RT_DEBUG_LOG(RT_DEBUG_IPC, ("mutex_release: resume thread: %s\n",
									thread->name));

		/* set new owner and priority */
		mutex->owner             = thread;
		mutex->original_priority = thread->current_priority;
		mutex->hold ++;

		/* resume thread */
		rt_ipc_list_resume(&(mutex->parent.suspend_thread));

		need_schedule = RT_TRUE;
	}
	else
	{
		/* increase value */
		mutex->value ++;

		/* clear owner */
		mutex->owner             = RT_NULL;
		mutex->original_priority = 0xff;
	}
	
rt_hw_interrupt_enable(temp);

/* perform a schedule */
if (need_schedule == RT_TRUE)
	rt_schedule();
	
```

有两个线程, 线程1和线程2, 线程1对两个number分别进行加1操作; 线程2也对两个number分别进行加1操作, 使用互斥量保证线程改变两个number值的操作不被打断
## [[事件集]]
![](../fujian/Pasted%20image%2020250719104155.png)
```
struct rt_event
{
    struct rt_ipc_object parent;                        /**< inherit from ipc_object */

    rt_uint32_t          set;                           /**< event set */
};
typedef struct rt_event *rt_event_t;
```

rt_event_send

```
/* set event */
event->set |= set;

if (!rt_list_isempty(&event->parent.suspend_thread))
{
    /* search thread list to resume thread */
    n = event->parent.suspend_thread.next;
    while (n != &(event->parent.suspend_thread))
    {
        /* get thread */
        thread = rt_list_entry(n, struct rt_thread, tlist);

        status = -RT_ERROR;
        if (thread->event_info & RT_EVENT_FLAG_AND)
        {
            if ((thread->event_set & event->set) == thread->event_set)
            {
                /* received an AND event */
                status = RT_EOK;
            }
        }
        else if (thread->event_info & RT_EVENT_FLAG_OR)
        {
            if (thread->event_set & event->set)
            {
                /* save recieved event set */
                thread->event_set = thread->event_set & event->set;

                /* received an OR event */
                status = RT_EOK;
            }
        }

        /* move node to the next */
        n = n->next;

        /* condition is satisfied, resume thread */
        if (status == RT_EOK)
        {
            /* clear event */
            if (thread->event_info & RT_EVENT_FLAG_CLEAR)
                event->set &= ~thread->event_set;

            /* resume thread, and thread list breaks out */
            rt_thread_resume(thread);

            /* need do a scheduling */
            need_schedule = RT_TRUE;
        }
    }
}

/* enable interrupt */
rt_hw_interrupt_enable(level);

/* do a schedule */
if (need_schedule == RT_TRUE)
    rt_schedule();

```
## 使用场合 
它能够在一定程度上代替信号量, 用于线程间同步
但是它与信号量不同的是，事件的发送操作在事件未清除前是不可累计的;，而信号量的释放动作是累计的
事件的另一个特性是, 接收线程可等待多种事件, 即多'个事件对应一个线程或多个线程
# 线程通信 
## 邮箱
非阻塞方式的邮件发送过程能够安全地应用于中断服务中

邮件收取过程**可能是阻塞的**，这取决于邮箱中是否有邮件，以及收取邮件时设置的超时时间。
**当邮箱中不存在邮件且超时时间不为0时, 邮件收取过程将变成阻塞方式。在这类情况下，只能由线程进行邮件的收取。**

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
```
## 消息
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
```


# 组件
# io设备管理 
![](../fujian/Pasted%20image%2020250719104823.png)

设备驱动框架层是对同类硬件设备驱动的抽象，它将不同厂家的同类硬件设备驱动中相同的部分抽取出来

对于操作逻辑简单的设备，可以不经过设备驱动框架层，直接将设备注册到I/O设备管理器中
序列图如图13-2所示
	(1 ) 设备驱动根据设备模型定义, 创建出具备硬件访问能力的设备实例, 将该设备通过rt_device_register () 接口注册到I/O设备管理器中。 
	(2) 应用程序通过rt_device_find () 接口查找到设备, 然后使用I/O设备管理接口来访问硬件。
	![](../fujian/Pasted%20image%2020250719105013.png)

对于另一些设备，如看门狗等，则会将创建的设备实例先注册到对应的设备驱动框架中，再由设备驱动框架向I/O设备管理器进行注册
	![](../fujian/Pasted%20image%2020250719105110.png)

# 通用外设接口 