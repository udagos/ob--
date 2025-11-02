
硬件抽象层
	倒置依赖
软件基础设施
	rtt 设备驱动库

看软件架构，看一个文件被谁调用

事件驱动的编程思想 





## 2
### rtos
通过 understand 得知 oslib. h 和 rt-thread 被外界调用，而没有设备模块？
	设备模块用的是赛灵思的框架应该
	oslib. h 中线程通讯同步的 api



要一个使用 rtt 设备驱动库的代码



### middlewares
![[Pasted image 20240815150221.png]]
middlewares .h 被 application 引用
### fwlib
![[Pasted image 20240815150628.png]]
### drivers
![[Pasted image 20240815151307.png]]
psldriver. h 被 middleware 及 appliaction 引用

application 也能用 driver 层，虽然没有直接过去的。但通过 middle 的 middle.h 引用，比如 QspiFlashInit 被 init. c 引用

driver 的电机除了初始化都被中间层隔离了

driver 电磁铁被拨叉中间层隔离

can 被 application 的 can 引用

内存保护和缓存都没有使用

flash 中断等直接被 application 使用

复位模块

driver 的 fpga 也被 driver 其他模块引用，也被 middle 的 fpga 引用，甚至直接被 application 调用

gpio 被 application  function的 gpio 引用
#### flash 
qspi 模块被 qspiflash 模块调用
#### drivercommon


### application 
#### functionapp
##### gpio
gpio 目前只有初始化，也没有中断
##### ee
引用 middle 的fam
##### cis 
##### magthick
##### module
入朝口
出钞口
##### motor
motorapp 是电机线程
motorManager 其实应该在 middle 层
#### cash
thickhandle 
	是一个创建的线程
#### commin
##### motorcommon
![[Pasted image 20240815183516.png]]
motorcommon 引用了 motorapp，被 trackmotor. h 引用。为什么不直接引用 motorapp 还要用这个？

##### appcommon
是把杂的丢进去，为了不同 app 使用么?
##### appgatecommon
![[Pasted image 20240815191254.png]]
被 flowctrl 中的钞口引用
#### datacommon
![[Pasted image 20240815203317.png]]
![[Pasted image 20240815203341.png]]
#### flowctrl 
##### gatemanater
gateinet 和 gateoutlet 被 gatemanager 引用
gatemanager 是钞口管理线程
![[Pasted image 20240815193254.png]]
##### bvctrl
##### moduletask
##### trackmotor
![[Pasted image 20240815201127.png]]
##### tracksensor
sensorcheck 传感器检测线程
sensorapp
![[Pasted image 20240815200844.png]]
sensorpwm
tracksensor
##### trackselector
![[Pasted image 20240815201048.png]]
##### pageManage
![[Pasted image 20240815202626.png]]
![[Pasted image 20240815202833.png]]