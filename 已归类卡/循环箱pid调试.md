---
up:
  - "[[../moc/work|work]]"
---
[moc pid](moc%20pid)
#ed 


## 让循环箱也能指令设置 pid
把 workin 和 RcbInitHandle 给屏蔽掉



## 问题
为什么无超跑不会出现有超的那种起始速度乱的现象


循环箱的多线程如果用全局变量或结构体多个线程不一起修改么



void OsTaskRecycleCashBox(void *Parameter)
{
    GATE_HANDLE_MSG TaskMsg;
    RCB_INDEX RcbId = (RCB_INDEX)(U 32) Parameter;

有钞的 pid 可以在入朝流程 RcbWorkInFlowStartHandle 中初始化，不断迭代



## 循环箱子 pid
### 无 pid
![[Pasted image 20240823201703.png]]
### i
020
![[Pasted image 20240823201740.png]]
050
![[Pasted image 20240823201810.png]]
0 10 0
![[Pasted image 20240823202243.png]]
震荡的剧烈
### d
5 00 
![[Pasted image 20240823201842.png]]
15 00
![[Pasted image 20240823201906.png]]
收敛于目标速度
25 00
![[Pasted image 20240823202158.png]]
震荡变大


第二部组合
15 02 00
![[Pasted image 20240823203603.png]]
震荡还是大，改小 pi
10 2 0

## 问题
![[Pasted image 20240824094606.png]]
原因起始速度不一样，中间没有降低到最低

以前的
![[Pasted image 20240824100633.png]]
速度都能到最低

为什么现在速度降低不到最低，是起始速度导致这种震荡么，争纸？
	因为通道内钞间距变化了？
	刹车改变了？
	触发节点?


上一版和现在通道有纸为什么往里面挪
之前循环箱出钞到了有超传感器会受到通道电机的干涉，所以初始化没法出钞



之前循环钞箱折纸，因为传动问题速度不对
