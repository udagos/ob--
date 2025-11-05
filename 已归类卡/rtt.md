---
up:
  - "[[../moc/MocRtos|MocRtos]]"
---

在 RT-Thread 中, 所有的数据结构都称之为对象。
每个对象都会有对应的一个结构体, 这个结构体叫做该对象的控制块。如线程会有一个线程控制块

这些控制块的开头都会包含一个内核对象结构体,或者直接将对象结构体的成员放在对象控制块结构体的开头。其中线程控制块的开头放置的就是对象结构体的成员

**创建一个对象，如线程，就会将这个对象放到一个叫做容器的地方**
什么是容器，从代码上看，容器就是一个数组，是一个全局变量，数据类型为 **structrt_object_information**，在 object. c 中定义
![[Pasted image 20240818100054.png]]

![[Pasted image 20240818100349.png]]
**容器的定义**
![[Pasted image 20240818100418.png]]
## ipc 
基类
![[Pasted image 20240818092523.png]]
``` c
/**
 * @addtogroup IPC
 */

/*@{*/

/**
 * This function will initialize an IPC object
 *
 * @param ipc the IPC object
 *
 * @return the operation status, RT_EOK on successful
 */
rt_inline rt_err_t rt_ipc_object_init(struct rt_ipc_object *ipc)
{
    /* init ipc object */
    rt_list_init(&(ipc->suspend_thread));

    return RT_EOK;
}

/**
 * This function will suspend a thread to a specified list. IPC object or some
 * double-queue object (mailbox etc.) contains this kind of list.
 *
 * @param list the IPC suspended thread list
 * @param thread the thread object to be suspended
 * @param flag the IPC object flag,
 *        which shall be RT_IPC_FLAG_FIFO/RT_IPC_FLAG_PRIO.
 *
 * @return the operation status, RT_EOK on successful
 */
rt_inline rt_err_t rt_ipc_list_suspend(rt_list_t        *list,
                                       struct rt_thread *thread,
                                       rt_uint8_t        flag)
{
    /* suspend thread */
    rt_thread_suspend(thread);

    switch (flag)
    {
    case RT_IPC_FLAG_FIFO:
        rt_list_insert_before(list, &(thread->tlist));
        break;

    case RT_IPC_FLAG_PRIO:
        {
            struct rt_list_node *n;
            struct rt_thread *sthread;

            /* find a suitable position */
            for (n = list->next; n != list; n = n->next)
            {
                sthread = rt_list_entry(n, struct rt_thread, tlist);

                /* find out */
                if (thread->current_priority < sthread->current_priority)
                {
                    /* insert this thread before the sthread */
                    rt_list_insert_before(&(sthread->tlist), &(thread->tlist));
                    break;
                }
            }

            /*
             * not found a suitable position,
             * append to the end of suspend_thread list
             */
            if (n == list)
                rt_list_insert_before(list, &(thread->tlist));
        }
        break;
    }

    return RT_EOK;
}

/**
 * This function will resume the first thread in the list of a IPC object:
 * - remove the thread from suspend queue of IPC object
 * - put the thread into system ready queue
 *
 * @param list the thread list
 *
 * @return the operation status, RT_EOK on successful
 */
rt_inline rt_err_t rt_ipc_list_resume(rt_list_t *list)
{
    struct rt_thread *thread;

    /* get thread entry */
    thread = rt_list_entry(list->next, struct rt_thread, tlist);

    RT_DEBUG_LOG(RT_DEBUG_IPC, ("resume thread:%s\n", thread->name));

    /* resume it */
    rt_thread_resume(thread);

    return RT_EOK;
}

/**
 * This function will resume all suspended threads in a list, including
 * suspend list of IPC object and private list of mailbox etc.
 *
 * @param list of the threads to resume
 *
 * @return the operation status, RT_EOK on successful
 */
rt_inline rt_err_t rt_ipc_list_resume_all(rt_list_t *list)
{
    struct rt_thread *thread;
    register rt_ubase_t temp;

    /* wakeup all suspend threads */
    while (!rt_list_isempty(list))
    {
        /* disable interrupt */
        temp = rt_hw_interrupt_disable();

        /* get next suspend thread */
        thread = rt_list_entry(list->next, struct rt_thread, tlist);
        /* set error code to RT_ERROR */
        thread->error = -RT_ERROR;

        /*
         * resume thread
         * In rt_thread_resume function, it will remove current thread from
         * suspend list
         */
        rt_thread_resume(thread);

        /* enable interrupt */
        rt_hw_interrupt_enable(temp);
    }

    return RT_EOK;
}
```
ipc 的基类
![[Pasted image 20240818092611.png]]

![[Pasted image 20240818092725.png]]
![[Pasted image 20240818103721.png]]
子类
![[Pasted image 20240818092513.png]]
![[Pasted image 20240818093721.png]]
实现
![[Pasted image 20240818103114.png]]



## rt_object_information 的引用


rt_hw_serial_register 
	rt_device_register 
		rt_device_find
			**rt_object_information**

rt_object_init 
	rt_object_information
# thread 
## 创建线程
这些控制块的开头都会包含一个内核对象结构体, 或者直接将对象结构体的成员放在对象控制块结构体的开头  
![[Pasted image 20240818102941.png]]
![[Pasted image 20240818103509.png]]


### 链表相关
初始化线程链表节点，往后我们要把线程插入到各种链表中，就是通过这个节点来实现的
### 初始化线程栈
所以要为每个线程都分配独立的栈空间，这个栈空间通常是一个预先定义好的全局数组，也可以是动态分配的一段内存空间，但它们都存在于 RAM 中
![[Pasted image 20240818111115.png]]
#### 寄存器
![[Pasted image 20240818110829.png]]
## 实现就绪列表
线程创建好之后, 我们需要把线程添加到就绪列表里面, 表示线程已经就绪, 系统随时可以调度

![[Pasted image 20240818111548.png]]
数组的下标对应了线程的优先级
同一优先级的线程统一插入到就绪列表的同一条链表中
### 将线程插入到就绪列表
rt_list_insert_before
## 实现调度器
主要功能就是实现线程的切换, 即从就绪列表里面找到优先级最高的线程, 然后去执行该线程
![[Pasted image 20240818112015.png]]
### 初始化调度器
rt_system_scheduler_init

rt_current_thread 是在 scheduler. c 中定义的一个 structrt_thread 类型的全**局指针，用于指向当前正在运行的线程的线程控制块**

### 启动调度器
rt_system_scheduler_start
	rt_hw_context_switch_to //第一次线程切换
		PendSV_Handler
PendSV_Handler ()函数是真正实现线程上下文切换的地方

调度器在启动的时候会从就绪列表中取出优先级最高的线程的线程控制块, 然后切换到该线程

rt_list_entry()是一个已知一个结构体里面的成员的地址，反推出该结构体的首地址的宏


### 系统调度 
系统调度就是在就绪列表中寻找优先级最高的就绪线程，然后去执行该线程。
 rt_schedule 
	 rt_hw_contex_switch
		 PendSVHandler

rt_hw_contex_switch ()函数用于产生上下文切换


目前线程还没有是实现优先级
# 空闲线程和阻塞延时
之前, 线程体内的延时使用的是软件延时, 即还是让 CPU 空等来达到延时的效果
RTOS 中的延时叫阻塞延时，线程需要延时时会放弃 CPU 的使用权

当线程**需要延时，进入阻塞状态，如果没有其它线程可以运行，RTOS 都会为 CPU 创建一个空闲线程，这个时候 CPU 就运行空闲线程**
空闲线程主体主要是做一些系统内存的清理工作。我们本章实现的空闲线程只是对一个全局变量进行计数
在实际应用中，当系统进入空闲线程的时候，可在空闲线程中让单片机进入休眠或者低功耗等操作。


空闲线程创建和普通线程一样 
## 阻塞延时
![[Pasted image 20240818143847.png]]
调用系统调度
![[Pasted image 20240818144452.png]]
![[Pasted image 20240818144520.png]]
![[Pasted image 20240818144534.png]]
## SysTick_Handler 中断服务函数
那么 remaining_tick 在哪里递减？
这个周期由 SysTick 中断提供，SysTick 中断服务函数我们放在 main. c 中实现
![[Pasted image 20240818150321.png]]
![[Pasted image 20240818150327.png]]
关中断。在程序开始的时候把中断关闭是一个好习惯, 等系统初始化完毕, 线程创建完毕, 启动系统调度的时候会重新打开中断。
**如果一开始不关闭中断的话, 接下来 SysTick 初始化完成, 然后再初始化系统和创建线程, 如果系统初始化和线程创建的时间大于 SysTick 的中断周期的话, 那么就会出现系统或者线程都还没有准备好的情况下就先执行了 SysTick 中断服务函数, 进行了系统调度, 显然,这是不科学的**

这个中断服务函数可能是 m3 内核的，我们的工程并没有？


代码清单 9-11 (1): 中断计数器, 是一个全局变量, 用了记录中断嵌套次数。
代码清单 9-11 (2): 当 BSP 文件的中断服务函数进入时会调用该函数, 应用程序不能调用, 切记。
代码清单 9-11 (3): 当 BSP 文件的中断服务函数离开时会调用该函数, 应用程序不能调用,切记。？




## main
![[Pasted image 20240818151420.png]]
![[Pasted image 20240818151439.png]]
![[Pasted image 20240818151454.png]]
![[Pasted image 20240818151326.png]]
# 支持优先级的线程
