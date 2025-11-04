---
up:
  - "[[../moc/MocCotex|MocCotex]]"
---



明白了！要讲解如何使用串口 FIFO，我会从配置、数据传输、中断处理等方面，提供一个清晰且实用的指南。以下是如何使用串口 FIFO 的详细步骤和说明：

**使用串口 FIFO 的步骤和方法：**

1.  ==**使能 UART FIFO 功能 (重要第一步):**==

    *   **查找 UART 控制寄存器:**  首先，你需要查阅你所使用的 MCU 的 UART 硬件手册 (Datasheet 或 Reference Manual)，找到 **UART 控制寄存器 (通常名称类似 `UARTx_FCR` - FIFO Control Register，或类似的，具体名称请查阅手册)**。这个寄存器是用来配置 UART FIFO 功能的关键。
    *   **设置 FIFO 使能位:**  在控制寄存器中，通常有一个或多个位专门用于 **使能 (Enable) 发送 FIFO (TX FIFO) 和接收 FIFO (RX FIFO)**。你需要将相应的位设置为 `1` 来启用 FIFO 功能。例如，你可能会找到类似 `FIFOEN` (FIFO Enable)、`TXFE` (Transmit FIFO Enable)、`RXFE` (Receive FIFO Enable) 这样的位。 **务必仔细阅读手册，确认具体的位名称和设置方法。**

    ```c
    // 示例代码 (伪代码，需根据具体 MCU 和寄存器定义修改)
    UARTx->FCR |= (1 << FIFOEN_BIT);     // 使能 TX 和 RX FIFO (如果合并控制)
    // 或者
    UARTx->FCR |= (1 << TXFE_BIT) | (1 << RXFE_BIT); // 分别使能 TX 和 RX FIFO
    ```

2.  **(可选) 配置 FIFO 深度/大小 (如果可配置):**

    *   **检查是否可配置深度:**  有些高级的 UART 控制器可能允许用户配置 FIFO 的深度 (例如，选择 8 字节、16 字节、32 字节等)。查看硬件手册，确认你的 UART 是否支持配置 FIFO 深度。
    *   **设置深度控制位:**  如果可以配置，控制寄存器中会有相应的位来设置 FIFO 深度。根据你的应用需求和系统资源，选择合适的 FIFO 深度。更大的 FIFO 可以提供更好的缓冲能力，但也会占用更多的硬件资源。
    *   **注意：**  不是所有的 UART 都允许配置 FIFO 深度，很多简单的 UART 的 FIFO 深度是固定的，例如 16 字节或 64 字节。

3.  **配置接收 FIFO 触发阈值 (RX FIFO Threshold Level):**

    *   **查找 RX FIFO 触发阈值配置位:**  在 UART 控制寄存器中，通常会有一些位用于 **设置 RX FIFO 的触发阈值 (RX FIFO Trigger Level)**。这个阈值决定了当 RX FIFO 中有多少字节的数据时，会触发接收数据可用中断 (或 DMA 请求，如果使用 DMA)。
    *   **选择合适的阈值:**  你可以根据你的应用需求选择合适的阈值。
        *   **较小的阈值 (例如 1 字节或 4 字节):**  可以更快地响应接收到的数据，延迟较低，但可能会导致更频繁的中断。适用于需要 **低延迟响应** 的应用。
        *   **较大的阈值 (例如 8 字节、16 字节，甚至更大):**  可以减少中断次数，降低 CPU 负载，提高系统效率。适用于 **数据吞吐量较大，但对延迟不敏感** 的应用。
    *   **设置阈值控制位:**  根据硬件手册，设置相应的位，选择你想要的触发阈值。

    ```c
    // 示例代码 (伪代码，需根据具体 MCU 和寄存器定义修改)
    UARTx->FCR &= ~(0x3 << RX_FIFO_TRIGGER_LEVEL_BITS); // 清除阈值配置位
    UARTx->FCR |= (TRIGGER_LEVEL_8_BYTES << RX_FIFO_TRIGGER_LEVEL_BITS); // 设置阈值为 8 字节触发中断
    ```

4.  **发送数据到 TX FIFO:**

    *   **检查 TX FIFO 是否未满:**  在写入数据之前，**务必先检查 TX FIFO 是否已满**。你可以读取 UART 状态寄存器 (例如 `UARTx_FR` - FIFO Register 或类似的)，找到 TX FIFO 满标志位 (例如 `TXFF` - Transmit FIFO Full)。
    *   **写入发送数据寄存器:**  如果 TX FIFO 未满，则将要发送的数据 ==**写入 UART 的发送数据寄存器 (通常名称类似 `UARTx_THR` - Transmit Holding Register)**。==硬件会自动将数据存入 TX FIFO 队列的尾部，并开始发送。
    *   **循环发送多个字节:**  你可以循环写入多个字节的数据，只要 TX FIFO 未满，就可以持续写入。
    *   **轮询或中断驱动发送:**  你可以使用 **轮询方式** 不断检查 TX FIFO 是否未满，并写入数据。更高效的方式是使用 **发送 FIFO 空中断 (TX FIFO Empty Interrupt)**，当 TX FIFO 空或者低于一定水位时，会触发中断，在中断服务程序中写入更多的数据。

    ```c
    // 示例代码 - 轮询方式发送字符串 (伪代码)
    const char* data_to_send = "Hello, FIFO!";
    int data_len = strlen(data_to_send);
    for (int i = 0; i < data_len; i++) {
        // 循环检查 TX FIFO 是否未满 (TXFF=0 表示未满)
        while (UARTx->FR & (1 << TXFF_BIT)) {
            // 等待 TX FIFO 空闲 (可以加入超时机制)
        }
        UARTx->THR = data_to_send[i]; // 写入发送数据寄存器 (实际写入 TX FIFO)
    }
    ```

5.  **从 RX FIFO 读取接收到的数据:**

    *   **检查 RX FIFO 是否非空:**  在读取数据之前，**务必先检查 RX FIFO 是否非空**。读取 UART 状态寄存器，找到 RX FIFO 空标志位 (例如 `RXFE` - Receive FIFO Empty)。  `RXFE = 0` 表示 RX FIFO 非空，有数据可以读取。
    *   **读取接收数据寄存器:**  如果 RX FIFO 非空，则从 **UART 的接收数据寄存器 (通常名称类似 `UARTx_RBR` - Receive Buffer Register 或 `UARTx_DR` - Data Register)** 读取数据。硬件会自动从 RX FIFO 队列的头部取出数据返回。
    *   **循环读取多个字节:**  你可以循环读取多个字节的数据，只要 RX FIFO 非空，就可以持续读取。
    *   **轮询或中断/DMA驱动接收:**  你可以使用 **轮询方式** 不断检查 RX FIFO 是否非空，并读取数据。更高效的方式是使用 **接收数据可用中断 (RX Data Available Interrupt 或 RX FIFO Threshold Interrupt)**，当 RX FIFO 中有数据达到触发阈值时，会触发中断，在中断服务程序中读取 FIFO 中的数据。如果需要传输大量数据，可以使用 **DMA**，配置 UART DMA 请求，让 DMA 控制器自动将 RX FIFO 中的数据搬运到内存中。

    ```c
    // 示例代码 - 轮询方式接收数据 (伪代码)
    uint8_t received_byte;
    if (!(UARTx->FR & (1 << RXFE_BIT))) { // 检查 RX FIFO 是否非空 (RXFE=0 表示非空)
        received_byte = UARTx->RBR;     // 读取接收数据寄存器 (实际从 RX FIFO 读取)
        // 处理 received_byte
    }
    ```

6.  **处理 FIFO 相关的状态标志和中断:**

    *   **状态寄存器 (Status Register - 例如 `UARTx_FR` 或 `UARTx_USR` 等):**  密切关注 UART 的状态寄存器，它提供了各种 FIFO 的状态信息，例如：
        *   **TX FIFO 空标志 (TXFE 或 TXFE):** 指示 TX FIFO 是否为空，可以用于判断是否可以写入更多数据。
        *   **TX FIFO 满标志 (TXFF 或 TXFF):** 指示 TX FIFO 是否已满，避免写入溢出。
        *   **RX FIFO 空标志 (RXFE 或 RXFE):** 指示 RX FIFO 是否为空，用于判断是否还有数据可以读取。
        *   **RX FIFO 满标志 (RXFF 或 RXFF):** 指示 RX FIFO 是否已满，如果持续接收数据可能导致溢出。
        *   **接收溢出错误标志 (OE 或 OERR):**  指示 RX FIFO 是否发生过溢出。如果设置了这个标志，需要清除它，才能继续正常接收。
        *   **奇偶校验错误、帧错误等标志 (PE, FE):**  如果启用了奇偶校验或帧错误检测，状态寄存器也会包含这些错误标志。

    *   **中断使能寄存器 (Interrupt Enable Register - 例如 `UARTx_IER` 或 `UARTx_IMSC` 等):**  使能你需要的 FIFO 相关中断：
        *   **发送 FIFO 空中断 (TX Empty Interrupt - TXEIE 或 TXIM):**  当 TX FIFO 为空或者低于某个水位时触发，用于在中断服务程序中填充更多要发送的数据。
        *   **接收数据可用中断 (RX Data Ready Interrupt, RX Threshold Interrupt - RXIE, RXIM, RTIM):**  当 RX FIFO 中数据达到触发阈值或接收到新数据时触发，用于在中断服务程序中读取接收到的数据。
        *   **接收溢出错误中断 (Receive Overrun Interrupt - OEI 或 OEIM):**  当 RX FIFO 发生溢出时触发，用于在中断服务程序中处理溢出错误 (例如，清空 FIFO 或记录错误)。

    *   **中断服务程序 (ISR - Interrupt Service Routine):**  编写中断服务程序来处理各种 UART FIFO 相关中断。在 ISR 中，通常需要完成以下操作：
        *   **读取状态寄存器，判断中断源。**
        *   **如果是 TX 空中断:**  向 TX FIFO 写入更多的数据。
        *   **如果是 RX 数据可用中断:**  从 RX FIFO 读取接收到的数据。
        *   **如果是溢出错误中断:**  清除溢出错误标志，并进行错误处理 (例如，丢弃 FIFO 中的数据，重新初始化 UART)。
        *   **清除中断标志位 (如果需要手动清除):**  一些 UART 的中断标志位需要手动清除，才能再次触发中断。查看硬件手册了解清除中断标志的方法。

7.  **错误处理:**

    *   **接收溢出 (RX FIFO Overflow):** 特别注意 RX FIFO 溢出的情况。一旦发生溢出，新接收的数据通常会丢失。你需要在软件中检测溢出错误标志，并在发生溢出时进行适当的处理，例如：
        *   **清空 RX FIFO:**  可以通过读取 RX 数据寄存器多次，直到 RX FIFO 为空，来清空 FIFO 中的残留数据。
        *   **复位 UART 接收器 (在严重错误情况下):**  在某些情况下，可能需要复位 UART 接收器来恢复正常工作。
        *   **增加 RX FIFO 大小或调整触发阈值 (如果条件允许):**  在系统设计初期，可以考虑选择 FIFO 深度更大的 UART 或者调整 RX FIFO 触发阈值，以减少溢出的风险。
        *   **确保 CPU 处理接收数据的速度足够快:**  软件设计上要确保 CPU 能够及时处理串口接收的数据，避免 RX FIFO 长期处于满的状态。

**总结使用 UART FIFO 的关键点:**

*   **使能 FIFO 功能是第一步，务必配置 UART 控制寄存器。**
*   **根据应用需求配置 RX FIFO 触发阈值，平衡延迟和中断开销。**
*   **发送数据前检查 TX FIFO 是否未满，接收数据前检查 RX FIFO 是否非空。**
*   **使用状态寄存器监控 FIFO 状态，避免溢出和错误。**
*   **利用中断或 DMA 驱动数据传输，提高效率。**
*   **认真阅读 MCU 的 UART 硬件手册，了解具体的寄存器定义、位功能和操作方法。**

通过合理地配置和使用串口 FIFO，你可以更有效地管理串口数据，降低 CPU 负载，提高数据传输效率和可靠性，尤其是在高速率串口通信和需要处理大量数据的嵌入式系统中，FIFO 的作用尤为重要。



# 2
明白了！你想了解如何实际使用 USART 的 FIFO 功能。我会从软件配置和操作的角度，结合代码示例，一步一步地讲解如何使用 USART FIFO 进行数据发送和接收。

**使用 USART FIFO 的步骤 (软件层面):**

1.  **初始化 USART 和 FIFO:**

    *   **使能 USART 时钟:**  在 MCU 的 RCC (Reset and Clock Control) 外设中，找到 USART 对应的时钟使能位，并将其置位，开启 USART 模块的时钟。
    *   **配置 GPIO 引脚:**  配置与 USART 的 TX 和 RX 功能对应的 GPIO 引脚。通常需要将这些引脚配置为复用功能 (Alternate Function) 模式，并选择正确的 USART 复用功能。具体的引脚和复用功能选择请查阅 MCU 的数据手册。
    *   **配置 USART 基本参数 (不含 FIFO):**  在 USART 控制寄存器中，配置基本的串口参数，例如：
        *   **波特率:**  设置 `USARTx_BRR` 寄存器，计算并写入合适的波特率分频值。
        *   **数据位长度、停止位、奇偶校验:**  配置 `USARTx_CR1` 和 `USARTx_CR2` 寄存器中的相关位域。例如，选择 8 位数据位，1 个停止位，无奇偶校验。
        *   **使能发送器 (TE) 和接收器 (RE):**  设置 `USARTx_CR1` 寄存器中的 `TE` 和 `RE` 位，使能 USART 的发送和接收功能。
    *   **使能 FIFO 功能:**  **关键步骤！** 在 USART 的 FIFO 控制寄存器 (例如 `USARTx_FCR`) 中，**找到并设置 FIFO 使能位 (例如 `FIFOEN`, `TXFE`, `RXFE`)**。通常，设置为 `1` 来使能 FIFO。

    ```c
    // 示例代码 (伪代码，需根据具体 MCU 修改)
    void USART_FIFO_Init(uint32_t baudrate) {
        // 1. 使能 USART 时钟 (假设 USART1)
        RCC->APB2ENR |= (1 << USART1EN_BIT); // 假设 USART1EN_BIT 是 USART1 时钟使能位

        // 2. 配置 GPIO 引脚 (假设 PA9-TX, PA10-RX, 具体引脚查阅手册)
        // 使能 GPIOA 时钟
        RCC->APB2ENR |= (1 << GPIOAEN_BIT);

        // 配置 PA9 为复用推挽输出, PA10 为浮空输入 (或复用输入)
        GPIOA->CRH &= ~(0xF << GPIO_CRH_CNF9_MODE9_POS); // 清除 PA9 配置
        GPIOA->CRH |=  (GPIO_CRH_CNF_AF_PP << GPIO_CRH_CNF9_MODE9_POS) | (GPIO_CRH_MODE_OUT50 << GPIO_CRH_MODE9_MODE9_POS); // PA9: 复用推挽输出, 50MHz
        GPIOA->CRH &= ~(0xF << GPIO_CRH_CNF10_MODE10_POS); // 清除 PA10 配置
        GPIOA->CRH |=  (GPIO_CRH_CNF_IN_FLOAT << GPIO_CRH_CNF10_MODE10_POS); // PA10: 浮空输入

        // 配置 PA9,PA10 复用功能为 USART1 (具体复用功能号查阅手册)
        // (某些 MCU 可能有 AFIO 或 SYSCFG 寄存器来配置 GPIO 复用功能)
        // ... (具体配置方法请查阅 MCU 手册) ...

        // 3. 配置 USART 基本参数 (不含 FIFO)
        USARTx->CR1 = 0; // 复位 CR1
        USARTx->CR2 = 0; // 复位 CR2
        USARTx->CR3 = 0; // 复位 CR3

        // 配置波特率 (假设系统时钟 SYSCLK, 计算分频值)
        uint32_t baud_div = SystemCoreClock / baudrate; // 简化计算，实际需考虑小数部分和过采样等因素
        USARTx->BRR = baud_div;

        // 配置数据位长度, 停止位, 奇偶校验 (例如 8N1 - 8位数据, 无校验, 1停止位)
        USARTx->CR1 &= ~(1 << USART_CR1_M_BIT);  // 8 位数据 (M=0)
        USARTx->CR1 &= ~(1 << USART_CR1_PCE_BIT); // 无奇偶校验 (PCE=0)
        USARTx->CR2 &= ~(0x3 << USART_CR2_STOP_BITS); // 1 停止位 (STOP=00)

        // 4. 使能 FIFO 功能 (在 FIFO 控制寄存器中设置 FIFOEN 位)
        USARTx->FCR |= (1 << FIFOEN_BIT); // 假设 FIFOEN_BIT 是 FIFO 使能位 (具体查阅手册)
        // 或者
        USARTx->FCR |= (1 << TXFE_BIT) | (1 << RXFE_BIT); // 分别使能 TX/RX FIFO (如果可以分别使能)

        // 5. 使能发送器和接收器
        USARTx->CR1 |= (1 << USART_CR1_TE_BIT); // 使能发送器 (TE=1)
        USARTx->CR1 |= (1 << USART_CR1_RE_BIT); // 使能接收器 (RE=1)

        // 6. 使能 USART 外设
        USARTx->CR1 |= (1 << USART_CR1_UE_BIT); // 使能 USART (UE=1)
    }
    ```

2.  **(可选) 配置 RX FIFO 触发阈值:**

    *   如果你的应用需要通过中断或 DMA 驱动接收，并且你想控制中断或 DMA 请求的触发频率，可以配置 **接收 FIFO 触发阈值 (RX FIFO Trigger Level)**。
    *   在 FIFO 控制寄存器 (`USARTx_FCR`) 中，找到并设置 **RX FIFO 触发阈值相关的位域 (例如 `RXFIFOTR`, `RFT`)**。常见的阈值选项可能有 1/4 满，1/2 满，3/4 满，或者 1 字节，4 字节，8 字节等。选择合适的阈值取决于你的应用需求，例如：
        *   **小阈值 (例如 1/4 满或 1字节):**  更早地触发中断或 DMA 请求，响应更及时，延迟较低，但中断或 DMA 请求更频繁。适用于需要低延迟响应的应用。
        *   **大阈值 (例如 3/4 满或 8字节或更大):**  减少中断或 DMA 请求次数，降低 CPU 负载，提高系统效率。适用于数据吞吐量大，但对延迟要求不高的应用。

    ```c
    // 示例代码 (伪代码)
    // 配置 RX FIFO 触发阈值为 8 字节 (假设 TRIGGER_LEVEL_8_BYTES 常量定义了 8 字节阈值对应的位值)
    USARTx->FCR &= ~(0x3 << RX_FIFO_TRIGGER_LEVEL_BITS); // 清除之前的阈值配置位
    USARTx->FCR |= (TRIGGER_LEVEL_8_BYTES << RX_FIFO_TRIGGER_LEVEL_BITS); // 设置阈值为 8 字节
    ```

3.  **发送数据 (使用 TX FIFO):**

    *   **轮询方式发送:**
        *   在发送每个字节之前， **检查 TX FIFO 是否已满**。读取 USART 状态寄存器 (例如 `USARTx_SR` 或 `USARTx_FR`)，检查 **TX FIFO 满标志位 (例如 `TXFF`)**。如果 `TXFF` 位为 0 (或未置位，具体看手册)，表示 TX FIFO 未满，可以写入数据。
        *   将要发送的==数据 **写入 USART 的数据寄存器 (`USARTx_DR`)**。硬件会自动将数据放入 TX FIFO 队列，并启动发送。==
        *   循环上述步骤，直到所有数据发送完毕。

    ```c
    // 示例代码 - 轮询方式发送字符串 (使用 TX FIFO)
    void USART_FIFO_SendString_Polling(USART_TypeDef *USARTx, const char *str) {
        while (*str) {
            // 循环检查 TX FIFO 是否未满 (假设 TXFF_BIT 是 TX FIFO 满标志位)
            while (USARTx->SR & (1 << TXFF_BIT)) {
                // 等待 TX FIFO 空闲 (可以加入超时机制)
            }
            USARTx->DR = (*str & 0xFF); // 写入数据寄存器 (实际写入 TX FIFO)
            str++;
        }
    }
    ```

    *   **中断驱动发送 (使用 TX FIFO 空中断):**
        *   **使能发送 FIFO 空中断 (TX Empty Interrupt Enable)**。在 USART 中断使能寄存器 (`USARTx_IER` 或 `USARTx_CR3`) 中，找到并设置 **TX FIFO 空中断使能位 (例如 `TXEIE`, `TXIM`)**。
        *   **编写 USART 中断服务程序 (ISR):**  在 ISR 中，执行以下操作：
            *   **判断中断类型:**  检查中断状态寄存器，确认是 TX FIFO 空中断。
            *   **填充 TX FIFO:**  只要 TX FIFO 未满，就从你的发送缓冲区 (例如，全局的发送数据数组) 中取出数据，写入 `USARTx_DR`，填充 TX FIFO。直到 TX FIFO 再次变满，或者所有数据都已放入 FIFO。
            *   **关闭 TX 空中断 (可选):** 如果一次发送的数据量固定，并且在 TX FIFO 填满后就完成了本次发送，可以考虑在 ISR 中关闭 TX 空中断，避免不必要的后续中断。在下一次需要发送数据时，再重新使能 TX 空中断。

    ```c
    // 示例代码 - 中断驱动发送 (使用 TX FIFO 空中断)
    uint8_t tx_buffer[TX_BUFFER_SIZE]; // 发送缓冲区
    uint32_t tx_buffer_head = 0;
    uint32_t tx_buffer_tail = 0;
    volatile bool tx_busy = false; // 发送忙标志

    void USART_FIFO_StartTransmit_Interrupt(USART_TypeDef *USARTx, const uint8_t *data, uint32_t len) {
        // 1. 将要发送的数据复制到发送缓冲区 (tx_buffer)
        // ... (代码实现，例如 memcpy) ...
        tx_buffer_head = 0;
        tx_buffer_tail = len;
        tx_busy = true;

        // 2. 使能 TX FIFO 空中断
        USARTx->IER |= (1 << TXEIE_BIT); // 假设 TXEIE_BIT 是 TX 空中断使能位

        // 3. (可选) 首次填充 TX FIFO (如果在使能中断前 TX FIFO 就为空，可能需要先启动发送)
        USART_Fill_TX_FIFO(USARTx); //  函数 USART_Fill_TX_FIFO 实现下面ISR中的填充逻辑
    }

    // USART 中断服务程序 (ISR)
    void USARTx_IRQHandler(void) {
        if (USARTx->SR & (1 << TXE_FLAG_BIT)) { // 检查是否是 TX 空中断 (假设 TXE_FLAG_BIT 是 TXE 标志位)
            USART_Fill_TX_FIFO(USARTx); // 填充 TX FIFO
        }
        // ... (处理其他可能的 USART 中断，例如 RX 中断，错误中断) ...
    }

    void USART_Fill_TX_FIFO(USART_TypeDef *USARTx) {
        while (!(USARTx->SR & (1 << TXFF_BIT)) && (tx_buffer_head < tx_buffer_tail)) { // TX FIFO 未满 且 还有数据要发送
            USARTx->DR = tx_buffer[tx_buffer_head++]; // 写入数据寄存器 (填充 TX FIFO)
        }
        if (tx_buffer_head >= tx_buffer_tail) { // 所有数据发送完毕
            tx_busy = false;
            USARTx->IER &= ~(1 << TXEIE_BIT); // 关闭 TX 空中断
            // (可选) 发送完成后的处理，例如发送完成回调函数
        }
    }
    ```

4.  **接收数据 (使用 RX FIFO):**

    *   **轮询方式接收:**
        *   **检查 RX FIFO 是否非空**。读取 USART 状态寄存器，检查 **RX FIFO 空标志位 (例如 `RXFE`)**。如果 `RXFE` 位为 0 (或未置位)，表示 RX FIFO 非空，有数据可以读取。
        *   **从 USART 的数据寄存器 (`USARTx_DR`) 读取数据**。硬件会自动从 RX FIFO 队列中取出数据。
        *   循环上述步骤，直到接收到期望数量的数据，或者 RX FIFO 变空。

    ```c
    // 示例代码 - 轮询方式接收字符串 (使用 RX FIFO)
    void USART_FIFO_ReceiveString_Polling(USART_TypeDef *USARTx, char *buffer, uint32_t max_len) {
        uint32_t rx_count = 0;
        while (rx_count < max_len) {
            // 检查 RX FIFO 是否非空 (假设 RXFE_BIT 是 RX FIFO 空标志位)
            if (!(USARTx->SR & (1 << RXFE_BIT))) {
                buffer[rx_count++] = (char)(USARTx->DR & 0xFF); // 读取数据寄存器 (从 RX FIFO 读取)
            } else {
                break; // RX FIFO 已空，退出循环 (可以加入超时机制)
            }
        }
        buffer[rx_count] = '\0'; // 添加字符串结束符
    }
    ```

    *   **中断/DMA 驱动接收 (使用 RX 数据就绪中断或 RX FIFO 阈值中断):**
        *   **使能接收数据就绪中断或 RX FIFO 阈值中断**。在 `USARTx_IER` 或 `USARTx_CR3` 中，找到并设置 **RX 数据就绪中断使能位 (例如 `RXNEIE`, `RXIE`, `RTIM`)**。如果配置了 RX FIFO 触发阈值，通常使用 RX FIFO 阈值中断。
        *   **编写 USART 中断服务程序 (ISR):**  在 ISR 中，执行以下操作：
            *   **判断中断类型:**  检查中断状态寄存器，确认是 RX 数据就绪或 RX FIFO 阈值中断。
            *   **读取 RX FIFO 数据:**  循环读取 `USARTx_DR`，从 RX FIFO 中取出接收到的数据，并将其存储到接收缓冲区 (例如，全局的接收数据数组)。直到 RX FIFO 变空 (通过检查 `RXFE` 标志)，或者接收到足够的数据。
            *   **处理接收到的数据 (可选):**  可以在 ISR 中直接处理接收到的数据 (如果处理逻辑简单)，或者将数据放入队列，由其他任务或函数在后台处理。

    ```c
    // 示例代码 - 中断驱动接收 (使用 RX 数据就绪中断)
    uint8_t rx_buffer[RX_BUFFER_SIZE]; // 接收缓冲区
    uint32_t rx_buffer_head = 0;
    uint32_t rx_buffer_tail = 0;

    void USART_FIFO_StartReceive_Interrupt(USART_TypeDef *USARTx) {
        rx_buffer_head = 0;
        rx_buffer_tail = 0;
        // 使能 RX 数据就绪中断
        USARTx->IER |= (1 << RXNEIE_BIT); // 假设 RXNEIE_BIT 是 RX 数据就绪中断使能位
    }

    // USART 中断服务程序 (ISR)
    void USARTx_IRQHandler(void) {
        if (USARTx->SR & (1 << RXNE_FLAG_BIT)) { // 检查是否是 RX 数据就绪中断 (假设 RXNE_FLAG_BIT 是 RXNE 标志位)
            uint8_t received_byte = USARTx->DR; // 读取数据寄存器 (从 RX FIFO 读取)
            rx_buffer[rx_buffer_tail++] = received_byte; // 存入接收缓冲区
            if (rx_buffer_tail >= RX_BUFFER_SIZE) { // 缓冲区满处理 (示例：环形缓冲区，或者丢弃旧数据)
                rx_buffer_tail = 0; // 环形缓冲区，从头开始覆盖
                // 或者  rx_buffer_tail = RX_BUFFER_SIZE -1; // 限制缓冲区大小，忽略后续数据
            }
            // (可选) 处理 received_byte，例如放入队列
        }
        // ... (处理其他可能的 USART 中断，例如 TX 中断，错误中断) ...
    }
    ```

5.  **错误处理 (接收溢出错误):**

    *   在接收数据时，需要 **定期检查 USART 状态寄存器中的错误标志**，特别是 **接收溢出错误标志 (例如 `ORE`, `OVR`)**。
    *   如果检测到溢出错误标志被置位，说明 RX FIFO 发生了溢出，新接收到的数据可能已经丢失。你需要采取适当的错误处理措施，例如：
        *   **清除溢出错误标志:**  通常需要通过 **读取 USART 状态寄存器，或者向特定的清除寄存器写入值** 来清除溢出错误标志 (具体看 MCU 的手册说明)。  **在清除错误标志之前，通常需要先读取 `USARTx_DR` 来清除可能残留在接收数据寄存器中的错误数据。**
        *   **清空 RX FIFO (可选):**  可以通过循环读取 `USARTx_DR`，直到 RX FIFO 为空，来清空 FIFO 中的数据。
        *   **通知上层应用:**  可以通过设置错误标志，或者调用错误回调函数，通知上层应用发生了串口接收错误，以便进行进一步的处理 (例如，重传数据，或者提示用户)。

    ```c
    // 示例代码 - 检查和清除接收溢出错误
    void USART_Check_ReceiveError(USART_TypeDef *USARTx) {
        if (USARTx->SR & (1 << ORE_FLAG_BIT)) { // 假设 ORE_FLAG_BIT 是溢出错误标志位
            // 发生接收溢出错误
            uint32_t dummy_read = USARTx->DR; // 读取数据寄存器，清除数据寄存器中的错误数据 (有些 MCU 需要)
            USARTx->SR &= ~(1 << ORE_FLAG_BIT); // 清除溢出错误标志 (具体清除方法查阅手册，可能需要读SR再写CR)
            // 可以记录错误，或者通知上层应用
            // Error_Handler("USART Receive Overflow Error!");
        }
        // ... (可以检查其他错误标志，例如帧错误 FE，奇偶校验错误 PE) ...
    }
    ```

**总结使用 FIFO 的关键点:**

*   **务必使能 FIFO 功能 (设置 `FIFOEN` 或相关位)。**
*   **根据应用场景选择合适的 RX FIFO 触发阈值 (如果需要中断或 DMA 驱动)。**
*   **发送数据前检查 TX FIFO 是否未满 (`TXFF` 标志)，接收数据前检查 RX FIFO 是否非空 (`RXFE` 标志)。**
*   **使用中断或 DMA 可以提高数据传输效率，降低 CPU 轮询开销。**
*   **重视错误处理，特别是接收溢出错误 (`ORE`)，确保数据通信的可靠性。**
*   **始终以你所使用的 MCU 的 *参考手册* 为准，查找正确的寄存器名称、位定义、以及操作方法。**

希望这些步骤和代码示例能够帮助你理解和使用 USART 的 FIFO 功能。实际应用中，你需要根据你的具体 MCU 型号和应用需求，参考硬件手册，进行详细的配置和编程。