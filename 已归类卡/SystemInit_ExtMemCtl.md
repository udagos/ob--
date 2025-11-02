---
up:
  - "[[../inbox/cotex|cotex]]"
---


```
void SystemInit_ExtMemCtl(void)

{

  __IO uint32_t tmp = 0x00;

  

  register uint32_t tmpreg = 0, timeout = 0xFFFF;

  register __IO uint32_t index;

  

  /* Enable GPIOC, GPIOD, GPIOE, GPIOF, GPIOG, GPIOH and GPIOI interface clock */

  RCC->AHB1ENR |= 0x000001F8;

  

  /* Delay after an RCC peripheral clock enabling */

  tmp = READ_BIT(RCC->AHB1ENR, RCC_AHB1ENR_GPIOCEN);

  /* Connect PDx pins to FMC Alternate function */

  GPIOD->AFR[0]  = 0x00CCC0CC;

  GPIOD->AFR[1]  = 0xCCCCCCCC;

  /* Configure PDx pins in Alternate function mode */  

  GPIOD->MODER   = 0xAAAA0A8A;

  /* Configure PDx pins speed to 100 MHz */  

  GPIOD->OSPEEDR = 0xFFFF0FCF;

  /* Configure PDx pins Output type to push-pull */  

  GPIOD->OTYPER  = 0x00000000;

  /* No pull-up, pull-down for PDx pins */

  GPIOD->PUPDR   = 0x00000000;

  

  /* Connect PEx pins to FMC Alternate function */

  GPIOE->AFR[0]  = 0xC00CC0CC;

  GPIOE->AFR[1]  = 0xCCCCCCCC;

  /* Configure PEx pins in Alternate function mode */

  GPIOE->MODER   = 0xAAAA828A;

  /* Configure PEx pins speed to 100 MHz */

  GPIOE->OSPEEDR = 0xFFFFC3CF;

  /* Configure PEx pins Output type to push-pull */  

  GPIOE->OTYPER  = 0x00000000;

  /* No pull-up, pull-down for PEx pins */

  GPIOE->PUPDR   = 0x00000000;

  /* Connect PFx pins to FMC Alternate function */

  GPIOF->AFR[0]  = 0xCCCCCCCC;

  GPIOF->AFR[1]  = 0xCCCCCCCC;

  /* Configure PFx pins in Alternate function mode */  

  GPIOF->MODER   = 0xAA800AAA;

  /* Configure PFx pins speed to 50 MHz */

  GPIOF->OSPEEDR = 0xAA800AAA;

  /* Configure PFx pins Output type to push-pull */  

  GPIOF->OTYPER  = 0x00000000;

  /* No pull-up, pull-down for PFx pins */

  GPIOF->PUPDR   = 0x00000000;

  

  /* Connect PGx pins to FMC Alternate function */

  GPIOG->AFR[0]  = 0xCCCCCCCC;

  GPIOG->AFR[1]  = 0xCCCCCCCC;

  /* Configure PGx pins in Alternate function mode */

  GPIOG->MODER   = 0xAAAAAAAA;

  /* Configure PGx pins speed to 50 MHz */

  GPIOG->OSPEEDR = 0xAAAAAAAA;

  /* Configure PGx pins Output type to push-pull */  

  GPIOG->OTYPER  = 0x00000000;

  /* No pull-up, pull-down for PGx pins */

  GPIOG->PUPDR   = 0x00000000;

  /* Connect PHx pins to FMC Alternate function */

  GPIOH->AFR[0]  = 0x00C0CC00;

  GPIOH->AFR[1]  = 0xCCCCCCCC;

  /* Configure PHx pins in Alternate function mode */

  GPIOH->MODER   = 0xAAAA08A0;

  /* Configure PHx pins speed to 50 MHz */

  GPIOH->OSPEEDR = 0xAAAA08A0;

  /* Configure PHx pins Output type to push-pull */  

  GPIOH->OTYPER  = 0x00000000;

  /* No pull-up, pull-down for PHx pins */

  GPIOH->PUPDR   = 0x00000000;

  /* Connect PIx pins to FMC Alternate function */

  GPIOI->AFR[0]  = 0xCCCCCCCC;

  GPIOI->AFR[1]  = 0x00000CC0;

  /* Configure PIx pins in Alternate function mode */

  GPIOI->MODER   = 0x0028AAAA;

  /* Configure PIx pins speed to 50 MHz */

  GPIOI->OSPEEDR = 0x0028AAAA;

  /* Configure PIx pins Output type to push-pull */  

  GPIOI->OTYPER  = 0x00000000;

  /* No pull-up, pull-down for PIx pins */

  GPIOI->PUPDR   = 0x00000000;

/*-- FMC Configuration -------------------------------------------------------*/

  /* Enable the FMC interface clock */

  RCC->AHB3ENR |= 0x00000001;

  /* Delay after an RCC peripheral clock enabling */

  tmp = READ_BIT(RCC->AHB3ENR, RCC_AHB3ENR_FMCEN);

  

  FMC_Bank5_6->SDCR[0] = 0x000019E4;

  FMC_Bank5_6->SDTR[0] = 0x01115351;      

  /* SDRAM initialization sequence */

  /* Clock enable command */

  FMC_Bank5_6->SDCMR = 0x00000011;

  tmpreg = FMC_Bank5_6->SDSR & 0x00000020;

  while((tmpreg != 0) && (timeout-- > 0))

  {

    tmpreg = FMC_Bank5_6->SDSR & 0x00000020;

  }

  

  /* Delay */

  for (index = 0; index<1000; index++);

  /* PALL command */

  FMC_Bank5_6->SDCMR = 0x00000012;          

  timeout = 0xFFFF;

  while((tmpreg != 0) && (timeout-- > 0))

  {

    tmpreg = FMC_Bank5_6->SDSR & 0x00000020;

  }

  /* Auto refresh command */

  FMC_Bank5_6->SDCMR = 0x00000073;

  timeout = 0xFFFF;

  while((tmpreg != 0) && (timeout-- > 0))

  {

    tmpreg = FMC_Bank5_6->SDSR & 0x00000020;

  }

  /* MRD register program */

  FMC_Bank5_6->SDCMR = 0x00046014;

  timeout = 0xFFFF;

  while((tmpreg != 0) && (timeout-- > 0))

  {

    tmpreg = FMC_Bank5_6->SDSR & 0x00000020;

  }

  /* Set refresh count */

  tmpreg = FMC_Bank5_6->SDRTR;

  FMC_Bank5_6->SDRTR = (tmpreg | (0x0000027C<<1));

  /* Disable write protection */

  tmpreg = FMC_Bank5_6->SDCR[0];

  FMC_Bank5_6->SDCR[0] = (tmpreg & 0xFFFFFDFF);

  

#if defined(STM32F427xx) || defined(STM32F437xx) || defined(STM32F429xx) || defined(STM32F439xx)

  /* Configure and enable Bank1_SRAM2 */

  FMC_Bank1->BTCR[2]  = 0x00001011;

  FMC_Bank1->BTCR[3]  = 0x00000201;

  FMC_Bank1E->BWTR[2] = 0x0fffffff;

#endif /* STM32F427xx || STM32F437xx || STM32F429xx || STM32F439xx */

#if defined(STM32F469xx) || defined(STM32F479xx)

  /* Configure and enable Bank1_SRAM2 */

  FMC_Bank1->BTCR[2]  = 0x00001091;

  FMC_Bank1->BTCR[3]  = 0x00110212;

  FMC_Bank1E->BWTR[2] = 0x0fffffff;

#endif /* STM32F469xx || STM32F479xx */

  

  (void)(tmp);

}
```
这是一个用于STM32微控制器的外部存储器控制器初始化函数，主要配置FMC（Flexible Memory Controller）接口以连接外部SDRAM和SRAM。以下是中文解析：

1. GPIO配置部分：
- 使能GPIOC-I的时钟（AHB1总线）
- 将PD-PI端口引脚配置为FMC复用功能：
  * 设置AFR（复用功能寄存器）选择FMC功能
  * 配置MODER为复用模式
  * 设置OSPEEDR速度 (100MHz或50MHz)
  * 配置OTYPER为推挽输出
  * 禁用PUPDR的上拉/下拉

2. FMC控制器配置：
- 使能FMC时钟（AHB3总线）
- 配置SDRAM控制寄存器 (SDCR) 和时序寄存器 (SDTR)

3. SDRAM初始化序列：
- 发送时钟使能命令 (0x11)
- 发送预充电命令 (0x12)
- 发送自动刷新命令 (0x73)
- 设置模式寄存器 (0x46014)
- 配置刷新定时器
- 禁用写保护

4. 附加SRAM配置（根据型号）：
- 对于F427/437/429/439系列：配置Bank1 SRAM2
- 对于F469/479系列：不同的SRAM2配置参数

这个函数是STM32 HAL库中用于外部存储器初始化的典型实现，通过精确的时序控制和寄存器配置确保外部存储器正常工作。使用时需要注意：
1. 必须与硬件设计匹配（引脚连接、存储器型号等）
2. 不同STM32系列可能需要调整参数
3. 初始化序列的时序要求严格，不要随意修改延时

对于具体应用，建议参考对应型号的参考手册和硬件设计检查这些配置值是否适合您的硬件。

# 1
在STM32的FMC（Flexible Memory Controller）控制器中，**地址的配置**主要涉及以下几个方面：

---

## **1. FMC 存储区域划分（Bank 地址分配）**
FMC 将外部存储器划分为不同的 **Bank**，每个 Bank 有固定的基地址，具体如下：

| **Bank**  | **存储器类型**       | **起始地址**      | **典型用途**         |
|-----------|---------------------|------------------|---------------------|
| Bank1     | NOR/PSRAM/SRAM      | `0x6000 0000`    | 外部 SRAM/NOR Flash  |
| Bank2     | NAND Flash          | `0x7000 0000`    | NAND 存储器          |
| Bank3     | NAND Flash          | `0x8000 0000`    | 另一个 NAND 存储器   |
| Bank5~6   | SDRAM               | `0xC000 0000`    | 外部 SDRAM（16/32位）|

在您的代码中：
- ==**SDRAM** 使用的是 **Bank5~6**，基地址是 `0xC000 0000`。==
- **SRAM2**（如果启用）位于 **Bank1**，地址由 `BTCR[2/3]` 配置。

---

## **2. SDRAM 地址配置（Bank5~6）**
SDRAM 的地址配置主要通过 **`SDCR`（控制寄存器）和 `SDTR`（时序寄存器）** 进行设置：

### **(1) `SDCR[0]`（SDRAM 控制寄存器）**
```c
FMC_Bank5_6->SDCR[0] = 0x000019E4;
```
- **`0x000019E4`** 的位域解析：
  - **`NC` (bit2:0)**：列地址位数（`001` = 8位，`010` = 9位，`011` = 10位）
  - **`NR` (bit4:3)**：行地址位数（`00` = 11位，`01` = 12位，`10` = 13位）
  - **`MWID` (bit6:5)**：数据总线宽度（`00` = 8位，`01` = 16位，`10` = 32位）
  - **`NB` (bit7)**：Bank 数量（`0` = 2个Bank，`1` = 4个Bank）
  - **`CAS` (bit9:8)**：CAS 延迟（`01` = 2个周期，`10` = 3个周期）
  - **`WP` (bit10)**：写保护（`0` = 禁用，`1` = 启用）
  - **`SDCLK` (bit12:11)**：时钟分频（`00` = 禁用，`01` = 2分频，`10` = 3分频）

### **(2) `SDTR[0]`（SDRAM 时序寄存器）**
```c
FMC_Bank5_6->SDTR[0] = 0x01115351;
```
- **`0x01115351`** 的位域解析：
  - **`TMRD` (bit3:0)**：加载模式寄存器到激活命令的延迟（通常 `2` 个周期）
  - **`TXSR` (bit7:4)**：自刷新退出时间（例如 `9` 个周期）
  - **`TRAS` (bit11:8)**：行激活时间（例如 `7` 个周期）
  - **`TRC` (bit15:12)**：行周期时间（例如 `9` 个周期）
  - **`TWR` (bit19:16)**：写恢复时间（例如 `2` 个周期）
  - **`TRP` (bit23:20)**：行预充电时间（例如 `2` 个周期）
  - **`TRCD` (bit27:24)**：行到列延迟（例如 `2` 个周期）

---

## **3. SRAM 地址配置（Bank1）**
如果启用了 SRAM2（如 `STM32F429`），则通过 **`BTCR[2]` 和 `BTCR[3]`** 配置：
```c
FMC_Bank1->BTCR[2] = 0x00001011;  // SRAM/NOR 控制寄存器
FMC_Bank1->BTCR[3] = 0x00000201;  // SRAM/NOR 时序寄存器
```
- **`BTCR[2]`** 配置：
  - **`ADDSET` (bit3:0)**：地址建立时间（`1` 个周期）
  - **`DATAST` (bit11:8)**：数据保持时间（`1` 个周期）
  - **`BUSTURN` (bit19:16)**：总线恢复时间（`0` 个周期）
- **`BTCR[3]`** 配置：
  - **`ACCMOD` (bit1:0)**：访问模式（`01` = 模式A，`10` = 模式B）
  - **`DATLAT` (bit7:4)**：数据延迟（`2` 个周期）

==SRAM2 的地址通常映射到 **`0x6000 0000`**（Bank1）==。

---

## **4. 如何计算 SDRAM/SRAM 的地址范围？**
- **SDRAM（Bank5~6）**：
  - 基地址：`0xC000 0000`
  - 大小取决于硬件连接（如 `8MB`、`16MB`）
  - 例如，如果使用 `16MB` SDRAM，地址范围是 `0xC000 0000` ~ `0xC0FF FFFF`。

- **SRAM（Bank1）**：
  - 基地址：`0x6000 0000`
  - 大小由 `BTCR` 配置（如 `1MB`，地址范围 `0x6000 0000` ~ `0x600F FFFF`）。

---

## **5. 如何访问外部存储器？**
配置完成后，可以直接通过指针访问：
```c
// 访问 SDRAM（Bank5~6）
uint32_t *sdram = (uint32_t*)0xC0000000;
sdram[0] = 0x12345678;  // 写入数据
uint32_t data = sdram[0];  // 读取数据

// 访问 SRAM（Bank1）
uint32_t *sram = (uint32_t*)0x60000000;
sram[0] = 0xABCD1234;
```

---

## **6. 关键注意事项**
1. **硬件连接必须匹配**：
   - SDRAM 的 **行/列地址位数** 必须与 `SDCR` 配置一致。
   - **数据总线宽度（16位/32位）** 必须与硬件一致。
   
2. **时序参数**：
   - `SDTR` 和 `BTCR` 的时序必须符合存储器芯片的规格（查阅芯片手册）。

3. **初始化顺序**：
   - SDRAM 必须按照 **时钟使能 → 预充电 → 自动刷新 → 模式寄存器设置** 的顺序初始化。

4. **不同 STM32 型号可能有差异**：
   - 例如 `STM32F429` 和 `STM32F7` 的 FMC 配置可能略有不同。

---

## **总结**
| **配置项**       | **寄存器**       | **关键参数**                     | **典型值示例** |
|------------------|------------------|--------------------------------|--------------|
| **SDRAM 控制**   | `SDCR[0]`        | 行/列地址位数、数据宽度、CAS 延迟 | `0x000019E4` |
| **SDRAM 时序**   | `SDTR[0]`        | 行预充电时间、自刷新时间等       | `0x01115351` |
| **SRAM 控制**    | `BTCR[2]`        | 地址建立时间、数据保持时间       | `0x00001011` |
| **SRAM 时序**    | `BTCR[3]`        | 访问模式、数据延迟               | `0x00000201` |

如果你的硬件连接不同（比如 SDRAM 是 16 位数据总线），需要调整 `SDCR` 的 `MWID` 位。建议结合 **存储器芯片的数据手册** 和 **STM32 参考手册** 进行精确配置。

# sct
在STM32开发中，**sct文件**（Scatter-Loading Description File，分散加载文件）用于**自定义代码和数据在内存中的布局**，通常用于ARM编译工具链（如Keil MDK、ARM GCC）。它定义了程序如何分布在Flash、RAM等存储区域，尤其在复杂内存管理（如多块Flash/SRAM、外部存储器）时至关重要。

---

### **1. sct文件的核心作用**
- **指定代码/数据的存放位置**（Flash、SRAM、外部SDRAM等）。
- **控制栈、堆的分配**。
- **处理多块非连续内存**（如STM32H7的ITCM/DTCM/AXI SRAM）。
- **支持Bootloader+App的分区设计**。

---

### **2. STM32典型的sct文件结构**
以Keil MDK的默认 `sct` 文件为例：
```scatter
LR_IROM1 0x08000000 0x00100000 {    ; 加载区域（Flash起始地址+大小）
  ER_IROM1 0x08000000 0x00100000 {  ; 执行区域（Flash）
    *.o (RESET, +First)             ; 首先存放中断向量表
    *(InRoot$$Sections)             ; 标准库需要的段
    .ANY (+RO)                      ; 所有只读代码和常量
  }
  RW_IRAM1 0x20000000 0x00030000 {  ; 执行区域（SRAM）
    .ANY (+RW +ZI)                  ; 全局变量、栈、堆等
  }
}
```

#### **关键字段解析**
| **字段**          | **说明**                                                                 |
|-------------------|-------------------------------------------------------------------------|
| `LR_IROM1`        | **加载区域**（Load Region），定义Flash的起始地址和大小。                  |
| `ER_IROM1`        | **执行区域**（Execution Region），代码实际运行的地址（通常与加载地址相同）。|
| `RESET, +First`   | 强制将中断向量表放在Flash起始位置（0x0800 0000）。                         |
| `InRoot$$Sections` | ARM标准库需要的特殊段（如 `__main.o` 的初始化代码）。                       |
| `.ANY (+RO)`      | 所有只读（Read-Only）代码和常量（如 `.text`、`.constdata`）。              |
| `RW_IRAM1`        | 可读写数据（RAM）区域，存放全局变量（`.data`）、未初始化变量（`.bss`）。   |
| `+RW +ZI`         | `+RW`：已初始化变量；`+ZI`：未初始化变量（Zero-Initialized）。            |

---

### **3. 常见自定义配置场景**

#### **(1) 将代码放到外部Flash（如QSPI Flash）**
```scatter
LR_IROM1 0x08000000 0x00200000 {      ; 内部Flash（2MB）
  ER_IROM1 0x08000000 0x00200000 {
    *.o (RESET, +First)
    *(InRoot$$Sections)
  }
}

LR_IROM2 0x90000000 0x00800000 {       ; 外部QSPI Flash（8MB）
  ER_IROM2 0x90000000 0x00800000 {
    .ANY (+RO)                         ; 将大部分代码放到外部Flash
  }
}

RW_IRAM1 0x20000000 0x00050000 {       ; 内部SRAM（320KB）
  .ANY (+RW +ZI)
}
```

#### **(2) 使用外部SDRAM（如Bank5~6）**
```scatter
RW_IRAM2 0xC0000000 0x01000000 {       ; 外部SDRAM（16MB）
  .ANY (EXTERNAL_RAM)                  ; 手动指定的数据段
  heap.o (+ZI)                         ; 堆区放在SDRAM
}
```

#### **(3) Bootloader + App 分区**
```scatter
/* Bootloader (占用前64KB Flash) */
LR_IROM1 0x08000000 0x00010000 {
  ER_IROM1 0x08000000 0x00010000 {
    bootloader.o (+RO)
  }
}

/* Application (从64KB偏移开始) */
LR_IROM2 0x08010000 0x000F0000 {
  ER_IROM2 0x08010000 0x000F0000 {
    *.o (RESET, +First)
    *(InRoot$$Sections)
    .ANY (+RO)
  }
  RW_IRAM1 0x20000000 0x00030000 {
    .ANY (+RW +ZI)
  }
}
```

---

### **4. 关键注意事项**
1. **中断向量表位置**  
   - 必须保证 `RESET` 段在**0x0800 0000**（或重映射后的地址），否则CPU无法启动。

2. **堆栈分配**  
   - 默认情况下，栈（Stack）和堆（Heap）由启动文件定义，但可在 `sct` 中显式指定：
     ```scatter
     ARM_LIB_STACK 0x20020000 EMPTY 0x1000 {}  ; 栈区
     ARM_LIB_HEAP 0x20021000 EMPTY 0x2000 {}   ; 堆区
     ```

3. **变量强制指定地址**  
   - 通过 `__attribute__((section("EXTERNAL_RAM")))` 将变量固定到SDRAM：
     ```c
     uint8_t buffer[1024] __attribute__((section("EXTERNAL_RAM")));
     ```

4. **多块RAM的优化使用**  
   - 在STM32H7等有多块RAM的芯片中，可分开分配：
     ```scatter
     RW_ITCM 0x00000000 0x00010000 {   ; ITCM（高速RAM）
       *(.fast_code)                   ; 关键中断服务函数
     }
     RW_AXI_SRAM 0x24000000 0x00080000 {
       .ANY (+RW +ZI)
     }
     ```

---

### **5. 如何检查sct配置是否生效？**
- **查看生成的map文件**（编译后生成的 `.map` 文件），确认各段地址是否符合预期。
- **通过调试器读取内存**（如STM32CubeIDE的Memory Browser），验证数据位置。

---

### **总结**
| **配置需求**           | **sct文件关键操作**                              |
|-----------------------|-----------------------------------------------|
| 默认Flash+RAM布局      | 使用IDE自动生成的sct文件即可。                   |
| 外部存储器扩展         | 添加新的 `LR_IROM` 或 `RW_IRAM` 区域。              |
| Bootloader分区        | 分两个 `LR_IROM` 区域，设置不同起始地址。          |
| 关键代码放高速RAM      | 定义独立的执行区域（如ITCM）。                   |
| 变量固定到特定地址     | 结合 `__attribute__` 和自定义Section。            |

sct文件是**内存布局的“地图”**，合理配置可优化性能（如将频繁访问的数据放TCM RAM）或扩展存储空间（如QSPI Flash）。