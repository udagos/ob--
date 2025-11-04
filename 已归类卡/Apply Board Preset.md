---
up:
  - "[[../moc/MocZynq]]"
---



好的，明白了。如果您在 "Run Block Automation" 对话框中 **没有看到 "Apply Board Preset" 这个选项**，这通常意味着以下几种情况：

1.  **您在创建 Vivado 工程时，没有选择开发板型号，或者选择了 "无开发板" (Not specified)。**  "Board Preset" 选项是依赖于您在工程中指定的开发板信息的。 如果 Vivado 不知道您使用的是哪块开发板，自然就无法应用预设的板级配置。

2.  ==**您可能使用的是自定义硬件平台，而不是 Xilinx 官方的开发板==。**  在这种情况下，本来就不会有官方的 "Board Preset" 可用。

3.  **在某些非常早期的 Vivado 版本中，可能 Block Automation 的功能或选项有所不同。** （但这种情况相对较少，如果您使用的是较新版本的 Vivado，则不太可能是这个原因）。

**即使没有 "Apply Board Preset" 选项，仍然可以运行 Block Automation，并且对于创建 PS 最小系统来说，Block Automation 仍然可以帮助您进行一些基本的配置。**  只是配置的方式和内容会略有不同。

==**针对没有 "Apply Board Preset" 的情况，以下是配置 "Run Block Automation" 的步骤和说明：**==

**运行 Block Automation (无 Board Preset 情况):**

1.  **像之前一样，将 "ZYNQ Processing System" IP 核添加到 Block Design 后，点击 "Run Block Automation" 提示** (通常仍然会在画布顶部绿色横幅显示，或者在 IP 核上方)。

2.  **查看弹出的 "Run Block Automation" 对话框。**  **在没有 "Apply Board Preset" 的情况下，对话框的内容会简化，您可能看不到 "Board Preset" 相关的选项。**  对话框中通常会包含以下类型的配置选项 (具体选项可能因 Vivado 版本和 IP 核版本略有不同，但核心思路类似):

    *   **Processor Configuration (处理器配置):**  这部分通常是关于 Zynq PS 处理器的一些基本设置，例如：
        *   **Clocking (时钟配置):**  Block Automation 仍然会尝试为您配置 PS 的基本时钟。  通常会提供一些默认的时钟配置方案。  对于最小系统，**保持默认的时钟配置即可**。  一般不需要修改。
        *   **Interrupts (中断配置):**  可能会有一些关于中断控制器的基本配置，通常也 **保持默认即可**。
        *   **AXI Interconnect (AXI 互联配置):**  Block Automation 会处理 PS 内部的 AXI 总线互联。  **通常保持默认设置**。

    *   **Interface Options (接口选项):**  这部分可能会列出 Zynq PS 的一些接口选项，例如：
        *   **External Memory Interfaces (外部存储器接口):**  如果您需要在 PS 侧使用外部 DDR 存储器，可以在这里配置 DDR 控制器。  **对于最小系统，如果只是运行简单的 "Hello World" 程序，并且不涉及大量数据存储，您可以暂时不配置 DDR，或者使用默认的 DDR 配置** (如果 Block Automation 默认启用了 DDR)。  **但为了通用性和后续扩展，建议还是保留基本的 DDR 配置**。
        *   **Fixed IO Interfaces (固定 IO 接口):**  例如 MIO (Multiplexed I/O) 配置。  Fixed IO 用于连接 PS 的一些固定外设，例如 UART, GPIO, I2C, SPI 等。  Block Automation 可能会默认启用一些常用的 Fixed IO 外设接口。  **对于 "Hello World" 程序，可能 UART 接口是需要的 (用于串口输出)**。  您可以检查 Fixed IO 配置，**确保 UART 接口 (通常是 UART0 或 UART1)  被启用 (如果默认未启用，可以手动启用)**，以便后续通过串口终端查看 "Hello World" 输出。  其他 Fixed IO 外设接口，在最小系统中可以暂时保持默认或者禁用，后续需要时再启用。
        *   **PL to PS Interfaces (PL 到 PS 的接口):**  这部分通常是 AXI 总线接口，用于 PS 和 PL 之间的通信。  **对于纯 PS 系统，并且不需要 PL 侧的任何逻辑，PL to PS 接口可以保持默认不配置，或者禁用**。  如果您看到类似 "AXI_GP0", "AXI_HP0" 等接口，并且确定最小系统不需要 PL 侧的任何交互，可以暂时忽略这些接口的配置。

3.  **配置 "Run Block Automation" 对话框:**  **在没有 "Board Preset" 的情况下，您需要根据您的实际需求和对 Zynq PS 的理解，手动配置 "Run Block Automation" 对话框中的选项。**

    *   **最简化的 "Hello World" 配置:**  如果您 **仅仅** 需要运行最简单的 "Hello World" 程序，并且只是想通过串口终端 (UART) 输出，那么您可能只需要关注以下配置:
        *   **Clocking (时钟):**  保持默认。
        *   **External Memory Interfaces (DDR):**  可以使用默认的 DDR 配置 (如果 Block Automation 默认启用)，或者如果非常 minimal，**可以尝试暂时禁用 DDR 配置 (但通常不推荐，除非内存资源非常紧张)，直接使用 PS 内部的 OCM (On-Chip Memory) 来运行程序 (但 OCM 容量有限)**。  为了通用性，建议保留 DDR 配置。
        *   **Fixed IO Interfaces (UART):**  **确保 UART 接口被启用** (例如 UART0 或 UART1)。  查找类似 "UART" 或 "Serial" 的配置选项，确认其被选中或启用。  记下选用的 UART 接口 (例如 UART0)，后续在 SDK/Vitis 中配置串口终端时需要用到。
        *   **其他选项:**  例如中断, AXI 互联等，**通常保持默认即可**。  PL to PS 接口可以忽略或保持默认。

4.  **点击 "OK" 运行 Block Automation。**  Vivado 会根据您的配置完成 PS IP 核的初始化和连接。

**截图示例 (无 "Apply Board Preset" 的 "Run Block Automation" 对话框):**

下图是一个 **没有勾选 "Apply Board Preset"** 的 "Run Block Automation" 对话框的示例 (对话框的具体内容可能因器件和 Vivado 版本而略有不同，但配置思路是类似的)。  在这个示例中，您可以看到一些关于处理器、时钟、中断、以及接口的配置选项，但 **没有 "Board Preset" 相关的选项**。

![无 Board Preset 的 Run Block Automation 对话框示例](https://i.imgur.com/j85JHyV.png)

**在这个示例对话框中，您可以关注以下几个方面 (红色框标识):**

*   **Page Navigator (页面导航):**  对话框左侧是页面导航，您可以点击不同的页面 (例如 "PS-PL Configuration", "Clock Configuration", "MIO Configuration") 来查看和修改不同方面的配置。
*   **配置选项:**  在每个配置页面中，会显示相应的配置选项。  例如在 "Clock Configuration" 页面，您可以查看和修改时钟设置。  在 "MIO Configuration" 页面，您可以配置 MIO (包括 UART 等 Fixed IO 外设)。
*   **Description (描述信息):**  对话框下方通常会有一些描述信息，帮助您理解当前页面的配置项的含义。

**配置完成后，点击 "OK" 按钮，运行 Block Automation。**

**后续步骤 (与之前类似):**

*   **验证 Block Design (Validate Design)。**
*   **生成 HDL Wrapper (Create HDL Wrapper)。**
*   **生成 Bitstream (Generate Bitstream)。**
*   **导出硬件描述文件 (Export Hardware - \*.xsa)。**
*   **在 SDK 或 Vitis 中创建软件工程，并选择 "Hello World" 模板。**
*   **在软件工程中，配置串口终端 (如果使用了 UART 输出)，并编译、运行程序。**

**总结 (无 Board Preset 情况):**

即使没有 "Apply Board Preset" 选项，您仍然可以使用 "Run Block Automation" 来配置 Zynq PS 的基本硬件系统。  您需要 **根据您的需求，手动配置 "Run Block Automation" 对话框中的选项**。  对于最简单的 "Hello World" 程序，关注 **时钟配置** 和 **UART 接口的启用** 即可。  **为了通用性，建议保留基本的 DDR 存储器配置**。  然后按照之前的步骤，完成后续的硬件生成和软件开发流程。

如果您在配置 "Run Block Automation" 对话框时遇到具体的选项不清楚如何配置，或者在后续的软件开发过程中遇到问题，欢迎随时提供更详细的信息，我会尽力协助您！