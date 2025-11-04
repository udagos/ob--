---
up:
  - "[[../moc/mocwork]]"
---
Error 146: Assuming a binary constant
Warning  537:Repeatedincludefile
Warning 641: Converting enum 'TASK_PRIO' to 'int'
Warning 534: Ignoring return value of function 'OsThreadInit 
Info 830: Location cited in prior message
	先去掉所有的 Info 830: Location cited in prior message，这条意思大概是前一条消息的提示（不太明白，反正没什么用）
	不时错误，上条信息的补充信息。
Warning 545: Suspicious use of &
	可疑使用&
Info 843: Variable 'sRCBTaskName' could be declared as const
Info 766: Header file `C:\Users\jingchangrui\Desktop\321\FW_BNE_R 10_MAIN_MASTER\trunk\BNE-R 10\src\Drivers\UartDriver\..\board. h' ` not used in module `'C:\Users\jingchangrui\Desktop\321\FW_BNE_R 10_MAIN_MASTER\trunk\BNE-R 10\src\Applications\Application. c'`

Info 818: Pointer parameter 'RecvFrameInfo' (line 76) could be declared  as pointing to const
Warning 506: Constant value Boolean
	Lint 提示对常量值 (`0`) 的逻辑操作 (`!`)。应该对布尔值
Info 774: Boolean within 'if' always evaluates to True
	布尔表达式始终返回真假
Info 831: Reference cited in prior message
	在之前的消息引用参考信息 831
Info 717: do ... while (0);
Info 718: Symbol 'U 8 BufChangToString 16' undeclared, assumed to return int 
符号'U 8 BufChangToString 16'未声明，假定返回 int--函数在未声明（或之前）被引用，或在当前模块中定义。这不一定是错误，您可能希望禁止显示此类消息。请注意，作者将声明添加到另一个模块，您将不会禁止此消息。它只能通过声明来抑制
在正在处理的模块中。
Info 746: call to function 'U 8 BufChangToString 16 ()' not made in the
    presence of a prototype
	头文件声明、external 声明、function (void)中的 void 都不能少，类型、形参要保持一致。
Warning 529: Symbol 'InstrResult' (line 498) not subsequently
	未引用
Info 838: Previously assigned value to variable 'FreeSize' has not
    been used
Info 752: local declarator 'GateIsInPosition (GATE_INDEX)' not referenced
Warning 528: Symbol 'CanCommCnt' not referenced
Info 830: Location cited in prior message