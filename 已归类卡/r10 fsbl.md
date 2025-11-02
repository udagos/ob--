---
up:
  - "[[../moc/work|work]]"
---



好的，我已经详细阅读了这五个核心文件。通过分析，我可以清晰地描绘出这个第一阶段引导加载程序（FSBL）的完整工作流程。

总的来说，FSBL 的核心任务是**初始化Zynq芯片的处理器系统（PS）和必要的外设，然后从一个非易失性存储设备（如QSPI Flash或SD卡）中加载一个或多个后续的软件镜像（如FPGA比特流或应用程序），最后将控制权交给加载的应用程序**。

下面我将为您详细分解其工作流程，并创建一个计划来总结这些信息。

### FSBL 工作流程分析

1.  **`main.c` - 主流程控制**
    *   **入口点**: `main()` 函数是整个程序的起点。
    *   **硬件初始化**:
        *   调用 [`ps7_init()`](ps7_init.c:10932) 函数。这是最关键的第一步，它负责初始化PS端的核心部分，包括：
            *   MIO (Multi-use I/O) 引脚复用。
            *   PLLs (锁相环) 以生成正确的系统时钟。
            *   DDR 内存控制器。
        *   初始化PCAP（处理器配置访问端口），这是用于对FPGA（PL部分）进行编程的接口。
        *   初始化看门狗定时器以防止系统死锁。
    *   **启动模式检测**:
        *   通过读取 `BOOT_MODE_REG` 寄存器，FSBL 判断系统是从哪个设备启动的，例如 QSPI Flash ([`QSPI_MODE`](fsbl.h:383))、NAND Flash、SD 卡 ([`SD_MODE`](fsbl.h:386)) 或 JTAG ([`JTAG_MODE`](fsbl.h:382))。
    *   **设备驱动初始化**:
        *   根据检测到的启动模式，调用相应的初始化函数，如 [`InitQspi()`](qspi.c)、[`InitNand()`](nand.c) 或 [`InitSD()`](sd.c)。
        *   它设置一个名为 [`MoveImage`](image_mover.c:127) 的函数指针，使其指向特定于设备的读取函数，如 [`QspiFlashRead`](qspi.c) 或 [`SDAccess`](sd.c)。这是一种很好的抽象，使得上层代码无需关心底层存储介质。
    *   **加载启动镜像**:
        *   调用 [`image_mover.c`](image_mover.c) 中的 [`LoadBootImage()`](image_mover.c:161) 函数。这是处理启动镜像（通常是 `BOOT.BIN`）的核心。
    *   **执行自定义应用**:
        *   在正式交接之前，它调用了一个名为 [`Application()`](main.c:716) 的函数。这个函数看起来是用户自定义的，用于初始化GPIO、点亮LED以及配置FPGA，这是对标准FSBL流程的一个重要扩展。
    *   **交接控制权**:
        *   调用 [`FsblHandoff()`](main.c:749) 函数，该函数最终会跳转到 [`fsbl_handoff.S`](fsbl_handoff.S) 中的汇编代码，将CPU的控制权交给加载的应用程序。

2.  **`image_mover.c` - 镜像解析与加载**
    *   **解析分区**: [`LoadBootImage()`](image_mover.c:161) 函数首先会寻找并解析镜像中的分区头（Partition Header）。一个启动镜像可以包含多个分区。
    *   **遍历分区**: 它会遍历所有的分区，对每一个分区进行处理。
    *   **验证与安全**:
        *   **校验和**: 如果分区头中标记了需要校验和，它会使用MD5算法计算分区的校验和并与头部信息进行比对。
        *   **RSA签名**: 如果分区被签名，它会使用RSA算法进行验签，以确保分区的完整性和来源的可靠性。
        *   **解密**: 如果分区被加密，它会调用解密程序。
    *   **分区加载**:
        *   **FPGA比特流 (PL)**: 如果分区是比特流，FSBL会通过PCAP将其加载到FPGA（PL）中进行编程。
        *   **应用程序 (PS)**: 如果分区是应用程序，FSBL会将其从启动设备复制到DDR内存中指定的加载地址。
    *   **确定执行地址**: FSBL会记录下第一个应用程序分区的执行地址，以便最后跳转。

3.  **`ps7_init.c` - 底层硬件配置**
    *   这个文件是由Xilinx工具自动生成的，包含了大量的寄存器地址和配置值，用于对PS进行精确的初始化。
    *   它根据芯片的硅片版本（Silicon Version）选择不同的配置数组，确保了对不同版本芯片的兼容性。
    *   [`ps7_init()`](ps7_init.c:10932) 函数是这些配置的执行者，它将Zynq芯片从上电复位状态配置到可以运行软件的状态。

4.  **`fsbl_handoff.S` - 控制权交接**
    *   这是一个汇编文件，负责执行CPU状态的最后清理和跳转。
    *   **清理工作**: 在跳转到应用程序之前，它会：
        *   使指令缓存（I-Cache）和分支预测器无效。
        *   禁用I-Cache和MMU（内存管理单元）。
    *   **跳转**: 最后，它使用 `bx` (Branch and Exchange) 指令，将程序计数器（PC）设置为应用程序的入口地址，从而完成控制权的交接。此后，FSBL的使命便告完成。



### FSBL 工作流程分析报告

#### 1. 总体概述

此FSBL（第一阶段引导加载程序）是为Xilinx Zynq-7000系列SoC设计的。其核心职责是在系统上电或复位后，对处理器系统（PS）进行基础的硬件初始化，包括时钟、DDR内存和MIO（多功能IO）。初始化完成后，它会根据预设的启动模式（如QSPI、NAND、SD卡），从相应的非易失性存储设备中加载一个启动镜像（通常是 `BOOT.BIN`）。

该启动镜像包含一个或多个分区。FSBL会逐一解析这些分区：
*   **如果是FPGA比特流**，FSBL会通过PCAP接口将其配置到可编程逻辑（PL）部分。
*   **如果是应用程序**，FSBL会将其加载到DDR内存中。

FSBL支持对分区进行**MD5校验和验证**和**RSA签名认证**，以确保镜像的完整性和安全性。完成所有分区的加载和验证后，FSBL会执行一个用户自定义的应用程序（[`Application()`](main.c:716) 函数），该函数负责初始化特定的外设，如GPIO和LED，并配置FPGA。最后，FSBL将CPU的控制权移交给加载到DDR中的主应用程序，从而完成引导过程。

#### 2. 详细执行步骤

FSBL的执行流程可以分解为以下几个关键步骤：

1.  **硬件初始化 ([`main.c:249`](main.c:249))**
    *   调用 [`ps7_init()`](ps7_init.c:10932) 函数，该函数是底层硬件配置的核心。它根据芯片版本（1.0, 2.0, 或 3.0+）选择合适的配置数据。
    *   **初始化PLL**：配置ARM、DDR和IO的锁相环，为系统提供稳定的时钟源。
    *   **初始化时钟**：设置各个模块的时钟频率。
    *   **初始化DDR**：配置DDR控制器和PHY，使DDR内存可用。
    *   **初始化MIO**：配置引脚复用，将物理引脚连接到所需的内部外设。
    *   初始化PCAP控制器，为后续加载FPGA比特流做准备。
    *   初始化看门狗定时器，以防止系统在引导过程中挂起。

2.  **启动模式检测与设备初始化 ([`main.c:388`](main.c:388))**
    *   读取 `BOOT_MODE_REG` 寄存器以确定启动源（QSPI, NAND, SD, JTAG等）。
    *   根据启动模式，调用相应的初始化函数，例如 [`InitQspi()`](qspi.c)或[`InitSD()`](sd.c)。
    *   设置 [`MoveImage`](image_mover.c:127) 函数指针，使其指向对应存储设备的读取函数。这使得上层代码可以透明地从不同设备读取数据。

3.  **加载和解析启动镜像 ([`main.c:570`](main.c:570), [`image_mover.c:161`](image_mover.c:161))**
    *   调用 [`LoadBootImage()`](image_mover.c:161) 函数开始处理 `BOOT.BIN`。
    *   `GetPartitionHeaderInfo()` 函数被调用，以读取并解析镜像中的所有分区头信息，并将它们存储在 `PartitionHeader` 数组中。
    *   FSBL会遍历 `PartitionHeader` 数组中的每一个分区。

4.  **分区处理循环 ([`image_mover.c:301`](image_mover.c:301))**
    *   对于每个分区，FSBL会：
        *   **验证头部信息**：检查分区头的校验和，确保其未损坏。
        *   **属性判断**：解析分区属性，判断其是FPGA比特流还是应用程序，以及是否加密或签名。
        *   **安全验证**：
            *   如果分区有签名（`SignedPartitionFlag`），则调用 `AuthenticatePartition()` 进行RSA验签。
            *   如果分区有校验和（`PartitionChecksumFlag`），则调用 `ValidateParition()` 进行MD5校验。
        *   **加载分区**：
            *   调用 `PartitionMove()` 函数将分区数据从启动设备移动到内存。
            *   对于非线性设备（如NAND/SD），数据首先被读到DDR的临时区域。对于线性设备（如QSPI），可以直接通过PCAP传输。
            *   如果分区是比特流，最终通过 `PcapLoadPartition()` 加载到FPGA。
            *   如果分区是应用程序，它被加载到其在DDR中指定的 `LoadAddr`。
        *   **解密**：如果分区是加密的，在验证后通过 `DecryptPartition()` 进行解密。

5.  **自定义应用逻辑 ([`main.c:716`](main.c:716))**
    *   在将控制权交给主应用程序之前，会调用一个名为 [`Application()`](main.c:716) 的自定义函数。
    *   在此项目中，此函数执行了以下操作：
        *   `GpioAppInit()`: 初始化GPIO。
        *   `OutCashLedOn()`: 打开一个指示灯。
        *   `FpgaConfig()`: 配置FPGA（具体实现未在提供的代码中）。
        *   `OutCashLedDisplay()`: 在LED上显示信息。

6.  **控制权交接 ([`main.c:749`](main.c:749), [`fsbl_handoff.S:97`](fsbl_handoff.S:97))**
    *   调用 [`FsblHandoff()`](main.c:749)，它会准备CPU进行跳转。
    *   在 [`fsbl_handoff.S`](fsbl_handoff.S) 中：
        *   清理指令缓存和分支预测器。
        *   禁用MMU和I-Cache，确保CPU处于一个干净的状态。
        *   最后，通过 `bx lr` 指令跳转到第一个应用程序分区的执行地址，FSBL的任务到此结束。

#### 3. Mermaid 流程图

```mermaid
graph TD
    A[上电/复位] --> B{ps7_init()};
    B --> C{初始化PLL, 时钟, DDR, MIO};
    C --> D{检测启动模式};
    D --> E{初始化启动设备 (QSPI/SD)};
    E --> F{LoadBootImage()};
    F --> G{解析分区头};
    G --> H{遍历所有分区};
    H --> I{验证分区头?};
    I -- 成功 --> J{是比特流?};
    I -- 失败 --> Z[Fallback/错误处理];

    J -- 是 --> K{加载比特流到PL};
    J -- 否 --> L{是应用程序?};
    
    L -- 是 --> M{加载应用到DDR};
    L -- 否 --> H;

    K --> N{安全验证 (RSA/MD5)};
    M --> N;
    
    N -- 成功 --> H;
    N -- 失败 --> Z;

    H -- 遍历完成 --> P{执行自定义 Application()};
    P --> Q{初始化GPIO/LED/FPGA};
    Q --> R{FsblHandoff()};
    R --> S{清理CPU状态 (Cache/MMU)};
    S --> T[跳转到应用程序执行地址];
    T --> U[FSBL结束];
```

#### 4. 总结
该FSBL是一个功能完备且健壮的引导加载程序。它不仅完成了Zynq PS端标准的核心初始化，还集成了安全启动（RSA/MD5）、多种启动设备支持以及灵活的分区处理机制。此外，通过 [`fsbl_hooks.c`](fsbl_hooks.c)（虽然在此次分析中未深入）和[`Application()`](main.c:716) 函数，它为用户提供了在引导流程的关键节点插入自定义代码的扩展能力，例如初始化板级外设或执行特定的应用前配置。

这个项目中的 [`Application()`](main.c:716) 函数表明，FSBL除了引导之外，还被用于执行一些早期的系统配置和状态指示任务，这在嵌入式系统中是非常常见的做法。

---


好的，我们继续。根据您的要求，我对“加载和解析启动镜像”以及“分区处理循环”这两个部分进行更详细的解释。

### 3. 加载和解析启动镜像 (`LoadBootImage` 函数)

这是FSBL的核心逻辑，负责处理 `BOOT.BIN` 镜像。整个过程在 [`image_mover.c`](image_mover.c) 的 [`LoadBootImage()`](image_mover.c:161) 函数中实现。

1.  **定位镜像**:
    *   FSBL首先需要知道 `BOOT.BIN` 在启动设备（如QSPI Flash）中的起始地址。这个地址（`ImageStartAddress`）是通过读取多功能引导寄存器（`MULTIBOOT_ADDR_OFFSET`）来计算的。这允许存在多个启动镜像，FSBL可以根据需要选择加载哪一个（例如，用于安全回退的黄金镜像）。

2.  **读取分区表**:
    *   `BOOT.BIN` 的结构是：一个包含FSBL自身信息的头部，紧接着是一个分区表，然后是各个分区的数据。
    *   FSBL调用 [`GetPartitionHeaderInfo()`](image_mover.c:557) 函数来读取这个分区表。
    *   这个函数会读取并解析分区表中的每一项，并将结果存入一个名为 `PartitionHeader` 的全局数组中。数组的每个元素都是一个结构体，详细描述了一个分区的所有信息（大小、加载地址、执行地址、属性等）。
    *   `GetPartitionCount()` 会统计分区表中有效的分区数量。

3.  **分区表安全验证**:
    *   在处理任何分区之前，FSBL会先对整个分区表进行一次安全验证。如果芯片的eFuse中启用了RSA认证，FSBL会调用 `AuthenticatePartition()` 函数，使用存储在OCM（片上存储器）中的公钥来验证整个分区表的签名。
    *   **这一步至关重要**：它确保了启动镜像的结构本身没有被篡改。如果分区表被恶意修改（例如，替换了一个合法的应用程序分区），签名验证会失败，FSBL将停止引导过程并进入回退（Fallback）流程。

### 4. 分区处理循环 (在 `LoadBootImage` 函数内部)

在成功加载并验证了分区表之后，FSBL会进入一个 `while` 循环，从第一个分区（索引为1，因为索引0是FSBL自身）开始，逐一处理到最后一个分区。

对于循环中的**每一个分区**，FSBL执行以下操作：

1.  **头部验证**:
    *   调用 [`ValidateHeader()`](image_mover.c:913) 函数，计算当前分区头的校验和，并与头中存储的期望值进行比较。如果校验和不匹配，说明分区头已损坏，引导失败。

2.  **属性解析**:
    *   从分区头的 `PartitionAttr` 字段中，FSBL会解析出该分区的详细属性，设置一系列标志位，例如：
        *   `PLPartitionFlag`: 这是一个FPGA比特流。
        *   `PSPartitionFlag`: 这是一个ARM处理器上运行的应用程序。
        *   `EncryptedPartitionFlag`: 分区数据是加密的。
        *   `SignedPartitionFlag`: 分区数据带有RSA签名。
        *   `PartitionChecksumFlag`: 分区数据带有MD5校验和。

3.  **地址检查**:
    *   如果这是一个应用程序分区 (`PSPartitionFlag` 为真)，FSBL会检查其加载地址（`LoadAddr`）是否在有效的DDR内存范围内。如果地址无效，引导失败。
    *   FSBL会记录下它遇到的**第一个**应用程序的执行地址（`ExecAddr`），这个地址将作为最后控制权交接的目标。

4.  **数据移动 (`PartitionMove` 函数)**:
    *   这是将分区数据从Flash搬运到DDR的核心步骤。
    *   **对于需要安全验证的FPGA比特流**：数据会先被完整地复制到一个DDR的临时缓冲区（`DDR_TEMP_START_ADDR`）。
    *   **对于应用程序**：数据会被直接复制到其在分区头中指定的最终加载地址（`LoadAddr`）。
    *   这个函数内部会根据启动设备是线性寻址（如QSPI）还是非线性寻址（如SD卡）来选择不同的数据拷贝方式（DMA或CPU拷贝）。

5.  **安全验证与处理**:
    *   数据被移动到DDR后，FSBL会根据之前解析的属性标志位进行相应的安全处理：
        *   **MD5校验和**: 如果 `PartitionChecksumFlag` 为真，调用 `ValidateParition()` 函数，计算DDR中数据的MD5值，并与镜像中存储的MD5值进行比对。
        *   **RSA验签**: 如果 `SignedPartitionFlag` 为真，调用 `AuthenticatePartition()` 函数，对DDR中的数据进行RSA签名验证。
        *   **解密**: 如果 `EncryptedPartitionFlag` 为真，调用 `DecryptPartition()` 函数，使用硬件解密引擎（DEVCFG）对DDR中的数据进行原地解密。
    *   任何一步验证失败，都会导致引导中止并进入回退流程。

6.  **加载比特流**:
    *   如果当前分区是FPGA比特流，在所有验证（如果有）通过后，FSBL会调用 `PcapLoadPartition()` 函数，通过PCAP接口将DDR中的比特流数据配置到FPGA逻辑单元中。

7.  **循环继续**:
    *   处理完当前分区后，循环计数器加一，继续处理下一个分区，直到所有分区都成功加载和验证。

这个循环确保了 `BOOT.BIN` 中的每一个部分都按照预定的方式被正确、安全地加载到系统中。

---