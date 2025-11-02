---
up:
  - "[[../moc/work|work]]"
---
#ed
CIS 原始输出信号较弱，转换为数字信号前要对其进行处理。
对 CIS 输出信号采样、偏移、放大和数字化的芯片称为模拟前端
![[Pasted image 20240312194825.png]]
cds 取样  pga 可编程增益放大



cis 扫描控制
CIS 行同步信号、光源控制信号以及点时钟之间的时序约束关系由 CPLD（或 FPGA）提供；
每行扫描时的光源导通时间、点时钟频率及行同步信号周期由单片机（或 DSP）程序设置；
每行的行同步信号由单片机（或 DSP）程序触发。


AFE 接收 CIS 输出的模拟信号，并按照主控制模块配置的偏移和增益参数，对 CIS 的模拟输出信号进行偏置和幅值放大处理；处理后的模拟信号经过模拟前端的 A/D 转换为数字信号，由 AFE 的并行接口输出到主控制模块。
AFE 的工作模式可以由主控制模块通过串行接口对其进行编程设置。



AFE 的输入 Analog Input 连接 CIS 的输出 SIG，CDSCLK2为采样时钟，ADCCLK 为 AD 转换时钟，Output Data 为输出的16位数字信号。采样时钟和 AD 转换时钟也由主控制模块提供。
AFE 的数字输出信号与输入信号间有约11个像素的延迟且数字信号先输出高8位后输出低8位，设计时需要注意。
![[Pasted image 20240312195414.png]]



## 偏移量校正
原因：A/D 转换输入中的参考信号可能导致量化的值有负数，经 A/D 转换后负数和零都转为零，从而引起负值信号的丢失。
目的：获取 AFE 偏移量值，使得 CIS 暗输出最小值通过偏移模块后大于且接近参考电压值
![[Pasted image 20240312200403.png]]
图中，黑色线为 CIS 暗输出示意，红色线为参考电压示意。
# cis 组成
## 光源

发光二极管阵列：多个发光二极管均匀分布在光源PCB上，保证扫描方向 光强的一致性。光源PCB通过导线连接到CIS PCB上引入光源控制信号。

![[Pasted image 20240318142757.png]]
“发光二极管阵列在 CIS 中的位置，截面图”
![[Pasted image 20240318142805.png]]
## 透镜
“将原稿反射光线聚焦到感光 IC 表面的光口” ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=13&annotation=CEUBMYL5))
![[Pasted image 20240318142913.png]]
## 感光 ic
核心部件，接收透镜聚焦的光信号并将光信号转换为电信号的光电传感器 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=14&annotation=4J27HJW2))
# 工作原理
![[Pasted image 20240318143051.png]]
CIS 工作时，光源发出的光透过 CIS 玻璃照射到原稿表面，并在原稿表面反射；
•经原稿表面反射后载有图像信息的光信号通过透镜阵列聚焦到感光 IC 的表面；
•**感光 IC** 表面的各个光口接受光照进行**电荷积蓄**；

达到**一定的电荷积蓄时间后移位寄存器控制模拟开关依次打开，将与像素信息一一对应的模拟信号依次输出。**
![[Pasted image 20240318143203.png]]

## 工作时序
![[Pasted image 20240318143646.png]]
**输出信号SIG**
CIS 正常工作扫描白色样张时的输出信号称为明输出，CIS 关闭光源后工作时的输出信号称为暗输出 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=21&annotation=PE8HAVBP))
## 扫描过程
CIS 在 SI 和 CLK 驱动下，**沿着扫描方向依次输出 P 1、P 2 等像素点的值**，完成 L 1 行的扫描；介质前进一行，CIS 继续输出 L 2 行的 P 1、P 2 等像素点的值 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=22&annotation=X2Y8E3M9)) ![[Pasted image 20240318143426.png]]
## 光源控制时序
![[Pasted image 20240318143722.png]]
黑白扫描工作原理 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=23&annotation=S2X3KHE7))
黑白扫描是以单色光或者混和光作为光源的扫描模式；([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=23&annotation=ELV8A5JQ))
黑白扫描时原稿前进一行，CIS 光源发光一次，扫描一行数据。

彩色扫描工作原理：
彩色扫描时原稿前进一行，CIS 三色光源轮流发光，分别扫描一行数据。
## 扫描实现
![[Pasted image 20240318143855.png]]
cis 输出模拟信号，经过前端处理转换为数字信号
## 主要参数
1）扫描宽度 mm 2）分辨率 DPI、dots/mm 3）扫描速度 ms/line 4）时钟频率 1 M-16 MHz 

扫描速度与分辨率、时钟频率、输出相关，一般来说，分辨率越低、时钟频率越高、输出越多，扫描速度越高。

 5）参考电平 mV 6）暗输出 mV 7）最大明输出 mV
 ![[Pasted image 20240318144154.png]]

8）MTF 

9）DOI
## CIS 校正和图像补偿
CIS 是由光源、透镜和感光 IC 等一系列部件组成的成像系统，**各个部件之间的差异最终导致 CIS 扫描的图像不均匀**，扫描应用前需要对 CIS 进行校正，**生成补偿数据，对 CIS 扫描的原始图像进行补偿**。
# 选择 cis
有效扫描宽度：
	CIS 有效宽度（对于有白基准的 CIS，不包含白基准宽度）
光源
	需要提取特殊油墨信息时选用特殊光源的 CIS，如**纸币识别中用红外光提取红外油墨信息，用紫外光提取荧光反应信息**；([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=50&annotation=J7IHFV4R))
	**双光源 CIS 可以消除待扫描介质的折痕** ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=50&annotation=CI4C3CSC))
扫描频率：
	扫描频率计算公式：([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=51&annotation=IHGPN4KW))
	扫描频率 ≥（产品最大扫描宽度×扫描分辨率÷扫描行周期）([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=51&annotation=JCPH56VD))
	扫描频率单位为 MHz ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=51&annotation=WI47IIS8))
	扫描行周期单位为 sec/line ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=51&annotation=NHUFG8GR))  sec 是秒
	最大扫描宽度单位为 mm（也可以为 mm/line，方便公式计算中单位转换）([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=51&annotation=ZVAZEVG8))
	扫描分辨率单位为 dpi 5 即 dots/inch ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=51&annotation=SNDL9Y7S))  像素/英寸
扫描行周期 
	扫描行周期计算公式：([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=52&annotation=ZLCVG75H))
	扫描行周期<(1÷(扫描速度×扫描分辨率))([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=52&annotation=5XSCDP8X))
	**行周期单位为 sec/line** ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=52&annotation=DD8UGBUX))
	扫描速度单位为 mm/sec ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=52&annotation=BAIL9TWS))
	扫描分辨率单位为 dpi（即 dots/inch，从走纸方向定义，也可以为 lines/inch ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=52&annotation=A4KIVTG6))
通道选择：
	优选单通道输出的 CIS。**当单通道输出的 CIS 扫描行周期不能满足产品要求时，再选择 3 通道或者 6 通道 CIS。**
温度传感器：
	新认证的 CIS 如果有特殊原因没有白基准时必须配置温度传感器
白基准：
	新认证的 CIS 必须要有白基准，白基准从有效扫描起始点开始，至少占用有效输出 2 mm。
	![[Pasted image 20240318144836.png]]
扫描方向：
	从右向左。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=57&annotation=55FZTUFP))
	![[Pasted image 20240318144914.png]]
参数变化及其影响 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=58&annotation=2AAUARCD))
	![[Pasted image 20240318144946.png]]
# 应用
## 扫描一副图像方法
同步扫描：**电机走一步，CIS 扫描一点行**，走纸周期和扫描行周期相等。
异步扫描：电机走纸和扫描独立控制，走纸周期和扫描行周期不相等，扫描图像的纵向分辨率完全由固件控制，通过周期比率配置可以实现以 1 dpi 为单位的纵向分辨率的调整。
## 校正和补偿
### 均一性补偿
CIS 输出具有不均匀性，同时 **CIS 输出又近似线性，故针对 CIS 各个像素采用线性运算实现均一性的补偿**。
均一性补偿公式为：
Y=(X–a)\*b 
其中 Y 为补偿后的图像数据，X 为 CIS 输出经模拟前端芯片处理后的数字信号，**a、b 为补偿数据**。CIS 各个像素点都有自己专属的补偿数据。
![[Pasted image 20240318153648.png]]
### 校正和补偿的关系
扫描过程中应用校正生成的参数：
✓应用校正获得的发光时间控制 CIS 工作；
✓应用校正获得的 AFE 参数配置 AFE，对 CIS 模拟输出进行偏移和放大处理；
✓应用均匀性补偿数据对 CIS 扫描生成的数字图像进行补偿。
### 校正方法
以达到不同 CIS 扫描同一幅样张时可以得到灰度均匀、亮度一致的电子图像。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=92&annotation=KYR8E943))
**CIS 校正按照如下顺序执行** ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=92&annotation=6RXTC4K9))
偏移校正—>发光时间校正—>增益校正—>暗校正—>均一性校正
简化：可以将 AFE 增益固定，仅校正其它四种应用参数。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=92&annotation=RYHV5PKS))
注意：同一支 CIS 在不同的行周期（行同步信号周期）或不同的点时钟频率条件下工作时，需要分别进行参数校正 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=92&annotation=A29CRSEJ))
## 偏移量校正 
原因
	A/D 转换输入中的**参考信号可能导致量化的值有负数，经 A/D 转换后负数和零都转为零，从而引起负值信号的丢失**。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=93&annotation=YD24XV5M))
目的
	获取 AFE 偏移量值，使得 CIS 暗输出最小值通过偏移模块后大于且接近参考电压值。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=93&annotation=UW725YD6))
	![[Pasted image 20240318150948.png]]
图中，黑色线为 CIS 暗输出示意，红色线为参考电压示意。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=93&annotation=JXAU45ZQ))
详细过程和校正标准参见《CIS 应用设计规范》之 5.2.3 CIS 校正设计规范 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=93&annotation=XBLY5922))
## 发光时间校正 
原因
	**cIS 输出信号强弱与发光时间相关**，CIS 输出仅在规格书标定范围内保持线性，**为使 CIS 工作在线性区，需获取合适的发光时间**；([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=94&annotation=XBI9TYSL))
	**各 CIS 光源差异导致使用相同发光时间时 CIS 输出各不相同，为使不同 CIS 扫描相同介质时输出相同幅度的信号**，需为各 CIS 校正其专属的发光时间。
目的
	实验获取 CIS 发光时间，**使得 CIS 在该发光时间条件下扫描校正纸时明输出在规格书标称范围之内**。校正纸为与 CIS 等幅面的白色均匀介质 ([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=95&annotation=PFDMAGHF))
![[Pasted image 20240318151124.png]]
**黑色线为 CIS 明输出示意，蓝色和紫色线为 CIS 规格书标称的明输出范围示意**。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=95&annotation=VMQPW3YI))
详细过程和校正标准参见《CIS 应用设计规范》之 5.2.3 CIS 校正设计规范。([pdf](zotero://open-pdf/library/items/EAQ9PEWQ?page=95&annotation=48R7XTEU))
## 增益校正 
原因 
	“CIS 原始输出较弱，需要进行放大，**丰富图像灰度细节**。”
目的
	实验获取 AFE 增益值，放大 CIS 明输出信号，同时保证放大后信号的峰值小于 A/D 转换器的满量程。
![[Pasted image 20240318151334.png]]
## 暗校正
原因
	CIS 和 AFE 等模拟电路的零点漂移导致各个**像素点的暗输出不在零点**。
目的
	检测 CIS 各个像素点经过 AFE 之后的暗输出值 D\[n]，**获取 CIS 以及 AFE 等引入的零点漂移。该值即为均匀性补偿公式“Y = (X - a) * b”中的参数 a。**
	![[Pasted image 20240318151513.png]]
## 均一性校正 
原因
	透镜及 IC 本身特性引起的各感光 IC 间输出具有差异
目的
	**检测 CIS 各个像素点经过 AFE 之后的明输出值 L\[n]，从而计算各个像素点的有效输出 VEp\[n], 获取系数 S\[n]，使得扫描校正纸时最终获取的各像素点灰度值都为 Lmax。**
![[Pasted image 20240318151644.png]]
## 白基准
白基准是 CIS 一端玻璃内侧的一块白色区域。
CIS **校正完成后，获取该区域的平均输出作为基准值**；
CIS **扫描应用前，先启动扫描获取该区域的平均输出**，将**实时获取的值与基准值比较**，如果二者相近则不做调整；如果二者有差异，则调节 CIS 发光时间，重新扫描进行比较，**直到二者接近**。
![[Pasted image 20240318151901.png]]

利用有白基准的 CIS，以其局部特性代表整体特性，认为白基准的输出值与校正值相符时则整体输出也可达到校正值，从而弥补环境温度变化或者光源老化对 CIS 输出造成的影响。

主动校正保存白基准区域，自动校正处理

# 规格
dpi ：50   200 
Full 216   864
Effective 15 th to 202 th     60 th to 805 th
si **9**×5 (RGBIRUV)     **23**×5 (RGBIRUV)    μsec/line
	9 (B&W)     23 (B&W)
另一个 cis 没有紫外  23\*4



![[Pasted image 20240318162008.png]]
White image target    0.05~0.09 OD
Vref         800±200
Vdmin    ≥-200       **Darkoutput minimum**
Vdmax    ≤+150
Vpmax    800±100 T.B.D     **White output maximum**
UEp   ≤55   **White output uniformity**


![[Pasted image 20240318162027.png]]
SI   23
Effective number of sensor elements      748 (60 th to 805 th)
White output maximum     800±100
White output uniformity  ≤55


## 解释
vref
	基准电压是基准输出。**Vdmin 输出值基于 Vref**。
Vdmin
	如图 2 所示，Vdmin 是**暗输出信号（关闭 LED**）中的最小值。**其他参数使用 Vdmin 作为参考。**
vpmax 
	如图 2 所示，Vpmax 为最大白光输出信号，定义公式为：Vpmax=MAX[Vp（n）]
	其中：Vp（n） 是使用白色图像目标的第 n 个像素的输出信号。
	通过调整 LED 的发光时间（LED 脉冲宽度应为 Tmax 的 5%~95%）。
ud
	如图 2 所示，Ud 是黑暗中的输出信号（关闭 LED），定义如下：
	Ud=Vdmax-Vdmin
	Vdmax 是黑暗中第 n 个像素的最大输出信号
	Vdmin 是黑暗中第 n 个像素的最小输出信号
	**是同一个像素么**
uep
	UEp 是减去暗信号的白色输出不均匀性，定义如下：
	UEp = （（VEpmax – VEpmin） / （VEpmax））×100%
	式中：VEpmax = MAX[VEp（n）]，为最大有效输出信号;
	VEpmin = MIN[VEp（n）]，为最小有效输出信号;
	VEp（n） 是每个像素的有效输出信号，定义如下：
	VEp（n） = Vp（n） – Vd（n）
![[Pasted image 20240318163500.png]]


![[Pasted image 20240318164348.png]]
Tsu    30    Tw              SI setup time
Th     30     5\*Tw        SI hold time
Data output stability time       typ: 20   max:30
![[Pasted image 20240318164842.png]]
## 总结
si  
	200 dpi
		单色  1/16\*(64+8+288)=22.5     三色\*3
	50 dpi 输出多少像素，si 为 9 单色？
	透射的 si 和输出怎么说？
	两个 cis 都测？
	发光总的时间肯定覆盖输出
	50 200 dpi 图像都输出  si 是怎么定的
电压
	明电平时候暗电平怎么知道
校正
	每个暗校正都是像素点的偏移，而明校正则是每个像素点的系数
白基准
	白基准区域用示波器量