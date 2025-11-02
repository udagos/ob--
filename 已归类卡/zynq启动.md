---
up:
  - "[[../moc/zynq|zynq]]"
---


# 清分机启动流程梳理 ([pdf](zotero://open-pdf/library/items/FJZ2PW99?page=119&annotation=8CCWF9EK))
主要包括BootRom、FSBL、Uboot、Linux内核、RT-Loader以及RTT系统。
![](../fujian/Pasted%20image%2020250711090954.png)
## BootRom
设备上电后自动开始 Stage0 Boot, 即执行片内 BootRom 中代码。BootRom 会初始化 CPU 和一些外设, 根据 MIO (多功能) 的配置从启动设备 (SD、QSPIA 等) 中**将 FSBL 拷贝到 OCM** (On Chip Memory)。
## FSBL
1.FSBLmain函数首先执行ps7_int () 函数, 初始化MIO、PLL、CLOCK、DDR以及外设。
	![](../fujian/Pasted%20image%2020250711091143.png)
2. FSBL将根据启动状态寄存器判断是采用的哪种启动模式。四种启动模式,分别是 QSPI,NOR,JTAG,SD 卡等模式
清分机正常启动采用 QSPI 模式。
3. 确定启动方式后,调用LoadBootImage函数将加载FPGA和uBoot。然后调用FsblHandoff()函数启动UBoot
	![](../fujian/Pasted%20image%2020250711091310.png)
## uboot
UBoot在清分机中主要用于**引导 Linux 系统**
UBOOT部分主要功能为初始化linux运行环境, 将ramdisk文件系统、devicetree读入DDR, 将linux内核读入DDR。并将启动参数传递给内核, 引导内核启动。
## APP 程序启动
**Linux内核启动后**主要执行sh脚本进行APP和RTT系统的启动
执行/media/mmc1/appfs/apps/byinit1. sh, 该脚本中**安装RTT引导程序rtloader. ko**。
![](../fujian/Pasted%20image%2020250711091732.png)


runapp. sh 脚本如下:

bymain. sh 脚本如下:
## rtloader
rtloader的功能较为简单, 首先进行地址映射, 然后**加载并启动rtthread. bin**
## 下载
![](../fujian/Pasted%20image%2020250711091929.png)


⦁	将需要升级的文件（uImage、devicetree. dtb、uramdisk. image. gz）放在tftpd64. exe所选的CurrentDirectory目录下。
⦁	在控制台中依次输入如下指令进行升级（每条指令操作完后观察是否执行完成后再下发下一条指令）
	tftpboot0x3000000uImage
	tftpboot0x2A00000devicetree. dtb
	tftpboot0x2000000uramdisk. image. gz
	bootm0x30000000x20000000x2A00000
	
用户名为root，密码为SDlinux2376
vi /media/mmc1/appfs/apps/byinit1. sh


[zynq工作总结](zynq工作总结.md)



E:\资料\linux_ROM\002_ROM\SourceData生成flashrootfile 用jk下载
