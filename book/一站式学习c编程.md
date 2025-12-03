---
obsidian-note-status: []
prev:
  - "[[bookCode]]"
---
[ai问题](../已归类卡/ai问题.md)
[读一站c](../book/读一站c.md)
# 程序的基本概念
有些高级语言以**解释** (Interpret)的方式执行，解释执行过程和 C 语言的编译执行过程很不一样。如 Shell 脚本 
用 Shell 程序/bin/sh 解释执行这个脚本
还有很多编程语言采用**编译和解释相结合**的方式执行，Python 为例，程序员写的源代码. py 文件首先被编译成. pyc 文件，称为字节码 (ByteCode), 然后字节码被 Python 虚拟机解释执行

**语法规则是由符号(Token)和结构**(Structure)的规则所组成的([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=17&annotation=RALTZ24V))
**结构是指Token的排列方式**([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=17&annotation=FMQ5BNI6))
**Token的规则称为词法(Lexical)规则，而关于结构的规则称为语法(Grammar)规则**([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=17&annotation=LR2MLXFN))oken 的排列方式 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=17&annotation=FMQ5BNI6))

语义（Semantic）

搭建开发环境
列出需要安装的软件包
gcc:TheGNUCcompiler
•libc 6-dev:GNUCLibrary:DevelopmentLibrariesandHeaderFile•manpages-dev 
•manpages-dev: ManualpagesaboutusingGNU/Linuxfordevelopment
•manpages-posix-dev:ManualpagesaboutusingaPOSIXsystemfordevelopment
•binutils: TheGNUassembler, linkerandbinaryutilities
•gdb:TheGNUDebugger•make: TheGNUversionofthe"make"utility

用 gcc 的・o 参数自己指定文件名：$gcc main. c-o main
**一个好的习惯是打开 gcc 的-Wall 选项，让 gcc 提示所有的，告信息，不管是严重的还是不严重的**，然后把这些问题从代码中全部消灭$ gcc -Wall main. c


# 常量、变量和表达式
“常量有字符(Character)常量、整数(Integer) 常量、浮点数(Floatingpoint)常量和枚举常量”
C 语言中的声明有变量声明、函数声明和类型声明三种
**==分配存储空间的声明同时也是定义==**，不分配存储空间的声明不是定义。
**如果一个函数声明带有函数体**，要求编译器为它生成指令 (当然也需要分配存储空间来保存这些指令), 那么**这个声明同时也是函数的定义**。
类型声明总是不分配存储空间的

注意变量一定要先声明后使用
变量的定义和赋值也可以一步完成，这称为变量的初始化。**==初始化是一种特殊的声明，而不是一种赋值语句==**

表达式可以是单个的常量或变量，也可以是根据以上规则组合而成的更复杂的表达式 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=33&annotation=TUVC9K77))
![[Pasted image 20240219153852.png]]
编译器在翻译这条语句时，首先根据上述语法规则把这个语句解析成如图 2.2 所示的语法树，然后再根据语法树生成相应的指令。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=33&annotation=WYUC3JVZ))
![[Pasted image 20240219153905.png]]
**语法树**的每一步分解利用一条语法规则，直到分解成 Token 为止，**所以语法树的末端全部是 Token**



我们知道 char 型本质上就是整数 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=36&annotation=LUUCXQU5))
以后我们**把 char 型和 int 型统称为整数类型** (IntegerType)或简称整型 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=36&annotation=FPLSRUGC))
# 简单函数
使用 printf 函数必须包含 stdio.
**使用 math. h 中声明的库函数**还有一点特殊之处，gcc 命令行必须加-Im 选项，因为**数学函数位于 libm. so库文件中 (这些库文件通常位于/lib 目录下)，-lm 选项**
**告诉编译器，我们程序中用到的数学函数要到这个库文件里找**。注意库文件名是 libm, 但使用-l 选项指定库文件时省略 lib, 只写成-lm
**用到的大部分库函数 (例如 printf)位于 libc. so 库文件中，使用 libc. so 中的库函数在编译时不需要加-lc 选项**，当然加了也不算错，因为这个选项是 gcc 的默认选项

**Linux 平台上最广泛使用的 C 函数库是 glibc**, 其中包括 C 标准库的实现，也包括本书第三部分介绍的所有系统函数
几乎所有 C 程序都要调用 glibc 的库函数
glibc 提供一组头文件和一组库文件，
**最基本、最常用的 C 标准库函数和系统函数在 libc. so 库文件中**，几乎所有 C 程序的运行都依赖于 libcso, 有些做数学计算的 C 程序除了 libc. so 之外还依赖于 libm. so, 还有很多 C 程序依赖于 glibc 的其他库文件
以后我说 libc 时专指 Ubc. so 这个库文件，而说 glibc 时指的是 glibc 提供的所有库文件



“编译器见到函数原型(不管带不带函数体)就明确了这个函数的名字、参数类型和返回值，之后编译器碰到函数调用代码就知道该生成什么样的指令来实现函数调用了”
所以函数原型应该出现在函数调用之前，这也是遵循“先声明后使用”的原则。

**==并非所有函数声明都包含完整的函数原型==**，例如 void three lines ()。；**==这个声明并没有明确指出参数类型和个数==**，==所以不算函数原型==
果在这样的声明之后调用函数，**编译器不知道参数的类型和个数，就不会做语法检查**，所以很容易引入 Bug
==**编译器认为所有隐式声明的返回值类型都是 int**==

**==如果写一个非定义的函数声明，可以只写参数类型而不写参数名==**
![[Pasted image 20240219161322.png]]
定义变量时可以把相同类型的变量列在一起，而定义参数却不可以 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=45&annotation=A2AUBNPM))
形参相当于函数中定义的变量，**调用函数传递参数的过程相当于定义形参变量并且用实叁的值来初始化** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=47&annotation=SR4XBCFM))
为什么我们每次调用用 printf 传的实参个数都不一样呢？因为 C 语言规定了一种特殊的参数列表格式，用命令 man 3 printf 可以查看到 printf 函数的原型：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=47&annotation=M5Y6XA8S))
![[Pasted image 20240219161754.png]]
第一个参数是 const char* 类型的，==**后面的…可以代表 0 个或任意多个参数，这些参数的类型也是不确定的==，这称为可变参数**. 总之，每个函数的原型都明确规定了返回值类型以及参数的类型和个数 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=47&annotation=BQNGFIJS))

ManPage 各 Section 的含义如表 3.1所示。
用户命令和系统管理命令，用户命令通常位于/bin 和/usr/bin 目录，系统管理命令通常位于/sbin 和/usr/sbin 目录 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=48&annotation=YE7ADFSB))
ManPage 中有些页面有重名，比如敲 manprintf 命令看到的并不是 C 函数 printf, 而是位于第 1 个 Section 的命令 printf, ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=48&annotation=M7WBJX83))
要查看位于第 3 个 Section 的 printf 函数应该敲 man 3 prin ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=48&annotation=N9A9S7E4))
**也可以敲 man-kprintf 命令搜索哪些页面的主题包含 printf 关键字** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=48&annotation=SF43SJF7))



虽然全局变二用起来很方便，但一定要慎用，**能用函数传参代替的就不要用全局变量。**
==局部变量可以用类型相符的任意表达式来初始化, **而全局变量只能用常量表达式（ConstantExpression）来初始化**== ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=51&annotation=87NKN965))
例如，全局变量 pi 这样初始化是合法的：
![[Pasted image 20240219164517.png]]
**但这样初始化是不合法的: 然而局部变量这样初始化却是合法的。**
![[Pasted image 20240219164528.png]]
在程序运行一开始（在还没有执行 main 函数中的任何语句之前）就要用初始值来初始化全局变量
**如果全局变量在定义时不初始化则初始值是 0, 如果局部变量在定义时不初始化则初始值是不确定的。所以，==局部交, 在使用之前一定要先赋值**==

非定义的函数声明也可以写在局部作用域中 ![[Pasted image 20240219164927.png]]
这样声明的标识符 print_time 具有局部作用域，只在 main 函数中是有效的函数名，出了 main 函数就不存在 prmttime 这个标识符了。
# 分支语句

“通常把加 default 分支写在最后，但不是必需的”
.case 后面跟的表达式必须是常量表达式，这个值和全局变量的初始值一样必须在编译时计算出来。
以 **C 语言规定 case 后面跟的必须是整型常量表达式。**
通**常每个 case 后面都要加上 break 语句，但有时会故意不加 break,**例如
![[Pasted image 20240219165534.png]]

“函数的返回值应该这样理解：函数返回一个值相当于定义一个和返回值类型相同的临时变量并用 return 后面的表达式来初始化” ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=66&annotation=XC4UDPHV))

如果定义一个概念需要用到这个概念本身,我们称它的定义是递归的 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=72&annotation=Y7QUS3WC))
==**写递归函数时一定要记得写 BaseCas**== ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=75&annotation=M33WN3JX))
# 循环语句
==a+++++b 这个表达式如何理解？==
编译的过程分为词法解析和语法解析两个阶段，在词法解析阶段，**编译器总是从前到后找最长的合法 Token。把这个表达式从前到后解析** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=82&annotation=4DJSJ3G7))
变量名 a 是一个 Token, a 后面有两个以上的+号，在 C 语言中一个+号是合法的 Token（可以是加法运算符或正号），两个+号也是合法的 Token（可以是自增运算符），根据最长匹配原则，编译器绝不会止步于一个+号，而一定会把两个+号当做一个 Token。再往后解析仍然有两个以上的+号，所以又是一个++运算符。再往后解析只剩一个+号了，是加法运算符。再往后解析是变量名 b
**词法解析之后进入下一阶段语法解析**，a 是一个表达式，表达式++还是表达式，表达式再什还是表达式，表达式再+b 还是表达式，语法上没有问题
**最后编译器会做一些基本的语义分析**，这时就有问题了，++运算符要求操作数能做左值，a 能做左值所以 a++没问题，但表达式 a++的值只能做右值，不能再++了，所以最终编译器会报错。

C 99 规定了一种新的 for 循环语法（其实是从 C++借鉴的），在控制表达式 1 的位置可以有变量定义。例如上例的循环变量 i 可以只在 for 循环中定义：
![[Pasted image 20240220083029.png]]
**注意这个程序用 gcc 编译时必须加上选项-std=c 99。**


滥用 goto语句会使程序的控制流程非常复杂，可读性很差
goto 语句不是必须存在的，显然可以用别的办法替代，比如上面的代码段可以改写为：
![[Pasted image 20240220083237.png]]
==**通常 goto 语句只用于这种场合**==，一个函数中任何地方出现了错误条件都可以立即跳转到函数末尾做出错处理 (例如释放先前分配的资源、恢复先前改动过的全局变量等)，处理完之后函数返回
有些编程语言 (如 C++)中有异常 (Exception)处理的语法，可以代替 goto 和 setjmp/longjmp 的这种用法。
# 结构体
最基本的、不可再分的数据类型称为基本类型 (PrimitiveType), 例如整型、浮点型；根据语法规则由基本类型组合而成的类型称为复合类型

struct complex_struct { double x, y; }==整个可以**看作一个类型名**==，就像 int 或 double 一样，==只不品是一个复合类型==
如果用这个类型名来定义变量
![[Pasted image 20240220083446.png]]
==这样 zl 和 z 2 就是两个变量名==
**先前的例子那样只定义了 complex_struct 这个 Tag 而不定义变量**
**==以后都可以直接用 struct complex_struct 来代替类型名了==**
![[Pasted image 20240220083541.png]]
==<span style="background:#40a9ff">如果在定义结构体类型的同时定义了变量，也可以不必写</span>== Ta
![[Pasted image 20240220083555.png]]
成员 (Member) x 和 y,可以用.后缀运算符来访问
结构体 Tag 也可以定义在全局作用域中，这样定义的 Tag 在其定义之后的各函数中都可以使用

**==结构体变量也可以在定义时初始化==**
![[Pasted image 20240220083801.png]]
如果 Initializer 中的数据比结构体的成员多，编译器会报错，**但如果只是末尾多个逗号则不算错**。如果 Initializer 中的数据比结构体的成员少，未指定的成员将用 0 来初始化，就像未初始化的全局变量一样。例如以下几种形式的初始化都是合法的:,
![[Pasted image 20240220083932.png]]
注意，Z 1 必须是局部变量才能用另一个变量 X 的值来初始化它的成员，如果是全局变量就只能用常量表达式来初始化。这也是 C 99 的新特性

==**{}这种语法不能用于结构体的赋值**==，例如这样是错误的：”
![[Pasted image 20240220084056.png]]

**DesignatedInitializer 是 C 99 引入的新特性，用于初始化稀疏 (Sparse)结构体和稀疏数组很方便**。有些时候结构体或数组中只有某一个或某几个成员需要初始化, 其他成员都用 0 初始化即可，==**用 DesignatedInitializer 语法可以很方便地针对每个成员做初始化 (MemberwiseInitialization)例如**==：![[Pasted image 20240220084646.png]]

**结构体类型用在表达式中有很多限制**，不像基本类型那么自由，**比如+-*/等算术运算符和&&||! 等逻辑运算符都不能作用于结构体类型，if 语句、while 语句中的控制表达式的值也不能是结构体类型**
可以做算术运算的类型称为算术类型，算术类型包括整型和浮点型。可以表示零和非零，可以参与逻辑与、或、非运算或者做控制表达式的类型称为标量类型 (Scalar Type), 标量类型包括算术类型和以后要讲的指针类型

==**结构体变量之间使用赋值运算符是允许的**，**用一个结构体变量初始化另一个结构体变量也是允许的**== ![[Pasted image 20240220085141.png]]
同样地，z 2 必须是局部变量才能用变量 zl 的值来初始化。
**==既然结构体变量之间可以相互赋值和初始化，也就可以当做函数的参数和返回值来传递==：**![[Pasted image 20240220085332.png]]
“如果在main函数中这样调用：”
![[Pasted image 20240220085413.png]]
“那么调用传参的过程如图7.2所示。”
![[Pasted image 20240220085538.png]]
变量 z 在 main 函数的栈帧上，参数 zl 和 z 2 在 add_complex 函数的栈帧上，z 的值分别赋给 zl 和 z 2. 在这个函数里，z 2 的实部和扁被累加到 zl 中，然后 return zl;可以看成是：
1. 用 Z 1 初始化一个临时变量。2. 函数返回并释放栈帧。3. 把临时变量的值赋给变量 z, 释放临时变量。

**枚举常量也是一种整型，其值在编译时确定，因此也可以出现在常量表达式中，可以用于初始化全局变量或者作为 case 分支的判断条件。**


结构体也是一种递归定义，换句话说，结构体的成员可以是另一个结构体
![[Pasted image 20240220090415.png]]
InitiaUzer 的语法可以看出，Initializer 也可以嵌套，==因此嵌套结构体可以嵌套地初始化==
![[Pasted image 20240220090422.png]]
“也可以==平坦（Flat）地初始化==。例如：”
![[Pasted image 20240220090437.png]]
甚至可以把两种方式混合使用（这样可读性很差，应该避免）
![[Pasted image 20240220090458.png]]
**利用 ==C 99 的新特性也可以做 MemberwiseInitialization）==例如**：
![[Pasted image 20240220090523.png]]
访问嵌套结构体的成员要用到多个. 后缀运算符
![[Pasted image 20240220090600.png]]
# 数组
数组（Array）也是一种复合数据类型
和结构体成员类似，数组 count 的 4 个元素的存储空间也是相邻的。结构体成员可以是基本数据类型，也可以是复合数据类型，数组中的元素也是如此
根据组合规则，我们可以定义一个由 4 个结构体元素组成的数组：
![[Pasted image 20240220090708.png]]

数组类型的长度应该用一个整数常量表达式来指定

五种后缀运算符：后缀++、后缀-、结构体取成员.、数组取下标[]、函数调用 ()。还学习了五种单目运算符（或者叫前缀运算符）：前缀++、前缀-、正号+、负号-、逻辑非!。在 C 语言中后缀运算符的优先级最高，单目运算符的优先级仅次于后缀运算符，比其他运算符的优. 先级都高，所以上面举例的++count[2]应该看作对 count[2]做前缀++运算

**数组下标也可以是表达式, 值必须是整型**

**==数组也可以像结构体一样初始化==**，未赋初值的元素也是用 0 来初始化 
![[Pasted image 20240220091046.png]]

**如果==定义数组的同时初始化它，也可以不指定数组的长度**==
![[Pasted image 20240220091106.png]]
==**利用 C 99 的新特性也可以做 MemberwiseInitialization==：** 
![[Pasted image 20240220091222.png]]

数组和结构体虽然有很多相似之处，==**但也有一个显著的不同：数组不能相互赋值或初始化**==
**既然不能相互赋值，也就不能用数组类型作为函数的参数或返回值**
![[Pasted image 20240220091331.png]]
![[Pasted image 20240220091336.png]]
**编译器也不会报错，但这样写并不是传一个数组类型参数的意思**。**数组类型做右值使用时，自动转换成指向数组首元素的指针**
**在函数原型中，如果参数写成数组的形式，则该叁数实际上是指针类型**
所以上面的函数调用其实是传一个指针类型的参数，而不是数组类型的参数

数组类型不能相互赋值或初始化也是因为这条规则，例如上面提到的 a=b 这个表达式，a 和 b 都是数组类型的变量，但是 b 做右值使用，自动转换成指针类型，而左边仍然是数组类型，所以编译器报的错是 error:incompatibletypesinassignmento




实际上编译器的工作分为两个阶段，先是预处理 (Preprocess)阶段，然后才是编译阶段，用 gcc 的正选项可以看到预处理之后、编译之前的程序，例如：
![[Pasted image 20240220091840.png]]
预处理器做了两件事情，一是把头文件 stdio. h 和 stdlib. h 在代码中展开，二是把 ` #define` 定义的标识符 N 替换成它的定义20 (在代码中做了三处替换，分别位于数组的定义中和两个函数中
像 `#include和 #define这种以 #号` 开头的行称为预处理指示 (Preprocessing Directive
**那么用 ` #define` 定义的常量和第7 .3 节讲的枚举常量有什么区别呢？**
首先，加 fine 不仅用于定义常量，也可以定义更复杂的语法结构，称为宏 (Macro)定义。其次，**define 定义是在预处理阶段处理的，而枚举是在编译阶段处理的**
## 字符串
字符串字面值和数组类型相似，它的每个元素是字符型的 ![[Pasted image 20240220092159.png]]
字符串末尾都有一个字符\0做结束符, 也就是 ASCH 码为 0的 Null 字符
数组元素可以通过数组名加下标的方式访问，而字符串字面值也可以像数组名一样使用，可以加下标访问其中的字符
即字符串字面值所代表的存储空间是只读的，不允许修改
字符串字面值还有一点和数组类型相似，做右值使用时自动转换成指向首元素的指针

字符串字面值有一种特殊用法，**前面讲过数组可以像结构体一样初始化，如果是==字符数组，也可以用一个字符串字面值来初始化**：==
![[Pasted image 20240220092621.png]]
==**相当于**==
![[Pasted image 20240220092631.png]]
str 的后 4 个元素没有指定，自动初始化为 MT, 即 Null 字符

有一种情况需要特别注意，如果用于初始化的字符串字面值比数组刚好长出一个 Null 字符的长度，比如：
![[Pasted image 20240220092846.png]]
则数组 str 不包含 Null 字符，并且编译器不会给出警告
## 多维数组
就像结构体可以嵌套一样，数组也可以嵌套
==多维数组也可以像嵌套结构体一样用嵌套 Initializer 初始化== 
![[Pasted image 20240220092940.png]]
==**利用 C 99 的新特性也可以做 Memberwise Initializatio**==
![[Pasted image 20240220093000.png]]
==**结构体和数组嵌套的情况也可以做 MemberwiseInitialization）例如：**== 
![[Pasted image 20240220093030.png]]
![[Pasted image 20240220093038.png]]




![[Pasted image 20240220094620.png]]
**这个程序和例 4.1 的功能其实是一样的**，但是代码简洁多了 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=112&annotation=JM9JUA8J))

![[Pasted image 20240220094604.png]]
==**通过下标访问字符串组成的数组可以代替一堆 case 分支判断，这样就可以把每个 case 里重复的代码 (printf 调用)提取出来，从而又一次达到了 “提取公因式”的效果。这种方法称为[[../已归类卡/数据驱动]]的编程**==
**代码最重要的是选择正确的数据结构来组织信息，设计控制流程和算法尚在其次, 就像这里的 printf 自然而然就被提取出来了**
# 编码风格
因为基本上所有的 C 代码风格对于空白字符的规定都差不多，主要有以下几条。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=116&annotation=CVR6BP6X))
内核代码风格关于缩进的规则有以下几条。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=117&annotation=RPCIRYWS))

.函数注释。说明此函数的功能、参数、返回值、错误码

短的单词可以通过去元音形成缩写，较长的单词可以取单词的头几个字母形成缩写。看别人的代码看多了就可以总结出一些缩写惯例，例如 count 写成 ent, block 写成 blk, length 写成 len, window 写成 win, message 写成 msg, number 写成 nr, temporary 可以写成 temp, 也可以进一步写成 tmp, 最有意思的是 internationalization 写成 il 8 n, 词根 trans 经常缩写成 x,例如 transmit 写成 xmt
.内核编码风格规定变量、函数和类型采用全小写加下划线的方式命名，常量（比如宏定义和枚举常量）采用全大写加下划线的方式命名，比如上一节举例的函数名 radix_tree_insert、类型名 struct radix_tree_root、常量名 RADIX_TREE_ MAP_SHIFT 鎏
微软发明了一种变量命名法叫匈牙利命名法（HungarianNotation）, 在变量名中用前缀表示类型，例如 iCnt （i 表示 int）、pMsg （p 表示 pointer）
.全局变量和全局函数的命名一定要详细。局部变量和只在一个源文件中调用的内部函数的命名可以简略一些，但不能太短。尽量不要使用单个字母做变量名，只有一个例外：用 i、j、k 做循环变量是可以的


.执行函数就是执行一个动作，函数名通常应包含动词，例如 get_current. radixtreeinserto


indent **工具可以把代码格式化成某种风格**，例如把例 9.1 格式化成内核编码风格: ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=124&annotation=3F622WH8))
# gdb
## 单步执行和跟踪函数调用
![[Pasted image 20240222190813.png]]
![[Pasted image 20240222190820.png]]
上面的 (gdb)就是提示符，在这个提示符下输入 help 可以查看命令的类别：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=127&annotation=6DU894Y5))
进一步查看某一类别中有哪些命令 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=128&annotation=YZYW5XUG))
用 list 命令从第一行开始列出源代码: ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=128&annotation=K6WCIU6Z))一次只列 10 行，如果要从第 11 行开始继续列源代码可以再输入一次 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=128&annotation=MIHSJYC9))也可以什么都不输直接敲回车 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=129&annotation=TQL7TYWG)).在提示符下直接敲回车表示重复上一条命令。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=129&annotation=6TT5J9BJ))
gdb 的很多常用命令有简写形式，例如 list 命令可以写成 l, 要列一个函数的源代码也可以用函数名做参数：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=129&annotation=5QJKB7UJ))

我们可以用 next 命令 (简写为 n)控制这些语句一条一条地执行：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=130&annotation=PT3GMCJY))

用 start 命令重新来过 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=130&annotation=FLPIZUC4)).这次用 step 命令 (简写为 s)钻进 add_range 函数中去跟踪执行：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=130&annotation=S5WYMFBH))

**在函数中有几种查看状态的办法，backtrace 命令 (简写为 bt)可以查看函数调用的栈帧**：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=130&annotation=VCSYVHDN))
![[Pasted image 20240222182103.png]]

可见当前的 addrange 函数是被 main 函数调用的，main 传进来的参数是 low=l, high=10 .main 函数的栈帧编号为 1 addrange 的栈帧编号为 0 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=130&annotation=E37SS6RP))
**现在可以用 info 命令 (简写为 i)查看 add_range 函数局部变量的值**：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=130&annotation=SG2JZXDG))

如果想**查看 main 函数当前局部变量的值也可以做到，先用 frame 命令 (简写为 f)选择 1 号栈帧然后再查看局部变量**：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=130&annotation=M6P8FG6T))

然后用 **print 命令（简写为 p）打印出变量 sum 的值**：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=131&annotation=G5JJV537))

可以用 **finish 命令让程序一直运行到从当前函数返回为止**：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=131&annotation=M5AAWN8K))

由于局部变量 i 和 sum 没初始化，所以具有不确定的值，又由于两次调用是挨着，i 和 sum 正好取了上次调用时的值。但 sum 如果初值不是 0, 累加得到的结果就错了。好了，我们已经找到错误原因，可以退出 gdb 修改源代码了。如果我们不想浪费这次调试机会, 可以在 gdb 中马上把 sum 的初值改为 0 继续运行，看看这一处改了之后还有没有别的 Bug：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=132&annotation=99VDBDGU))
**修改变量的值除了用 set 命令之外也可以用 print 命令，因为 print 命令后面跟的是表达式，而我们知道赋值和函数调用也都是表达式** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=132&annotation=W3H3FFDK))

![[Pasted image 20240222182305.png]]
![[Pasted image 20240222182317.png]]
## 断点
我们可以用 **display** 命令使得每次停下来的时候都显示当前 **sum** 的值 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=134&annotation=RVC4JA9V))
undisplay 命令可以取消跟踪显示 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=134&annotation=5AMMYPAJ))变量 sum 的编号是 1, 可以用 undisplay 1 命令取消它的跟踪显示 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=134&annotation=MI7PQN9W))

可以用 **break** 命令 (简写为 b)在第 9 **行**设一个断点 (Breakpoint ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=134&annotation=MX7VZ264)) break 命令的参数也可以是函数名 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=134&annotation=Y2HCL8IH))
可以用编号指定删除某个断点：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=135&annotation=RMQH4QS9))
断点暂时不用可以禁用掉而不必删除 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=135&annotation=7J9JV2V6))这样以后想用的时候可以直接启用 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=135&annotation=W758H5KP))
gdb 的断点功能非常灵活，还可以设置断点在满足某个条件时才激活 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=135&annotation=A75JN2AV))


在用 continue 命令 (简写为 c)连续运行而非单步运行 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=134&annotation=Q7JIUK48))
![[Pasted image 20240222191744.png]]
## 观察点
![[Pasted image 20240222193724.png]]
**使用 scanf 函数是非常凶险的 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=137&annotation=6RAE5X4A))如果输入的字符串超长了会怎么样？我们知道数组访问越界是不会检查的，所以 scanf 会写出界**。现象是这样的：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=137&annotation=CCYQQFYT))

input 数组只有 5 个元素 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=138&annotation=U98UHYP3))x 命令 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=138&annotation=EPEF3GNL))查看更清楚
![[Pasted image 20240603133324.png]]
X 命令打印指定存储单元里保存的内容，**后缀 7 bx 是打印格式**，7 表示打印 7 组, b 表示每个字节一组，x 表示按十六进制格式打印，x/7 bx 这条命令从 input 数组的第一个字节开始连续打印 7 个字节 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=138&annotation=GFK38LSB))

进入下一次循环，原来的 0 x 04 又莫名其妙地变成了 0 x 05, 这是怎么回事？这个暂时解释不了，但 123407 这个结果可以解释了，是 12345 x 10+0 x 05-0 x 30 得到的，虽然多循环了一次，但下次一定会退出循环了，因为 0 x 05 的后面是 O ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=139&annotation=FRWLCF7M))
**input[4]后面那个字节到底是什么时候变的？可以用观察点 (Watchpoint)来跟踪** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=139&annotation=3ZPWYL6J))
**而观察点是当程序访问某个存储单元时中断，如果我们不知道某个存储单元是在哪里被改动的，这时候观察点尤其有用** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=139&annotation=IC6YTTP8))
用 watch 命令设置观察点 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=139&annotation=M92GKRKS))跟踪 input[4]后面那个字节 (可以用 input[5]表示，虽然这是访问越界)：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=139&annotation=VWD4C8RJ))

已经很明显了，每次都是回到 for 循环开头的时候改变了 input［5］的值，而且是每次加 1, 而循环变量 i 正是在每次回到循环开头之前加 1,原来 input\[5 ]就是变量 i 的存储单元，换句话说，i 的存储单元是紧跟在 input 数组后面的。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=140&annotation=HBVFQFI8))
![[Pasted image 20240222194015.png]]
## 段错误

![[Pasted image 20240612134205.png]]
![[Pasted image 20240612134213.png]]
在 gdb 中运行，遇到段错误会自动停下来，这时可以用命令查看当前执行到哪一行代码了。gdb 显示段错误出现在_iO_vfscanf 函数中，用**bt 命令**可以看到这个函数是被 main. c 的第 6 行间接调用，就是 scanf 这行代码引发的段错误 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=142&annotation=VQ2SC8XC))

gdb 指出，段错误发生在第 19 行。可是这一行什么都没有啊，只有表示 main 函数结束的｝括号。这可以算是一条规律，**3**
，如果某个函数的局部交派发生访问越界, 有可能并不立即产生畏倩误，而是在函数返回时产生段借误。
# 排序与查找
# 栈与队列
## 堆栈
堆栈是一组元素的集合，**类似于数组，不同之处在于**，数组可以按下标随机访问，这次访问 a[5]下次可以访问 a[l], 但是堆栈的**访问规则**被限制为 Push 和 Pop 两种操作 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=160&annotation=YISF2EPM))
只能访问栈顶元素而不能访问栈中其他元素
**如果==所有元素的类型相同==，堆栈的存储也可以用==数组来实现**==
![[Pasted image 20240220095502.png]]
![[Pasted image 20240220095517.png]]
运行结果是 cba。运行过程图示如图 12.1 所示。
![[Pasted image 20240220095606.png]]
数组 stack 是堆栈的存储空间，变量 top 总是保存数组中栈顶的下一个元素的下标, 我们说 top 总是指向栈顶的下一个元素，或者把 top 叫做栈顶指针（Pointer）([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=161&annotation=8G7GKGQW))

堆栈这种数据结构的特点可以概括为 LIFO ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=162&annotation=MVBIZRB2))
我们也可以写一个递归函数做倒序打印，利用函数调用的栈帧实现后进先出：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=162&annotation=A8MIH53P))
![[Pasted image 20240220095829.png]]
**又是堆栈又是递归的，倒序打印一个数组犯得着这么大动干戈吗** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=162&annotation=E3XKMS9S))
![[Pasted image 20240220095844.png]]
**对于数组来说确实没必要搞这么复杂，因为数组既可以从前向后访问也可以从后向前访问，甚至可以随机访问，但有些数据结构的访问并没有这么自由** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=162&annotation=YHZA2G33))
## 深度优先搜索
![[Pasted image 20240603140100.png]]
![[Pasted image 20240603140106.png]]
其中的 1 表示墙壁，0表示可以走的路，只能横着走或竖着走, 不能斜着走
要求编程序找出从左上角到右下角的路线
![[Pasted image 20240603144805.png]]
![[Pasted image 20240603145104.png]]


这次堆栈里的元素是结构体类型的
每个走过的点都有一个前趋 (Predecessor)点，表示是从哪儿走到当前点的
一开始 predecessor 的各元素初始化为无效坐标 (-1,-1)，已经走过的点在 maze 数组中记为 2 防止重复走
我把这个算法改写成伪代码 (Pseudocode)如下：
![[Pasted image 20240603145832.png]]
![[Pasted image 20240603144858.png]]

但 predecessor 这种数据结构却有很多限制：
.不能随机访问一条路线上的任意点，只能通过一个点找到另一个点，通过另一个点再找第三个点，因此只能顺序访问。2. 每个点只知道它的前趋是谁，而不知道它的后继 (Successor)是谁，所以只能反向顺序访问。

## 队列与广度优先搜索 
下面我们用队列解决迷宫问题
![[Pasted image 20240603145535.png]]
![[Pasted image 20240603145552.png]]
其实仍然可以像例 12.3 一样用 predecessor 数组表示每个点的前趋, 但我想**==换一种更方便的数据结构，直接在每个点的结构体中加一个成员表示前趋：==**
![[Pasted image 20240603145621.png]]
head 总是指向队头，tail 总是指向队尾的下一个元素
**predecessor 成员也是一个指针，指向它的前趋在 queue 数组中的位置**
![[Pasted image 20240603145713.png]]

把这个算法改写成如下伪代码：
![[Pasted image 20240603145912.png]]
队列中的元素总是由前线的点组成的，可见正是队列先进先出的性质使这个算法具有了广度优先的特点。广度优先搜索还有一个特点是可以找到从起点到终点的最短路径，而深度优先搜索找到的不一定是最短路径，比较本节和上一节程序的运行结果可以看出这一点，想一想为什么。???

## 环形队列
**栈操作的 top 指针在 Push 时增大而在 Pop 时减小，栈空间是可以重复利用的**
而**队列的 head、tail 指针都在一直增大**，虽然前面的元素已经出队了，但它所占的**存储空间却不能重复利用**。


**在例 12.4 的解法中，出队的元素仍然有用**，保存着走过的路径和每个点的前趋，**但大多数程序并不是这样使用队列的，一般情况下出队的元素就不再有保存价值了，这些元素的存储空间应该回收利用，由此想到把队列改造成环形队列**
：把 queue 数组想象成一个圈，head 和 tail 指针仍然是一直增大的，当指到数组末尾时就自动回到数组开头。
从 head 到 tail 之间是队列的有效元素, 从 tail 到 head 之间是空的存储位置
如果 head 追上 tail 就表示队列空了，如果 tail 追上 head 就表示队列的存储空间满


![[Pasted image 20240603150414.png]]
注意图 12.5 中的第三个小图和最后一个小图，**head 和 tail 指向相同的位置既可能表示队列空也可能表示队列满，这是肯定不行的，在实现环形队列时必须要区分这两种状态，请思考一下可以用哪些办法来区分**。
# 计算机中数的表示
LSB 称为第 0 位而不是第 1 位，所以如果一个数是 32 位的，则 MSB 是第31位

我们将 13 反复除以 2 取余数就可以提取出上式中的 1101 四个数字，为了让读者更容易看清楚是哪个 1 和哪个 0, 上式和下式中对应的数字都加了下标： 
![[Pasted image 20240220101534.png]]
## 1's Complement 表示法
负数用 1 的补码 表示，减法转换成加法，计算结果的高位如果有进位则要加回到量低位上去
取 1 的补码就是把每个 bit 取反，所以 1 的补码也称为反码
![[Pasted image 20240220101807.png]]

**美中不足的是** 0 的表示仍然不唯一，既可以表示成 11111111 也可以表示成 00000000, 为了解决这最后一个问题，我们引入 2'sComplement 表示法。
## 2's Complement 表示法
==**负数先取反码再加 1**==
**负数的取值范围是从 10000000 到 11111114 (-128--1)**, 正数是从 00000000 到 01111111 (0〜127), 也可以根据最高位判断一个数是正是负

减法转换成加法，**忽略计算结果最高位的进位，不必加回到最低位上去**

计算机的加法器在做完计算之后，根据最高位产生的进位设置进位标志，同时根据最高位和次高位产生的进位的异或设置溢出标志 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=184&annotation=2P2QLXXP))
**如果程序把它理解成有符号数加法，下一步就要检查溢出标志，如果程序把它理解成无符号数加法，下一步就要检查进位标志** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=184&annotation=IVZIAGI2))
**通常计算机在做算术运算之后还可能设置另外两个标志**，如果计算结果的所有 bit 都是零则设置零标志，如果计算结果的最高位是 1 则设置负数标志 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=184&annotation=LKIUVTIC))
## 浮点数
浮点数 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=184&annotation=38ZJH2WT))
# 数据类型详解
## 整型
在 C 语言中 char 型占一个字节的存储空间，一个字节通常是 8 个 bit。如果这 8 个 bit 按无符号整数来解释，取值范围是 0〜255, ==如果按有符号整数来解释，采用 2 sComplement 表示法，取值范围是-128〜127== ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=187&annotation=3RYRF98W))
**以前我们常用的不带 signed 或 unsigned 关键字的 char 型是无符号数还是有符号数呢？C 标准规定这是 ImplementationDefined, 编译器可以定义 char 型是无符号的，也可以定义 char 型是有符号的** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=187&annotation=XDHZMERW))
在该编译器所对应的体系结构上哪种实现效率高就可以采用哪种实现，x 86 平台的 gcc 定义 char 型是有符号的。这也是 C 标准的 Rationale 之一：优先考虑效率，而可移植性尚在其次 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=187&annotation=2TSYSHUK))
其实，对于**有符号数在计算机中的表示**是 SignandMagnitude, l'sComplement 还是 2'sComplement, C 标准也没有明确规定，**也是 ImplementationDefined**。大多数体系结构都采用 2，sComplement 表示法 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=189&annotation=CPUKTBSP))
还有一点要注意，==**除了 char 型以外的这些类型如果不明确写 signed 或 unsigned 关键字都表示 signed, 这一点是 C 标准明确规定的==，不是 ImplementationDefined**。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=189&annotation=CGMPI2VB))

除了 char 型在 C 标准中明确规定占一个字节之外，**其他整型占几个字节都是 Implementation Defined**»通常的编译器实现遵守 ILP 32 或 LP64规范
![[Pasted image 20240220103912.png]]
**ILP 32 这个缩写的意思是 int（D、long（L）和指针（P）类型都占 32 位，通常 32 位计算机的 C 编译器采用这种规范**
**LP 64 是指 long （L）和指针（P）占 64 位，通常 64 位计算机的 C 编译器采用这种规范**

八进制整数常量以 0 开头 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=189&annotation=M7EW4YRH))
十六进制整数常量以 Ox 或 0 X 齐头 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=189&annotation=YRDPPY6J))
但二进制的整数常量从条进入 C 标准，只是某些编译器的扩展，所以不建议使 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=189&annotation=E2YUQ3GD))


int 的取值范围是-2147483648〜2147483647, 那么用 printf ("%d\n",-2147483648); 打印 int 类型的下界有没有问题呢？([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=191&annotation=SFTIWG4Z))
gccmain. c-std=c 99 编译会有警告信息：warning: format 4%d\*expectstype'int', butargument 2 hastype'longlongint' ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=191&annotation=533XQDVK))
编译器会把它当成一个整数常量 2147483648 和一个负号运算符组成的表达式 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=191&annotation=MUDP9LI8))
，这个整数常量应该算 longlong 型的，前面再加个负号组成的表达式仍然是 longlong 型，而 printf 的％d 转换说明要求后面的参数是 int 型，所以编译器报警告。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=191&annotation=ALJBEYWR))
如果改成 printf ("%d\n",-2147483647-1); 编译器就不会报警告了，-号运算符的两个操作数-2147483647 和 1 都是 int 型 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=191&annotation=W3CQJZKF))，计算结果也应该是 int 型, 并且它的值也没有超出 int 型的取值范围

long long i=1234567890\*1234567890; 编译时会有警告信息；warning: integeroverflowinexpressiono 1234567890 是 int 型，两个 int 型相乘的表达式仍然是 int 型，而乘积已经超过 int 型的取值范围了 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=191&annotation=E5NZDSH8))
其中一个常量是 10 ngiong 型，另一个常量也会先转换成 longlong 型再做乘法运算，两数相乘的表达式也是 longlong 型，编译器就不会报警告了 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=191&annotation=K8W4KLQS))
## 浮点型
## 类型转换
首先介绍哪些情况下会发生类型转换，会把什么类型转成什么类型，然后介绍编译器如何处理这样的类型转换。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=192&annotation=TMJ9H7TA))
### Integer Promotion  整数提升
在一个表达式中，凡是可以使用 int 或 unsignedint 类型做右值的地方也都可以使用有符号或无符号的 char 型、short 型和 Bit-field。
如果原始类型的取值范围都能用 int 型表示, 则其类型被提升为 int, ==**如果原始类型的取值范围用 int 型表示不了，则提升为 unsigned int 型**==，这称为 Integer Promotion
C 99 规定 **==Integer Promotion 适用于以下几种情况==**：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=192&annotation=USNDIQMX))
1. **如果一个函数的形参类型未知或者函数的参数列表中有...**，那么调用函数时要对相应的实参做 Integer Promotion, 此外，**相应的实参如果是 float 型的也要被提升为 double 型 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=192&annotation=XH5SCGYK))**
==printf 的参数列表中有…，除了第一个形参之外，其他形参的类型都是未知的== ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=192&annotation=STGQZQMN))
![[Pasted image 20240220112039.png]]
==ch 要被提升为 int 型之后再传给 printf.== ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=192&annotation=MFNXNDLP))
1. 有符号或无符号的 **char 型、short 型和 Bit-field 在==做算术运算之前==首先要做 IntegerPromotion**，然后才能参与计算 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=193&annotation=XS3HVQZU))
“除了 +号之外还有哪些运算符在计算之前需要做Integer Promotion呢？”
### Usual Arithmetic Conversion  寻常算数转换
**两个算术类型的操作数做算术运算**。比如 a+b, 如果两边操作数的类型不同，**编译器会自动做类型转换，使==两边类型相同之后才做运算==**，这称为 UsualArithmeticConversiono 转换规则如下：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=193&annotation=GD7JDA9D))

“，两边应该都是整数。我们规定 char、short, int、 long、long long 的**转换级别** (Integer Conversion Rank)一个比一个高，**同一类型的有符号和无符号数具有相同的 Rank**
	**如果一边是无符号数另一边是有符号数，无符号数的 Rank 不低于有符号数的 Rank, 则把有符号数转成另一边的无符号类型。例如 unsigned long 和 int 做算术运算时都转成 unsigned long, unsigned long 和 long 做算术运算时也都转成 unsigned long。**
	“一边有符号另一边无符号，并且无符号数的 Rank 低于有符号数的 Rank”
		这时又分为两种情况，如果这个**有符号数类型能够覆盖这个无符号数类型的取值范围**，则把无符号数转成另一边的有符号类型。例如遵循 LP 64 的平台上 unsigned int 和 long 在做算术运算时都转成 long
		“有符号数类型不足以覆盖这个无符号数类型的取值范围，则把两边都转成有符号数的 Rank 对应的无符号类型”。例如在遵循 ILP 32 的平台上 unsigned int 和 long 在做算术运算时都转成 unsigned long。


**到目前为止我们学过的 `+ - * / % > < ＞= ＜= == !=` 运算符都需要做 Usual Arithmetic Conversion, 因为都要求两边操作数的类型一致，在下一章会介绍几种新的运算符也需要做 UsualArithmeticConversion。单目运算符+-〜只有一个操作数，==移位运算符＜< >＞两边的操作数类型不要求一致，这些运算不需要做 UsualArithmeticConversion, 但也需要做 Integer Promotio==**
### 由赋值产生的类型转换
==赋**值或初始化时等号两边的类型不相同，则编译器会把等号右边的类型转换成等号左边的类型再做赋值**== ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=194&annotation=5M3DD3LE))

，函数调用传参的过程相当于定义形参并且用实参对其做初始化，函数返回的过程相当于定义一个临时变量并且用 return 的表达式对其做初始化 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=194&annotation=YC3F8X64))**由赋值产生的类型转换也适用于这两种情况** ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=194&annotation=THL53FFU))


### 强制类型转换
“**以上三种情况通称为隐式类型转换**”

### 编译器如何处理类型转换
“**把一个 M 位的类型(值为 X)转换成一个 N 位的类型**”
![[Pasted image 20240220113232.png]]

比如把 double 型转换成 short 型，对应表中的"floating-point to signed or unsigned integerw ,如果原值在 (-32769.0, 32768.0).之间则截掉小数部分得到转换结果，否则产生溢出，结果是 Undefined, 例如对于 short s = 32768.4; 这样的代码 gcc 会报警告。

比如把 int 型转换成 unsigned short 型，对应表中的"signed integer to unsigned integer", 如果原值是正的，则把它除以 2 16取模，其实就是取它的低 16 位，如果原值是负的，则加上 216 的整数倍，使结果落在［0,65535］之间。

比如把 int 类型转换成 short 类型，对应表中的"signed integer to signed integerw , 如果原值在［-32768, 32767］之间则值不变，否则产生溢出，结果是 Implementation-defined, 例如对于 shorts = -32769; 这样的代码 gcc 会报警告。

最后一个例子，把 short 型转换成 int 型，对应表中的"signed integer to signed integer", 转换之后应该值不变。那怎么维持值不变呢？是不是在高位补 16 个 0 就行了呢？如果原值是-1, 十六进制表示就是 ffff, 要转成 int 型的-1 需要变成 ffffifff, 因此需要在高位补 16 个 1 而不是 16 个 0。换句话说，要维持值不变，在高位补 1 还是补 0 取决于原来的符号位，这称为符号扩展 (Sign Extension)。
# 运算符详解
## 位运算
“移位运算符不同于 + -*/=等运算符，两边操作数的类型不要求一致，但两边操作数都要做Integer Promotion，整个表达式的类型和左操作数提升后的类型相同”

==“当操作数是有符号数时，右移运算的规则比较复杂==:”
•如果是正数，那么高位移入 0。
•如果是负数，那么高位移入 1 还是 0 不一定，这是 Implementation-defined 的。对于 x 86 平台的 gcc 编译器，最高位移入 1, 也就是仍保持负数的符号位，这种处理方式对负数仍然保持了右移 1 位相当于除以2的性质

由于类型转换和移位等问题，用有符号数做位运算是很不方便的，所以，==建议只对无符号数做位运算，以减少出错的可能==。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=199&annotation=SJHC5UYZ))
## 异或运算的特性
==配合掩码实现某些位的翻转==
**可用于奇偶校验** (ParityCheck)
交换两个变量的值，不得借助额外的存储空间
	![[Pasted image 20240603152541.png]]
	。为了避免混淆，把 a 和 b 的初值分别记为劭和瓦。第一行， a = aoAbo；第二行，把 a 的新值代入，得到 b—o^ao 入％, 等号右边的瓦相当于上面公式中的 x, 即相当于 y, 所以结果为彻；第三行，把 a 和 b 的新值代入，得到 a = ao 入加入即，结果为反。注意这个过程不能把同一个变量自己跟自己交换，而利用中间变量 temp 则可以交换。
如果需要一个常数 0, x 86 平台的编译器可能会生成这样的指令：xorl %eax, %eax, 不管 eax 寄存器里的值原来是多少，做异或运算都能得到 0, 这条指令比同样效果的 movl$0,%eax 指令快，直接对寄存器做位运算比生成一个立即数再传送到寄存器要快一些


## 其他运算符

根据组合规则可以写出表达式 1，表达式 2, 表达式 3,…，表达式 n 这种形式 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=202&annotation=FYPDQPEP))
整个计算过程就是从左到右**依次求值**，**最后一个表达式的值成为整个表达式的值**。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=202&annotation=4PTK4B25)) ![[Pasted image 20240220154933.png]]
==“f (a, (t=3, t+2), c) 传给函数 f 的参数有三个，其中第二个参数的值是表达式 t+2的值”==

### sizeof 运算符与 typedef 类型声明

==它有两种形式==：sizeof 表达式和 sizeof (类型名)([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=202&annotation=MFI4EVAR))
sizeof 表达式中的**子表达式并不求值，而只是根据类型转换规则求得子表达式的类型，然后把这种类型所占的字节数**作为整个表达式的值 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=202&annotation=89ANCJ5Q))
有些人==喜欢写成 sizeof(表达式)==的形式也可以, 这里的括号和 retum (1); 的括号一样，不起任何作用

但另外一种形式 sizeof (类型名)的括号则是必须写的 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=202&annotation=9KNR726V))


![[Pasted image 20240220161131.png]]
**sizeof a 中的 a 做左值，表示整个数组。而不是做右值转换成指向首元素的指针**
表达式 a 的类型在编译时就可以确定，所以 sizeof a 的值在编译时计算

**即使写成 sizeof i++, 表达式 i++也不求值**
求 sizeof i++就是**求表达式 i++的类型所占的字节数**，而 i++的类型在编译时就知道了，不需要到运行时求值之后才知道。

“此 sizeof（'Hello")的值是6。”

sizeof 运算符的结果是 size_t 类型的，这个类型定义在 stddef. h 头文件中，不过你的代码中只要不出现 size_t 这个类型名就不用包含这个头文件，
C 标准规定 size_t 是一种无符号整型，编译器可以用 typedef 做一个类型声明：
![[Pasted image 20240220161605.png]]
**不同平台的编译器可能会根据自己平台的具体情况最 size_t 所代表的类型**
C 标准规定 size_t 这个名字就是为了隐藏这些细节，使代码具有可移植性

==typedef 这个关键字用于给某种类型起个新名字，那么加上 typedef 之后，size_t 就是一个类型名==
C 标准库的头文件 stdint. h 中定义了很多这样的类型名，如表 15.1 所示，使用这些类型名写代码就可以屏蔽 ILP 32 和 LP 64 之间的差异了：

# 计算机体系结构基础
==cpu 内存是主要组成部分==
==**内存中保存着数据和指令**，CPU 从内存中取指令（Fetch）执行，其中有些指令让 CPU **做运算**，有些指令让 CPU **读写内存中的数据**==
## 内存和地址
==一个地址所对应的内存单元不能存很多东西,只能存一个字节,以前讲过的int、float等多字节的数据类型保存在内存中要占用连续的多个地址,这种情况下数据的地址是它所占内存单元的起始地址。==
## cpu 
从内存取指令，然后解释执行它，然后再取下一条指令，再解释执行。==**CPU 最核心的功能单元包括**：==
- 寄存器。有些寄存器只能用于某种特定的用途，比如程序计数器，这称为特殊寄存器。 而另外一些寄存器可以用在各种运算和读写内存的指令中，这称为通用寄存
- 程序计数器 pc。是特殊寄存器。CPU 按程序计数器保存的地址去内存中取指令然后解释执行，**这时程序计数器保存的地址会自动加上该指令的长度，指向内存中的下一条指令。**
- 指令译码器。CPU 取上来的指令由若干个字节组成，这些字节中有些位表示内存地址，有些位表示寄存器编号,, 有些位表示这种指令做什么操作，是加减乘除还是读写内存，**指令译码器负责解释这条指令的含义，然后调动相应的执行单元去执行它**。
- 算数逻辑单元 **ALu。指令中会指示运算结果保存到哪里，可能保存到寄存器中，也可能保存到内存中**。
- 地址和数据总线 BUS。CPU 和内存之间用地址总线、数据总线和控制线连接起来

![[Pasted image 20240220162423.png]]
==“看一下**内存读数据过程**”==
.CPU 内部将**==寄存器对接到数据总线==上**，使寄存器的每一位对接到一条数据线
**==CPU 通过控制线发一个读请求，并且将内存地址通过地址线发给内**==
==**内存收到地址和读请求之后，将相应的内存单元对接到数据总线的另一端。通过一条数据线到达 CPU 寄存器中相应的位，==**


32 条地址线和 32 条数据线，CPU 寄存器也是 32 位，可以说这种体系结构是 32 位的
地址线、数据线和 CPU 寄存器的位数通常是一致的。图 16.2 可以看出**数据线和 CPU 寄存器的位数应该一致**。另外**有些寄存器 (比如程序计数器)需要保存一个内存地址，因而地址线和 CPU 寄存器的位数也应该一致**
处理器的位数也称为字长，字 (Word)这个概念用得比较混乱，在有些上下文中指 16 位, 在有些上下文中指 32 位 (这种情况下 16 位被称为半字 HalfWord), 在有些上下文中指处理器的字长

最后还要说明一点，**本节所说的地址线、数据线是指 CPU 的内总线，是直接和 CPU 的执行单元相连的，==内总线经过 MMU 和总线接口的转换之后引出到芯片引脚才是外总线**==，外地址线和外数据线的位数都有可能和内总线不同，**例如 32 位处理器的外地址总线可寻址的空间可以大于4G**

**看一下 CPU ==取指执行的过程==**
![](../fujian/Pasted%20image%2020250301141952.png)
![[Pasted image 20240221153321.png|700]]
1. eip 寄存器指向地址0x80483a2, CPU 从这里开始**取一条5个字节的指令**，然后 eip 寄存器指向下一条指令的起始地址0x80483a7。==注意指令内存中的排列==
2.  2. **CPU 对这5个字节译码**，得知这条指令要求从地址0x804a01c 开始取4个字节保存到 eax 寄存器。
3.  3. **执行指令**,读内存,取上来的数是3,保存到 eax 寄存器。注意，==地址0x804a01c ~0x804a01f 里存储的四个字节不能按地址从低到高的顺序看成0x03000000==,而要按地址从高到低的顺序看成0x00000003。也就是说，**对于多字节的整数类型，低地址保存的是整数的低位，这称为小端(Little Endian)字节序(ByteOrder)**。x86 平台是小端字节序的，而另外一些平台规定低地址保存整数的高位，称为大端(Big Endian)字节序。
== [[../未归类卡/Q *数据分配向低地址分配*]] ==
## 设备
**CPU ==执行指令除了访问内存之外还要访问很多设备==（Device）**
**那么它们和 CPU 之间如何连接呢**
![[Pasted image 20240220162955.png]]
设备**==像内存芯片一样连接到处理器的地址总线和数据总线==**
但不同的==**设备和内存芯片应该占不同的地址范围**。**访问这种设备就像访问内存一样，按地址读写即可**==
**==和访问内存不同的是==**，**往一个地址写数据只是给设备发一个命令**，数据不一定要保存，而从一个地址读数据也不一定是读先前保存在这个地址的数据，而是得到设备的当前状态
“==**设备中可供读写访问的单元通常称为设备寄存器**==（注意和 CPU 寄存器不是一回事），**操作设备的过程就是读写这些设备寄存器的过程”**。如向串口发送寄存器里写数据，串口设备就会把数据发送出去，读串口接收寄存器的值，就可以读取串口设备接收到的数据。

无论是在 CPU 外部接总线的设备还是在 CPU 内部接总线的设备都有各自的地址范围，**==都可以像访问内存一样访问**==
==**采用这种方式操作设备，称为内存映射 I/O**==
**x 86 比较特殊**，x 86 对于设备有独立的端口地址空间，CPU 核需要引出额外的地址线来连接片内设备（和访问内存所用的地址线不同），==**访问设备寄存器时用特殊的 in/out 指令，而不是和访问内存用同样的指令，这种方式称为端口 I/O**==

==从 CPU 的角度来看，访问设备只有内存映射 I/O 和端口 I/O 两种，要么像内存一样访问，要么用一种专用的指令访问==
访问设备是相当复杂的，出现了各种适应不同要求的设备总线。==**设备总线并不直接和 CPU 相连**，CPU 通过内存映射 I/O 或端口 I/O 访问相应的**总线控制器**，通过总线控制器再去访问挂在总线上的设备==


**==<span style="background:#ff4d4f">保存在硬盘上的程序是不能被 CPU 直接取指令执行的, 操作系统在执行程序时会把它从硬盘拷贝到内存，这样 CPU 才能取指令执行，这个过程称为加载</span>==**（Load）
程序加载到内存之后，成为操作系统调度执行的一个任务，就称为进程（Process）
计算机在启动时执行一段固定的启动代码（称为 Bootloader）首先把操作系统从磁盘加载到内存, 然后执行操作系统中的代码把用户需要的其他程序加载到内存
操作系统和其他用户程序的不同之处在于：操作系统是常驻内存的，而其他用户程序则不一定
	操作系统最核心的功能是管理进程调度、管理内存的分配使用和管理各种设备，做这些工作的程序称为内核

**访问设备还有一点和访问内存不同**。
内存总是被动地等待被读或者被写。而设备往往会自己产生数据，并且需要主动通知 CPU 来读这些数据。这是由中断（Interrupt）机制实现的，**每个设备都有一条中断线**
**程序计数器会指向某个固定的地址**，于是 CPU 从这个地址开始取指令（或者说跳转到这个地址），执行中断服务程序（InterruptServiceRoutine, ISR）
比如发生中断时跳转到地址 0 x 00000010 执行，那么就要==**事先把一段 ISR 程序加载到这个地址**==。ISR 程序是内核代码的一部分，在==这段代码中首先判断是哪个设备引发了中断，然后调用该设备的中断处理函数做进一步处理==。
设备驱动程序通常是内核里的一组函数，通过读写设备寄存器实现对设备的初始化、读、写等操作，有些设备还要提供一个中断处理函数供 ISR 调用。
## mmu
现代操作系统普遍采用**虚拟内存管理，需要处理器中的 MMU（MemoryManagementUnit, 内存管理单元）提供支持**
**如果处理器没有 MMU, 或者有 MMU 但没有启用，CPU 执行单元发出的内存地址将直接传到芯片引脚上，被内存芯片（以下称为物理内存，以便与虚拟内存区分）接收，这称为物理地**

操作系统利用体系结构提供的 VA 到 PA 的转换机制实现虚拟内存管理机制

CPU 执行单元发出的内存地址将直接传到芯片引脚上，被内存芯片（以下称为物理内存，以便与虚拟内存区分）接收，这称为物理地址
![[Pasted image 20240607162912.png]]
> 处理器**启用了 MMU, ==CPU 执行单元发出的内存地址将被 MMU 截获==**, 从 CPU 到 MMU 的地址称为虚拟地址
![[Pasted image 20240607163048.png]]
32 位处理器，则内地址总线是 32 位的
**而经过 MMU 转换之后的外地址总线则不一定是 32 位的**


MMU 将 VA 映射到 PA 是**以页 (Page)为单位的**，32 位处理器的页尺寸通常是 4 KB。例如，MMU 可以通过一个映射项将 VA 的一页 0 xb 7001000~0 xb 7001 fff 映射到 PA 的一页 0 x 2000〜0 x 2 fff, 如果 CPU 执行单元要访问虚拟地址 0 xb 7001008, 则实际访问到的物理地址是 0 x 2008。**物理内存中的页称为物理页面或者页帧 (PageFrame)«==虚拟内存的哪个页面映射到物理内存的哪个页帧是通过页表 (PageTable)来描述的==，页表保存在物理内存中，MMU 会查找页表来确定一个 VA 应该映射到什么 PA,** 

**操作系统和 MMU 是这样配合的：**
.1.**操==作系统在初始化或分配、释放内存时会执行一些指令在物理内存中填写页表**==
**指令设置 MMU, 告诉 MMU 页表在物理内存中的什么位置**
2.，**CPU 每次执行访问内存的指令都会自动引发 MMU 做查表和地址转换操作**，地址转换操作由硬件自动完成
在程序中使用的变量和函数都有各自的地址，程序被编译后，这些地址就成了指令中的地址, 指令中的地址被 CPU 解释执行，就成了 CPU 执行单元发出的内存地址，所以在启用 MMU 的情况下，程序中使用的地址都是虚拟地址，都会引发 MMU 做查表和地址转换操作

MMU 除了做地址转换之外，还提**供内存保护机制。设置每个内存页面的访问权限**
当 CPU 要访问一个 VA 时，MMU 会检查 CPU 当前处于用户模式还是特权模式，访问内存的目的是读数据、写数据还是取指令，如果和操作系统设定的页面权限相符，就允许访问，把它转换成 PA, 否则不允许访问，产生一个异常 (Exception)

**通常==操作系统把虚拟地址空间划分为用户空间和内核空间**==

**段错误我们已经遇到过很多次了，它是这样产生的：**
1. **用户程序要访问的一个 VA, 经 MMU 检查无权访问**。
2. 2. MMU 产生一个异常，CPU 从用户模式**切换到特权模式**，跳转到内核代码中执行异常服务程序。
3. 3. **内核把这个异常解释为段错误**，把引发异常的进程终止掉。
## MemoryHierarchy 内存层次结构
CPU 寄存器：使用哪个寄存器，如何使用寄存器，这些都是由指令决定的
Cache：一级 Cache 是这样工作的：CPU 执行单元要访问内存时首先发出 VA, Cache 利**用 VA 查找相应的数据有没有被缓存**，如果 Cache 中有就不需要访问物理内存了，如果是读操作就直接将 Cache 中的数据传给 CPU 寄存器，如果是写操作就直接改写到 Cache 中；**如果 Cache 没有缓存该数据，就去物理内存中取数据，但并不是要哪个字节就取哪个字节，而是把相邻的几十个字节都取上来缓存着**，以备下次用，这称为一个 CacheLine. 典型的 CacheLine 大小是 32~256 字节。**==如果计算机还配置了二级缓存，则在访问物理内存之前先用 PA 去二级缓存中查找。一级缓存是用 VA 寻址的，二级缓存是用 PA 寻址的**==，这是它们的区别。Cache 所做的工作是由硬件自动完成的，
内存：在启用 MMU 的情况下，**程序指令中的地址是 VA, 而访问内存用的是 PA,**它们之间的映射关系由操作系统维护
硬盘：**由驱动程序操作设备总线控制器去访问**。由于硬盘的访问速度较慢，操作系统通常一次**从硬盘上读几个页面到内存中缓存起来，**
**除了访问寄存器由程序指令直接控制之外，访问其他存储器都不是由指令直接控制的**，有些是硬件自动完成的，有些是操作系统配合硬件完成的。
Cache 从内存取数据时会预取一个 CacheLine 缓存起来，操作系统从硬盘读数据时会预读几个页面缓存起来。预读+缓存的办法是很有效
# x86 汇编程序基础
## 简单的汇编程序
![[Pasted image 20240221160952.png]]
用汇编器 **as** 把汇编程序中的助记符翻译成机器指令，生成目标文件 hello.o：
![[Pasted image 20240221101542.png]]
然后用链接器 (Linker, 或 Link Editor) Id 把目标文件 hello. o 链接成可执行文件 hello： 
![[Pasted image 20240221101605.png]]、

**链==接主要有两个作用==，一是修改目标文件中的信息，对地址做重定位，二是把多个目标文件合并成一个可执行文件**

现在执行这个程序，==它只做了一件事就是退出，退出状态是 4==
Shell 中可以用**特殊变量$?** 得到上一条命令的退出状态![[Pasted image 20240221162451.png]]

**.开头**的名称并不是指令的助记符，是给汇编器一些特殊指示，称为*==*汇编指示** (AssemblerDirective)或伪指令== (Pseudo-operation)

**.section 指示把代码划分成若干个段** (Section), 程序被操作系统加载执行时，每个段被加载到不同的地址
**.data 段保存程序的数据，是可读可写的，相当于 C 程序的全局变量**
**.text 段保存代码，是只读和可执行的**


- ==`.data` 段通常用于存放 **已初始化的数据**。==
- ==`.bss` 段用于存放 **未初始化的数据**。==
- ==`.text` 段用于存放 **程序代码 (指令)**。 我们的指令都放在 `.text` 段。==

![[Pasted image 20240221102336.png]]
_start 是一个符号 (Symbol), **==符号在汇编程序中代表一个地址==**。汇编程序经过汇编器的处理之后，所有的符号都被替换成它所代表的地址值，所以要在目标文件的符号表中标记它是一个全局符号
**.globl 指示告诉汇编器，_start 这个符号==要被链接器用到**==
_start 就像 C 程序的 main 函数一样特殊，是整个程序的入口。链接器在链接时会查找目标文件中的_start 符号代表的地址，把它设置为整个程序的入口地址
如果一个符号没有用. globl 声明，就表示这个符号木会被链接器用到。
汇编程序中，立即数前面要加$, 寄存器名前面要加％, **以便跟符号名区分开**


![[Pasted image 20240604094347.png]]
前两条指令都是为这条指令做准备的
1.**int 指令称为软中断指令**，CPU 从用户模式切换到特权模式，然后跳转到内核代码中执行异常处理程序。
2.int 指令中的立即数 ==0 x 80 是一个参数==，在异常处理程序中要根据这个参数决定如何处理，==**在 Linux 内核中 int$0 x 80 这种异常称为系统调用**==
3.==eax 和 ebx 的值是传递给系统调用的两个参数==。eax 的值是系统调用号,
内核需要==**通过 eax 判断用户要调哪个系统调用**==，_exit 的系统调用号是1. ==**ebx 的值是传给_exit 的参数,表示退出状态**==，大多数系统调用完成之后会返回用户空间继续执行片面的指令，而_exit 系统调用比较特殊，它会终止掉当前进程，而不是返回用户空间继续执行。
> x 86 汇编一直存在两种不同的语法
intel 语法
==UNIX 平台的汇编器一直使用 AT&T 语法==
movl %edx,%eax 这条指令如果用 intel 语法来写，就是 mov  eax, edx, 寄存器名不加％号，源操作数和目标操作数的位置互换，字长也不是用指令的后缀 1 表示而是用另外的方式表示

## x 86 寄存器 
x 86 的通用寄存器有 eax、ebx、ecx、edx、edi、esi
x 86 的特殊寄存器有 ebp、esp、eip、eflags。 eip 是程序计数器，eflags 保存着计算过程中产生的标志位
## 第二个汇编程序
求一组数中量大值的汇编程序
![[Pasted image 20240221162839.png]]
**.long 指示声明一组数**，每个数占 32 位，相当于 C 语言中的数组
符号 data_items, 汇编器会把数组的首地址作为 data_items 符号所代表的地址，==data_items 类似于 C 语言中的数组名==
**data_items 这个标号没有用. globl 声明，因为它只在这个汇编程序内部使用，链接器不需要用到这个名字**
**除了. long 之外，常用的数据声明还有**：
	. byte：声明一组数，每个数占 8 位
	. ascii ：取值为相应字符的 ASCII 码，和 c 语言不同，这样声明的字符串末尾是没有*\\0 字符的


过程
![[Pasted image 20240604100337.png]]
初始化 **edi 指向数组的第0个元素**。
![[Pasted image 20240604100427.png]]
这条指令把数组的**第 0 个元素传送到 eax 寄存器中**。d**ata_items 是数组的首地址, edi 的值是数组的下标**，4 表示数组的每个元素占 4 字节，那么数组中第 edi 个元素的地址应该是 data_items+edi\*4

进入一个循环，循环的开头定义一个符号 start_loop,、==循环的末尾之后定义一个符号 loop_exit==
![[Pasted image 20240604101147.png]]
比较 eax 的值是不是 0, 如果是。就说明到达数组末尾了，就要跳出循环
## 寻址方式 
**变址寻址**   ==movl data_items (,%edi, 4),== 用于访问数组元素比较方便
**间接寻址**   movl (%eax),%ebx
**基址寻址**   例如 movl 4 (%eax),%ebx, 用于访问结构体成员比较方便
这条指令的作用是从内存地址 `%eax + 4` 中读取一个32位的数据，并将其存储到寄存器 `%ebx` 中。
## elf 文件
ELF (ExecutableandLinkingFormat)是一个开放标准
E==LF 格式的可执行文件==，它有三种不同的类型：
	可重定位的==目标文件==
	==可执行文件== 
	共享库

详细解释一下这个程序的汇编、链接、运行过程
	. 1写一个汇编程序保存成文本文件 max. s。
	2目标文件由若干个 Section 组成，我们在汇编程序中**声明的. section 会成为目标文件中的 Section, 此外==汇编器还会自动添加一些 Section (比如符号表)**。==
	3**链接器==把目标文件中的 Section 合并成几个 Segmen**，生成可执行文件==
	加载器 (Loader)根据可执行文件中的 Segment 信息加载运行这个程

“**==ELF格式提供了两种不同的视角==，链接器把ELF文件看成是Section的集合，而 加载器把ELF文件看成是Segment的集合**”
![[Pasted image 20240221105559.png]]
**==左边是从链接器的视角==**来看 ELF 文件
**开头的 ELFHeader 描述了体系结构和操作系统等基本信息，并指出 Section Header Table 和 Program Header Table 在文件中的什么位置**
==Section Header Table== 中保存了所有 Section 的描述信息

**==右边是从加载器的视角==**来看 ELF 文件，开头是 ELF Header, ==Program Header Table== 中保存了所有 Segment 的描述信息. 
一个 Segment 由一个或多个 Section 组成。这些 Section 加载到内存时具有相同的访问权限。**有些 Section 只对链接器有意义，在运行时用不到，也不需要加载到内存，那么就不属于任何 Segment**

**==目标文件需要链接器做进一步处理，所以一定有 SectionHeaderTable；可执行文件需要加载运行，所以一定有 ProgramHeaderTable；而共享库既要加载运行，又要在加载时做动态链接，所以既有 SectionHeaderTable 又有 ProgramHeaderTableo==**
### 目标文件
“==r**eadelf 工具**==读出==目标文件 max.o 的 ELF Header 和 Section Header Table==,”
![[Pasted image 20240221111919.png]]
![[Pasted image 20240221112320.png]]
![[Pasted image 20240221112328.png]]
ELFHeader中描述了这样一些信息：
	ELF文件开头四个字节都是0x7f、0x45、0x4c、0x46,其中后三个字节就是ELF的ASCII码，**在文件开头用几个特殊字符来标识文件类型是UNIX系统的惯用伎俩**
	文件格式是ELF32；
	文件类型是Relocatablefile
	序的**入口地址是0x0**,因为目标文件的人口地址还没确定，链接成可执行文件时才能确定入口地址；
	**Program Header Table在文件中的开始位置是0,因为目标文件没有**
	**Section Header Table中有8个Section Header表项，每个表项占40字节**
	**Section Header String Table 也是一个 Section, 它由 Section Header Table 中的第 5 个表项来描述。**

![[Pasted image 20240221112421.png]]
![[Pasted image 20240221112434.png]]
<span style="background:#ff4d4f">.==**text 和. data 是我们在汇编程序中声明的 Section.其他 Section 是汇编器自动添加的**==</span>
==Addr 列指出这些 Section 加载到内存中的地址（虚拟地址）==，**目标文件中各 Section 的加载地址是待定的, 所以是 00000000, 到链接时再确定这些地址**
Off 和 Size 列指出各 Section 的起始文件地址和长度。==**比如.data 段从文件地址0x60开始**，一共0x38个字节==，回去翻一下程序，.data 段定义了14个4字节的整数，一共是56个字节，也就是0x38。**根据以上信息可以描绘出整个目标文件的布局**，如表17.1所示。

![[Pasted image 20240221112808.png]]
我们直接**==用 hexdump 工具把目标文件的字节全部打印出来看==。 **出来看。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=230&annotation=I7WDHNEQ))
![[Pasted image 20240221112849.png]]
左边一列是文件地址，中间是每个字节的十六进制表示，右边是把这些字节解释成 ASCII 码所对应的字符 ([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=232&annotation=HLR26UK8))
==中间的\*号表示省略的部分全是 0。==([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=232&annotation=6X8K579M))
.data 段对应的是这一块：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=232&annotation=72KS672L))
![[Pasted image 20240221190645.png]]
<span style="background:#ff4d4f">.data 段将被原封不动地加载到内存中</span>


.shstrtab 和. strtab 这两个 Section 中存放的都是 ASCH 码：
![[Pasted image 20240221191005.png]]
==.shstrtab 段保存着各 Section 的名字，. strtab 段保存着程序中用到的符号的名字==
每个名字都是以 Null 结尾的字符串

<span style="background:#ff4d4f">**全局变量如果在代码中没有初始化属于. bss 段**</span>
在加载时它和. data 段一样都是可读可写的数据，.data 段需要占用一部分空间保存初始值，而. bss 段则不需要
也就是说，**. bss 段在文件中只占一个 SectionH eader 而没有对应的 Section, 程序加载时. bss 段占多大内存空间在 Section Header 中描述**


**继续分析 readelf 输出的最后一部分，是从. rel. text 和. symtab 这两个 Section 中读出的信息。**

![[Pasted image 20240221192051.png]]
**==.rel. text 告诉链接器指令中的哪些地方需要做重定位==**
==**.symtab 是符号表**==
==Ndx 列是每个符号所在的 Section 编号。例如符号 dataitems 在第 3 个 Section 里 (也就是. data 段)==，各 Section 的编号见 SectionHeaderTableo
**Value 列是每个符号所代表的地址，在目标文件中，符号地址都是相对于该符号所在 Section 的相对地址**，比如 datajtems 位于. data 段的开头，所以地址是 O
Bind 这一列可以看出_start 这个符号是 GLOBAL

==剩下. text 段没有分析，==
==**objdump 工具可以把程序中的+机器指令反汇编**== (Disassemble)
![[Pasted image 20240221192546.png]]
![[Pasted image 20240221192635.png]]
![[Pasted image 20240221192645.png]]
显然，所有的==符号都被替换成地址了，比如 je 23==
==**没有加$的数表示内存地址**==
**＜loop_exit>并不是指令的一部分，而是反汇编器从. symtab 和. strtab 中查到的符号名称**
**目前所有指令中用到的符号地址都是相对地址，下一步链接器要修改这些指令，把其中的地址都改成加载时的内存地址，这些指令才能正确执行。**
### 可执行文件
==分析可执行文件 max,== **看看链接器都做了什么改动**。
![[Pasted image 20240604135830.png]]
![[Pasted image 20240604135847.png]]

Entry point address 改成了 0x8048074（这是_start 符号的地址）
==多了两个 Program  Header, 少了两个 Section Header。==
SectionHeaderTable 中.text 和. data 段的加载地址分别改成了 0 x 08048074 和 0 x 080490 a 0。
==**. bss 段没有用到，所以被删掉了。.rel. text 段就是用于链接过程的，做完链接就没用了，所以也删掉了**。==

==**<span style="background:#ff4d4f">多出来的 Program Header Table 描述了两个 Segment 的信息</span>==**
==**.text 段和前面的 ELFHeader,Program Header Table 一起组成一个 Segment**（FileSiz 指出总长度是0x9e）,**.data 段组成另一个 Segment**==（总长度是0x38）
**这两个 Segment 分别叫做 ==<span style="background:#ff4d4f">TextSegment 和 DataSegment</span>**==
==**<span style="background:#ff4d4f">VirtAddr 列指出 TextSegment 加载到虚拟地址0x08048000</span>**==(x86平台上后面的 PhysAddr 列是没有意义的，并不代表实际的物理地址)
Fig列指出TextSegment的访问权限是可读可执行
==**Align 的值0x1000（4K）是 x86平台的内存页面大小**==

**在加载时文件也要按内存页面大小分成若干页，==文件中的一页对应内存中的一页，对应关系如图17.2所示==。**
![[Pasted image 20240221193733.png]]
==**为了简化链接器和加载器的实现，还规定每个Segment在文件的页面中偏移多少加载到内存页面也要偏移多少**==
==**<span style="background:#ff4d4f">Text Segment 在文件的第0个页面开头，加载到内存页面也是从首地址0x08048000开始</span>**，由于 Text Segment 包含了文件名和.text 段，所以,text 段的加载地址是0x08048074,_start 符号位于.text 段的开头，所以一 start 符号的地址也是 0x08048074==
<span style="background:#ff4d4f">Data Segment 在文件的第0个页面中的偏移是 Oxa0,在内存页面中的偏移也是 Oxa 0,所以从0x080490a0开始</span>


原来目标文件符号表中的 Value 都是相对地址，现在都改成绝对地址了。**此外还多了三个符号_bss_start、_edata 和_end,这些符号在链接脚本中定义，被链接器添加到可执行文件中**

==再看一下反汇编的结果==：检查一下改了哪些地方
**首先看==跳转指令==**
![[Pasted image 20240221194732.png]]
其实只是反汇编的结果不同了，*==*指令的机器码根本没变**==
==**为什么不用改指令就能跳转到新的地址呢？因为跳转指令中指定的是相对于当前指令向前或向后跳多少字节，而不是指定一个完整的内存地址**==，内存地址有 32 位，这些跳转指令只有 16 位，显然也不可能指定一个完整的内存地址，称为相对跳转
跳转指令只有 16 位，只能在当前指令前后的一个小范围内跳转
==也有的跳转指令指定一个完整的内存地址，可以跳到任何地方，绝对跳转==。

**==再看内存访问指令==，**
![[Pasted image 20240221194802.png]]
**指令中的地址原本是0x00000000,现在改成了0x080490a0**(注意是小端字节序)。那么==**链接器怎么知道要改这两处呢**？是根**据目标文件中的.rel.text 段提供的重定**==
![[Pasted image 20240221195245.png]]
==**第一列 Offset 的值就是.text 段需要改的地方，在.text 段中的相对地址是8和0x17,正是这两条指令中00000000的位置。**==



**strip 命令去除可执行文件中的符号信息，这样可以有效减小文件的尺寸而不影响运行：([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=238&annotation=WRA3V9A4))：**
**不要对目标文件和共享库使用 strip 命令，因为链接器需要利用目标文件和共享库中的符号信息来做链接。**


**strip 命令去除可执行文件中的符号信息**，这样可以有效减小文件的尺寸而不影响运行： 
![[Pasted image 20240604140908.png]]
![[Pasted image 20240604140919.png]]
不要对目标文件和共享库使用 strip 命令，因为链接器需要利用目标文件和共享库中的符号信息来做链接。
# 汇编与 c 之间的关系
## 函数调用
用下面的代码来研究函数的调用过程。
![[Pasted image 20240222180131.png]]
==**如果在编译时加上・g 选项== (在第 10 章讲过・g 选项)，==那么用 objdump 反汇编时可以把 C 代码和汇编代码穿插起来显示==**，这样 C 代码和汇编代码的对应关系看得更清楚
![[Pasted image 20240221113358.png]]
![](../fujian/Pasted%20image%2020250302161026.png)
**要查看编译后的汇编代码，==其实还有一种办法是 gcc-S main. c, 这样只生成汇编代码 main. s, 而不生成二进制的目标文件。**==

整个程序的执行过程是 main 调用 foo, foo 调用 bar, 我们用 gdb 跟踪程序的执行, 直到 bar 函数中的 inte=c+d; **执行完毕准备返回时，才在 gdb 中打印函数栈帧**。([pdf](zotero://open-pdf/library/items/MGBQJ6CB?page=241&annotation=IIAWJ6YB))


![[Pasted image 20240604142318.png]]
![[Pasted image 20240604142350.png]]
![[Pasted image 20240604142405.png]]
这里又用到几个==**新的 gdb 命令**:==
- disassemble 可以反汇编当前函数或者指定的函数
- 以前我们讲过 step 命令可以一行代码一行代码地单步调试,而这里用到的 si 命令可以一条指令一条指令地单步调试。
- info registers 可以显示所有寄存器的当前值。
- 在 gdb 中表示**寄存器名时前面要加个 $**，如 $ esp 可以打印 esp 寄存器的值
	x/12x $esp 命令可以查看内存中从0xbffff358地址开始的12个32位数。


==在执行程序时，操作系统为进程分配一块栈空间来保存函数栈帧，**esp 寄存器总是指向栈顶**==
==调用一个函数都要分配一个栈帧来保存参数和局部变量==
详细分析这些数据在栈空间的布局
根**据 gdb 的输出结果如图** 18.1 所示：
![](../fujian/Pasted%20image%2020250302161112.png)
在每个函数的栈帧中，==ebp 指向栈底，而 esp 指向栈顶==
![[Pasted image 20240604201049.png]]
1==**要调用函数 foo。先要把参数准备好**，第二个参数保存在<span style="background:rgba(160, 204, 246, 0.55)"> esp+4</span> 指向的内存位置，第一个参数保存在 esp 指向的内存位置==
2然后执行 call 指令
	. ==foo 函数调用完之后要返回到 call 的下一条指令继续执行，所以把 call 的下一条指令的地址 0 x 80483 ff 压栈，同时把 esp 的值减4==
	
修改程序计数器 eip, 跳转到 foo。函数的开头执行。



现在看 foo 函数的汇编代码：
![[Pasted image 20240604201355.png]]
push %ebp 指令把 ebp 寄存器的值压栈，同时把 esp 的值减 4 。esp 的值现在是 0 xbffff 378, 下一条指令把这个值传送给 ebp 寄存器。**==这两条指令合起来是把原来 ebp 的值保存在栈上，然后又给 ebp 赋了新值，新值在图 18.1 中标注为 ebp(foo)。==**
==**然后 esp 所指向的地址向下移动 8 个字节 (在图 18.1 中标注为 esp (foo)), 为即将压栈的参数 d 和 c 留出空间。**==


**在函数执行过程中 ==esp 随着压栈和出栈操作随时变化, 而 ebp 是不动的==, ==函数的参数和局部变量==都是通过 ebp 的值加上一个偏移量==来访问==**. ==例如 f oo 函数的参数 b 和 a 分别通过 ebp+12 和 ebp+8来访问。==（**==ebp (bar) 的==**）

==所以 f oo 函数接下来的指令把参数 b 和 a 取出来，作为参数 d 和 c 再次**压栈**==，为调用 bar 函数做准备，然后把**返回地址 0 x 80483 e3压栈**，调用 bar 函数：如下
![[Pasted image 20240605201104.png]]


**现在看 bar 函数的指令**
![[Pasted image 20240605201229.png]]
![[Pasted image 20240605201239.png]]

这次又把 foo 函数的 ebp 压栈保存，然后给 ebp 赋了新值。然后 esp 所指向的地址**向下移动16个字节(在图18.1中标注为 esp(bar))，为局部变量 e 留出空间。**
**通过 ebp+12 和 ebp+8 分别可以访问参数 d 和 c, 通过 ebp-4 可以访问局部变量 e。**
lea (%edx,％eda 1),%eda 泰这条指令的意思是 eax=edx+eax\*1


gdb 中可以用 **bt 命令和 frame 命令查看每层栈帧上的参数和局部变量,** 现在可以解释它的工作原理了：如果我当前在 bar 函数中，我可以通过 ebp 找到 bar 函数的参数和局部变量, 也可以找到 foo 函数的 ebp 保存在栈上的值, 有了 foo 函数的 ebp, 又可以找到它的参数和局部变量，也可以找到 main 函数的 ebp 保存在栈上的值，因此各层函数栈帧通过保存在栈上的 ebp 的值串起来了。

bar 函数的返回指令：
![[Pasted image 20240605202733.png]]
==bar 函数返回值是通过 eax 寄存器传递的，==
==所以**首先把 e 的值读到 eax 寄存器中。然后执行 leave 指令**，==
**这个指令是函数开头的 push %ebp 和 mov%esp,%ebp 的逆操作**：
	1, 把 ebp 的值赋给 esp, 现在 esp 的值是 0 xbffff 368。 2 .现在 esp 所指向的栈顶保存着 fbo 函

最后是 ==**ret 指令，它是 call 指令的逆操作**：==
	1 .现在esp所指向的栈顶保存着返回地址0x80483e3,把这个值恢复给eip,同时 esp增加4, esp的值变成0xbffff370 2 .由于修改了程序计数器eip,程序跳转到返回地址处继续执行。

**注意函数调用和返回过程中的这些规则：**
1. ==参数压栈传递，并且是从右到左依次压栈，传参所使用的栈空间由调用者分配和释放。==
2. 2. ebp 总是指向当前栈帧的栈底。
3. 3. **返回值通过 eax 寄存器传递**。

## main 函数、启动例程和退出状态
为什么汇编程序的入口是_start 而 C 程序的入口是 main 函数呢

==-s选项生成汇编代码，-c 选项生成目标文件==
==-o 搭配使用，给输出文件重新命名而不使用 gcc 默认的输出文件名==
用-v 选项可以了解详细的编译过程：



==看看**编译器提供的目标文件里都有什么，我们只看符号表，可以用 readelf 命令的・s 选项**，也可以用 **nm 命令**==。我们重点分析 crtl.o 中的符号。
![[Pasted image 20240605203734.png]]
**符号表**的每一行由地址、符号类型和符号名组
**大写字母是全局符号，小写字母是局部符号**
==U main 这一行表示 main 这个符号在 crtL. o 中**引用了，但是没有定义（U 表示 Undefined）**==, 因此需要别的目标文件提供一个定义并且和 crtl. o 链接在一起。==T start 这一行表示_start 这个符号在 crtL. o 中提供了定义==，**这个符号的类型是代码（T 表示 Text）。**

C 程序的入口点其实是 crtl. o 提供的_start, 它首先做一些初始化工作, 然后调用我们写的 main 函数。





把 main. c 编译成目标文件 main.o，然后和编译器提供的目标文件链接，对生成的可**执行文件 main 做反汇编分析**：
main. c 中除了 main 函数还定义了 foo、bar 两个函数，**链接完成后，crtl. o 中定义的符号_start 和 main. o 中定义的符号 bar、foo、main 都合并到可执行文件的. text 段中**。符号 main 的地址是 0 x 080483 e 5, 因此_start 中的 push $0 x 0 指令被链接器改成了 push $0x80483e5。
一个目标文件中引由了某个符号，链接器在另一个目标文件中找到这个符号的定义并确定它的地址，这个过程叫做==符号解析==
==符号解析和重定位都是通过修改指令中的地址实现的==
**链接的过程** 
![[Pasted image 20240605204610.png]]
crtl. o 还引用了一个未定义符号_libc_start_mai 你，这个符号在 libc 中定义
==**libc 是一个共享库，不链接到可执行文件 main 中，而是在运行时做动态链接：**==
	我们在链接时用-Ic 选项指定了共享库 libc, 用 Yynamic-linker /lib/ld-linux. so. 2 指定了动态链接器，这些信息都会写到可执行文件中。



![[Pasted image 20240605205423.png]]
![[Pasted image 20240605205435.png]]
我们回头看_start 的反汇编。首先将一系列参数压栈，然后通过 call 80482 e 8 指令调用库函数_Iibc_start_main 做初始化工作，其中最后一个压栈的参数 push $0 x 80483 e 5 正是 main 函数的首地址，\_libc_start_main 在做完初始化工作之后会根据这个参数调用 main 函数。
==**由于\_libc_start_main 需要动态链接，所以这个库函数的指令在可执行文件 main 的反汇编中肯定是找不到的**，然而我们在地址 0 x 80482 e 8 处找到了这几条指令：==
![[Pasted image 20240605205832.png]]
==`这几条指令位于. pit 段而不是. text 段，**. pit 段协助完成动态链接`==**


**main 函数最标准的原型**应该是 int main (int argc, char\*argv[])
**我们都把 main 函数的原型写成** int main (void);, 这也是 C 标准允许的
**多传了参数而不用是没有问题的，少传了参数却用了则会出问题**。


由于 main 函数是被启动例程调用的，所以从 main 函数 return 时就返回到启动例程中，**main 函数的返回值被启动例程得到**，如果将启动例程表示成等价的 C 代码 (实际上启动例程一般是直接用汇编写的)，则它调用 main 函数的形式是：
![[Pasted image 20240605224933.png]]
启动例程得到 main 函数的返回值后，会立刻用它做参数调用 exit 函数
exit 也是 libc 的库函数，它首先做一些清理工作，然后调上一章讲过的_exit 系统调用终止进程
main 函数的返回值最终被传给_exit 系统调用，成为进程的退出状态
我们也可以在 main 函数中直接调用 exit 函数终止进程而不返回到启动例程，
![[Pasted image 20240606074133.png]]
这样和 int main (void){return 4;}的效果是一样的
按照惯例，退出状态为 0 表示程序执行成功，退出状态非 0 表示出错

在 C 程序中也可以调用_exit 函数退出 (需要包含头文件 unistdh), 它是_exit 系统调用的简单包装。怎么包装呢？它可能是一个 C 函数，其中内嵌了 movl$1,%eax、movl?,%ebx 和 int$0x80三条指令???

。头文件 ==unistd. h== 中声明的函数并不是 C 标准库函数，==而是 POSIX 标准定义的 UNIX 系统函数，但也在 libc 中实现。==
POSIX 统一各种 UNIX 系统的接口。UNIX 系统的函数接口，既包括 C 标准库函数，也包括系统调用和其他 UNIX 库函数

一个进程调用 exit 或_exit 终止，或者从 main 函数返回而终止，都属于正常终止 (NormalTermination),也称为退出 (Exit)。但并非所有的进程终止都是正常的，比如按 Ctrl+C 组合键终止一个进程，或者运行时产生段错误，或者用 kill 命令终止一个进程，这几种情况本质上都是进程收到一个信号然后内核把进程强行终止掉了，进程并没有执行_exit 系统调用，也没有退出状态，这称为异常终止
## 变量的存储布局
![[Pasted image 20240606074346.png]]
![[Pasted image 20240606074355.png]]
那么这些==变量的存储空间怎么分配呢？我们编译之后用 **readelf 命令看它的符号==表，了解各变量的地址分布**
![[Pasted image 20240606074416.png]]
==变量 A 用 const 修饰，从 readelf 的输出可以看到这个地址位于. rodata 段：==
![[Pasted image 20240606074451.png]]
.rodata 段在内存中的地址是 0 x 08048568~0 x 08048583
**用 hexdump 命令看看这个段的内容**
![[Pasted image 20240606074521.png]]
在链接时. rodata 段和. text 段合并到 TextSegment 中，在加载运行时操作系统把 TextSegment 的页面只读保护起来
==从 readelf 的输出可以看出. rodata 段和. text 段被合并到一个 Segment,. data 段和. bss 段被合并到另一个 Segment== 
![[Pasted image 20240606074556.png]]
像 A 这种 const 变量在定义时必须初始化。因为只有初始化时才有机会给它一个值，一旦定义之后就不能再改写了，如果给它赋值编译器会报错，也就是说
操作系统的内存管理和编译器的语义检查为全局 const 变量提供了双重保护
我们知道函数的局部变量在栈上分配，如果把局部变量声明为 const 就少了一层保护，操作系统无法对栈空间只读保护（因为栈上的其他数据要求可读可写），但编译器仍可以做语义检查。???


.data 段在内存中的地址是0x804a010〜0x804a023,在.data 段中有三个变量，a,b 和a.1706。链接器不会对局部符号做符号解析。一个函数定义前面也可以用 static 修饰，表示这个函数名是局部符号。

==a.1706 是什么呢？它就是 main 函数中的 static int a==
函数中的 static 变量不同于我们以前讲的局部变量，它并不是在调用函数时分配，在函数返回时释放，而是**像全局变量一样静态分配**
static 变量也是局部作用域的，a 这个**变量名只在 main 函数中起作用**，在别的函数中说变量 a 就不是指它了，所以
编译器给它的符号名加了一个后缀，**变==成a.1706, 以便和全局变量 a 以及其他函数的静态变量 a 区分开==**


,bss 段在内存中的地址是0x804a024〜0x804a02f （紧挨着.data 段），变量 c 位于这个段

**.data 段和. bss 段在链接时合并到 DataSegment 中**
.bss 段和. data 段的不同之处在于，**. bss 段在文件中不占存储空间**，加载到内存时这个段用0填充。未初始化的和明确初始化为 0 的全局变量、static 变量都会分配在. bss 段外


剩下 main 函数中的变量 b 和 c 没有分析。b 是一个**==数组，在栈上分配==**
看 main 函数的反汇编代码：
![[Pasted image 20240606075748.png]]
b 初始化用的这个字符串"Hell。world"不需要在. rodata 段分配，而是写到栈上
![[Pasted image 20240606075944.png]]
==虽然栈是从高地址向低地址增长的，但数组总是从低地址向高地址排列的，按从低地址到高地址的顺序依次是 b[0]、b[l]、b[2]等==

到==调用 printf 时对于"Helloworld%d\n"这个参数压栈的是它在.rodata 段中的首地址0x804857,而不是把整个字符串压栈==


作用域
链接属性
## 结构体和联合体
![[Pasted image 20240606084250.png]]
![[Pasted image 20240606084719.png]]
![[Pasted image 20240606084231.png]]
==栈是从高地址向低地址增长的，结构体成员也是从低地址向高地址排列的，这一点和数组类似。但有一点和数组不同，结构体的各成员并不是一个紧挨一个排列的，中间有空隙，称为填充==（Padding）不仅如此，在这个结构体的末尾也有三个字节的填充
==为什么编译器要这样处理呢？**指令访问 4 个字节（比如上面的 movl）, 起始内存地址应该是 4 的整数倍**，这称为对齐==（Alignment）。
如果一条指令访问两个字节（比如上面的 movw）, 起始内存地址应该是 2 的整数倍
**合理设计结构体各成员的排列顺序可以节省存储空间**，比如如下
![[Pasted image 20240606085055.png]]
gcc 提供了一种扩展语法可以消除结构体中的填充字节:
![[Pasted image 20240606085121.png]]
==数据类型最少也要占一个字节，而**结构体中还可以使用 Bit-field 语法定义只占几个 bit 的成员**==
![[Pasted image 20240606090825.png]]
**s 这个结构体的布局如图 18.6 所示:**
![[Pasted image 20240606090842.png]]

**Bit-field 也属于整型，用 int 或 unsigned int 声明**，表示有符号数或无符号数，
**但它不像普通的 int 型一样占 4 个字节**
**即使不写未命名的 Bit-field, 编译器也有可能在两个成员之间插入填充位, 例如图 18.6 的 five 和 six 之间有填充位，这样 six 这个成员就刚好单独占一个字节了，访问效率会比较高**
**这个结构体的末尾还填充了 3 个字节，以便对齐到 4 字节边界**

从图 18.6 中 one 和 two 的排列顺序可以看出，如果对一个字节再细分，则**字节中的 Bit Order 也是小端的，因为排在结构体前面的成员（靠近低地址一边的成员）取字节中的低位**

Bit-field 在驱动程序中是很有用的，因为经常需要单独操作设备寄存器中的一个或几个 bit, 但一定要小心使用，首先弄清楚每个 Bit-field 和设备寄存器中每个 bit 的对应关系

**在上例中我没有给出反汇编结**果，直接画了个图说这个结构体的布局是这样的，那我**有什么证据这么说呢？上例的反汇编结果比较繁琐，我们可以用==另一种手段得到这个结构体的内存布局==：**
![[Pasted image 20240606091656.png]]

联合体如果用 Initializer 初始化，则只初始化它的第一个成员，例如 demo_typeu= {{1,5,513,17,129,0x81}} ; **初始化的是u.bitfield**, 这样我们只知道u.bitfield 结构体各成员的值是多少，**却不知道它的内存布局是什么样的**，
然后我们换一个视角，同样是这 8 个字节，**我们把它看成一个u.byte 数组，就可以看出每个字节分别是多少，内存布局是什么样了**。???
用 C 99 的 Memberwise 初始化语法，则可**以初始化联合体的任意一个成员**，例如：
![[Pasted image 20240606091855.png]]




应用程序二进制接口规范（ABLApplicationBinaryInterface）, 如果两个平台具有相同的体系结构，并且遵循相同的 ABL 就可以保证一个平台上的二进制程序直接拷贝到另一个平台就能运行，不用重新编译
## c 内联汇编
有些平台相关的指令必须手写，在 C 语言中没有等价的语法，因为 C 语言中的概念是对各种平台的抽象，**每种平台特有的一些东西就不会在 C 语言中出现了，==例如** **x 86 是端口 I/O, 而 C 语言就没有这个概念，所以 in/out 指令必须用汇编来写。**==

**最简单的格式是**_asm_("assemblycode");, 例如_asm_("nop");, nop 这条指令什么都不做，只是让 CPU 空转一个指令执行周期。
**如果需要执行多条汇编指令**，则应该用\\n\\t 将各条指令分隔开，
![[Pasted image 20240606092621.png]]
通常**内联汇编需要和 C 代码中的变量建立关联，要用到完整的内联汇编格式:**
![[Pasted image 20240606092844.png]]
第一部分是汇编指令，和上面的例子一样，
第二部分和第三部分是约束条件，**第二部分**告诉编译器**汇编指令的运算结果要输出到哪些 C 语言操作数中**，这些操作数应该是左值表达式，**第三部分**告诉编译器汇编指令需要**从哪些 C 语言操作数获得输入**，
第四部分是在**汇编指令中被修改的寄存器列表** (称为 ClobberList), 告诉编译器哪些寄存器的值在执行这条_asm_语句时会改变。
**后三个部分是可选的，如果有就填写，没有就空着只写个冒号**
例子
![[Pasted image 20240606093039.png]]
![[Pasted image 20240606093104.png]]
**这个程序将变量 a 的值赋给 b。**
**“r”（a）告诉编译器分配一个寄存器保存变量 a 的值，作为汇编指令的输入**，也就是**指令中的％1**（按照约束条件的顺序，b 对应％0, a 对应 1%）, 至于％1 究竟代表哪个寄存相则由编译器自己决定。汇编指令首先把%1 所代表的寄存器的值传给 eax（**为了和％1 这种占位符区分，eax 前面要求加两个％号**），然后把 eax 的值再传给％0 所代表的寄存器。**"=r"（b）表示把％0 所代表的寄存器的值输出给变量 b**。在**执行这两条指令的过程中，寄存器 eax 的值被改变了，所以把"％eax"写在第四部分**，告诉编译器在执行这条_asm_语句时 eax 要被改写，所**以在此期间不要用 eax 保存其他值。**

**这个程序的反汇编结果：**
![[Pasted image 20240606093859.png]]
**可见%0 和%1 都代表 edx 寄存器，首先把变量 a（位于 esp+0xlc 的位置）的值传给 edx 然后执行内联汇编的两条指令，然后把 edx 的值传给 b（位于 espX）xl8的位置）。**??
## volatile 限定符
编译器优化会对生成的指令产生什么影响

我们用 recv 和 send 这两个全局变量来模拟设备寄存器。假设某种平台采用内存映射 I/O, 串口发送寄存器和串口接收寄存器位于固定的内存地址, 而 recv 和 send 这两个全局变量也有固定的内存地址，所以在这个例子中把它们假想成串口接收寄存器和串口发送寄存器。
在 main 函数中，首先从串口接收三个字节存到 buf 数组，然后把这三个字节取反，依次从串口发送出去，我们查看这段代码的反汇编结果：
![[Pasted image 20240606170351.png]]
movz 指令把字长较短的值存到字长较长的存储单元中，存储单元的高位用0填充。该指令可以有 b(byte)、w(word)、1(long)三种后缀，分别表示单字节、两字节和四字节。比如 movzbl 0x804a019,%eax 表示把地址0x804a019处的一个字节存到 eax 寄存器中，而 eax 寄存器的长度是4个字节，高3个字节用0填充，如果高3个字节采用符号扩展则应该用 movsbl 指令
下一条指令 mov%al,0x804a01a 中的 al 寄存器正是 eax 寄存器的低字节，这条指令把 eax 寄存器的低字节存到地址0x804a01 a 处的一个字节中。以 eax 为例，al 表示低8位，ah 表示次低8位，ax 表示低16位，如图18.7所示。
![[Pasted image 20240606134957.png]]
如果**指定优化选项-O 编译，反汇编的结果就不一样了**
![[Pasted image 20240606165755.png]]
![[Pasted image 20240606170450.png]]
**==为什么编译器优化的结果会错呢==**？因为编译器并不知道 0 x 804 a 018 和 0 x 804 a 019 是设备寄存器的地址，**把它们当成普通的内存单元了。如果是普通的内存单元，只要程序不去改写它，它就不会变，可以先把内存单元里的值读到寄存器缓存起来，以后每次用到这个值就直接从寄存器读取，这样效率更高**，我们知道读寄存器远比读内存要快。另一方面，**如果对一个普通的内存单元连续做三次写操作，只有最后一次的值会保存到内存单元中，所以前两次写操作是多余的，可以优化掉**。

**然而访问设备寄存器的代码这样优化就错了**，因为设备寄存器通常具有以下特性：
	・设备寄存器中的数据不需要改写就可以自己发生变化，每次读上来的值可能不一样。 
	・连续多次向设备寄存器中写数据并不是在做无用功，而是给设备发命令，是有意义的。
	
**程序员应该明确告诉编译器哪些内存单元的访问是不能优化的，在 C 语言中可以用 volatile 限定符修饰变量**
**我们把代码的开头几行改成**：
![[Pasted image 20240606165528.png]]
然后**指定优化选项・O 编译**，查看反汇编的结果：
![[Pasted image 20240606170209.png]]
确实每次读 recv 都从内存地址0x804a019读取，每次写 send 也都写到内存地址0x804a 018了
每次写 send 并不需要取出 buf 中的值，而是取出先前缓存在寄存器 eax、edx、ecx 中的值,因为 buf 并没有用 volatile 限定. 试着在 buf 的定义前面也加上 volatile, 再优化编译，再查看和比较反汇编的结果。


“-o0表示不优化，这是缺省的选项”

如果在编译时指定了优化选项，源代码和生成指令的次序可能无法对应
这一点在**用 gdb 做源码级调试时尤其需要注意 (做指令级调试没关系)，在为调试而编译时不要指定优化选项，否则可能无法一步步跟踪源代码的执行过程**。



有了 **volatile 限定符可以防止编译器优化对设备寄存器的访问**，但对于有 Cache 的平台仅仅这样还不够,还是**无法防止 Cache 优化对设备寄存器的访问**
访问内存地址时 Cache 对程序员是透明的, 比如执行 movzbl 0x804a019,%eax 这样一条指令，我们并不知道 eax 的值是真的从内存地址0x804a019读到的，还是从 Cache 中读到的

通常，**有 Cache 的平台都有办法对某一段地址范围禁用 Cache**, 一般是在页表中设置的，可以设定哪些页面允许 Cache 缓存，哪些页面不允许 Cache 缓存，MMU 不仅要做地址转换和访问权限检查，也要配合 Cache 工作


除了**设备寄存器需要用 volatile 限定之外，当一个全局变量被同一进程中的多个控制流程访问时也要用 volatile 限定，比如信号处理函数和多线程就属于这种情况,**
# 链接
## 多目标文件的链接
现在我们把例 12.1 拆成两个. c 文件，stack. c 实现堆栈，而 maimc 使用堆栈：

这段程序和原来有点不同，**在例 12.1 中 top 总是指向栈顶元素的下一个元素，而在这段程序中 top 总是指向栈顶元素，所以要初始化成-1 才表示空堆栈，这两种堆栈使用习惯都很常见。**

![[Pasted image 20240607084033.png]]

==**用 nm 命令查看目标文件的符号表**==
会发现 main. o 中有未定义的符号 push、pop、is_empty、putchar, 前三个符号在 stack.o 中定义了，在链接时做符号解析，而 putchar 是 libc 的库函数，在可执行文件 main 中仍然是未定义的，要在程序运行时做动态链接。

**通过 readelf-a main 命令可以看到**：main 的. bss 段合并了
![[Pasted image 20240607084228.png]]
==链接过程是由一个链接脚本 (LinkerScript)控制的，**链接脚本决定了给每个段分配什么地址，如何对齐**，哪个段在前，哪个段在后，哪些段合并到同一个 Segment。 **另外链接脚本还要把一些特殊地址定义成符号**==，例如_bss_start 代表, bss 段的起始地址，_end 代表. bss 段的结束地址，**这些符号会出现在可执行文件的符号表中，加载器可以由这些符号得知. bss 段的地址范围**，以便把它清零。
如果用 Id 做链接时没有通过・T 选项指定链接脚本，则使用 Id 的默认链接脚本，==**默认链接脚本可以用 Id --verbose 命令查看**==


![[Pasted image 20240607085810.png]]
![[Pasted image 20240607085823.png]]
**==ENTRY (\_start)指明整个程序的入口点是_start==**


![[Pasted image 20240607090017.png]]
PROVIDE (executable start=SEGMENT_START (Htext-segmentM, 0 x 08048000)); ==语句**导出一个 GLOBAL 的符号_executable_start, 它的值是 Text Segment 的起始地址** (默认值是 0 x 8048000)。==
==**.  表示当前链接地址**，即程序加载运行时的虚拟地址，链接器每组装一个段就把当前链接地址自动加上这个段的长度==，因此各段在加载时一般是紧挨着的，中间没有空隙，==只有一种情况例外：如果在链接脚本中**给"."赋值, 那么链接器组装下一个段就从赋值的新地址开始，而不是和前一个段紧挨着了**。所以这条语句表示把当前链接地址改成 Text Segment 的起始地址加上 SIZEOF_HEADERS 偏移量，**后面的段从这里开始组装**。==**后面的我们熟悉的. pit 段、. text 段和. rodata 段)，这些段都被组装到 TextSegment 中。**
==**每个段的描述格式都是“段名：{组成}"**==，例如. plt:{*(. plt)*(. iplt)}, ==左边表示链接生成的文件的. pit 段，右边表示所有目标文件的. pit 段和. iplt 段==，意思是链接生成的文件的. pit 段由各目标文件的. pit 段和. iplt 段组成。



==**组装完 TextSegment== 之后又给当前链接地址赋了新值，从新的虚拟地址开始组装 DataSegment：**
![[Pasted image 20240607090920.png]]
==计算 DataSegment 的起始地址要做一系列对齐操作，可以结合图 17.2 来理解==，DataSegment 从 TextSegment 的下一个页面开始，并且不是从该页面的起始地址开始，而是有一个偏移量



**==组装完 DataSegment 之后**==又给当前链接地址赋了新值，**从新的虚拟地址==开始组装调试信息等其他 Segment==：**
![[Pasted image 20240607091106.png]]



从现在开始我们写的很多程序都是由多个.c 文件编译链接在一起的，在 gdb 调试时如何指定某个.c 文件中的某一行代码呢？现在我们调试这个程序，在 push 函数和 pop 函数里设断点，注意 gdb 命令的写法。
![[Pasted image 20240607091619.png]]
![[Pasted image 20240607091639.png]]
**在 gdb 命令中指定某个. c 文件中的某一行或某个函数，可以用“文件名: 行号”或 “文件名: 函数名”的语法。**
## 定义和声明
### extern 和 static 关键字 
如果我**想在 main. c 中直接访问 stack. c 中定义的变量 top, 可以用 extern 声明它：**
**extern int top; 只是一个声**明而不是定义，因为它不在 main. c 中分配存储空间,而是在 stack. c 中定义和分配存储空间

变量声明如果不写 extern 意思就完全变了，**如果上面的例子不写 extern 就表示在 main 函数中定义一个局部变量 top**。函数声明中的 extern 关键字也可以省略不写。

,但是从实现 stack. c 这个模块的角度来看，top 这个变量是不希望被外界访问到的，变量 top 和 stack 都属于这个模块的内部状态，外界应该只允许通过 push、p 印函数来改变模块的内部状态
**怎么才能阻止外界访问 top 和 stack 呢**？答案就是用 static 关键字把它们声明为 Internal Linkage 的：
**这样, 即使在 main. c 中用 extern 声明也访问不到 stack. c 的变量 top 和 stack, 从而保护了 stackc 模块的内部状态，这也是一种封装。**
### 头文件 
对于用**角括号**包含的头文件，gcc 首先查找选项指定的目录，然后查找系统的头文件目录 
用**引号**包含的头文件，gcc 首先查找正在被处理的 \ #include 指示所在的当前文件所在的目录，**然后查找-I 选项指定的目录**，然后查找系统的头文件目录。

如：
假如三个代码文件都放在当前目录下：
![[Pasted image 20240607181729.png]]
用 gcc-c main. c 编译，gcc 会自动在 main. c 所在的目录中找到 stack.h
假如把 stack. h 移到一个子目录下：
![[Pasted image 20240607181834.png]]
则需要**用 gcc-c main.c-Istack** 编译，用选项告诉 gcc 头文件要到子目录 stack 里找

**在 # include 预处理指示中可以使用相对路径**，例如把上面的代码改成 # include "stack/stack.h"。**那么编译时就不需要加-Istack 选项了**. gcc 会自动在 main. c 所在的目录中查找，**而头文件相对于 main. c 所在目录的相对路径正是 stack/stack.h**

-I选项可以指定相对路径也可以指定绝对路径，**如果指定相对路径，它是相对于 gcc 进程的当前工作目录的路径**，而不是相对于正在被处理的 # include 指示所在的当前文件的路径。





 ==\# iftidef STACK_H 和 # endif , 意思是说，**如果 STACK_H 这个宏没有定义过，那么从 # iftidef 到 # endif 之间的代码就包含在预处理的输由结果中，否则这一段代码就不出现在预处理的输出结果中。**==
 ==**重复包含头文件主要有以下问题**：==
 1.预处理和编译的速度变慢
2.如果不小心出现 foo. h 包含 bar. h、bar. h 又包含 fbo. h 的情况，就陷入死循环
3.头文件里有些代码不允许重复出现，虽然变量和函数允许多次声明（只要不是多次定义就行），但头文件里有些代码是不允许多次出现的，比如用 typedef 定义一个类型名，在一个编译单元中只允许定义一次。

应遵循以下原则：
.C 文件中可以有变量或函数定义，而. h 文件中应该只有变量或函数声明而没有定义。
.不要把一个. c 文件包含到另一个. c 文件中
### 定义和声明的详细规则 
例如在一个编译单元中在文件作用域两次声明同一个函数
![[Pasted image 20240607094237.png]]
则这里的 extern 修饰的标识符 f 具有 InteranlLinkage 而不是 External Linkage
从表 19.1 的前两行可以总结出我们先前所说的规则——函数声明中的 extern 关键字可以省略不写


变量声明的规则要复杂一些
....
## 静态库
这些文件的目录结构是：
![[Pasted image 20240607094644.png]]
我们把 stack. c、push. c、pop. c、is_empty. c 编译成目标文件：
![[Pasted image 20240607094654.png]]
然后打包成一个静态库 libstack. a：
![[Pasted image 20240607094725.png]]
==库文件名都是以 lib 开头的，静态库以. a 作为后缀==
**ar 命令**类似于 tar 命令，也是用来打包的，但是把目标文件打包成静态库的格式只能用 ar 命令而不能用 tar 命令。
**选项 r** 表示将后面的目标文件列表添加到文件包 libstack.a, **选项 s** 表示为静态库创建索引，这个索引被链接器使用

**ranlib 命令也可以为静态库创建索引**，以上命令等价于：
![[Pasted image 20240607095446.png]]
**然后我们把 iibstack.a 和 main. c 编译链接在一起：**
![[Pasted image 20240607095509.png]]
**-L 选项告诉编译器去哪里找需要的库文件**，・L.表示在当前目录找
**-lstack 选项告诉编译器要链接 libstack 库,-I 选项告诉编译器去哪里找头文件**

在处理-Istack选项时，gcc首先到-L选项指定的目录下查找，首先看有没有共享库libstacks。，如果有就链接它，否则再找有没有静态库libstack.a,如果有就链接它，如果还是没有，就到默认搜索路径下按同样的步骤查找
gcc 在链接时优先考虑共享库，其次才是静态库，如果希望 gcc 只考虑静态库，可以指定-static 选项。

**那么链接共享库和链接静态库有什么区别呢**？
链接 libc 共享库时，链接器只是确认可执行文件 main 引用的某些符号在 libc 中有定义，并没有最终确定这些符号的地址，这些符号在可执行文件 main 中仍然是未定义符号，要在运行时做动态链接
而链接静态库时，链接器会把静态库中的目标文件取出来和可执行文件真正链接在一起


这是使用静态库的一个好处，**链接器从静态库中只取出需要的目标文件呈做链接，不需要的目标文件可以不链接**

如果直接把那些目标文件和 main. c 编译链接在一起：
![[Pasted image 20240607100751.png]]
则没有用到的函数也会链接进来

使用静态库的另一个好处是只需写一个库文件名，而不需要写一长串目标文件名。
## 共享库

### 编译链接运行
**组成共享库的目标文件和一般的目标文件有所不同**，在编译时要加-fPIC 选项，
![[Pasted image 20240607101041.png]]
**-f 后面跟一些编译选项，PIC 是其中一种，表示生成位置无关代码**
那么用**-fPIC 生成的目标文件和一般的目标文件有什么不同呢**？

**我们先不加-fPIC 选项编译生成目标文件：**
![[Pasted image 20240607102742.png]]
**用objdump-dS 把反汇编指令和源代码穿插起来分析**，**所以用-g 选项加调试信息**
注意，**必须在编译每个目标文件时加-g 选项，而不能只在最后链接时加-g 选项**
反汇编查看 push. o：
![[Pasted image 20240612141739.png]]
![[Pasted image 20240612141834.png]]
指令中凡是用到 **stack 和 top 的地址都用 0 x 0 表示**，准备在重定位时修改。
再看 readelf 输出的. rel.text 段的信息：
![[Pasted image 20240612141943.png]]
标出了指令中有**四处需要在重定位时修改**


再看 readelf 输出的. reLtext 段的信息：
![[Pasted image 20240612142622.png]]
**标出了指令中有四处需要在重定位时修改**，
编译**链接成可执行文件之后再做反汇编**分析，
![[Pasted image 20240612142701.png]]
![[Pasted image 20240612142714.png]]
原来指令中的0x0被改成了0x804a010和0x804a04


**看看用-fPIC 选项编译生成的目标文件有什么不同：**
![[Pasted image 20240612142921.png]]
指令中用到的 stack 和 top 的地址**不再以0x0表示，而是以0x0(%ebx)表示**

再看 readelf 输出的. reLtext 段的信息:
![[Pasted image 20240612143012.png]]
我们先编译生成共享库再做反 汇编分析

指令中的**0x0(%ebx)被修改成-0xc(%ebx)和-0x8(%ebx),而不是修改成绝对地址。所以共享库各段的加载地址并没有定死，可以加载到任意位置**

没有使用绝对地址，只要根据实际的加载情况修改 ebx 就可以了，**这就是位置无关代码的特点**

**top 和 stack 的绝对地址保存在一个地址表中，而指令通过地址表做间接寻址，可以避免将绝对地址写死在指令中**
![[Pasted image 20240612143732.png]]




现在把 mainx 和共享库编译链接在一起
![[Pasted image 20240612145739.png]]
由于指定了・L.选项，编译器可以在当前目录下找到 libstack. so, ==而运行时却说找不到 libstack. so。**那么运行时在哪些路径下找共享库呢**？==


先用 **Idd 命令查看可执行文件依赖于哪些共享库：**
![[Pasted image 20240612150146.png]]
 gcc 调动 Id 做链接时用-dynamic-linker /lib/ld-linux. so. 2 选项指定动态链接器的路径

另外一个选项-lc 只说明需要链接 libc 库，却没有指出 libc 库的完整路径，-Istack 也是如此，**共享库的路径需要在运行时由动态链接器/lib/ld-linux. so.2去查找**


linux-gate. so. l'这个共享库文件其实并不存在，它是由内核虚拟出来的，所以没有对应的路径。linux-gate. so. l 负责处理一些特殊的系统调用

从 ld.so (8)可以查到**共享库路径的搜索顺序**：
1. 首先在环境变量 LD_LIBRARY_PATH 保存的路径中查找。
2. 2. 然后从缓存文件/etc/ld. so. cache 中查找。这个缓存文件是由 Idconfig 命令读取配置文件/etc/ld. so. conf 生成的，稍后详细解释。
3. 3. 如果上述步骤都找不到，则到默认的系统库文件目录中查找，先是/lib 然后是/usr/libo 先试试第一种方法，在运行程序时设置环境变量 LD_LIBRARY__PATH 把 libstackso 共享库所在的目录添加到搜索路径：$LD_LIBRARY_PATH=/home/akaedu/testdir ./main

先试试**第一种方法**，在运行程序时设置环**境变量 LD_LIBRARY__PATH 把 libstack.so 共享库所在的目录添加到搜索路径**：
![[Pasted image 20240612152131.png]]
这种方法只适合在开发调试中临时用一下,**设置环境变量 LD_LIBRARY_PATH 通常是不推荐的**
==环境变量==(EnvironmentVariable)是**进程运行时保存在内存中的一组字符串**，每个字符串都是"**key=value** 这样的形式，key 是变量名，value 是变量的值。
上面这条命令告诉 Shell,在创建进程 main 时传给它一个环境变量 LD_LIBRARY_PATH=/home/akaedu/testdir。也可以用这样两条命令：
![[Pasted image 20240612152319.png]]
第一条命令在**当前 Shell 进程中设置一个环境变量** LD_LIBRARY_PATH=/home/akaedu/testdir,―旦在 Shell 进程中设置了环境变量，**以后每次执行命令时 Shell 进程都会把自己的环境变量传给新创建的进程**，所以第二条命令创建的进程 main 就会获得这个环境变量
上面的 LD_LIBRARY_PATH=/home/akaedu/testdir./main 命令表示**只有当前创建的 main 进程才获得这个环境变量**，Shell 进程本身不保存这个环境变量，以后执行的其他命令也不会获得它。


**第二种方法**，这是最常用的方法。把 libstack. so 所在目录的绝对路径 (比如 /home/akaedu/testdir)**添加到配置文件**/etc/ld.so.conf (该文件中每个路径占一行)，然后运行 Idconfig：
![[Pasted image 20240612152844.png]]
第三种方法就是把 libstack. so 拷到/usr/lib 或/lib 目录, 这样可以确保动态链接器能找到这个共享库。
第四种方法，在链接生成可执行文件时就把 libstack. so 的路径写到文件中：
![[Pasted image 20240612152954.png]]
注意选项 ![[Pasted image 20240612153047.png]]
-Wl 表示 gCC 传给链接器的选项，在这个例子中传给链接器的选项是・rpath/home/akaedu/testdir.可以看到 **readelf 输出的. dynamic 段的信息中多了一条 rpath 记录：**
![[Pasted image 20240612153232.png]]
还可以看出，可执行文件运行时需要哪些共享库也都记录在. dynamic 段中。当然 **rpath 这种办法也是不推荐的**，把共享库的搜索路径写到可执行文件中也是一种**硬编码**的做法。
### 函数的动态链接过程  
**在 main.c 中调用共享库的函数 push 是怎样一个过程**。用 gcc main.c-g -L. -Istack-Istack -o main 命令行编译，然后反汇编查看可执行文件 main：

和链接静态库的情况不同，**push 函数的指令没有链接到可执行文件中，而且 call 80483fc< push@plt >这条指令调用的也不是 push 函数的地址，而是.pit 段里的地址**
**.pit 段里保存的也是指令，和.text 一起合并到 Text Segmento** 
那么地址0x80483fb 处的三条指令和 push 函数是什么关系？通过这三条指令能最终调用到 push 函数吗？我们用 gdb 跟踪一下：
....

### 共享库的命名规则 
每个共享库有三个文件名：realname、soname 和 linkername

soname 是符号链接的名字，**只包含共享库的主版本号**，**主版本号一致即可保证库函数的接口一致，可执行文件的. dynamic 段只记录共享库的 soname**, 动态链接器只要找到 soname 一致的共享库就可以加载它做动态链接。例如上面的 **libcap. so. 2 其实是指向 libcap. so.2.17 的符号链接**，这说明**主版本号是 2, 次版本号是1**

注意 **libc** 的版本编号有一点特殊，libc-2.11.1.so 的主版本号是 6 而不是 2 或 2.11, 这也是由于历史原因，Linux 曾经用过另外一套 libc 的实现，后来才改用 glibc, 但主版本号仍沿用了原来的。
另外，**动态链接器**的 soname 也很特殊，叫 **ld**-linux.so. 2, 它指向 ld-2.11.1.so。
...
##  虚拟内存管理 
操作系统利用体系结构提供的 VA 到 PA 的转换机制实现虚拟内存管理机制
例子
![[Pasted image 20240612161847.png]]

用 **ps 命令查看当前终端下的进程**，得知 bash 进程的 id 是 1549, 然后**用 cat/proc/1549/maps 命令查看它的虚拟地址空间**

**/proc 目录下的文件并不是真正的磁盘文件**，而是由内核虚拟出来的，当前**运行的每个进程在/proc 下都有一个子目录，目录名就是进程的 id,** 查看子目录下的文件可以得到该进程的相关信息。**比如/proc/进程号/maps 文件是进程地址空间的信息**，当用户敲 cat 命令查看 maps 文件时，内核将该进程地址空间的信息按上面的格式打印输出，就**好像**这些信息保存在 maps 文件中一样如图19.4所示 ![[Pasted image 20240612162044.png]]...

# 预处理 
## 宏定义
“较大的项目都会用大量的宏定义来组织代码”

### 函数式宏定义
变量式宏定义
另外一种宏定义可以像函数调用一样在代码中使用，称为函数式宏定义
![[Pasted image 20240607104525.png]]

我们想看表达式展开成什么样，可以用 gcc 的正选项或 cpp 命令
![[Pasted image 20240220164954.png]]
注意这种**函数式宏定义和真正的函数调用之间的区别：**




尽管函数式宏定义和真正的函数相比有很多缺点，**但只要小心使用还是会显著提高代码的执行效率，毕竟==省去了分配和释放栈帧、传参、传返回值等一系列工作==**，**==一般来说简短的、被频繁调用的函数适合用函数式宏定义来代替实现==**。


函数式宏定义经常写成这样的形式
![[Pasted image 20240607105243.png]]


==为什么要用 do{...}while (0)括起来呢==
假如这样定义和使用函数式宏定义：
![[Pasted image 20240612164737.png]]
**则宏展开之后函数体的第二条语句不在 if 条件中**
**用{…}括起来组成一个语句块不行吗？**
![[Pasted image 20240612164907.png]]
问题出在加 vice_init_wakeup (d, v); 末尾的;号
展开之后的形式是 if ()**{};** else...
用 do{..}while (0)是一种比较好的解决办法，展开之后的形式是 if (...) do{...}while (0); else **其中 do{...}while (0); 就是一条语句**。

### 内联函数
==**inline 关键字告诉编译器，这个函数的调用要尽可能快，可以当普通的函数调用实现，也可以用宏展开的办法实现**==

把上一节的例子改一下
![[Pasted image 20240613085047.png]]
编译然后反汇编:
![[Pasted image 20240613085148.png]]**
![[Pasted image 20240613085116.png]]
**可以看到 MAX 是作为普通函数调用的**。
**如果指定优化选项编译**，然后反汇编:
![[Pasted image 20240613085240.png]]
**没有生成调用 MAX 函数的 call 指令，事实上 MAX 函数并不独立存在，它的指令内联在 max 函数中**
**由于源代码和指令的次序无法对应，max 和 MAX 函数的源代码也交错在一起显示。**

思考一下，inline 函数与函数式宏定义相比有哪些优点？

## \#、\#\# 运算符与可变参数 
==\#号运算符后面应该跟一个形参 ( \#号和形参之间可以有空格或Tab ), 用于**创建字符串字面值**==
![[Pasted image 20240607111337.png]]
==用 cpp 命令预处理之后是"hello-world“==
注意如果实参中包含字符常量或字符串字面值，则宏展开之后字符串的界定符"要替换成\", 字符常量或字符串字面值中的\\和"字符要替换成 `\\` 和\"。

==**用##运算符把前后两个预处理 Token 连接成一个预处理 Token**== 。和 # 号运算符不同， ## 运算符不仅限于函数式宏定义，变量式宏定义也可以用

我们知道 printf 函数带有可变参数，函数式宏定义也可以带可变参数，同样是在参数列表中==**用... 表示可变参数**==
![[Pasted image 20240607111938.png]]
预处理后变为 
![[Pasted image 20240607111955.png]]



==**调用函数式宏定义允许传空参数，这一点和函数调用不同**==
![[Pasted image 20240607112100.png]]
又如
![[Pasted image 20240607112109.png]]
![[Pasted image 20240607112114.png]]

FOO 在定义时带一个参数，在调用时必须传一个参数给它，如果不传参数则表示传了一个空参数。
![[Pasted image 20240607112244.png]]
FOO 在定义时带三个参数，在调用时也必须传三个参数给它，空参数的位置可以空着，**但必须给足三个参数，用两个逗号隔开，FOO (1,2)这样的调用是错误的。**


![[Pasted image 20240607112327.png]]


gcc 有一种扩展语法，==如果##运算符用在_VA_ARGS_前面，除了起连接 Token 的作用之外还有一种特殊用法==
![[Pasted image 20240607112908.png]]
这个函数式宏定义可以这样调用：DEBUGP ("info no.%d", 1). 
也可以这样调用：DEBUGP ("info")  后者相当于可变参数部分传了一个空参数，**但展开之后并不是 printk ("info",), 而是 printk('info"), ==当_VA_ARGS_是空参‘数时, ##  运算符把它前面的逗号吃掉了。==**

### `#undef` 预处理指示
如果需要重新定义一个宏，和原来的定义不同，==可以先用  # undef  取消原来的定义 , 再重新定义==
### 宏展开的步骤 
![[Pasted image 20240607134732.png]]
1. # x 要替换成 "sub_z"。
2. 2. n##x 要替换成 nsub_z。
3. 3. **除了带 # 和 ##运算符的参数之外，其他参数在替换之前要对实参本身做充分展开，所以应该先把 sub_z 展开成 26 再替换到 alt[x]中 x 的位置。**
4. 4. 现在展开成了 printff ("n" "sub_z"=%d, or %d\\n", nsub_z,alt[26]), **所有参数都替换完了，这时编译器会再扫描一遍，再找出可以展开的宏定义来展开，假设 nsub_z 或 alt 是变量式宏定义，这时会进一步展开。**
再举一个例子
![[Pasted image 20240607135056.png]]
1. 先把 g 展开成 f 再替换到 # definet t(a) a 中，得到 t (f (0)+t)(1);。
2. 2. 根据 # define f (a)  f(x*(a)), 得到 t (f (x*(0))+t)(1);。
3. 3. 把 x 替换成 2, 得到 t (f (2*(0))+t)(1);。注意，一开始定义 x 为3, 但是后来用 # undef x 取消了 x 的定义，又重新定义 x 为 2。**当预处理器处理到 t (t (g)(0)+t)(1); 这一行代码时 x 已经定义成 2 了，所以用 2 来替换**。                        **还要注意一点，现在得到的 t (f (2*(0))+t)(1)中仍然有 f, 但不能再次根据 # define f (a ) f (x*(a))展开了，f (2*(0))就是由展开 f (0)得到的，展开的结果中再出现 f(…)就不展开了**，这样规定可以避免无穷展开 (类似于无穷递归)，因此我们可以放心地使用递归定义，例如 # define a a [0], # define a a.member 等。
4. 4. 根据 # define t(a) a 最终展开成 f(2*(0))+t(1);。**这时不能再展开 t(1)了**，因为这里的 t 就是由展开 t (f ( 2 * (0)) +1)得到的，展开的结果中再出现 t (…)就不展开了

## 条件预处理指示
## 其他预处理指令
  \# **pragma 预处理指示供编译器实现一些扩展特性** , C 标准没有规定 # pragma 后面应该写什么以及起什么作用，由编译器自己规定. 有的编译器用 # pragma 定义一些特殊功能寄存器名，有的编译器用 # pragma 定位链接地址
如果编译器在代码中碰到不认识的 # pragma 指示则忽略它

C 标准规定了==**几个特殊的宏**，**不需要定义即可使用**==
==\_FILE_展开成当前源文件的文件名==
==\_LINE_展开成当前代码行的行号==
这两个宏在源代码中不同的地方使用会自动展开成不同的值，显然不是用 # define 能定义得出来的，==它们是编译器内建的特殊宏定义==

自己实现 assert, 以便理解它的工作原理
![[Pasted image 20240613092040.png]]
请结合前面讲过山==宏展开步骤思考一下，为什么不直接定义 # define _STR (x) # x 呢 ==？

\_Assert 函数是我们自己定义的
![[Pasted image 20240613092645.png]]
==定义了一些以一线开头的标识符，例如_STR、\_VAL、\_Assert, 这些标识符是我们的实现**内部使用的，并不打算提供给用用程序榜用**==

**为什么我们不直接在 assert 宏定义中调用 fputs 和 abort 函数呢**？因为 C 标准规定 C 标准库的头文件是相互独立的，用户程序只要包含 assert. h 就应该能使用 assert 宏定义，assert. h 不应该依赖于别的头文件。**如果在 assert. h 中直接调用 fputs 和 abort, 那么用户程序只包含 assert.h 是不够的，还必须同时包含 stdio.h 和 stdlibh 头文件之间就不是独立的了**


**注意 # include asserth 要用引号而不要用角括号，以保证包含的是我们自己写的 assert.h 而非 C 标准库的头文件**

在打印调试信息时除了文件名和行号之外还可以**打印出当前函数名**，==C 99 引入一个特殊标识符**\__func__** 支持这一功能。==**这个标识符应该是一个变量名而不是宏定义，不在预处理阶段求值**

# makefile 基础
## 基本规则
这个例子由例 12.3 改写而成
我们把堆栈和迷宫的代码分别转移到 stack. c 和 maze. c 中, main. c 包含它们提供的头文件 stack.h 和 maze.h

例 12.3 代码中的堆栈规定死了只能放 char 型数据，现在我们做进一步抽象，堆栈中放 item_t 类型的数据，item_t可以定义为任意类型
要改变它的定义只需改变 main. h 中的一行代码。
> 注意 print_maze 函数的声明可以不加 extern, 而 **maze 数组的声明必须加 extern**


这些源文件可以这样编译链接在一起：
![[Pasted image 20240603162013.png]]
但这不是个好办法，如果编译之后又对 maze. c 做了修改，**又要把所有源文件编译一遍**
**这样编译也许更好一些**：
![[Pasted image 20240603162111.png]]
如果编译之后又对 maze. c 做了修改，只需重新编译 maze. c, 然后和原来编译好的 main. o、stack.o 做链接
这样又有一个问题，每次编译敲的命令都不一样，很容易出错
更复杂的问题是，假如**我改了 main. h 怎么办？所有包含 main. h 的源文件都需要重新编译，我得挨个找哪些源文件包含了 main. h**

**可见手动处理这些问题非常容易出错，那有没有自动的解决办法呢？有，就是写==一个 Makefile 文件和源代码放在同一个目录下==：**
![[Pasted image 20240603162320.png]]
main 是这条规则的目标 (Target), main. o、stack. o 和 maze. o 是这条规则的条件 (Prerequisite). **目标和条件之间的关系是：欲更新目标，必须先更新它的所有条件；所有条件中只要有一个条件被更新了. 目标也必须随之被更新**。
所谓“更新”就是执行一遍规则中的命令列表

对于上面这个例子，make 执行如下步骤：
1. 尝试更新 Makefile 中第一条规则的目标 main, 第一条规则的目标称为缺省目标，只要缺省目标更新了就算完成任务了，其他工作都是为这个目标而做的。由于我们是第一次编译，main 文件还没生成，显然需要更新，**但规则说必须先更新了 main. o、stack. o 和 maze. o 这三个条件，然后才能更新 main.** 
2. 2. ==所以 make 会进一步查找以这三个条件为目标的规则，这些目标文件也没有生成, 也需要更新==，所以执行相应的命令 (gcc-c main. c、gcc-c stackc 和 gcc-c maze. c)更新它们。
3. 3. 最后执行 gcc main. o stack. o maze.o-o main 更新 main.

如果**修改了 maze.h (比如加个无关痛痒的空格)再运行 make**：
**make 会自动选择那些受影响的源文件重新编译，不受影响的源文件则不重新编译，这是怎么做到的呢**？在这种情况下 make 的处理步骤是：
1. 检查目标 main 是否需要更新，由于它依赖于三个条件，因此要先检查 main.o、stack. o 和 maze. o 这三个条件是否需要更新。
2. 2. make 进一步查找以这三个条件为目标的规则，然后**发现 main. o 和 maze.o需要更新，因为它们都有一个条件是 maze. h**, 而**这个文件的修改时间比 main. o 和 maze. o 晚，所以执行相应的命令更新 main. o 和 maze. o。**
3. 3. 既然 main 的三个条件中有两个被更新过了，那么 **main 也需要更新**，所以执行命令 gcc main. os tack.o maze.o-omain 更新 main。


**通常 Makefile 都会有一个 clean 规则，用于清除编译过程中产生的二进制文件**，保留源文件：
![[Pasted image 20240603163422.png]]
clean 目标不依赖于任何条件

在这个例子中还演示了命令前面加@和-字符的效果：
如果 make 执打的命令前面**加了@字符**（AtSign）, 则**不显示命令本身而只显示它的输出结果**
**通常 make 执行的命令如果出错（该命令的退出状态非 0）就立刻终止**，不再执行后续命令，**但如果命令前面加了-字符**（Hyphen）, 即使这条命令出错，make 也会继续执行后续命令
**通常 rm 命令和 mkdir 命令前面要加上-字符，因为 rm 要删除的文件可能不存在**


如果存在 clean 这个文件，clean 目标又不依赖于任何条件，make 就认为它不需要重新了。而我们希望把 clean 当做一个特殊的名字使用，==不管 clean 文件存在不存在都要更新 clean 目标，可以添加一条特殊规则，把 clean 声明成一个伪目标：==
![[Pasted image 20240603164310.png]]
**这条规则没有命令列表。类似. PHONY 这种 make 内建的特殊目标还有很多**
在 C 语言中要求变量和函数先声明后使用，而 Makefile 不太一样，**这条规则写在 clean: 规则的后面也行，也能起到声明 clean 是伪目标的作用**
![[Pasted image 20240603164428.png]]




**==gcc 处理一个 C 程序分为预处理和编译两个阶段，类似地, make 处理 Makefile 的过程也分为两个阶段==**：
	.1.从前到后读取所有规则，建立起完整的依赖关系图，如图 21.1 所示。
	![[Pasted image 20240603164714.png]]
	.2从缺省目标或者命令行指定的目标开始，根据依赖关系图选择适当的规则执行

clean 目标是一个约定俗成的名字.**类似这样的约定俗成的目标名字有**
•all, 执行主要的编译工作，通常用作**缺省**目标。
•install, 执行编译后的安装工作，把可执行文件、配置文件、文档等分别拷贝到不同的安装目录。
•clean, 删除编译生成的二进制文件。
•distclean, 不仅删除编译生成的二进制文件，也删除其他的生成文件，比如内核源代码 makemenuconfig 配置之后会生成. config 文件, 一些文档源文件（比如本书的 Docbook 源文件）经过 make 之后会转换生成 HTML 或 PDF 文件，执行 makedistclean 应该清除所有的生成文件，只留下源文件。
## 隐含规则和模式规则
Makefile 有很多灵活的写法，可以写得更简洁

一个目标依赖的所有条件不一定非得写在一条规则中，也可以拆开写
![[Pasted image 20240613100409.png]]
相当于 
![[Pasted image 20240613100426.png]] 
如果一个目标拆开写多条规则，其中只有一条规则允许有命令列表，其他规则应该没有命令列表，否则 make 会报警告并且采用最后一条规则的命令列表。

我们的例子可以改写成
![[Pasted image 20240613102547.png]]
**这不是比原来更繁琐了吗？现在可以把提出来的三条规则删去，写成**：
![[Pasted image 20240613102603.png]]
**可是现在 main. o、stack. o 和 maze. o 这三个目标连编译命令都没有了，怎么编译呢？试试看：**
![[Pasted image 20240613102715.png]]
**前三条编译命令是怎么来的**？**如果一个目标在 Makefile 中的所有规则都没有命令列表，make 会尝试在内建的隐含规则 (ImplicitRule)中查找适用的规则**
**用 make-p 命令可以查看所有这些规则和变量定义**

从 make-p 命令的输出可以看到，在我们这个例子中起作用的隐含规则及变量定义有：
![[Pasted image 20240613103640.png]]
\# 号在 Makefile 中表示单行注释
**CC=cc 定义一个变量 CC 并给它赋值**，Makefile 变量就像环境变量或者 C 语言的宏定义一样，代表一串字符 (或者空字符串)

**变量名加上括号和 \$符**(DollarSign)写成$ (CC)**表示将变量 CC 的值展开**
在 Linux 系统上 cc 是指向 gcc 的符号链接，在其他 UNIX 系统上 cc 可能指向另外一种 C 编译器。
![[Pasted image 20240613103011.png]]

CFLAGS 这个变量没有定义，\$(CFLAGS)展开是空，CPPFLAGS 和 TARGET_ARCH 也是如此。**这样\$( COMPILE. c)展开** 应该是 cc\_空_空_空_-c，去掉所有的空得到        cc_-c,注意中间留下了4个空格，所以%.o:%.c **规则的命令 \$( COMPILE. c) \$(OUTPUT_OPTION)_$ <展开之后是  cc\_-c\_-o\_\$@\_\$ <和编译命令 cc\_-c\_-o\_main. o main.c 已经很接近了。**

\$@和\$ <是两个**特殊的变量**
**\$@的取值是当前规则中的目标，\$ <的取值是当前规则中的第一个条件**

%. o:%. c 是一种**特殊的规则**，称为**模式规则** (PatternRule)

在我们的 Makefle 中以 **main. o**为目标的规则都没有命令列表，所以 make 会查找隐含规则，发现隐含规则中有这样一条模式规则适用，main. o 符合％. o的模式，现在％就代表 main (称为 main. o 这个名字的 Stem), 替换到％.c 中就是 main。**所以这条模式规则相当于**：
![[Pasted image 20240613103143.png]]


**先前我们写 Makefile 都是以目标为中心，一个目标依赖于若干条件，现在换个角度，以条件为中心，Makefile 还可以这么写**：
![[Pasted image 20240613110759.png]]
对于多目标的规则，make 会拆成几条单目标的规则来处理，例如：
![[Pasted image 20240613110915.png]]
**相当于**： 
![[Pasted image 20240613110839.png]]
## 变量
## 自动处理头文件的依赖关系
## 常用的 make 命令行选项
# 函数接口
Man Page
现在我们来分析 strcpy (3)。
![[Pasted image 20240220170201.png]]


![[Pasted image 20240531072032.png]]
**malloc 函数不知道用户拿到这块内存要存放什么类型的数据，所以返回通用指针 void\***
![[Pasted image 20240531072112.png]]

## 传入参数与传出参数 
把指针所指向的数据传给函数使用（称为传入参数，如表 23.1 所示），也可以由函数填充指针所指的内存空间，传回给调用者使用（称为传出参数，如表 23.2 所示）
如：strcpy 的 src 参数是传入参数，dest 参数是传出参数。**有些函数的指针参数同时充当这两种角色**，如 select 的 fd_set\*参数，==x `==，如表23.3所示。
![[Pasted image 20240531072811.png]]
![[Pasted image 20240531072818.png]]
![[Pasted image 20240531073308.png]]
==由于传出参数和 Value-result 参数的函数接口完全相同，应该在文档中说明是哪种参数==
## 两层指针的参数 

==两层指针也是指针, 同样可以表示传入参数、传出参数或者Value-result参数, 只不过该参数所指的内存空间应该解释成指针变量==
![[Pasted image 20240531073515.png]]
**有 const 限定符，却不是传入参数而是传出参数，为什么？**
**如果是传入参数应该怎么表示？**
![[Pasted image 20240531113242.png]]



==两层指针作为传出参数还有一种特别的用法，可以**在函数中分配内存==**
==调用者通过传出参数取得指向该内存的指针==
![[Pasted image 20240531132558.png]]
![[Pasted image 20240531132615.png]]
为什么在 main 函数中不能直接调用分 free (p)释放内存，而要调用 free_unit (p)? 为什么一层指针的函数接口 void alloc_unit (unit_t \*p); 不能分配内存，而一定要用两层指针的函数接口？



总结一下，**两层指针参数如果是传出的，可以有两种情况**：==第一种情况，传出的指针指向静态内存 (比如上面的例子)，或者指向已分配的动态内存 (比如指向某个链表的节点)==；第二种情况是==在函数中动态分配内存，然后传出的指针指向这块内存空间==，这种情况下调用者应该在使用内存之后调用释放内存的函数，调用者的责任是请求分配和释放内存，实现者的责任是完成分配和释放内存的操作。由于这两种情况的函数接口相同，应该在函数的文档中说明是哪一种情况。??????
## 返回值是指针的情况 
**返回值传出的是指针也分为两种情况**：==一种是传出指向静态内存或已分配的动==
==态内存的指针, 第二种是在函数中动态分配内存并传出指向这块内存的指针==，
![[Pasted image 20240531075045.png]]
**==通过参数分配内存需要两层的指针，而通过返回值分配内存就只需要返回一层的指针，为什么？==**(和上面双层指针的例子做对比)
## 回调函数
参数是一个函数指针，调用者可以传递一个函数的地址给实现者，即**调用者提供一个函数但自己不去调用它，而是让实现者去调用它**，这称为回调函数
![[Pasted image 20240603084445.png]]
![[Pasted image 20240603084502.png]]

**前面几节的例子，参数类型都是由实现者规定的。而本例中回调函数的参数按什么类型解释由调用者规定**
**对于实现者来说就是一个 void\*指针，实现者只负责将这个指针转交给回调函数，而不关心它到底指向什么数据类型**


max 函数可以在任意一组对象中找出最大值，可以是一组 int、一组 char 或一组结构体，但是实现者并不知道怎样去比较两个对象的大小，**需要调用者再提供一个做比较操作的回调函数**。
![[Pasted image 20240603090000.png]]
![[Pasted image 20240603090037.png]]
**cmp 是调用者提供的回调函数，调用者当然知道对象是什么类型以及如何比较。**


**==以上举例的回调函数都是被同步调用的，调用者调用 max 函数，max 函数则调用 cmp 函数，相当于调用者间接调用了自己提供的回调函数**。==

除此之外，**异==步调用也是回调函数的一种典型用法，调用者首先将回调函数传给实现者，实现者记住这个函数，这称为注册一个回调函数，然后当某个事件发生时实现者再调用先前注册过的函数**==。以下是一个代码框架。???
![[Pasted image 20240603090630.png]]
![[Pasted image 20240603090650.png]]
**既然参数可以是函数指针，返回值同样也可以是函数指针，因此可以有 func ()() 这样的调用**。返回函数指针的函数在 C 语言中很少见

[[../已归类卡/回调函数]]
## 可变参数 
可变参数的函数 printf：
![[Pasted image 20240603090835.png]]
**要处理可变参数，需要用到 C 标准库的 va_list 类型和 va__start、va__arg、va_end 宏**，这些定义在 stdarg.h 头文件中

**宏是如何取出可变参数的呢**
首先对照反汇编分析在调用 myprintf 函数时这些参数的内存布局
...
# 指针
我们讲过全局变量只能用常量表达式来初始化，然而用 i 的地址来初始化一个指针却没有错。因为 i 的地址是在编译链接时确定的，不需要到运行时才知道，&i 是常量表达式。

[]括号用在声明中表示声明一个数组，用在表达式中是取下标运算符。同样道理，\*号用在声明中表示声明一个指针类型，用在表达式中是间接寻址运算符。
，==pi 是 int\*型的，pc 是 char\*型的，pi=pc; 这样赋值就是错误的。但是可以先强制类型转换然后赋值==
![[Pasted image 20240221132053.png]]
==通过*pc 只能访问到一个字节，而通过*pi 可以访问到 4 个字节==
“
在栈上分配的变量初始值是不确定的，也就是说指针 P 所指向的内存地址是不确定的，后面用*P 访问不确定的地址会导致不确定的后果为避免出现野指针，**在定义指针变量时就应该明确地给它赋初值**，或者把它初始化成 NULL：”

NULL 在 C 标准库的头文件 stddef. h 中定义:
![[Pasted image 20240221132504.png]]
指针也是一种标量类型，可以用 0 运算符做强制类型转换，其他标量类型可以转成指针类型，指针类型也可以转成其他标量类型

**操作系统不会把任何数据保存在地址 0 及其附近, 也不会把地址 0〜Oxfff 的页面映射到物理内存**，所以任何对 0 地址的访问（比如上面的\*p=0;）一定会引发段错误
由于指针是标量类型，因此可以做逻辑与、或、非运算的操作数和 if、for, while 的控制表达式

**void\***类型了。在编程时经常需要一种**通用指针**
**可以转换成任意其他类型的指针，任意其他类型的指针也可以转换成通用指针**
规定 **void\*指针与其他类型的指针之间可以隐式转换，而不必用 ()运算符强制转换**
只能定义 void\*类型的指针，**而不能定义 void 类型的变量**；因为 void\*指针和别的指针一样都占 4 个字节，而如果定义 void 型变量（即类型不确定的变量），编译器不知道该给这个变量分配几个字节
同样道理，void\*指针不能直接 Derefrence, **而必须先转换成别的类型的指针再做 Dereference**, 
==**void\*指针常用于函数传参和传返回值**==
## 指针类型的参数和返回值
![[Pasted image 20240221134036.png]]
“return px;语句相当于定义一个临时变量并且用 px 初始化：”
![[Pasted image 20240221133501.png]]

==函数返回值传指针有一种常见的错误==
![[Pasted image 20240221134007.png]]
f==oo 函数的返回值是一个指向局部变量 a 的指针==，可是 foo 函数返回之后它的栈帧就要释放掉，要这个指针还有什么用呢？这其实也是一种野指针
上面的代码错得比较明显，编译器会报警告 warning: 
fimctionreturnsaddressoflocalvariable, 有时候错得不那么明显，例如：
![[Pasted image 20240221133954.png]]
“编译器是不会报警告的，这就需要程序员自己多加小心了”
## 指针与数组
![[Pasted image 20240221141007.png]]
==pa++让 pa 指向下一个数组元素 a[l]==
==pa++使 pa 里保存的地址值加 4 而不是加1。==

E 1[E 2]这种写法和 (\*((E 1)+(E 2)))是等价的，\*(pa+2)也可以写成 pa[2],

表达式 pa \[-1]或者写成*(pa-1)是合法的

只有指向同一个数组中元素的指针之间相互比较才有意义，也只有指向数组元素的指针加或减一个常数才有意义，否则都是 Undefined


数组类型做右值时和指针的语法是统一的，但如果把数组类型做左值使用，和指针就有区别了.例如++pa 是合法的，但++a 就不合法，pa=a+1 是合法的，但 a=pa+l 就不合法
数组类型做左值时表示整个数组的存储空间
**数组类型做左值支持&运算符，所以&a 是合法的，这个表达式的类型是指向数组的指针**
## 指针与 const 限定符
“const 限定符和指针结合起来常见的情况有以下几种。”
- 
![[Pasted image 20240221134323.png]]
a 是一个指向 const int 型的指针, ==a 所指向的内存单元不可改写==，
但指针 a 本身可以改写


- 指针类型声明的\*号后面加 const 
- ![[Pasted image 20240221134344.png]]
a 是一个指向 int 型的 const 指针，\*a 是可以改写的，但 ==a 本身不允许改写==。


- 指针类型声明的\*号前后都加 const
指针 p 赋给指针 q,应注意 const 限定符的语义作用：


- c 指向的类型不带有 const 限定，而 q 指向的类型带有 const 限定
![[Pasted image 20240221142131.png]]
==可以赋值，赋值后\*q 不允许改写，即不能通过指针 c 来改写变量 c 的值。==


- 如果 p 指向的类型带有 const 限定，而 q 指向的类型不带有 const 限定,==则不能把 p 赋给 q==
![[Pasted image 20240221142103.png]]
**表达式&c 是 const char\*型的**
，假如允许赋值，则赋值后就可以通过指针 q 来改写变量 c 的值，等于绕过了变量 c 的 const 限定这道防线，这是很危险的，如果变量 c 被分配在. rodata 段，改写它会导致段错误，因此编译器不允许这样赋值。

==在指针赋值过程中 volatile 和 restrict 限定符也有和 const 限定符类似的作用==
==**要想把指针 p 赋给指针 q, q 指向的类型应该比 p 指向的类型限定得更严格, 或至少是同样严格, 而不能比 p 指向的类型限定得更松**==




即使不用 const 限定符也能写出功能正确的程序，但良好的编程习惯应该尽量使用 const 限定符，理由是：
	const 给读代码的人传达非常有用的信息。比如一**个函数的形参是 const char* 指针，你在调用这个函数时就可以放心地传给它 char *或 const char *指针，而不必担心指针所指的内存单元被改写**，因为该函数无法通过它的形参改写你传给它的内存单元。
	把程序中不该变的变量都加上 const 限定符，可以依靠编译器检查程序的 Bug, 防止运行时意外改写了不该变的数据
	const 对编译器优化是一个有用的提示，编译器也许会把 const 变量优化成常量


字符串中的元素是 char 型的，因此指向首元素的指针应该是 char\*型。改写字符串字面值中的元素会怎么样呢
![[Pasted image 20240221142556.png]]
这样可以绕过编译器的检查，在编译时不报错，但在运行时却出现段错误
**gcc 把这种字符串字面值分配在. rodata 段，在运行时. rodata 段加载到 Text Segment, 操作系统会保护 TextSegment 不被改写，因此改写它会==导致段错误**==
按照 C 标准，==字符串字面值做右值时自动转换成 char\*指针，但在 gcc 的实现中字符串字面值是只读的，**因此字符串字面值做右值时看作 const char•指针==。**


我们知道 printf 函数原型的第一个参数是 const char *型, 可以把 char *或 const char\* 。所以下面这些调用都是合法的：![[Pasted image 20240221142850.png]]
“**注意上面的 printf(p)和 printf(str2)调用在编译时会报警告**”
编译器认为用 printf (p)这种形式打印一个字符串是危险的，因为字符串中可能包含％号而被 printf 当成转换说明，printf 并不知道后面没有传其他参数，照样会从栈帧上取参数从而造成非法内存访问。比较保, 险的写法是 printf (“%s”, p)。
## 指针与结构体
![[Pasted image 20240221143220.png]]
**==要通过指针 p 访问结构体成员可以写成** (\*p). c 和 (\*p).num==
==**也可以写成 p->c 和 p->num==**
## 指向指针的指针和指针数组
指针也可以指向复合类型，比如**指向另外一个指针类型的变量，这称为指向指针的指针。**
![[Pasted image 20240607140700.png]]


**数组中的每个元素也可以是指针类型**。例如定义一个数组 a 由 10 个元素组成，每个元素都是 int\*指针：**称为指针数组**
![[Pasted image 20240607141252.png]]

![[Pasted image 20240607141337.png]]


main 函数的标准原型应该是 int main( int argc, char \*argv[]);
argc 是命令行参数(或者叫命令行选项)的个数。
而 **a==rgv 是一个指向指针的指针，为什么不是指针数组呢？因为前面讲过，函数原型中的[]表示指针而不表示数组**==，等价于 char \*\*argv ==那**为什么要写成 char *argv[]而不写成 char\**argv 呢==**？这样写给读代码的人提供了有用的信息，argv 不是指向单个指针，而是指向一个指针数组的首元素。数组中每个元素都是 char*指针，指向一个命令行参数字符串。

## 指向数组的指针与多维数组
以下定义一个**==指向数组的指针==**，这种数组由 10 个 int 元素组成：
![[Pasted image 20240607141117.png]]



**现在看指向数组的指针如何使用：**
![[Pasted image 20240607143041.png]]
&a[0]表示数组 a 的首元素的首地址，而&a 表示数组 a 的首地址，==虽然这两个地址的数值相同，但这两个表达式的类型是两种不同的指针类型==，**前者的类型是 int\*, 而后者的类型是 int (\*)[10]**

\*pa 就表示 pa 所指向的数组 a,  \*pa 做右值时也会自动转换成指向数组首元素的指针，**所以取数组的 a[0]元素也可以用表达式 (\*pa)[0]**
注意到\*pa 可以写成 pa[0],所以 (*pa)[0]这个表达式可以改写成 pa\[0][0]

分析一下**指向数组的指针和二维数组是什么关系**。
int a\[5][10]; 和 int (\*pa)[10]; 之间的关系同样类似于 int a[10]; 和 int \*pa; 之间的关系：
![[Pasted image 20240607152439.png]]
**==pa 比 a 用起来更灵活,== 数组类型不支持赋值、自增等运算，而指针可以支持, pa++使 pa 跳过二维数组的一行**
## 函数类型与函数指针类型
**函数指针的内存单元里存放的就是函数的入口地址** (位于. text 段)
![[Pasted image 20240607152811.png]]
表达式 say_hello 是一种函数类型
**函数类型**和数组类型相似，**做右值使用时自动转换成函数指针类型**，因此可以直接赋给 f, 也可以写成 void (\*f)(const char\*)=&say_hello




区分函数类型和函数指针类型
定义函数类型 F；
![[Pasted image 20240607152953.png]]
==这种类型的函数不带参数，返回值是 int==。那么可以这样声明 f 和 g：
![[Pasted image 20240607152957.png]]
相当于声明：
![[Pasted image 20240607153006.png]]
==**下面这个函数声明是错误的**：==
![[Pasted image 20240607153019.png]]
不能返回函数类型

==而下面这个函数声明是正确的：==
![[Pasted image 20240607160248.png]]
**函数 e 返回一个 F\*类型的函数指针, 函数指针是标量类型**



![[Pasted image 20240607160503.png]]
**相当于** 
![[Pasted image 20240607160531.png]]
**==现在给这种函数指针起一个类型名叫== FP**：
![[Pasted image 20240607160646.png]]
有一个地址 0 x 12345678 正好是这样一个函数的首地址, **==我们把它强制转换成一个函数指针并调用它==**，以下两种写法皆可：
![[Pasted image 20240607160924.png]]
**不用类型名 FP 也可以写出强制转换运算符**：
![[Pasted image 20240607161012.png]]
![[Pasted image 20240607161028.png]]



**==通过函数指针调用函数和通过函数名直接调用函数相比有什么好处呢==**
由于结构体中多了一个类型字段，需要重新实现 real_part、img__part、magnitude、angle 这些函数
![[Pasted image 20240607161334.png]]
现在类型字段有两种取值，RECTANGULAR 和 POLAR, 每个函数都要用 if... else... 分别处理两种情况。**如果类型字段有三种取值呢**？每个函数都要有 if... elseif... else...»或者 switch... case…。**这样维护代码是不够理想的，现在我用函数指针给出一种实现：**
![[Pasted image 20240607162111.png]]
![[Pasted image 20240607162122.png]]
当调用 reaLpart (z)时，**==用类型字段z.t 做索引，从指针数组 real_part_tbl 中取出相应的函数指针来调用==**，也可以达到 if... else...的效果
**每个函数都只做一件事情**，而不必用 if... else... 兼顾好几件事情。而不必把它们的代码都耦合到一个函数中
**低耦合，高内聚**是程序设计的一条基本原则

==这种实现用数据 (函数指针数组)取代了代码 (if... else...), 和例 8.4 有异曲同工之处，也是应用了 Data-drivenProgramming 的思想。==


## 不完全类型和复杂声明
C 语言的类型分为函数类型、对象类型和不完全类型三大类
对象类型又分为标量类型和非标量类型。==**不完全类型是暂时没有完全定义好的类型**==。如：![[Pasted image 20240607143540.png]]

在同一个编译单元里，==**具有不完全类型的变量可以通过多次声明组合成一个完全类型**==
比如将数组 str 先后声明两次：
![[Pasted image 20240607144028.png]]
当编译器碰到第一个声明时，认为 str 的类型是不完全类型，碰到第二个声明时就组合成完全类型了，**如果编译器处理到编译单元的末尾仍然无法将 str 的类型组合成一个完全类型就会报错。**

另一例子
![[Pasted image 20240607144209.png]]
struct s 和 struct t 各有一个指针成员指向另一种类型。编译器从前到后依次处理，当看到 struct s{struct t \*pt;}; 时, 认为 struct t 是一个不完全类型，==**pt 是一个指向不完全类型的指针，尽管如此，这个指针却是完全类型，因为不管什么指针都占 4 个字节存储空间**，这一点很明确。然后编译器又看到 struct t (structs \*ps; 这时 struct t 有了完整的定义，**就组合成一个完全类型了**==，pt 的类型就组合成一个指向完全类型的指针。由于 street s 在前面有完整的定义，所以 structs \*ps; 也定义了一个指向完全类型的指针。


这样的类型定义是错误的：
![[Pasted image 20240607144834.png]]
这就成了一个无穷递归的定义。


**以上是两个结构体相互引用构成的递归定义**，一个结构体引用自身也可以构成递归定义：
![[Pasted image 20240607145106.png]]







**下面看几个复杂声明**
![[Pasted image 20240607145400.png]]
sighandler_t 是一个函数指针
sighandler_t 类型的参数，返回值也是 sighandlert 类型。**如果把这两行合成一行写**，就是：
![[Pasted image 20240607145449.png]]
==在分析复杂声明时，要借助 typedef 把复杂声明分解成几种基本形式：==
・T \*p;, p 是指向 T 类型的指针。
•T a[];, a 是由 T 类型的元素组成的数组。但有一个例外，在第 22.3 节讲过，如果 a 是函数的形参，则相当于 T\*a;。
・T1 f (T  2, T 3...);, f 是一个函数，参数类型是 T 2、T 3等，返回值类型是 T1。


**分解下面的复杂声明** 
![[Pasted image 20240607145802.png]]
1. fp 和\*号括在一起，说明用是一个指针，指向 T 1 类型：
![[Pasted image 20240607145940.png]]
1. T1应该是一个函数类型，参数是 void*,返回值是 T2类型：
![[Pasted image 20240607145951.png]]
1. T2和*号括在一起，应该也是个指针，指向 T3类型:
![[Pasted image 20240607150425.png]]
# c标准库 
已经见过 c 标准库的一些用法，总结如下：
含 stdio. h, 使用其中声明的 printf 函数，这个函数在 libc 中实现，程序在运行时要动态链接 libc 共享库。
math. h 中声明的 sin 和 log 函数，使用这些函数需要动态链接 libm 共享库。

总结一下，Linux 平台提供的 C 标准库包括：
一组头文件，定义了很多类型和宏，声明了很多库函数和全局变量。头文件放在哪些目录下取决于不同的 Linux 发行版和编译器版本
一组库文件。**提供了库函数和全局变量的定义**。**大多数库函数在 libc 共享库中**，有些库函数在另外的共享库中，例如数学函数在 libm 中。
在第 19.4 节讲过，**通常 libc 共享库是/lib/libc. so. 6**, 而我的系统启用了 hwcap 机制，libc 共享库是/lib/tls/i 686/cmov/libc.so.6。

本章集中介绍一些最基本和最常用的库函
## 字符串操作函数
**程序**按功能划分可分为**数值计算、符号处理和 I/O 操作**三类
**无论多复杂的符号处理都是由各种基本的字符串操作组成的**，本节介绍如何用 C 的库函数做字符串赋初值、取长度、拷贝、连接、比较、搜索、分割等基本操作。
### 给字符串赋初值
![[Pasted image 20240613112328.png]]

通常调用 memset 时传给 c 的值是 0, 把一块内存区清零。
例如定义 char buf[10];, 如果它是**全局变量或静态变量则自动初始化为 0**（位于. bss 段），如果它是**函数的局部变量则初值不确定**，可以用 memset（buf, 0,10）**清零**，由 m**alloc 分配的内存初值也是不确定的**，也可以用 memset **清零**。

为什么规定参数 c 的类型是 int 呢？
另一种说法认为，规定参数为 int 型是为了传字符常量方便，因为字符常量也是 int 型的，比如调用 memset (buf,'A',10)
![[Pasted image 20240613112620.png]]
[]()
### 取字符串的长度 
![[Pasted image 20240613112843.png]]
返回的长度不包括'\\0'字符在内

**注意**，如果定义 charbuf[5]="hello";, 则调用 strlen (buf)是危险的，会造成数组访问越界。
### 拷贝字符串
![[Pasted image 20240613113221.png]]
**和 stmcpy 不同，memcpy 并不是遇到,\\0，就结束，而是一定会拷贝完 n 个字节****
**
**memmove** 但是和 memcpy 有一点不同，memcpy 的两个参数 **src 和 dest 所指的内存区间如果重叠则无法保证正确拷贝**，而 memmove 却可以正确拷贝. 假设定义了**一个数组 char buf[20]="helloworld\n;, 如果想把其中的字符串往后移动一个字节 (变成"hhelloworld\n"), 调用 memcpy 是无法保证正确拷贝的：**

memmove 可以这样实现：
![[Pasted image 20240613133426.png]]
![[Pasted image 20240613133433.png]]
借助于一个**临时缓冲区 temp**, 即使 src 和 dest 所指的内存区间有重叠也能正确拷贝

用 memcpy 为什么会得到 hhhllooworrd 这个奇怪的结果呢？根据这个结果猜测的一种可能的实现是：
![[Pasted image 20240613133644.png]]
**在 32 位的 x 86 平台上，每次拷贝 1 个字节需要一条指令，每次拷贝 4 个字节也只需要一条指令，为了提高拷贝的效率，我们先处理完零头然后 4 个字节 4 个字节地拷贝**
这个**实现并不正确，把 void\*指针转成 int\*指针来访问应该考虑对齐的问题**，请读者自己实现一个更完善的版本。


字符串的拷贝也可以用 strdup (3)函数，这个函数属于 POSIX 标准但并不属于 C 标准。
![[Pasted image 20240613133927.png]]
这个函数**调用 malloc 动态分配内存**，把字符串 s 拷贝到新分配的内存中然后返回。用这个函数**省去了事先为新字符串分配内存的麻烦，但是用完之后要记得调用 free 释放新字符串的内存。**
### 连接字符串
![[Pasted image 20240613134045.png]]
strcat 和 strcpy 有同样的问题，调用者必须确保 dest 缓冲区足够大，否则会导致缓冲区溢出错误。strncat 函数通过参数 n 指定一个长度，就可以避免缓冲区溢出错误.
**strncat 总是保证 dest 缓冲区以'\\0'结尾**, 这一点又和 stmcpy 不同, stmcpy 并不保证 dest 缓冲区以 '\\0'结尾。
### 比较字符串
![[Pasted image 20240613134255.png]]

mememp 从前到后逐个比较缓冲区 si 和 s 2 的前 n 个字节（不管里面有没有 3）,

stremp 把 si 和 s 2 当做字符串比较
结束时有两种可能：1. 如果两个字符串完全相同，同时遇到（\\0, 字符，那么返回 0。2. 如果在比较过程中遇到不同的字符，那么把两个字符相比较返回正值或负值。如果在一个字符串遇到 \\0，，比另一个字符串先结束，也属于这种情况，这时把\\0 和另一个字符串中对应的字符相比较返回正值或负值。

stmcmp 的比较结束条件是：要么比较完 n 个字符结束 (类似于 memcmp),要么当遇到不同的字符或者当一个字符串比另一个先遇到时结束 (类似于 strcmp)
### 搜索
![[Pasted image 20240613135959.png]]
strchr 在字符串 s 中从左到右查找字符 c, 找到它第一次出现的位置就返回，返回的指针就指向这个位置
strrchr 和 strchr 类似，但是返回字符 c 最后一次出现的位置


![[Pasted image 20240613140048.png]]
strstr 在一个长字符串中从前到后找一个子串 (Substring)
搜索子串有一个显而易见的算法，可以用两层循环，外层循环把 haystack 中每个字符的位置依次假定为子串的开头，内层循环从这个位置开始逐个比较 haystack 和 needle 的每个字符是否相同



### 分割
每条记录占一行。每条记录又由若干个字段组成。字段之间的分隔符是: 号

strtok 函数可以很方便地完成分割字符串的操作
![[Pasted image 20240613140421.png]]
参数 str 是待分割的字符串，**delim 是分隔符**，可以指定一个或多个分隔符
...
## 标准 io 库函数
### 文件的基本概念
用 c 标准库对文件进行读写操作。本节介绍的大部分函数在头文件 stdio. h 中声明，称为标准 I/O 库函数。

件可分为文本文件 (TextFile)和二进制文件
文件是文本文件，而目标文件、可执行文件和库文件是二进制文件
文本文件是用来保存字符的，文件中的字节都是字符的某种编码 (例如 ASCH 或 UTF-8), 用 cat 命令可以查看文本文件的内容
二进制文件不是用来保存字符的，文件中的字节表示其他含义，例如可执行文件中有些字节表示指令，有些字节表示各 Section 在文件中的位置，有些字节表示各 Segment 的加载地址。


用 hexdump 命令查看二进制文件，现在我们再介绍一种二进制文件查看工具 od
## 数值字符串转换函数
## 分配内存的函数
# 链表、二叉树与哈希表 
**数据结构是数据的组织方式，包含存储方式和访问方式两层意思**
用指针组织的数据存储方式比数组更加灵活，相应的访问方式也会有新的特性

**到底该选用哪种数据结构呢？应该看哪种数据结构的存储方式和访问方式最符合你的应用需要。**
## 链表 
### 单链表 
最后一个节点的指针域为 NUL
数组支持随机访问，而链表是不支持随机访问的
以下代码实现了单链表的基本操作。
![[Pasted image 20240613142659.png]]
![[Pasted image 20240613142720.png]]
![[Pasted image 20240613142746.png]]
![[Pasted image 20240613142756.png]]
#### 2
```
```text
//定义结点类型
typedef struct Node {
    int data;       //数据类型，你可以把int型的data换成任意数据类型，包括结构体struct等复合类型
    struct Node *next;          //单链表的指针域
} Node,*LinkedList;  
//Node表示结点的类型，LinkedList表示指向Node结点类型的指针类型
```

```text
LinkedList listinit(){
    Node *L;
    L=(Node*)malloc(sizeof(Node));      //开辟空间 
    if(L==NULL){                     //判断是否开辟空间失败，这一步很有必要
        printf("申请空间失败");
        //exit(0);                  //开辟空间失败可以考虑直接结束程序
    }
    L->next=NULL;       //指针指向空
}
```

```text
//头插法建立单链表
LinkedList LinkedListCreatH() {
    Node *L;
    L = (Node *)malloc(sizeof(Node));   //申请头结点空间
    L->next = NULL;                      //初始化一个空链表
  
    int x;                         //x为链表数据域中的数据
    while(scanf("%d",&x) != EOF) {
        Node *p;
        p = (Node *)malloc(sizeof(Node));   //申请新的结点
        p->data = x;                     //结点数据域赋值
        p->next = L->next;     //将结点插入到表头L-->|2|-->|1|-->NULL
        L->next = p;
    }
    return L;
}
```
```text
//尾插法建立单链表
  
LinkedList LinkedListCreatT() {
    Node *L;
    L = (Node *)malloc(sizeof(Node));   //申请头结点空间
    L->next = NULL;                  //初始化一个空链表
    Node *r;
    r = L;                          //r始终指向终端结点，开始时指向头结点
    int x;                         //x为链表数据域中的数据
    while(scanf("%d",&x) != EOF) {
        Node *p;
        p = (Node *)malloc(sizeof(Node));   //申请新的结点
        p->data = x;                     //结点数据域赋值
        r->next = p;            //将结点插入到表头L-->|1|-->|2|-->NULL
        r = p;
    }
    r->next = NULL;
    return L;
}
```

```text
/单链表的插入，在链表的第i个位置插入x的元素
  
LinkedList LinkedListInsert(LinkedList L,int i,int x) {
    Node *pre;                      //pre为前驱结点
    pre = L;
    int tempi = 0;
    for (tempi = 1; tempi < i; tempi++) {
        pre = pre->next;                 //查找第i个位置的前驱结点
    }
    Node *p;                                //插入的结点为p
    p = (Node *)malloc(sizeof(Node));
    p->data = x;
    p->next = pre->next;
    pre->next = p;
  
    return L;
}
```


insert 函数虽然简单，其中也隐含了一种**特殊情况**：空链表

如果要摘除的节点是链表的第一个节点，它是没有前趋的，这种情况要用特殊的代码处理。因为 p=head 的情况处理代码是 head=p->next;而 pre->next=p 的情况处理代码是 pre->next=p->next;, **处理代码不一样**，不能合并
上述代码是分开处理的，如果想办法把处理代码变成一样的就可以合并了
![[Pasted image 20240613143338.png]]
**定义一个指向指针的指针 pnext,** 在 for 循环中 pnext 遍历 head 指针和每个节点的 next 指针域，==这样无论是 head 指针还是每个节点的 next 指针域都可以用*pnext 访问，就把处理代码统一起来了。==

如果限定每次只允许在链表头部插入和删除元素，就形成一个 LIFO 的访问序列，所以在链表头部插入和删除元素的操作**实现了堆栈的 Push 和 Pop 操作**
### 双向链表
如果每个节点再维护一个指向前趋的指针，删除操作就像插入操作一样容易了
![[Pasted image 20240613145106.png]]
![[Pasted image 20240613145114.png]]
如果在**表头和表尾各添加一个 Sentinel 节点**（这两个节点只用于界定表头和表尾，不保存元素），就可以把这些**特殊情况都转化为一般情况**了。

![[Pasted image 20240613150141.png]]
![[Pasted image 20240613151226.png]]

上面的例子还实现了队列的 enqueue 和 dequeue 操作，在 head 处 enqueue 而在 **tail 处 dequeue**
其实用**链表实现环形队列是最自然的，以前基于数组实现环形队列，我们还要假想它是首尾相接的**，而如果基于链表实现环形队列，根本不需要假想
把**上面的程序改成环形链表** (CircularLinkedList)也非常简单，只需要把 doublylinkedlist.c 中的：
![[Pasted image 20240613145902.png]]
改为
![[Pasted image 20240613145924.png]]
再把 doublylinkedlist.c 中所有的 tail 替换成 head 即可，**相当于把 head 和 tail 合二为一了**,
### 静态链表 
![[Pasted image 20240613152114.png]]
一个静态分配的数组，每个数组元素都有 row、col 和 predecessor 三个成员，
predecessor 成员保存一个数组下标，指向数组中的另一个元素，==这其实也是链表的一种形式==，**称为静态链表**
比如图 25.8 中的第 6、4、2、1、0 个元素串成一条链表。
## 二叉树 
### 基本概念
![[Pasted image 20240613152219.png]]
二叉树可以这样递归地定义：
1. **就像链表有头指针一样，每个二叉树有一个根指针** 根指针可以是 NULL, 表示空二叉树。
2. 2. 根指针可以指向一个节点，称为根节点，**根节点除了保存元素之外还有两个指针域，这两个指针域又分别是另外两个二叉树 (左子树和右子树)的根指针**。
> **先序遍历(VLR)**、**中序遍历(LVR)**、**后序遍历(LRV)**

 二叉树的基本操作
 ...
### 排序二叉树 
## 哈希表
首先分配一个**指针数组，数组中的每个元素是一个链表的头指针**，哈希表由若干个链表组成，**每个链表称为一个槽** (Slot) 。 
然后向哈希表中插入节点，哪个节点应该插入哪个槽中由哈希函数决定

简单地选取哈希函数 h (x)=x%1
...