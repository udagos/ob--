---
up:
  - "[[../moc/软件工程]]"
---
```


好的，我们来更深入地对比 **Makefile** 和 **CMake** 的 **语法** 以及它们之间在语法层面的 **主要区别**。

**1. Makefile 语法:**

Makefile 的语法主要==围绕 **规则 (Rules)** 展开==。==一个规则通常由以下几个部分组成==：

```makefile
目标 (target) ... : 依赖 (prerequisites) ...
        命令 (command)
        ...
```

*   **目标 (target):**  要生成的文件名 (例如 `my_program`, `main.o`)，或者一个 **伪目标 (phony target)** (例如 `all`, `clean`)，用于表示一个构建步骤。
*   **依赖 (prerequisites):**  目标所依赖的文件列表 (例如 `main.o utils.o`, `main.c`)。在构建目标之前，Make 工具会先检查和构建所有的依赖。
*   **命令 (command):**  构建目标所需要执行的 ==shell 命令== (例如 `gcc -c main.c`, `rm -f *.o`)。命令必须以 **Tab 字符** 开头。

**Makefile 的关键语法元素:**

*   **规则 (Rules):**  核心语法结构，定义构建步骤。
*   **变量 (Variables):**  ==使用  = 赋值，使用 `$(变量名)` 或 `${变量名}` 引用== (推荐 `$(变量名)`)。
    ```makefile
    CC = gcc
    CFLAGS = -Wall -O2
    my_program: main.o
        $(CC) $(CFLAGS) -o my_program main.o
    ```
*   **==内置变量== (Built-in Variables):**  Make 工具预定义的变量，例如:
    *   `$@`:  表示规则的目标文件名。
    *   `$<`:  表示规则的第一个依赖文件名。
    *   `$^`:  表示规则的所有依赖文件名 (不重复)。
    *   `$+`:  表示规则的所有依赖文件名 (允许重复)。
    *   `$*`:  表示目标文件名去除后缀的部分。
    *   `$$@`, `$$<`, `$$^`, `$$+`, `$$*`:  在命令中引用上述变量时，需要使用双美元符号 `$$` 转义，避免被 shell 解析。
    *   `$?`:  表示比目标文件更新的所有依赖文件名。
    *   `$|`:  表示 order-only 的依赖文件名 (GNU Make 特性)。
    *   等等，还有很多内置变量，用于简化 Makefile 编写。
*   **模式规则 (Pattern Rules):**  使用通配符 `%` 定义一类目标的规则。
    ```makefile
    %.o: %.c
        $(CC) $(CFLAGS) -c $< -o $@
    ```
*   **静态模式规则 (Static Pattern Rules):**  更精细的模式规则，可以指定具体的目标文件列表。
    ```makefile
    OBJECTS = main.o utils.o
    $(OBJECTS): %.o: %.c
        $(CC) $(CFLAGS) -c $< -o $@
    ```
*   **函数 (Functions):**  GNU Make 提供的内置函数，用于字符串处理、文件操作、控制流程等。例如 `$(wildcard *.c)`, `$(patsubst %.c,%.o,$(SOURCES))`, `$(if ...)`, `$(foreach ...)` 等。
*   **条件语句 (Conditional Statements):**  使用 `ifeq`, `ifneq`, `ifdef`, `ifndef`, `else`, `endif` 等关键字实现条件判断。
    ```makefile
    ifeq ($(DEBUG), 1)
        CFLAGS += -g
    else
        CFLAGS += -O2
    endif
    ```
*   **包含其他 Makefile (Include Directives):**  使用 `include` 关键字包含其他 Makefile 文件。
    ```makefile
    include common.mk
    ```
*   **伪目标 (Phony Targets):**  使用 `.PHONY:` 声明伪目标，例如 `clean`, `all`。
    ```makefile
    .PHONY: all clean
    all: my_program
    clean:
        rm -f my_program *.o
    ```

**Makefile 语法的特点:**

*   ==**面向规则== (Rule-based):**  核心是定义如何从依赖文件构建目标文件。
*   **命令式 (Imperative):**  规则中的命令是具体的 shell 命令，需要手动编写。
*   **依赖驱动 (Dependency-driven):**  Make 工具根据文件的时间戳和依赖关系，自动决定哪些目标需要重新构建。
*   **底层和灵活:**  可以直接控制编译、链接等细节，灵活性高，但也要求开发者对构建过程有较深入的了解。

**2. CMake 语法:**

CMake  使用 `CMakeLists.txt` 文件来描述项目构建配置。  CMake 的语法基于 **命令 (Commands)**。

```cmake
cmake_minimum_required(VERSION 3.10)
project(my_program)

# 添加可执行文件目标
add_executable(my_program main.c utils.c)

# 添加库目标
# add_library(my_library SHARED utils.c)

# 链接库
# target_link_libraries(my_program my_library)

# 设置编译选项
# target_compile_options(my_program PRIVATE -Wall -O2)

# 设置安装目标
# install(TARGETS my_program DESTINATION bin)
```

**CMake 的关键语法元素:**

*   **命令 (Commands):**  CMake 提供的预定义命令，用于描述项目的构建结构和配置，例如 `project()`, `add_executable()`, `add_library()`, `target_link_libraries()`, `set()`, `find_package()`, `install()`  等等。  CMake 命令是 **大小写不敏感** 的 (例如 `PROJECT`, `Project`, `project` 都可以)。
*   **变量 (Variables):**  使用 `set()` 命令设置变量，使用 `${变量名}` 引用变量。
    ```cmake
    set(CMAKE_CXX_STANDARD 14)
    set(PROJECT_VERSION "1.0.0")
    message(STATUS "Project Version: ${PROJECT_VERSION}")
    ```
*   **属性 (Properties):**  CMake 对象 (例如 target, source file, directory) 可以拥有属性，用于配置构建行为。可以使用 `set_property()`, `get_property()`, `target_sources()`, `target_compile_options()` 等命令设置和获取属性。
*   **作用域 (Scoping):**  CMake  支持作用域的概念，例如 directory scope, target scope, function scope 等。变量和属性的作用域决定了它们在哪些地方可见和生效。
*   **列表 (Lists):**  CMake  使用 `;` 分隔列表元素。可以使用 `set()` 命令创建和操作列表。
    ```cmake
    set(SOURCES main.c utils.c)
    add_executable(my_program ${SOURCES})
    ```
*   **控制结构 (Control Structures):**  CMake  提供了 `if()`, `elseif()`, `else()`, `endif()`, `foreach()`, `while()` 等控制结构，用于实现条件判断和循环。
    ```cmake
    if (CMAKE_BUILD_TYPE STREQUAL "Debug")
        add_compile_options(-g)
    else()
        add_compile_options(-O2)
    endif ()
    ```
*   **函数和宏 (Functions and Macros):**  CMake  允许用户自定义函数和宏，用于封装常用的构建逻辑，提高代码重用性。使用 `function ()` 和 `endfunction ()` 定义函数，使用 `macro ()` 和 `endmacro ()` 定义宏。
*   **模块 (Modules):**  CMake  提供了大量的预定义模块 (Find Modules)，用于查找和配置第三方库和软件包。例如 `find_package (Boost REQUIRED COMPONENTS system filesystem)`, `find_package (Qt5 COMPONENTS Core Widgets)`。
*   **目标 (Targets):**  CMake  中的核心概念，表示构建系统要生成的目标产物，例如可执行文件 (`add_executable ()`), 库文件 (`add_library ()`), 自定义命令 (`add_custom_target ()`), 接口库 (`add_interface_library ()`)  等等。大多数 CMake 命令都是围绕 target 进行操作的。

**CMake 语法的特点:**

*   ==**面向命令== (Command-based):**  核心是调用各种 CMake 命令来描述项目构建。
*   **声明式 (Declarative):**  `CMakeLists. txt` 文件主要描述项目的 **结构和构建意图**，而不是具体的构建命令。  CMake  负责生成平台特定的构建文件。
*   **抽象和高级:**  CMake  隐藏了底层构建细节，提供了更高层次的抽象，更专注于项目配置和依赖管理。
*   **跨平台性强:**  CMake 命令是平台无关的，可以生成各种平台的原生构建文件。
*   **功能丰富:**  CMake  提供了大量的功能和特性，例如依赖管理、构建配置、测试集成、安装打包等。

**3. Makefile 和 CMake 语法的主要区别:**

| 特征            | Makefile                             | CMake                                        |
| ------------- | ------------------------------------ | -------------------------------------------- |
| **语法风格**      | 命令式 (命令 + 规则)                        | 声明式 (命令 + 配置)                                |
| **抽象程度**      | 底层, 直接命令                             | 高级, 描述构建意图                                   |
| ==**平台依赖性**== | ==平台依赖的 shell 命令==                   | 平台无关的 CMake 命令                               |
| **核心元素**      | 规则 (targets, dependencies, commands) | 命令 (commands), 目标 (targets), 属性 (properties) |
| **依赖管理**      | 手动编写依赖规则, 较弱                         | Find Modules, FetchContent, 更强大              |
| **跨平台性**      | 需要平台特定的 Makefile                     | 使用同一份 `CMakeLists. txt` 生成多平台构建文件            |
| ==**变量引用**==  | `$(变量名)`                             | `${变量名}`                                     |
| **命令前缀**      | 命令必须以 Tab 字符开头                       | 命令不需前缀, 命令名本身标识                              |
| **内置函数/模块**   | GNU Make 函数                          | CMake 命令和模块 (Find Modules)                   |
| **错误处理**      | 错误信息可能较简略                            | 错误信息更详细清晰                                    |
| **扩展性**       | 通过 shell 脚本和自定义规则扩展                  | 通过自定义函数、宏和模块扩展                               |

**总结:**

*   **Makefile 语法更偏向底层和命令式**，你需要直接告诉构建系统 **如何** 构建你的项目，需要编写具体的 shell 命令。  Makefile 更加灵活，但编写和维护复杂 Makefile 容易出错，跨平台性差。
*   **CMake 语法更偏向高级和声明式**，你需要描述你的项目 **是什么**，CMake 负责 **生成** 平台特定的构建文件。 CMake 更抽象，隐藏了底层细节，跨平台性好，功能更丰富，更易于维护和扩展，更适合大型和复杂项目。

选择 Makefile 还是 CMake  很大程度上取决于项目的复杂程度、跨平台需求、团队技术栈以及个人偏好。了解它们的语法和区别，可以帮助你更好地选择合适的构建工具。