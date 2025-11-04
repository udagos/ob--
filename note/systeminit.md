---
same:
  - "[[SystemInit_ExtMemCtl]]"
---

这段代码是用C语言编写的，主要用于初始化STM32微控制器的系统配置。它通常在系统复位后运行，用于设置时钟、浮点单元（FPU）、中断向量表等关键硬件配置。以下是对代码的详细解析：

### 1. **浮点单元（FPU）配置**
```c
#if (__FPU_PRESENT == 1) && (__FPU_USED == 1)
    SCB->CPACR |= ((3UL << 10*2)|(3UL << 11*2));  /* set CP10 and CP11 Full Access */
#endif
```
- **功能**：启用浮点单元（FPU）。
- **条件**：
  - `__FPU_PRESENT`：表示硬件是否支持浮点单元。
  - `__FPU_USED`：表示是否在代码中使用了浮点运算。
- **操作**：
  - `SCB->CPACR` 是系统控制块（SCB）的 Coprocessor Access Control Register（CPACR）。
  - `((3UL << 10*2)|(3UL << 11*2))`：将 CP10 和 CP11 的访问权限设置为全访问（Full Access）。这允许代码使用浮点单元。

### 2. **重置RCC时钟配置**
```c
/* Set HSION bit */
RCC->CR |= (uint32_t)0x00000001;

/* Reset CFGR register */
RCC->CFGR = 0x00000000;

/* Reset HSEON, CSSON and PLLON bits */
RCC->CR &= (uint32_t)0xFEF6FFFF;

/* Reset PLLCFGR register */
RCC->PLLCFGR = 0x24003010;

/* Reset HSEBYP bit */
RCC->CR &= (uint32_t)0xFFFBFFFF;

/* Disable all interrupts */
RCC->CIR = 0x00000000;
```
- **功能**：将RCC（Reset and Clock Control）模块的时钟配置恢复到默认状态。
- **操作**：
  - **启用HSI（High-Speed Internal）时钟**：
    ```c
    RCC->CR |= (uint32_t)0x00000001;
    ```
    - 设置 `HSION` 位，启用内部高速时钟。
  - **重置 `CFGR` 寄存器**：
    ```c
    RCC->CFGR = 0x00000000;
    ```
    - 将时钟配置寄存器 `CFGR` 清零，恢复默认值。
  - **清除 `HSEON`、`CSSON` 和 `PLLON` 位**：
    ```c
    RCC->CR &= (uint32_t)0xFEF6FFFF;
    ```
    - 清除外部高速时钟（HSE）、时钟安全系统（CSS）和PLL使能位。
  - **重置 `PLLCFGR` 寄存器**：
    ```c
    RCC->PLLCFGR = 0x24003010;
    ```
    - 设置PLL配置寄存器的默认值。
  - **清除 `HSEBYP` 位**：
    ```c
    RCC->CR &= (uint32_t)0xFFFBFFFF;
    ```
    - 清除外部高速时钟旁路位。
  - **禁用所有中断**：
    ```c
    RCC->CIR = 0x00000000;
    ```
    - 清除中断和中断标志寄存器 `CIR`，禁用所有中断。

### 3. ==**外部存储器配置**==
```c
#if defined (DATA_IN_ExtSRAM) || defined (DATA_IN_ExtSDRAM)
  SystemInit_ExtMemCtl(); 
#endif /* DATA_IN_ExtSRAM || DATA_IN_ExtSDRAM */
```
- **功能**：如果定义了 `DATA_IN_ExtSRAM` 或 `DATA_IN_ExtSDRAM`，则调用 [[SystemInit_ExtMemCtl]] 函数。
- **条件**：
  - `DATA_IN_ExtSRAM`：表示数据存储在外部SRAM中。
  - `DATA_IN_ExtSDRAM`：表示数据存储在外部SDRAM中。
- **操作**：
  - 调用 `SystemInit_ExtMemCtl` 函数，用于初始化外部存储器控制器（FMC）。

### 4. **中断向量表配置**
```c
/* Configure the Vector Table location add offset address ------------------*/
#ifdef VECT_TAB_SRAM
  SCB->VTOR = SRAM_BASE | VECT_TAB_OFFSET; /* Vector Table Relocation in Internal SRAM */
#else
  SCB->VTOR = FLASH_BASE | VECT_TAB_OFFSET; /* Vector Table Relocation in Internal FLASH */
#endif
```
- **功能**：==配置中断向量表的位置==。
- **条件**：
  - `VECT_TAB_SRAM`：表示中断向量表存储在内部SRAM中。
  - ==默认情况下，中断向量表存储在内部FLASH中。==
- **操作**：
  - `SCB->VTOR` 是系统控制块（SCB）的 Vector Table Offset Register（VTOR）。
  - `SRAM_BASE` 和 `FLASH_BASE` 是宏定义，分别表示内部SRAM和==FLASH的基地址。==
  - ==`VECT_TAB_OFFSET` 是中断向量表的偏移地址。==
  - 根据条件，将中断向量表的地址设置为内部SRAM或FLASH的基地址加上偏移量。

### 总结
这段代码的主要功能是初始化STM32微控制器的系统配置，包括：
1. **浮点单元（FPU）**：启用浮点单元。
2. **时钟配置**：将RCC模块的时钟配置恢复到默认状态。
3. **外部存储器**：如果使用外部存储器，调用相关初始化函数。
4. **中断向量表**：配置中断向量表的位置。

这些操作确保微控制器在启动时处于一个已知的、安全的状态，并为后续的程序运行做好准备。