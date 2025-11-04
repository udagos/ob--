1、设备共有3块FPGA，分别为7010PL，上部安路FPGA，下部安路FPGA，其中7010PL为7010内部FPGA，==与A核之间通过总线直接相连==。
==上部安路FPGA与7010PL直接相连，中间通讯自定义协议==。下部安路FPGA与7010PL直接相连，中间通讯自定义协议。==两片安路FPGA均由PL进行控制。==
2、==PL加载为在FSBL阶段从FLASH加载数据，通过Fabric加载==。
==上下部安路FPGA在设备初始化阶段进行加载==，。Linux从EMMC中加载数据与RTT通过内存共享进行加载，==加载时由7010 PS端SPI进行加载。==



安陆
==从动串行（SS）模式下，FPGA可以通过MCU进行加载==。 TD软件可以生成bin文件（EG4X20BG256、 EG4A20NG88）或者 rbf 文件（EG4A20BG256）用于MCU加载

MCU 通过CCLK、DIN信号使用串行方式将数据写入FPGA。EAGLE FPGA芯片在每个CCLK的上升沿接收数据，数据发送完成后，DONE拉高表示配置完成，如果配置出错，会将INITN/INIT_B信号拉低。

图2-8-4 所示。PROGRAMN拉低后，INITN信号被拉低，表示芯片开始初始化，芯片初始化完成后， INITN 回到高电平，配置开始，FPGA在时钟的上升沿采集配置数据，在配置完成之后，DONE信号变高，表示配置成功，芯片开始工作。

![](../fujian/Pasted%20image%2020250305094059.png)
EG4X20BG256、EG4A20NG88、EG4X20LG144从动串行配置方式的时序如图2-8-5所示。
![](../fujian/Pasted%20image%2020250305094111.png)
![](../fujian/Pasted%20image%2020250305094134.png)
EG4器件使用从动串行配置模式进行加载时，done信号拉高后CCLK至少需要再维持6us加10个周期的时钟输出，才能保证EG4A20BG256器件的D[0]/DIN/ MISO、D[1]/ MOSI、SPICSN、CSON/DOUT、 CCLK信号管脚或EG4X20BG256、EG4A20NG88、EG4X20LG144器件的D[0]/DIN/ MISO、CSI_B/MOSI、CSO_B、 DOUT、CCLK信号管脚进入用户模式。



# 7010 
## 地址映射
综合系统级地址映射如表 4‐1 所示。阴影条目表示地址范围是保留的, 不应访问。表 4‐2标识保留地址
![](../fujian/Pasted%20image%2020250305095549.png)

![](../fujian/Pasted%20image%2020250305095608.png)
### ps IO外设
I/O 外设寄存器通过 32 位 APB 总线访问
![](../fujian/Pasted%20image%2020250305095823.png)