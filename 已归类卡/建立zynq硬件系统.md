---
up:
  - "[[../moc/zynq]]"
---


# 定制基于 Zynq 的最小硬件系统的详细步骤
当然，创建基于 Zynq 的 PS 最小硬件系统，特别是为了运行简单的 “Hello World” 程序，是一个相对直接的过程。这种配置主要依赖于 Zynq 芯片的 Processing System (PS) 部分，而无需在 FPGA Fabric (PL) 中添加额外的硬件 IP 核。

以下是使用 Vivado 工具定制基于 Zynq 的最小硬件系统的详细步骤：

**步骤 1：创建 Vivado 工程**

1.  **启动 Vivado:**  打开你的 Vivado Design Suite。
2.  **创建新工程:**  点击 "File" -> "Project" -> "New Project"。
3.  **选择工程类型:**  在 "Project Type" 页面，选择 "RTL Project"。点击 "Next"。
4.  **工程名称和路径:**  在 "Project name" 页面，输入工程名称（例如 "zynq_ps_minimal"）和工程存放路径。点击 "Next"。
5.  **工程类型:**  在 "Project Type" 页面，确认选择 "RTL Project"，并勾选 "Do not specify sources at this time"。点击 "Next"。
6.  **选择器件:**  在 "Default Part" 页面，选择你的 Zynq 器件型号。你可以通过以下方式选择：
    *   **Parts:**  如果你知道具体的器件型号，可以在 Part 搜索框中输入，例如 "xc7z020clg400-1"。
    *   **Boards:** 如果你使用的是 Xilinx 官方开发板，可以选择 "Boards" 选项卡，然后在 Board 列表中找到你的开发板型号。选择开发板型号 Vivado 会自动配置好器件型号和一些预设。
    *   选择器件后，点击 "Next"。
7.  **工程摘要:**  在 "Project Summary" 页面，检查工程配置信息，确认无误后点击 "Finish" 完成工程创建。

**步骤 2：==创建 Block Design**==

1.  **创建 Block Design:**  在 Vivado 工程的 "Flow Navigator" 窗口中，点击 "IP INTEGRATOR" -> "Create Block Design"。
2.  **Design 名称:**  在弹出的 "Create Block Design" 对话框中，输入 Block Design 的名称，例如 "design_1"，然后点击 "OK"。
3.  **添加 Zynq PS IP 核:**  在 Block Design 画布中，点击 "+" 号 (Add IP) 或者在画布中右键选择 "Add IP"。在弹出的 IP Catalog 窗口中，==搜索 "zynq"，找到 "ZYNQ Processing System" IP 核==，双击添加 IP 核到 Block Design 中。

**步骤 3：配置 Zynq PS IP 核**

1.  **运行 Block Automation:**  添加 Zynq PS IP 核后，==Vivado 会在画布上方提示 "Run Block Automation"==。点击 "Run Block Automation"。
2.  **Block Automation 配置:**  在弹出的 "Run Block Automation" 对话框中：
    *   **Board Preset:**  如果使用了开发板，并且之前在创建工程时选择了开发板型号，==通常 "[[Apply Board Preset]]" 会被默认勾选==。==使用 Board Preset 可以自动配置 PS 的一些基本设置，例如时钟、接口等，**对于快速搭建最小系统非常方便，推荐勾选**。==如果不使用 Board Preset 或者需要自定义配置，可以取消勾选 "Apply Board Preset"。
    *   **点击 "OK"** 运行 Block Automation。  Vivado 会自动完成 PS IP 核的一些基本配置和连接。

**步骤 4：检查和精简 Block Design (最小系统关键步骤)**

1.  **检查 Block Design:**  Block Automation 完成后，检查 Block Design 画布。
2.  **移除不必要的外设接口:**  ==由于我们只需要 PS 最小系统，用于运行 "Hello World" 程序，因此 **可以移除所有 PL 侧的外设 AXI 接口**(如果 Block Automation 自动添加了)==。通常情况下，如果使用了 Board Preset 并且是最小系统，Block Automation 不会自动添加额外的 PL 侧 AXI 接口。但如果看到类似 "AXI_GP0", "AXI_HP0" 等 AXI 接口，并且你 **确定不需要 PL 侧的任何逻辑和外设**，可以选中这些 AXI 接口，然后 **按 "Delete" 键删除**。  **务必谨慎操作，不确定用途的接口不要随意删除。最小系统通常只需要 PS 的基本接口，例如 Fixed IO 和 DDR 接口 (如果需要使用片外 DDR 存储器)。**  ==对于最简单的 "Hello World" (例如只在 Console 输出，不涉及大量数据存储和访问)，甚至可以不用配置 DDR，直接使用 PS 内部的 OCM (On-Chip Memory)。但 **通常为了通用性，推荐保留 DDR 配置，以便后续程序有更大的运行空间**==。
3.  **时钟和复位:**  ==对于 PS 最小系统，Block Automation 通常会自动配置好基本的时钟和复位。  **一般情况下不需要额外添加时钟 IP 核 (例如 Clocking Wizard) 和复位 IP 核。**  PS 内部有自带的时钟和复位 logic 可以满足基本需求==。除非你有特殊的时钟需求 (例如需要生成额外的时钟频率，或者需要更复杂的时钟管理)，否则 **保持默认的时钟配置即可**。  ==Block Design 中应该能看到 `pl_clk` (PL Fabric Clock, 如果存在，最小系统可以忽略) 和 `ps_clk` (PS Clock, 必须有)==。==复位信号通常是 `axi_resetn` (AXI 总线复位) 和 `interconnect_aresetn` (互联复位==)。

**步骤 5：验证 Block Design**

1.  **运行 Design Rule Check ==(DRC)==:**  在 Block Design 画布中，点击 "Validate Design"  按钮 (或者在 Flow Navigator 中 "IP INTEGRATOR" -> "Validate Design")。  ==Vivado 会检查 Block Design 是否存在错误。==
2.  **检查 DRC 结果:**  ==在 "Design Runs" 窗口的 "Messages" 选项卡中查看 DRC 结果。确保没有 Critical Warnings 和 Errors==。如果有 Warning，根据 Warning 的内容判断是否需要处理。对于最小系统，通常应该能通过 DRC 检查。
	1. ![](../fujian/Pasted%20image%2020250328102352.png)

**步骤 6：生成 HDL Wrapper**

1.  **生成 Wrapper:**  **在 "Sources" 窗口中，右键点击之前创建的 Block Design 文件 (例如 "design\_1. bd")，选择 "Create HDL Wrapper"。**
	1. ![](../fujian/Pasted%20image%2020250328102550.png)
2.  **Wrapper 类型:**  在弹出的 "Create HDL Wrapper" 对话框中，选择  "Let Vivado manage wrapper and auto-update"。点击 "OK"。  ==Vivado 会自动生成 Block Design 的顶层 HDL Wrapper 文件 (VHDL 或 Verilog)。==

**步骤 7：<span style="background:#ff4d4f">生成 Bitstream**</span>

1.  **运行 Generate Bitstream:**  在 "Flow Navigator" 窗口中，==点击 "PROGRAM AND DEBUG" -> "Generate Bitstream"==。  V==ivado 会自动运行 Synthesis (综合), Implementation (实现), 和 Bitstream Generation (生成比特流) 流程==。这个过程会比较耗时，取决于你的工程复杂度和电脑性能。
2.  **等待 Bitstream 生成完成:**  等待 Vivado 完成 Bitstream 生成。在 "Design Runs" 窗口中可以查看 Bitstream 生成的进度和状态。当看到 "Bitstream Generation Completed" 的提示信息，表示 Bitstream 生成成功。

**步骤 8：<span style="background:#ff4d4f">导出硬件描述文件 (Export Hardware)**</span>

1.  **导出 Hardware:**  Bitstream 生成成功后，点==击 "File" -> "Export" -> "Export Hardware"。==
2.  **导出配置:**  在弹出的 "Export Hardware" 对话框中：
    *   **Output container:**  选择 `<Local to Project>` (默认)。
      - **Include bitstream:**  ==**务必勾选 "Include bitstream"**。这样导出的硬件描述文件会包含刚刚生成的 Bitstream 文件 ( \*. bit )==。后续在 SDK 或者 Vitis 中创建软件工程时，==可以直接使用这个硬件描述文件，方便软件工程直接加载硬件配置和 Bitstream。==
    *   **点击 "OK"** 导出硬件描述文件。  Vivado 会在工程目录下生成一个  \*. xsa  文件 (Xilinx Support Archive)。==这个 \*. xsa 文件就包含了你的硬件描述信息 (包括 Block Design, 器件信息, Bitstream 文件等)，可以用于后续的软件开发。==

**步骤 9：在 SDK 或 Vitis 中创建软件工程 (后续步骤)**

1.  **启动 SDK 或 Vitis:**  点击 ==Vivado== 的 "File" -> "Launch SDK" (如果使用 Vivado 2019 及之前的版本)  或者  =="Tools" -> "Launch Vitis IDE"== (如果使用 Vivado 2020 及之后的版本)。  Vivado 会启动 SDK 或 Vitis 集成开发环境。
2.  **创建 Application Project:**  在 SDK 或 Vitis 中，根据向导创建一个新的 Application Project。在创建 Application Project 的过程中，==指定 **Hardware Specification File** 为刚刚导出的  \*. xsa  文件。==
3.  **选择 "Hello World" 模板:**  在创建 Application Project 时，==可以选择 "Hello World" 模板。==  SDK 或 Vitis 会自动创建一个简单的 "Hello World" 例程代码。
4.  **编译和运行程序:**  编译软件工程，然后将程序下载到 Zynq 开发板上运行。  "Hello World" 程序通常会通过串口或者 JTAG Console 输出 "Hello World!"  字符串。

**总结:**

通过以上步骤，你就完成了基于 Zynq 的最小硬件系统的定制。这个最小系统只包含了 Zynq PS 的基本组件，非常适合用于 PS 端的软件开发入门，例如运行简单的 "Hello World" 程序。后续你可以根据实际需求，逐步在 Block Design 中添加更多的 IP 核 (例如外设接口, 定制 PL 逻辑等)，扩展你的 Zynq 硬件系统功能。

**关键点回顾:**

*   **选择合适的 Zynq 器件或开发板。**
*   **在 Block Design 中添加 "ZYNQ Processing System" IP 核。**
*   **运行 Block Automation 并尽量使用 Board Preset 简化配置。**
*   **精简 Block Design，移除不必要的外设接口 (对于最小系统)。**
*   **生成 Bitstream 和导出 Hardware ( \*. xsa 文件)。**
*   **在 SDK 或 Vitis 中基于 \*. xsa 文件创建软件工程，进行软件开发。**

希望这个详细的步骤可以帮助你成功定制基于 Zynq 的最小硬件系统！如果你在操作过程中遇到任何问题，欢迎随时提问。
# 下载
当然可以！将程序下载到 Zynq 开发板上执行，并通过串口终端查看 "Hello World!" 输出，是验证硬件平台和软件程序是否正确工作的关键步骤。

根据您目前的情况，假设您已经完成了以下步骤：

1.  **在 Vivado 中完成了 Block Design，包括 Zynq PS IP 核的配置。**
2.  **生成了 Bitstream，并导出了硬件描述文件 (\*. xsa)。**
3.  **在 Vitis 中创建了软件工程，选择了 "Hello World" 模板，并基于导出的硬件平台创建了应用程序工程。**
4.  **已经==<span style="background:#ff4d4f">成功编译了 "Hello World" 应用程序，生成了可执行文件 (\*. elf)</span>==。**

现在，您需要将这个可执行程序下载到 Zynq 开发板上运行。以下是详细的下载和执行步骤：

**前提条件和准备工作：**

*   **硬件连接：**
    *   **Zynq 开发板：** 确保您的 Zynq 开发板已正确连接电源，并已开启电源。
    *   **JTAG 编程器/调试器：**  您需要<span style="background:#ff4d4f">==使用 JTAG 编程器/调试器将程序下载到开发板==</span>。通常，Xilinx 的开发板上会板载 JTAG 接口，您只需要使用 USB 线缆连接开发板和您的电脑即可。确保 JTAG 线缆连接可靠。
    *   **串口连接 (可选，但强烈建议)：** 为了查看 "Hello World!" 的串口输出，您需要建立串口连接。通常使用 USB 转串口线缆连接开发板的 UART 接口和电脑的 USB 端口。确认您知道开发板所使用的 UART 接口 (例如 UART0 或 UART1)。

*   **软件准备：**
    *   **Vitis IDE 仍然处于打开状态：**  确保您的 Vitis IDE 仍然是打开的，并且您之前创建的 "Hello World" 应用程序工程在 Vitis 中是打开的。
    *   **串口终端软件：**  您需要在您的电脑上安装一个串口终端软件，例如 Putty, Tera Term, Minicom 等。用于接收和显示开发板通过串口发送的数据。

**下载和执行步骤 (Vitis IDE 中操作)：**

1.  **确保应用程序工程和硬件平台工程在 Vitis 中是激活的 (选中状态)。**

2.  **打开 "Run Configurations" (运行配置) 对话框：**
    *   在 Vitis IDE 的菜单栏中，选择 **"Run" -> "Run Configurations..."**  (运行 -> 运行配置)。
    *   这将打开 "Run Configurations" 对话框。

3.  **在 "Run Configurations" 对话框中，创建或选择 "Xilinx Single Application Debug" -> "System Debugger" 类型的运行配置 (如果已经存在，可以直接选择；如果不存在，需要新建)。**
    *   **如果已经存在 "System Debugger" 类型的配置:**  在左侧的配置列表中，找到并选择以您的系统工程 (system\_wrapper\_hw\_platform) 名称开头的 "System Debugger" 配置 (例如 "system\_wrapper\_system Debugger")。跳到步骤 5。
    *   **如果不存在 "System Debugger" 类型的配置:**
        *   在左侧的配置类型列表中，双击 **"Xilinx Single Application Debug" -> "System Debugger"**，创建一个新的 "System Debugger" 配置。
        *   新的配置会自动以您的系统工程名称命名 (例如 "system\_wrapper\_system Debugger")。

4.  **配置 "System Debugger" 运行配置 (重要):**
    *   **Connection 选项卡:**  默认情况下，Vitis 应该会自动检测到连接的 JTAG 编程器。  **确保 "Target Connection" (目标连接) 设置正确，通常保持默认的 "Local" 或 "Auto" 即可。  Vitis 应该能够自动找到您的 JTAG 连接。**  如果您有多个 JTAG 连接，可能需要手动选择正确的连接。
    *   **Application 选项卡:**
        *   **Application name (应用程序名称):**  确认 "Application name" 下拉列表中，**选择了您要下载和运行的 "Hello World" 应用程序工程的名称** (例如 "helloworld")。
        *   **硬件平台:**  确认 "Hardware Platform" (硬件平台)  显示的是您的硬件平台工程名称 (例如 "system\_wrapper\_hw_platform")。  **务必确保选择了正确的硬件平台！**  这非常重要，Vitis 需要知道您的硬件描述文件 (\*. xsa) 的位置，才能正确下载程序和配置硬件。
        *   **(可选) Bootloader:**  对于简单的 "Hello World" 程序，通常不需要 Bootloader。  "Bootloader" 设置可以保持默认。
        *   **(可选) Download to Tcl script:**  如果您需要使用 Tcl 脚本进行更精细的下载控制，可以勾选 "Download to Tcl script" 并指定 Tcl 脚本路径。对于基本下载，通常不需要使用 Tcl 脚本。

5.  **点击 "Run" (运行) 按钮 (或者 "Debug" 按钮):**
    *   在 "Run Configurations" 对话框的右下角，点击 **"Run" 按钮** (或者 **"Debug" 按钮**，如果您想使用调试器进行单步调试)。
    *   Vitis 将会开始执行以下操作：
        *   **连接到目标开发板 (通过 JTAG)。**
        *   **配置 FPGA (如果需要的话，例如对于 Bitstream 首次下载)。**  如果您的 Bitstream 还没有下载到 FPGA 中，Vitis 可能会先下载 Bitstream。但这通常在您第一次运行程序时发生。如果您只是重新运行程序，Bitstream 可能已经加载，Vitis 会跳过 Bitstream 下载步骤。
        *   **下载您的 "Hello World" 可执行程序 (\*. elf) 到开发板的内存中 (通常是 DDR 内存)。**
        *   **启动程序在 Zynq 处理器上运行。**

6.  **观察 Vitis 控制台 (Console) 输出和串口终端输出：**

    *   **Vitis Console (控制台) 输出：**  在 Vitis IDE 的 "Console" 视图中，您应该能看到程序下载和执行的进度信息。如果一切顺利，您应该看到类似 "Program downloaded successfully" 或 "程序下载成功" 的消息。如果没有错误，Console 窗口应该不会有红色错误提示。
    *   **串口终端软件输出：**  打开您之前准备好的串口终端软件 (例如 Putty, Tera Term)。
        *   **配置串口终端：**  设置正确的串口端口号 (与您的 USB 转串口线缆连接的端口对应。在 Windows 设备管理器或 Linux 的 /dev 目录下可以查看串口端口号)。设置波特率 (Baud Rate)。  **Zynq 默认的 UART 波特率通常是 115200 bps。**  数据位、停止位、校验位等设置通常保持默认 (8 数据位，1 停止位，无校验)。
        *   **连接串口：**  在串口终端软件中，打开您配置的串口端口。
        *   **观察输出：**  如果 "Hello World" 程序成功运行，您应该能在串口终端软件的窗口中看到 **"Hello World!" 的字符串输出**。这表明程序已经成功下载到 Zynq 开发板上，并在处理器上正确执行，并且通过 UART 接口输出了 "Hello World!" 消息。

**常见问题和故障排除：**

*   **Vitis 无法连接到目标 / 下载失败：**
    *   **检查 JTAG 连接：**  确保 JTAG 线缆连接牢固，USB 线缆连接正常，开发板已上电。
    *   **检查 Vitis 目标连接设置：**  在 "Run Configurations" -> "Connection" 选项卡中，确认 "Target Connection" 设置正确。尝试 "Local" 或 "Auto" 模式。如果仍然有问题，可以尝试手动指定 JTAG 编程器的类型 (如果 Vitis 提供了手动选择的选项)。
    *   **重启 Vitis 和开发板：**  有时重启 Vitis IDE 和重新上电开发板可以解决一些临时的连接问题。
    *   **检查 JTAG 驱动：**  确保您的电脑上安装了正确的 JTAG 驱动程序。  Xilinx 编程器驱动程序通常会随 Vivado/Vitis 安装一起安装。如果驱动程序有问题，可能需要重新安装驱动。

*   **串口终端没有 "Hello World!" 输出：**
    *   **检查串口连接：**  确认 USB 转串口线缆连接可靠，连接到开发板正确的 UART 接口。
    *   **检查串口终端配置：**  确认串口终端软件的端口号、波特率等参数设置与开发板的 UART 配置一致 (特别是波特率，通常是 115200)。
    *   **检查 "Hello World" 程序代码：**  确认您的 "Hello World" 程序代码中确实包含了串口输出的语句 (例如 `printf("Hello World!\r\n");`)，并且使用了正确的 UART 输出函数。检查代码中是否有其他错误导致程序没有执行到串口输出部分。
    *   **尝试复位开发板：**  按下开发板上的复位按钮 (如果有)，或者重新上电开发板，再次尝试运行程序。

**恭喜！** 如果您在串口终端软件中看到了 "Hello World!" 的输出，那么恭喜您，您的第一个基于 Zynq 的 "Hello World" 程序已经成功运行了！这标志着您的 Zynq 硬件平台和软件开发环境都已经基本配置正确，可以开始进行更深入的嵌入式系统开发了。

如果您在下载和执行过程中遇到任何问题，或者串口终端没有输出，请仔细检查上述步骤和故障排除建议。并随时提供更详细的错误信息或现象描述，我会尽力帮助您进一步分析和解决问题！