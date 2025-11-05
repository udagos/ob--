---
up:
  - "[[../moc/MocCotex|MocCotex]]"
---



STM32的 `.sct` 文件和Zynq的 `.ld` 文件在语法和功能上存在一些差异，以下是两者的主要区别：

### 语法结构
- **STM32的`.sct`文件**：
    - ==由一个或多个加载域（load regions）组成，每个加载域由一个或多个执行域（execution regions）组成。==
    - 加载域和执行域之间使用花括号“{}”分隔。
    - 示例：
        ```plaintext
        LR_IROM1 0x08000000 0x00020000  {
            ER_IROM1 0x08000000 0x00020000  {
                *.o (RESET, +First)
                *(InRoot$$Sections)
                .ANY (+RO)
            }
            RW_IRAM1 0x20000000 0x00005000  {
                .ANY (+RW +ZI)
            }
        }
        ```
- **Zynq的`.ld`文件**：
    - ==使用`MEMORY`关键字定义内存区域，使用`SECTIONS`关键字定义段的放置。==
    - 示例：
        ```plaintext
        MEMORY {
            ps7_ddr : ORIGIN = 0x10000000, LENGTH = 0x8000000
            ps7_ram : ORIGIN = 0x00000000, LENGTH = 0x100000
        }
        SECTIONS {
            .text : {
                *(.text)
            } > ps7_ddr
            .data : {
                *(.data)
            } > ps7_ddr
            .bss : {
                *(.bss)
            } > ps7_ddr
        }
        ```

### 输入节区描述
- **STM32的`.sct`文件**：
    - 使用模块选择样式“(`输入节区样式`, `+`输入节区属性)”。
    - 示例：
        ```plaintext
        *.o (RESET, +First)
        *(InRoot$$Sections)
        .ANY (+RO)
        ```
    - 其中，`*.o`表示选择所有`.o`文件，`RESET`是输入节区样式，`+First`是节区特性，表示将`RESET`节区放置到本区域的第一个位置。
- **Zynq的`.ld`文件**：
    - 使用`*(输入节区)`的形式。
    - 示例：
        ```plaintext
        *(.text)
        *(.data)
        *(.bss)
        ```

### 内存区域定义
- **STM32的`.sct`文件**：
    - 在加载域中直接指定基地址和大小。
    - 示例：
        ```plaintext
        LR_IROM1 0x08000000 0x00020000
        ```
- **Zynq的`.ld`文件**：
    - 使用`MEMORY`关键字定义内存区域的名称、起始地址和长度。
    - 示例：
        ```plaintext
        MEMORY {
            ps7_ddr : ORIGIN = 0x10000000, LENGTH = 0x8000000
        }
        ```

### 注释符号
- **STM32的`.sct`文件**：
    - 使用`;`作为注释符。
- **Zynq的`.ld`文件**：
    - 使用`//`或`/* */`作为注释符号。

### 变量分配到指定节区
- **STM32的`.sct`文件**：
    - 在`.sct`文件中定义节区后，使用`__attribute__ ((section ("节区名")))`关键字将变量分配到指定节区。
    - 示例：
        ```c
        uint32_t testValue __attribute__((section("EXRAM"))) = 7;
        ```
- **Zynq的`.ld`文件**：
    - 在`.ld`文件中定义段后，使用`__attribute__ ((section ("段名")))`关键字将变量分配到指定段。
    - 示例：
        ```c
        uint32_t testValue __attribute__((section(".my_section"))) = 7;
        ```

总的来说，STM32的`.sct`文件和Zynq的`.ld`文件在定义内存布局和控制代码及数据存放位置方面有着相似的功能，但它们的语法结构和具体用法存在明显差异。