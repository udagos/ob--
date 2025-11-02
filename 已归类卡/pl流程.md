---
up:
  - "[[../moc/fpga]]"
same:
  - "[[../note/补充25.3.26-14.12]]"
---



好的，我们从头开始，从 Vivado IDE 创建工程，一步一步熟悉整个流程，目标是实现 Zynq-7020 PL 端 LED 轮流点亮。

## **步骤 1：启动 Vivado IDE 并创建新工程**

1.  **启动 Vivado:**  在您的电脑上找到 Vivado IDE 的快捷方式 (通常在开始菜单的 Xilinx Design Tools 目录下)，双击启动 Vivado。

2.  **创建新工程:**
    *   在 Vivado 启动界面，您会看到 "Quick Start" 区域。点击 "Create Project"。

    *   **New Project 向导 - Page 1 of 5: Project name and location:**
        *   **Project name:**  输入您的工程名称，例如 `zedboard_led_blink_pl`.  （工程名称只能包含字母、数字和下划线，且不能以数字开头）
        *   **Project location:**  选择您想要保存工程的目录。建议选择一个方便查找的目录，例如您桌面上的一个文件夹。
        *   **Project is subdirectory:**  默认勾选，表示工程文件会保存在您指定的 Project location 下的一个以 Project name 命名的子目录中。保持默认即可。
        *   点击 "Next"。

    *   **New Project 向导 - Page 2 of 5: Project type:**
        *   **Project Type:**  选择 "RTL Project"。这表示我们要==创建一个基于 RTL (Register-Transfer Level) 级别==的硬件设计工程。
        *   **勾选 =="Do not specify sources at this time":**  暂时不添加源文件==，我们稍后手动添加。为了流程更清晰，建议勾选此项。
        *   点击 "Next"。

    *   **New Project 向导 - Page 3 of 5: Project Settings - Device Selection:**
        *   **Default part:**  选择 "Boards" 选项卡。这是最方便的方式，因为我们可以直接选择 ZedBoard 开发板。
        *   在 "Filter by Board Name" 输入框中输入 `zedboard`。
        *   在搜索结果中，找到并选择 **"ZedBoard Zynq Evaluation and Development Kit"**。确保您选择的是正确的 ZedBoard 版本。

        *   您可以在下方的 "Board Part Properties" 区域查看所选板卡的详细信息，例如器件型号 (xc7z020clg484-1)。
        *   点击 "Next"。

    *   **New Project 向导 - Page 4 of 5: Project Summary:**
        *   查看项目摘要信息，确认工程名称、路径、项目类型、目标器件等信息都正确。
        *   点击 "Finish"，完成工程创建。

3.  **Vivado 工程界面:**  Vivado 会打开新的工程。您会看到 Vivado IDE 的主要界面，包括：
    *   **Flow Navigator:** (左侧)  用于控制设计流程，例如综合、实现、生成比特流等。
    *   **Project Manager:** (左侧，Flow Navigator 下方)  显示工程的文件结构，包括 Design Sources, Constraints, Simulation Sources 等目录。
    *   **Design Canvas/Editor:** (中间)  主要的设计编辑区域，可以打开 HDL 代码编辑器、IP Integrator 等。
    *   **Properties/Sources/Libraries/IP Catalog/Board:** (右侧)  各种属性窗口，资源管理器等。
    *   **Tcl Console:** (底部)  Tcl 命令控制台，可以输入 Tcl 命令进行操作。

## **步骤 2：创建 HDL 设计源文件**

1.  ==**在 Project Manager 窗口中，展开 "Design Sources" 目录。**==  您现在应该看到 "Design Sources" 下面是空的，或者显示 "No Design Sources"。

2.  **添加设计源文件:**
    *   在 "Design Sources" 上方，您会看到一个 "+" 号图标 (Add Sources)。点击这个 "+" 号，选择 "Add or Create Design Sources..."。

    *   **Add Sources 向导 - Page 1 of 2: Add Sources:**
        *   选择 "Create File"。
        *   **File type:**  选择 "HDL"。
        *   **File name:**  输入文件名，例如 `led_controller`。您可以选择 VHDL 或 Verilog 语言。
            *   **VHDL:**  确保 "File type" 是 "HDL"，文件名输入 `led_controller.vhd`，并在 "File language" 中选择 "VHDL"。
            *   **Verilog:** 确保 "File type" 是 "HDL"，文件名输入 `led_controller.v`，并在 "File language" 中选择 "Verilog"。
        *   **File location:**  默认 "Local to Project"，保持默认即可。
        *   点击 "OK"。
        *   点击 "Finish"。[[../note/补充25.3.26-14.12]]

3.  **复制粘贴代码到 HDL 文件:**  Vivado 会自动打开您创建的 HDL 文件 (`led_controller.vhd` 或 `led_controller.v`) 在代码编辑器中。
    *   **VHDL 用户:**  复制您之前收到的 **VHDL 代码示例** (`led_controller.vhd` 的代码)  粘贴到 Vivado 代码编辑器中，替换掉默认生成的代码模板。
    *   **Verilog 用户:**  复制您之前收到的 **Verilog 代码示例** (`led_controller.v` 的代码) 粘贴到 Vivado 代码编辑器中，替换掉默认生成的代码模板。
    *   **保存文件:**  在 Vivado 菜单栏，点击 "File" -> "Save" (或者使用快捷键 Ctrl+S) 保存您的代码文件。

4.  **查看 Design Sources:**  在 "Project Manager" -> "Design Sources" 目录中，您应该能看到您刚刚创建的 `led_controller.vhd` 或 `led_controller.v` 文件。

## **步骤 3：创建约束文件 (XDC)**

1.  ==**在 Project Manager 窗口中，展开 "Constraints" 目录。**==  现在应该是空的，或者显示 "No Constraints Files Defined"。

2.  **添加约束文件:**
    *   在 "Constraints" 上方，您会看到一个 "+" 号图标 (Add Sources)。点击这个 "+" 号，选择 "Add or Create Constraints..."。

    *   ==**Add Sources 向导== - Page 1 of 2: Add Sources:**
        *   选择 "Create File"。
        *   **File type:**  选择 "XDC"。
        *   **File name:**  输入文件名，例如 `zedboard_constraints`。
        *   **File location:**  默认 "Local to Project"，保持默认即可。
        *   点击 "OK"。
        *   点击 "Finish"。

3.  **复制粘贴约束代码到 XDC 文件:**  Vivado 会自动打开您创建的 XDC 文件 (`zedboard_constraints.xdc`) 在文本编辑器中。
    *   复制您之前收到的 **`zedboard_constraints.xdc` 文件内容**  粘贴到 Vivado 代码编辑器中，替换掉默认生成的代码模板。
    *   **仔细检查并修改引脚号 (非常重要!):**  **再次强调，务必参考您 ZedBoard 版本的用户手册或原理图，核对 100MHz 时钟输入引脚和 LED 的引脚号。** 如果您的 ZedBoard 版本不同，或者您使用了不同的时钟源或 LED，请 **修改 `zedboard_constraints.xdc` 文件中对应的 `PACKAGE_PIN` 属性的值，使其与您的硬件连接一致。**
    *   **保存文件:**  在 Vivado 菜单栏，点击 "File" -> "Save" (或者使用快捷键 Ctrl+S) 保存约束文件。

4.  **查看 Constraints:**  在 "Project Manager" -> "Constraints" 目录中，您应该能看到您刚刚创建的 `zedboard_constraints.xdc` 文件。

## **步骤 4：设置顶层模块 (如果需要)**

*   对于这个简单的例子，我们的 `led_controller` 模块已经是顶层模块了。  Vivado 默认会将工程中唯一的 HDL 设计源文件作为顶层。
*   如果您的设计更复杂，有多个模块，并且您创建了一个专门的顶层模块来例化其他子模块，您需要手动设置顶层模块。对于这个 LED 闪烁例子，我们跳过这个步骤。

## **步骤 5：综合、实现、生成比特流**

1.  ==**运行综合 (Synthesis):**==
    *   在 Vivado 界面左侧的 **"Flow Navigator"** 窗口中，找到 "SYNTHESIS" 标题下的 "Run Synthesis"。双击 "Run Synthesis"。
    *   Vivado 会弹出 "Launch Runs" 对话框，直接点击 "OK" 即可开始综合。
    *   等待综合完成。您可以在 Vivado 窗口底部的 "运行" 选项卡中查看综合的进度和日志信息。如果综合成功，"Run Synthesis" 状态会变为 "Complete"。

2.  ==**运行实现 (Implementation):**==
    *   在 "Flow Navigator" 窗口中，找到 "IMPLEMENTATION" 标题下的 "Run Implementation"。双击 "Run Implementation"。
    *   类似地，弹出 "Launch Runs" 对话框时，点击 "OK"。
    *   等待实现完成。实现过程比综合时间稍长。如果实现成功，"Run Implementation" 状态会变为 "Complete"。

3.  ==**生成比特流 (Generate Bitstream):**==
    *   在 "Flow Navigator" 窗口中，找到 "PROGRAM AND DEBUG" 标题下的 "Generate Bitstream"。双击 "Generate Bitstream"。
    *   弹出 "Launch Runs" 对话框时，点击 "OK"。
    *   等待比特流生成完成。如果比特流生成成功，"Generate Bitstream" 状态会变为 "Complete"。==比特流文件 (`.bit` 文件) 会生成在工程的 `工程名.runs\impl_1` 目录下 (相对路径)。==

## **步骤 6：连接 ZedBoard 并加载比特流**

1.  **连接 ZedBoard:**
    *   将 ZedBoard 开发板通过 USB Type-B 线缆连接到您的电脑。
    *   确保 ZedBoard 开发板已上电 (通常连接 USB 线缆就会自动供电，或者检查是否有电源开关需要打开)。

2.  **打开 Hardware Manager:**
    *   在 Vivado 界面左侧的 **"Flow Navigator"** 窗口中，找到 =="PROGRAM AND DEBUG" 标题下的 "Open Hardware Manager"==。双击 "Open Hardware Manager"。

3.  **连接硬件目标:**
    *   在打开的 "Hardware Manager" 窗口中，点击左侧的 "HARDWARE" 标题。
    *   点击工具栏的 "Open target" 图标 (看起来像一个连接的图标)，选择 "Auto Connect"。
    *   Vivado 应该会自动检测到连接的 ZedBoard 开发板，并在 "Hardware" 窗口中显示  "localhost" (或者您的电脑名) -> "xc7z020_1"。如果连接不成功，请检查 USB 连接、ZedBoard 电源，以及是否安装了 ZedBoard 的驱动程序 (如果需要)。
	![](../fujian/Pasted%20image%2020250328100410.png)

4.  **编程器件:**
    *   ==在 "Hardware" 窗口中，选中  "xc7z020_1" 器件 (通常会高亮显示)。==
    *   ==右键点击 "xc7z020_1"，选择 "Program Device..."。==
    *   在弹出的 "Program Device" 对话框中：
        *   **Configuration file:**  默认情况下，Vivado 应该会自动选择您刚刚生成的比特流文件 (`.bit` 文件)。检查 "Configuration file" 路径是否正确指向您的 `.bit` 文件 (例如  `工程路径/工程名.runs/impl_1/led_controller_wrapper.bit`，文件名可能会根据您的顶层模块名称有所不同)。如果路径不正确，点击 "..." 按钮手动选择正确的 `.bit` 文件。
        *   其他选项保持默认即可。
        *   点击 "Program"。

5.  **等待编程完成:**  Vivado 会开始将比特流文件下载到 ZedBoard 的 FPGA 中。您可以在 Vivado 窗口底部查看编程进度。编程完成后，您应该会在 Vivado 窗口中看到 "Programmed device xc7z020_1 successfully" 的提示信息。

## **步骤 7：观察 LED 闪烁效果**

*   比特流成功加载到 ZedBoard 后，您应该立即看到 ZedBoard 板上的 8 个 LED 开始按照顺序轮流点亮，每个 LED 点亮 0.5 秒左右，然后熄灭，接着点亮下一个，循环往复。

*   **如果 LED 闪烁效果不正确或没有闪烁:**
    *   **检查硬件连接:**  确认 USB 线缆连接良好，ZedBoard 是否上电。
    *   **检查约束文件 (`zedboard_constraints. xdc`):**  再次仔细核对 **时钟输入引脚** 和 **LED 输出引脚** 的 `PACKAGE_PIN` 设置是否与您的 ZedBoard 版本和硬件连接完全一致。  **这是最常见的错误来源。务必认真检查！**
    *   **检查代码 (`led_controller. vhd` 或 `led_controller. v`):**  检查代码逻辑是否有错误，例如计数器计算、LED 索引更新、LED 状态赋值部分。虽然我们提供的代码示例经过验证，但也要仔细检查您粘贴的代码是否完整，是否有改动导致错误。
    *   **重新生成比特流并加载:**  如果修改了代码或约束文件，需要重新从 **步骤 5** 开始，重新进行综合、实现和生成比特流，然后再重新加载到 ZedBoard。
    *   **使用硬件调试工具 (进阶):**  如果问题依然无法解决，您可以考虑使用 Vivado 的硬件调试工具，例如 ILA (Integrated Logic Analyzer)，来在线观察 FPGA 内部信号的状态，帮助您定位问题。这涉及到更高级的调试技巧，对于初学者可以先关注前面的检查步骤。

恭喜您！如果一切顺利，您应该已经成功地使用 Vivado 创建工程，实现了 Zynq-7020 PL 端 LED 轮流点亮的功能，并熟悉了基本的 Vivado 设计流程。这是一个很好的开始！之后您可以尝试修改代码，例如调整 LED 闪烁速度，或者实现更复杂的功能。继续探索吧！