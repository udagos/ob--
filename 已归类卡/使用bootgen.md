---
up:
  - "[[../moc/zynq]]"
---


# bootrom如何创建
好的，我们来深入探讨一下如何创建 Zynq 设备的 BootROM (更准确的说是 **Boot Image**)。==您需要创建一个 Boot Image，才能让 Zynq 设备在没有 JTAG 连接的情况下，从 Flash 存储器 (例如 QSPI Flash, SD 卡等) 启动并运行您的程序。==

**澄清术语:**

*   **BootROM:**  在 Zynq 设备中，实际上存在一块固化在芯片内部的引导 ROM (也称为 BootROM 或 ROM Boot Loader, RBL)。  ==这部分 ROM 代码是不可修改的==，它负责 Zynq 设备上电后的 **第一阶段启动**。  它的主要任务是：
    *   初始化必要的硬件 (非常基础的初始化)。
    *   根据 Boot Mode Pins 的设置 (MIO 引脚配置)，决定从哪个启动设备 (例如 QSPI Flash, SD 卡, NAND Flash 等) 加载 **第二阶段引导程序 (Bootloader，通常指 FSBL - First Stage Boot Loader)**。
    *   ==将加载的第二阶段引导程序复制到 OCM (On-Chip Memory) 或 DDR 内存中==，并跳转到其入口地址开始执行。

*   **Boot Image (启动镜像):**  我们通常所说的 "创建 BootROM" 实际上是 **创建 ==Boot Image (启动镜像)**。  这个 Boot Image 是一个 **包含引导程序 (FSBL)、硬件配置 (Bitstream，如果需要)、应用程序 (或者操作系统内核等等) 的二进制文件**==。  我们需要将这个 Boot Image 烧写到启动设备 (例如 QSPI Flash, SD 卡) 中，Zynq 设备才能从这个启动设备启动。  在 Xilinx 的世界里，Boot Image 通常以  ==`BOOT.BIN`==  文件的形式存在。

**创建 Boot Image 的流程 (使用 Vitis 工具):**

Vitis IDE 提供了方便的工具来创建 Zynq Boot Image (`BOOT.BIN`)。  通常的流程如下：

1.  **准备 Hardware 设计 (Vivado):**
    *   确保您在 Vivado 中完成了硬件设计，包括 Zynq Processing System 的配置，以及任何必要的 PL 侧逻辑。
    *   **生成 Bitstream:**  在 Vivado 中生成 Bitstream 文件 (\*.bit 或 \*.bit.bin)。
    *   **导出 Hardware Description:**  在 Vivado 中导出 Hardware Description 文件 (\*.xsa)。  这个 ==\*.xsa 文件包含了硬件平台的描述信息，Vitis 需要使用它来构建 Bootloader 和应用程序。  导出时请 **包含 Bitstream**。==

2.  **创建 First Stage Bootloader (FSBL) 工程 (Vitis):**
    *   打开 Vitis IDE。
    *   **创建新的 Application Project:**  File -> New -> Application Project...
    *   **选择 Platform:**  ==在 "Platform" 页面，选择 "Create a new platform from hardware (XSA)"。  浏览并选择您之前在 Vivado 导出的 \*.xsa 文件==。  点击 "Next"。
    *   **Application 类型:**  ==在 "Application Project Details" 页面==：
        *   **Application name:**  输入 FSBL 工程的名称，例如 "fsbl"。
        *   **Domain:**  选择目标 Domain (通常是 standalone\_domain 或您自定义的 Domain)。
        *   **Board Support Package:**  保持默认即可。
        *   **System project name:**  Vitis 会自动创建一个 System Project，用于管理硬件平台和应用程序。  保持默认即可。
        *   点击 "Next"。
    *   **Templates:** 在 "Templates" 页面，选择 **"Zynq FSBL"** 模板。  点击 "Finish"。
    *   Vitis 会自动创建一个基于 "Zynq FSBL" 模板的工程。  这个 FSBL 工程已经包含了基本的 FSBL 代码框架，通常情况下，==对于简单的启动，**您不需要修改 FSBL 代码**==，直接编译即可。

3.  **编译 FSBL 工程:**
    *   在 Vitis 的 "Project Explorer" 视图中，右键点击您的 FSBL 工程 (例如 "fsbl")，选择 "Build Project"。
    *   编译成功后，在 FSBL 工程的 `Debug` 或 `Release` 目录下，==会生成 **FSBL 的可执行文件 (\*.elf)**。==  这个 \*.elf 文件就是 FSBL 的二进制代码。

4.  **准备您的应用程序 (或操作系统内核等) 可执行文件:**
    *   如果您要启==动的是您之前创建的 "Hello World" 应用程序，那么您已经有了应用程序的可执行文件 (\*.elf)。==  确保您已经编译了您的应用程序工程。
    *   如果您要启动的是 Linux 操作系统，==您需要准备 Linux 内核镜像 (例如 `image.ub` 或 `zImage`)、Device Tree 文件 (\*.dtb) 等。  Linux 系统的 Boot Image 创建过程会更复杂，这里我们先关注简单的应用程序启动。==

5.  **创建 Boot Image (BOOT.BIN) (在 System Project 中操作):**
    *   在 Vitis 的 "Project Explorer" 视图中，找到您的 **System Project** (通常以您的硬件平台名称命名，例如 "system\_wrapper\_system")。
    *   **右键点击 System Project**，==选择 **"Create Boot Image"**。==
    *   这将打开 "Create Boot Image" 对话框。

6.  **配置 Boot Image 设置 (Create Boot Image 对话框):**
    *   **Bif file partition settings (BIF 文件分区设置):**  Vitis 会自动为您生成一个默认的 BIF 文件 (\*.bif)。  BIF 文件 (Boot Image Format File) 是一个文本文件，用于 ==**描述 Boot Image 的结构和内容**。  您需要 **编辑 BIF 文件** 来指定要包含在 Boot Image 中的文件、加载地址、分区类型等信息。==
    *   **BIF 文件内容 (示例):**  以下是一个典型的 BIF 文件示例，用于创建一个包含 FSBL, Bitstream 和应用程序的 Boot Image:

    ```bif
    all:
    {
        [bootloader] <path_to_your_fsbl.elf>
        [pmufw_image] <path_to_your_pmufw.elf>  (如果适用，对于 ZynqMP 设备)
        [load=0x00000000, type=bin] <path_to_your_bitstream.bit.bin>  (如果需要加载 Bitstream)
        [load=<application_load_address>, entry=<application_entry_point>] <path_to_your_application.elf>
    }
    ```

    *   **解释 BIF 文件内容:**
        *   `all:`  关键字表示这是一个针对所有处理器的 Boot Image (对于 Zynq 7000 系列，只有一个 APU)。  对于 ZynqMP (UltraScale+) 设备，可能有 `pmufw` (Platform Management Unit Firmware) 等额外的分区。
        *   `[bootloader] <path_to_your_fsbl.elf>`:  指定 FSBL 的路径。  **将 `<path_to_your_fsbl.elf>` 替换为您的 FSBL 工程编译生成的 \*.elf 文件的实际路径。**  例如：`fsbl/Debug/fsbl.elf` （路径是相对于 System Project 的位置）。
        *   `[pmufw_image] <path_to_your_pmufw.elf>`:  (仅适用于 ZynqMP)  指定 PMU Firmware 的路径。  对于 Zynq 7000，通常不需要 PMU Firmware。
        *   `[load=0x00000000, type=bin] <path_to_your_bitstream.bit.bin>`:  指定 Bitstream 文件的路径。  **将 `<path_to_your_bitstream.bit.bin>` 替换为您的 Bitstream 文件的实际路径。**  `load=0x00000000` 表示 Bitstream 加载到地址 `0x00000000` 开始的 FPGA 配置空间。  `type=bin` 表示输入文件类型是二进制文件。  **如果您的硬件设计中 PL 侧没有逻辑，或者您希望在软件中加载 Bitstream，则可以省略此行。 但通常为了方便，将 Bitstream 打包到 Boot Image 中是推荐的做法。**  通常 Bitstream 文件位于 Vivado 工程的 `impl_1` 目录下，导出 \*.xsa 时如果包含了 Bitstream，则 \*.xsa 中也会包含 Bitstream。  Vitis 通常可以从 \*.xsa 中找到 Bitstream 的路径。
        *   `[load=<application_load_address>, entry=<application_entry_point>] <path_to_your_application.elf>`:  指定应用程序的可执行文件路径、加载地址和入口地址。
            *   **`<path_to_your_application.elf>`:**  **替换为您的应用程序工程编译生成的 \*.elf  文件的实际路径。**  例如：`helloworld/Debug/helloworld.elf`。
            *   **`<application_load_address>`:**  **应用程序的加载地址。**  这需要根据您的链接脚本 (Linker Script) 设置的应用程序运行的内存地址来确定。  对于简单的 "Hello World" 应用程序，如果使用默认设置，加载地址通常可以在 DDR 内存中，例如 `0x00100000` 或更高的地址 (需要避开 FSBL 和 Bitstream 占用的空间)。  **请务必检查您的应用程序工程的链接脚本 (.ld 文件)，确定正确的加载地址。**  错误的加载地址会导致程序运行失败。
            *   **`<application_entry_point>`:**  **应用程序的入口地址。**  通常情况下，Vitis 可以自动检测到应用程序的入口地址，可以省略 `entry=<application_entry_point>`  部分，让 Vitis 自动处理。  如果需要手动指定，可以在应用程序的链接脚本中找到入口地址 (通常是 `_start` 标号的地址)。

    *   **修改 BIF 文件:**  在 "Create Boot Image" 对话框中，您可以点击 "Edit..." 按钮来编辑 BIF 文件。  根据您的实际文件路径和加载地址，修改 BIF 文件内容。  **请务必仔细检查文件路径是否正确，加载地址是否与您的链接脚本设置一致。**
    *   **Output BIF file path:**  指定 BIF 文件的保存路径和文件名。  保持默认即可。
    *   **Output image file:**  指定要生成的 Boot Image 文件 (\*.BIN) 的路径和文件名。  通常命名为 `BOOT.BIN`。  保持默认即可。

7.  **生成 BOOT.BIN:**
    *   在 "Create Boot Image" 对话框中，配置好 BIF 文件内容和输出路径后，点击 "Create Image"。
    *   ==Vitis 工具会根据 BIF 文件的描述，将 FSBL, Bitstream, 应用程序等文件打包到一个 `BOOT.BIN` 文件中==。  生成的 `BOOT.BIN` 文件通常会保存在 System Project 的目录下 (具体路径取决于您在对话框中的设置)。

8.  **将 BOOT.BIN 烧写到启动设备:**
    *   **选择启动设备:**  根据您的硬件平台和设计需求，选择合适的启动设备，例如 QSPI Flash, SD 卡 等。  **最常用的启动设备是 SD 卡和 QSPI Flash。**
    *   **配置 Zynq Boot Mode Pins:**  **非常重要！**  您需要 **根据您选择的启动设备，正确配置 Zynq 开发板上的 Boot Mode Pins (通常是一些拨码开关或跳线)**。  Boot Mode Pins 的设置决定了 Zynq 设备上电后从哪个设备启动。  **请查阅您的 Zynq 开发板的用户手册，了解如何配置 Boot Mode Pins 以选择 QSPI Flash 或 SD 卡 启动模式。**
    *   **烧写 BOOT.BIN:**  使用 Xilinx 提供的烧写工具 (例如 Vivado Hardware Manager，或者第三方 Flash 烧写工具)，将生成的 `BOOT.BIN` 文件烧写到您选择的启动设备中。
        *   **烧写到 QSPI Flash:**  可以使用 Vivado Hardware Manager 通过 JTAG 连接，将 `BOOT.BIN` 烧写到 QSPI Flash 中。  Vivado Hardware Manager 提供了 Flash 编程的功能。
        *   **烧写到 SD 卡:**  可以直接将 SD 卡插入电脑，然后将 `BOOT.BIN` 文件复制到 SD 卡的根目录下即可 (对于 FAT32 或 FAT 文件系统)。  **注意，对于 SD 卡启动，BOOT.BIN 文件名必须为 `BOOT.BIN` (全大写)。**

9.  **启动 Zynq 设备:**
    *   **断开 JTAG 连接** (如果之前连接了 JTAG)。
    *   **确保 Boot Mode Pins 设置正确，选择了您烧写 BOOT.BIN 的启动设备。**
    *   **给 Zynq 开发板上电。**
    *   如果一切配置正确，Zynq 设备应该会 **自动从您烧写的启动设备 (例如 QSPI Flash 或 SD 卡) 启动**。
    *   您可以通过串口终端查看启动过程中的信息 (例如 FSBL 的输出，应用程序的输出)。  如果您的应用程序是 "Hello World"，您应该能在串口终端看到 "Hello World!" 的输出。

**注意事项和常见问题:**

*   **BIF 文件配置错误:**  BIF 文件是 Boot Image 创建的关键，任何 BIF 文件配置错误 (例如文件路径错误，加载地址错误，语法错误等) 都会导致 Boot Image 创建失败或启动失败。  **请务必仔细检查 BIF 文件内容。**
*   **启动设备选择错误:**  Boot Mode Pins 设置错误，选择了错误的启动设备，会导致 Zynq 从错误的设备启动，无法找到 Boot Image。  **请务必根据您的硬件平台和烧写设备，正确配置 Boot Mode Pins。**
*   **烧写失败:**  Flash 烧写过程中可能出现错误。  需要检查烧写工具的配置、连接是否正常、Flash 芯片是否支持等。  对于 SD 卡，请确保 SD 卡文件系统格式正确 (通常是 FAT32 或 FAT)，并且 `BOOT.BIN` 文件名正确 (全大写)。
*   **应用程序加载地址和链接脚本不匹配:**  应用程序的加载地址必须与链接脚本中设置的运行地址一致。  否则会导致程序在错误的地址运行，可能崩溃或运行不正常。  **务必检查和确认应用程序的链接脚本设置。**
*   **硬件初始化问题 (FSBL):**  如果您的硬件平台比较复杂，可能需要修改 FSBL 代码进行必要的硬件初始化 (例如更复杂的时钟配置，DDR 控制器初始化等)。  默认的 FSBL 模板可能无法满足所有硬件平台的需求。  **对于自定义硬件平台，可能需要深入了解 FSBL 代码，并根据硬件情况进行修改。**
*   **串口调试信息:**  在 Boot Image 创建和启动过程中，**串口调试信息非常重要**。  通过在 FSBL 和应用程序中添加串口输出语句，可以帮助您了解启动过程的状态，定位问题。  **建议在 FSBL 和应用程序中都添加必要的串口调试信息。**

**总结:**

创建 Zynq Boot Image 是将您的嵌入式系统部署到硬件的关键步骤。  需要仔细配置 Vitis 工程，编辑 BIF 文件，正确烧写 Boot Image 到启动设备，并配置 Boot Mode Pins。  这个过程相对复杂，需要您对 Zynq 启动流程、Vitis 工具、BIF 文件语法、硬件平台有一定了解。  请仔细参考 Xilinx 官方文档和您的开发板手册，并进行充分的测试和调试。

如果您在创建 Boot Image 的过程中遇到具体问题，例如报错信息，或者启动失败的现象，请提供更详细的信息，例如 BIF 文件内容、串口输出信息、错误提示等，以便我能够更准确地帮助您分析和解决问题。
# bootgen还有用么
当然！ `bootgen` 工具在当前的 Zynq 和 Zynq UltraScale+ 开发流程中仍然 **非常有用，并且在很多情况下是不可或缺的**。==虽然 Vitis IDE 提供了图形化的界面来创建 Boot Image，但 `bootgen` 作为一个独立的命令行工具，仍然有其独特的优势和应用场景。==

**总结来说，`bootgen` 并没有过时，仍然非常有用，并且是 Xilinx 嵌入式系统开发工具链中重要的一环。**  您可以根据您的具体需求和偏好，选择使用 Vitis IDE 的图形化界面或者直接使用 `bootgen` 命令行工具来创建 Boot Image。  ==**对于复杂的 Boot Image 定制和自动化构建流程，`bootgen` 通常是更强大和灵活的选择。**==

以下是一些关于 `bootgen` 工具仍然有用的关键点以及原因：

**1. 命令行工具的优势：自动化和脚本化**

*   `bootgen` 是一个命令行工具，这意味着它可以很容易地 **集成到各种自动化脚本和构建系统** 中，例如 Makefile, Python 脚本, Jenkins 等持续集成 (CI) 系统。
*   对于 **大规模的嵌入式系统开发项目**，自动化构建 Boot Image 是非常重要的。使用 `bootgen` 可以轻松地将 Boot Image 的生成过程自动化，提高开发效率，并保持构建过程的可重复性。
*   Vitis IDE 虽然方便，但在自动化方面不如命令行工具灵活。如果您需要 **完全自动化的构建流程**，`bootgen` 是更好的选择。

**2. Vitis IDE  实际上也使用了 `bootgen`**

*   Vitis IDE 在后台实际上是 **调用 `bootgen` 命令行工具来生成 Boot Image** 的。  Vitis IDE 的 "Create Boot Image" 功能只是对 `bootgen` 命令行工具的一个图形化封装。
*   这意味着，无论您使用 Vitis IDE 还是直接使用 `bootgen`，最终生成 Boot Image 的核心工具都是 `bootgen`。
*   了解 `bootgen` 的工作原理和 BIF 文件的语法，可以帮助您 **更深入地理解 Boot Image 的创建过程**，即使您主要使用 Vitis IDE。

**3.  更精细的 Boot Image 控制和定制**

*   `bootgen` 允许您 **直接编辑 Boot Image Format (BIF) 文件**，对 Boot Image 的结构和内容进行非常精细的控制。
*   通过 BIF 文件，您可以：
    *   **灵活地添加和排列 Boot Image 的分区 (partitions)**，例如 FSBL, Bitstream, PMU Firmware (ZynqMP), ATF (ARM Trusted Firmware, ZynqMP), U-Boot, Linux Kernel, Device Tree, Root Filesystem 等等。
    *   **指定每个分区的加载地址、入口地址、文件类型、属性等。**
    *   **支持加密和认证 (Authentication) 等高级安全特性。**
    *   **创建包含多个启动镜像 (Multi-boot images) 的 Boot Image。**
*   对于 **复杂的系统启动需求**，例如需要启动 Linux 操作系统，或者需要定制启动流程，`bootgen` 提供的灵活性是 Vitis IDE 图形界面难以完全替代的。

**4.  处理更复杂的 Boot Image 场景**

*   对于一些 **高级的 Boot Image 用例**，例如：
    *   **Secure Boot (安全启动)**
    *   **加密 Boot Image**
    *   **多重启动 (Multi-boot)**
    *   **加载和启动多个应用程序或操作系统**
    *   **从不同的启动设备启动 (例如 Fallback 启动)**
*   `bootgen` 提供了更多的配置选项和灵活性来应对这些复杂的场景。虽然 Vitis IDE 也在不断增强对这些高级特性的支持，但 `bootgen` 仍然是更强大和可靠的选择。

**5.  兼容性和长期支持**

*   `bootgen` 作为一个成熟的命令行工具，已经在 Xilinx 生态系统中存在多年，被广泛使用和验证。
*   Xilinx 会 **持续维护和支持 `bootgen` 工具**，以确保其与最新的器件和软件版本兼容。您可以放心 `bootgen` 在未来仍然会继续可用。
*   对于一些 **较老的项目或平台**，可能更依赖于 `bootgen` 工具，因为早期的 Vitis IDE 版本可能功能不够完善。

**在什么情况下你可能会更倾向于使用 `bootgen`?**

*   **当你需要自动化 Boot Image 构建过程时。**
*   **当你需要对 Boot Image 的结构和内容进行精细控制时。**
*   **当你需要实现高级的启动特性，例如 Secure Boot, Multi-boot 等时。**
*   **当你需要处理复杂的启动场景时。**
*   **当你习惯于使用命令行工具，或者需要在没有图形界面的环境下工作时 (例如在服务器上构建 Boot Image)。**
*   **当你需要使用一些 Vitis IDE 图形界面没有直接提供的 `bootgen` 高级功能时。**

**总结:**

`bootgen` 仍然是一个 **强大、灵活、且非常实用的工具**，尤其是在需要自动化、定制化和处理复杂 Boot Image 场景时。  Vitis IDE 提供了更友好的图形界面，适合快速上手和简单的 Boot Image 创建。  **最佳实践是，理解 `bootgen` 的原理和 BIF 文件语法，并根据具体的项目需求选择合适的工具或工具组合。**  在很多情况下，您可能会结合使用 Vitis IDE 和 `bootgen`，例如使用 Vitis IDE 进行硬件和软件的开发，然后使用 `bootgen` 命令行工具进行 Boot Image 的自动化构建和高级定制。