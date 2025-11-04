---
up:
  - "[[../moc/mocwork]]"
---
## 1 ImageRotateDstMemDmaClear
Description	Resource	Path	Location	Type
type defaults to 'int' in declaration of 'sBitNumTable' [-Wimplicit-int]	RecycleCashBox. c	/BNE-R 10/src/Applications/FlowControl/CashBox	line 477	C/C++ Problem

```static const sBitNumTable[256] = 
{
    0,	1,	1,	2,	1,	2,	2,	3,	1,	2,	2,	3,	2,	3,	3,	4,
    1,	2,	2,	3,	2,	3,	3,	4,	2,	3,	3,	4,	3,	4,	4,	5,
    1,	2,	2,	3,	2,	3,	3,	4,	2,	3,	3,	4,	3,	4,	4,	5,
    2,	3,	3,	4,	3,	4,	4,	5,	3,	4,	4,	5,	4,	5,	5,	6,
    1,	2,	2,	3,	2,	3,	3,	4,	2,	3,	3,	4,	3,	4,	4,	5,
    2,	3,	3,	4,	3,	4,	4,	5,	3,	4,	4,	5,	4,	5,	5,	6,
    2,	3,	3,	4,	3,	4,	4,	5,	3,	4,	4,	5,	4,	5,	5,	6,
    3,	4,	4,	5,	4,	5,	5,	6,	4,	5,	5,	6,	5,	6,	6,	7,
    1,	2,	2,	3,	2,	3,	3,	4,	2,	3,	3,	4,	3,	4,	4,	5,
    2,	3,	3,	4,	3,	4,	4,	5,	3,	4,	4,	5,	4,	5,	5,	6,
    2,	3,	3,	4,	3,	4,	4,	5,	3,	4,	4,	5,	4,	5,	5,	6,
    3,	4,	4,	5,	4,	5,	5,	6,	4,	5,	5,	6,	5,	6,	6,	7,
    2,	3,	3,	4,	3,	4,	4,	5,	3,	4,	4,	5,	4,	5,	5,	6,
    3,	4,	4,	5,	4,	5,	5,	6,	4,	5,	5,	6,	5,	6,	6,	7,
    3,	4,	4,	5,	4,	5,	5,	6,	4,	5,	5,	6,	5,	6,	6,	7,
    4,	5,	5,	6,	5,	6,	6,	7,	5,	6,	6,	7,	6,	7,	7,	8,
};
```
## 2
Description	Resource	Path	Location	Type
statement with no effect [-Wunused-value]	CashBoxComm. c	/BNE-R 10/src/Applications/CanComm	line 104	C/C++ Problem

格式不对
## 3
Description	Resource	Path	Location	Type
passing argument 5 of 'XUsbPs_EpBufferReceive' from incompatible pointer type [-Wincompatible-pointer-types]	UsbDriver. c	/BNE-R 10/src/Drivers/UsbDeviceDriver	line 380	C/C++ Problem
```
Status = XUsbPs_EpBufferReceive(InstancePtr, EpNum,&BufferPtr, (U32 *)&BufferLen, (U32 *)&Handle);    //获取数据Buffer


U32	Handle = 0;
```

## 4
Description	Resource	Path	Location	Type
return discards 'const' qualifier from pointer target type [-Wdiscarded-qualifiers]	MotorManager. c	/BNE-R 10/src/Applications/FunctionApp/MotorApp	line 187	C/C++ Problem
```
char *mystrtok(const char *input, const char *delim,char *rest) {
    int i;
    for (i = 0; input[i] != *delim && input[i] != '\0'; ++i) {
        continue;
    }
    char *result = malloc(sizeof(char) * (i + 2));
    memcpy(result, input, i + 1);
    result[i + 1] = '\0';
    if (input[i + 1] != '\0') 
        rest = input + i + 2;
    else
        rest = NULL;
    return result;
}

```

`input` 是一个指向常量字符的指针，并且您将它分配给一个指向**非常量**字符的指针

您还可以使用 (char*) 类型转换您的“输入”变量，这将解决警告。只是要小心使用像这样的显式转换，以免修改常量本身。

rest = (char*)input + i + 2;

## 5
Description	Resource	Path	Location	Type
pointer targets in passing argument 1 of 'rt_snprintf' differ in signedness [-Wpointer-sign]	InstrProcRT. c	/BNE-R 10/src/Applications/InstrExpelain	line 339	C/C++ Problem

```
DataLen += rt_snprintf(InstrReturn + DataLen, 60 * 1024 - DataLen, "%5s : %3d ", SensorGetName(SnsId), AppSensorGetAd(SnsId));
```

U 8 *InstrReturn

## 6
return makes pointer from integer without a cast [-Wint-conversion] MotorManager. c /BNE-R 10/src/Applications/FunctionApp/MotorApp line 55 C/C++ Problem 
赋值使指针整数不带强制转换
```
socket = tcp_socket;



int tcp_socket(void)
{
    int s;

    if ((s = socket(PF_INET, SOCK_STREAM, 0)) == -1) {
        _logf(LOG_DEBUG, "LOG %s:%d (%s) - %s", __FILE__, __LINE__, __func__, "Error creating socket");
        return -1;
    }
    return s;       
}

```

## 7
ASSERT_MOTOR_ID 在那定义

## 8
implicit declaration of function 'UpdateBNInitArray
### 原因：

1. 没有把函数所在的.c文件生成.o目标文件；
2. 在函数所在的.c 文件中声明了函数，但是没有在与之相关联的.h 文件中声明

在需要调用该函数的文件中声明该函数；
![[Pasted image 20240201152843.png]]

也可在相应. h 文件中声明函数
（不加 extern)
![[Pasted image 20240201152853.png]]
## 9
pointer targets in assignment differ in signedness 

```
ProcStart = &(DmaInstance.Chans[i].ProgBufPool[0].Buf[0]);
```
警告: 初始化中的指针目标的符号不同
## 10
initialization makes integer from pointer without a cast [-Wint-conversion] CorrectMath. c /BNE-R 10/src/Applications/FunctionApp/CisApp/Cis line 272 C/C++ Problem


初始化使指针中的整数不带强制转换

```
U32 pAddr = NULL;
```



## 11
没有 default
Description	Resource	Path	Location	Type
enumeration value 'GATE_MANAGER_INFLOW_FSM_NUM' not handled in switch [-Wswitch]	PageManage. c	/BNE-R 10/src/Applications/FlowControl/PageManage	line 5194	C/C++ Problem
## 12
Description	Resource	Path	Location	Type
assignment from incompatible pointer type [-Wincompatible-pointer-types]	CashBoxCmd. c	/BNE-R 10/src/Applications/CanComm	line 321	C/C++ Problem

一个类型指针赋值给另一个类型指针

```
    UPDATE_INFOR BoardUpdateInfor;
    U8 *ptData;

typedef struct
{
    U32 mUpdateInfoFalg;	    ///< 标示信息区的起始标志，0xAA555AA5
    
    U8  mUniqueName[32];        ///< 升级避让名称，如:"RSC-D400M_STM32"
    
	U8  mFWVersion[12];	        ///< 固件程序的版本号，如："FV1.000.00"
	U8  mPCBVersion[16];        ///< 硬件PCB版本号，如："FEDAAV12"

	U8  mCompileTime[24];	    ///< 程序编译日期
}UPDATE_INFOR;



    ptData = &BoardUpdateInfor;
```

```
void PlateStatusCallBack(CASHBOX_INDEX CashBoxID, COMPONENT_STATUS* Status)

sPlateStatus[CashBoxID].mCallBack   = PlateStatusCallBack;


typedef struct _COMPONENT_STATUS
{
    U32 mDevState;
    U32 mPosition;
    U8  mErrorGroup;
    U8  mErrorType;
    U8  mId;
    void (*mCallBack)(CASHBOX_INDEX CashBoxID, const struct _COMPONENT_STATUS* Status);
    U8 mReserve;
}COMPONENT_STATUS;
```
## 13
dereferencing type-punned pointer will break strict-aliasing rules


在该参数激活的情况下，编译器希望不同类型的对象不会指向同一个地址
最简单的方法是使用 -fno-strict-aliasing 参数来关闭 gcc 的优化选项，代价是放弃了 strict-aliasing 编译优化可能带来的可执行代码的性能提升。当然也可以用 -Wno-strict-aliasing 来屏蔽相关的 warning 信息，但无论这些 warning 信息多么的无关紧要，总还是“疑似危险”，所以可能的话最好还是把所有的 warning 都消灭掉。
　　消灭的方法也不算复杂，正如 gcc manual 所示的那样，可以是采用 union 的不同成员变量来完成类型的转换。上面那段代码可以改为：
　　



，如果我们确实需要做指针强制类型转换，怎样才能解决这个告警并得到健壮的代码呢？
使用 union 来解决，这也是 gcc 推荐的做法。type punning via unions feels 
```
natural。
int retLen;
someSetFunc ((unsigned long*)&retLen);
printf ("ret len = %d\n", retLen);

...

union u_retLen {
	int retLen;
	unsigned long ptr;
};
someSetFunc (&u_retLen. ptr);
printf ("ret len = %d\n", u_retLen. retLen);
```
## 14
复制丢失 const
Description Resource Path Location Type assignment discards 'const' qualifier from pointer target type [-Wdiscarded-qualifiers] TrackModule. c /BNE-R 10/src/Applications/FlowControl/TrackModule line 1634 C/C++ Problem

## 15
Description	Resource	Path	Location	Type
'struct MOTOR_STATUS' declared inside parameter list will not be visible outside of this definition or declaration	StorageCashBox. h	/BNE-R 10/src/Applications/FlowControl/CashBox	line 117	C/C++ Problem

**这个警告是提示在头文件中使用了未完全声明的结构体，两种解决办法；**  
1.在头文件中，使用前向声明来解决[结构体](https://so.csdn.net/so/search?q=%E7%BB%93%E6%9E%84%E4%BD%93&spm=1001.2101.3001.7020)未完全声明的问题；  
2.在头文件中，添加对 teacher.h 和 student.h 的[头文件包含](https://so.csdn.net/so/search?q=%E5%A4%B4%E6%96%87%E4%BB%B6%E5%8C%85%E5%90%AB&spm=1001.2101.3001.7020)，确保在 root.h 中使用到结构体能够正确引入。

## 16

Description	Resource	Path	Location	Type
conflicting types for 'ThickDacPwmSet'	MagThick. c	/BNE-R 10/src/Applications/FunctionApp/MagThickApp	line 670	C/C++ Problem

原因一：
没有函数声明，且函数定义在主函数之后；
原因二：
头文件的被循环引用，在引用时考虑清楚包含顺序
原因三：
头文件函数声明和函数定义参数不同
头文件中声明 voidtest (constchar*buf);
在定义时写作 voidtest (char*buf);
原因四：
函数使用的参数类型是自定义类型（如结构体），而自定义类型的定义在函数的声明和函数定义之间，由于在函数声明时，结构体并
没有被定义，不被系统识别为结构体，而后面定义函数时，结构体已经定义，系统将其识别为结构体，导致系统认为声明和定义使用
的是不同的参数类型；所以才会出现上述问题；
原因五：
在 linux 中，编译头文件，会出现一个中间的预编译文件（.h.gch），当再次编译整个文件时，如果该文件 (.h.gch)存在，则会直接使用该文件 (.h.gch)，而不会再编译. h 文件，此时，如果你改动了. h 文件，而继续编译，则会造成声明和定义不一致的现象，虽然在文件里显示声明和定义是一致的，但是实际上系统编译时并不会使用你改动后的文件 (. h)，而是直接使用你修改前编译生成的.h.gch 文件；(这个
错误一般很难发现，如果发现自己目录下有.h.gch 文件，则一定要及时更新；）
## 17
Description	Resource	Path	Location	Type
function with qualified void return type called	MotorApp. c	/BNE-R 10/src/Applications/FunctionApp/MotorApp	line 1007	C/C++ Problem

## 18
Description	Resource	Path	Location	Type
comparison between 'CASHBOX_INDEX {aka enum <anonymous>}' and 'enum <anonymous>' [-Wenum-compare]	CashBoxCmd. c	/BNE-R 10/src/Applications/CanComm	line 295	C/C++ Problem
Description	Resource	Path	Location	Type
comparison between 'CASHBOX_INDEX {aka enum <anonymous>}' and 'enum <anonymous>' [-Wenum-compare]	CashBoxCmd. c	/BNE-R 10/src/Applications/CanComm	line 295	C/C++ Problem



[c - 为什么直接比较两个枚举会出错？ - IT工具网](https://www.coder.work/article/1563570)


[c++ - 比较两个不同的枚举时，是否有避免警告的正确方法？ - IT工具网](https://www.coder.work/article/822219)

##  19
dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing] 
[dereferencing type-punned pointer will break strict-aliasing rules-CSDN博客](https://blog.csdn.net/FJDJFKDJFKDJFKD/article/details/107536386)

## 20

[从不兼容的指针类型初始化”](https://stackoverflow.org.cn/questions/52601379)
initialization from incompatible pointer type [-Wincompatible-pointer-types]	CashBoxComm. c	/BNE-R 10/src/Applications/CanComm	line 374	C/C++ Problem

## 21 
case 里可以不用括号
## 22
Description	Resource	Path	Location	Type
'CalculateTapeLength' declared 'static' but never defined [-Wunused-function]	ThickAlgorithm. c	/BNE-R 10/src/Applications/CashRecognition/ThickHandle	line 60	C/C++ Problem

   解决的办法很简单，将头文件中的声明转移到. c 文件中就可以了。
## 23
function with qualified void return type called MotorApp. c 

具有称为 MotorApp. c 的限定 void 返回类型的函数

## 24
ignoring #pragma anon_unions [-Wunknown-pragmas] 
[C语言 匿名联合体和匿名结构体\_#pragma anon\_unions-CSDN博客](https://blog.csdn.net/u012841414/article/details/128850110)

#pragma 用于知识编译器完成一些特定动作
[C语言#pragma使用方法\_c pragma-CSDN博客](https://blog.csdn.net/liuchunjie11/article/details/80502529)
## 25
 warning: incompatible implicit declaration of built-in function sqrt [enabled by default]

警告：隐式声明与内置的 sqrt 函数不兼容”，这个问题是因为 C 语言会为没有声明的函数自动添加隐式声明[[查看博文](https://blog.csdn.net/smstong/article/details/50523120)]。如果一个函数只声明但没定义，编译可以过，但链接过不了。估计当时碰到的就是这个问题
## 26
未初始化警告  static 警告消除？
## 27
Description	Resource	Path	Location	Type
Invalid project path: Include path not found (BNE-R 10\src\Applications\FunctionApp\PwmApp).	BNE-R 10		pathentry	Path Entry Problem


## 28
指针的类型
**int (*p)[4]=a**        int (*)[4]
int (*p)(int a,int b)=add            	int (*)(int,int)

## 29
Description	Resource	Path	Location	Type
assignment makes pointer from integer without a cast [-Wint-conversion]	ModuleApp. c	/BNE-R 10/src/Applications/FunctionApp/ModuleApp	line 1053	C/C++ Problem



MODULE_FLOW_PARA* OutletLockFlowParaInstance (U 8 CtrlMode)

   MODULE_FLOW_PARA *ptFLowPara = STD_NULL;

ptFLowPara = OutletLockFlowParaInstance (CtrlMode);

## 30
具有称为 MotorApp. c 的限定 void 返回类型的函数
 function with qualified void return type called MotorApp. c


## 31
Description	Resource	Path	Location	Type
pointer type mismatch in conditional expression	PageManageIn. c	/BNE-R 10/src/Applications/FlowControl/PageManage	line 1782	C/C++ Problem
警告:条件表达式中的指针/整数类型不匹配”
[是什么导致了“警告:条件表达式中的指针/整数类型不匹配”？-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/ask/sof/102428645)

## 32
Description	Resource	Path	Location	Type
missing braces around initializer [-Wmissing-braces]	RecycleCashBox. c	/BNE-R 10/src/Applications/FlowControl/CashBox	line 1463	C/C++ Problem

[这个问题是？error: missing braces around initializer \[-Werror=missing-braces\] - CSDN文库](https://wenku.csdn.net/answer/7qi8ze88o9)

RCB_WORKIN_MANAGER WorkInManager = 
{
	.mRcbId = RcbId,
	.mptCtrl = &sRcbCtrl[RcbId],
	.mTaskMsg = {0},
	.mWorkFsm = RCB_WORKIN_FSM_IDLE,
	.mPaperIdHandle = 0,
	.mFlowRes = RCB_WORKIN_FLOW_RES_NULL,
	.mIsTaskOver = STD_FALSE,
};

GATE_HANDLE_MSG mTaskMsg;       // 任务消息 

typedef struct
{
    union
    {
        // PAPER *mptPaper;    //   介质信息地址
        U 32 mNodeOutNum;    //  出钞张数
        U 32 mPara;          //  控制参数
        U 8 mDirConfig;      //  方向配置
    };
    U 16 mSpeedConfig;       //  速度配置
    U 8 mTask;               //  操作任务
    U 8 mReverse[1];
}GATE_HANDLE_MSG;



**BNE-R 10/src/Applications/CashRecognition/ImageHandle/ImageCorrect. c**


**BNE-R 10/src/Applications/FlowControl/FlowCtrl. c**
**BNE-R 10/src/Applications/FunctionApp/CisApp/Cis/Cis. c**






## 33  
ignoring #pragma anon_unions [-Wunknown-pragmas] AppCommon. h /BNE-R 10/src/Applications/Common line 24 C/C++ Problem 

[C语言 匿名联合体和匿名结构体\_#pragma anon\_unions-CSDN博客](https://blog.csdn.net/u012841414/article/details/128850110)
## 34
De cast to pointer from integer of different size [-Wint-to-pointer-cast] FpgaDriver. c /BNE-R 10/src/Drivers/FpgaDriver line 357 C/C++ Problem 
[c - 警告：从不同大小的整数转换为指针 \[-Wint-to-pointer-cast\]\_Stack Overflow中文网](https://stackoverflow.org.cn/questions/18221887)
[解决 warning: cast to pointer from integer of different size \[-Wint-to-pointer-cast\]-CSDN 博客]( https://blog.csdn.net/weixin_43828438/article/details/102406646 )

## 34
Description	Resource	Path	Location	Type
assignment from incompatible pointer type [-Wincompatible-pointer-types]	MidFpga. c	/BNE-R 10/src/Middlewares/Fpga	line 91	C/C++ Problem

sSlaveFpgaManager[FPGA_INDEX_SLAVE_L]. mErrStateCallBack = ptFun;

void MidFpgaErrStateChangeCallbackSet (DEVICE_INDEX DeviceId, void (*ptFun)(void))

void (*mErrStateCallBack)(U 8);

更改
sSlaveFpgaManager[FPGA_INDEX_SLAVE_L]. mErrStateCallBack =void (*)(U 8); ptFun;