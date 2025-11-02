---
up:
  - "[[../moc/瑞芯微|瑞芯微]]"
---
# `armbian-firmware-full`

### `armbian-firmware-full`: 解锁您 Armbian 设备的完整硬件潜能

在 Armbian 系统中，`armbian-firmware-full` 指的是一个软件包（package），它提供了比标准 Armbian 镜像中自带的固件更为全面的固件集合。简而言之，它是一个“全功能”的固件包，旨在为各种外围硬件设备提供最广泛的驱动支持。

#### `armbian-firmware-full` 与 `armbian-firmware` 的区别

标准的 Armbian 系统为了保持镜像的精简，通常只包含一个名为 `armbian-firmware` 的基础固件包。这个基础包主要涵盖了单板计算机（SBC）板载芯片（如 Wi-Fi 和蓝牙模块）以及一些最常见外部设备的固件。

然而，当您连接一些非标配或较少见的硬件时（例如特定型号的 USB Wi-Fi 网卡、蓝牙适配器、电视卡或某些 NVMe 硬盘），系统可能会因为缺少相应的固件而无法识别或正常驱动这些设备。

这时，`armbian-firmware-full` 就派上了用场。它包含了大量额外的固件文件，安装后可以显著提升系统的硬件兼容性。

**核心区别如下：**

|特性|`armbian-firmware` (默认)|`armbian-firmware-full` (可选)|
|---|---|---|
|**目标**|保持系统镜像小巧、精简|提供最大化的硬件兼容性|
|**包含内容**|仅包含板载芯片和常用设备的固件|包含一个庞大而全面的固件集合|
|**适用场景**|适用于仅使用基础功能和常见外设的用户|适用于需要连接各种或特定非板载硬件的用户|
|**大小**|较小|较大，会占用更多的存储空间|

#### 何时需要安装 `armbian-firmware-full`？

您可能需要安装此软件包的常见情况包括：

- **Wi-Fi 或蓝牙无法工作**：您插入了一个 USB 无线网卡或蓝牙适配器，但系统无法识别。
    
- **外围设备无响应**：连接了其他类型的硬件（如摄像头、声卡、DVB 电视棒等），但设备没有按预期工作。
    
- **系统日志提示缺少固件**：通过 `dmesg` 命令查看内核日志时，发现有 "failed to load firmware" (加载固件失败) 的错误信息。
    

#### 如何安装 `armbian-firmware-full`？

您可以通过 `apt` 包管理器在终端中轻松安装它。

**安装步骤：**

1. **更新软件包列表：**
    
    Bash
    
    ```
    sudo apt update
    ```
    
2. **安装 `armbian-firmware-full`：**
    
    Bash
    
    ```
    sudo apt install armbian-firmware-full
    ```
    

注意：

在某些情况下，armbian-firmware-full 可能会与默认的 armbian-firmware 或来自 Debian/Ubuntu 官方源的其他固件包（如 firmware-misc-nonfree）产生冲突。如果安装时提示冲突，您可能需要先卸载冲突的包，然后再进行安装。例如：

Bash

```
sudo apt remove armbian-firmware
sudo apt install armbian-firmware-full
```

安装完成后，建议**重启您的设备**，以确保新的固件能够被内核正确加载。



# armbian config
好的，除了安装额外的固件包之外，Armbian 还有许多非常实用且能极大提升使用体验的技巧。这些技巧涵盖了系统配置、性能优化、网络管理和硬件交互等多个方面。

以下是一些值得掌握的 Armbian 实用技巧，无论您是新手还是经验丰富的用户，都能从中受益。

### 1. 充分利用 `armbian-config` 图形化配置工具

这是 Armbian 的核心工具，也是最强大的技巧之一。您不需要记住复杂的命令，只需在终端中输入：

Bash

```
sudo armbian-config
```

即可进入一个图形化的菜单。在这里，您可以轻松完成以下操作：

- **System (系统设置)**:
    
    - **CPU afrilication (CPU 调频)**: 更改 CPU 的工作模式（如 `performance` 性能模式或 `ondemand` 按需模式）来平衡性能与功耗。
        
    - **Hardware (硬件配置)**: 启用或禁用特定的硬件接口，如 SPI, I2C, UART 等，这对于连接传感器等外设至关重要。
        
    - **Install (安装桌面环境)**: 快速安装或切换不同的桌面环境，如 XFCE, GNOME, KDE 等。
        
- **Networking (网络设置)**:
    
    - **IP**: 配置静态 IP 地址或切换为 DHCP。
        
    - **Hotspot**: 轻松将您的设备变成一个 Wi-Fi 热点。
        
- **Personal (个性化设置)**:
    
    - 更改时区、语言和主机名。
        

`armbian-config` 是您进行系统级配置的首选工具，安全且高效。

### 2. 优化系统性能与散热

#### a. 调整 CPU 频率和工作模式

如上所述，通过 `armbian-config` > `System` > `CPU` 可以调整 CPU 工作模式。对于需要持续高性能的场景（如服务器应用），可以设置为 `performance` 模式。日常使用 `ondemand` 或 `schedutil` 则更为节能。

#### b. 监控硬件状态

使用 `armbianmonitor` 命令可以实时监控 CPU/内存使用率、温度和频率等关键信息。

Bash

```
sudo armbianmonitor -m
```

这对于诊断性能问题或检查散热情况非常有用。

#### c. 将系统迁移到 eMMC 或 NVMe

如果您的开发板同时拥有 microSD 卡和 eMMC/NVMe 存储，强烈建议将系统从 microSD 卡迁移到速度更快的 eMMC 或 NVMe 上。这可以极大地提升系统的响应速度和 I/O 性能。

您可以使用 `armbian-config` 中的 `System` > `Install` > `Boot from eMMC/NVMe` 选项来完成这个操作。

### 3. 网络与安全技巧

#### a. 设置静态 IP 地址

对于服务器应用，一个固定的内网 IP 地址是必需的。同样，在 `armbian-config` > `Networking` > `IP` 中可以轻松设置。

#### b. SSH 安全加固

默认的 SSH 配置可能不够安全，您可以进行以下加固：

- **禁用密码登录，改用密钥登录**：这是最有效的安全措施之一。
    
- **修改默认 SSH 端口**：将默认的 22 端口改为其他端口，可以有效减少恶意扫描。
    
- **禁用 root 用户远程登录**。
    

这些配置都可以通过编辑 `/etc/ssh/sshd_config` 文件来完成。

### 4. 高级与日常使用技巧

#### a. 使用 `armbian-install` 安装 Docker

Armbian 对 Docker 容器化支持非常好。您可以利用 `armbian-config` > `Software` > `Softy` 来一键安装 Docker，轻松部署各种应用，如 Home Assistant, AdGuard Home, Pi-hole 等。

#### b. 管理内核和引导加载器 (U-Boot)

Armbian 提供了多个内核版本（稳定版、最新版等）供选择。您可以通过 `armbian-config` 切换内核，以获得对新硬件的支持或更高的系统稳定性。

**警告**：切换内核是高级操作，请在了解风险的情况下进行。

#### c. 冻结内核更新

有时，新版本的内核可能会引入不兼容的问题。如果您当前的系统运行非常稳定，不希望内核自动更新，可以冻结它：

Bash

```
sudo armbian-add-overlay kernel-freeze.dts
```

或者使用 `armbian-config` > `System` > `Freeze` 选项。

#### d. 使用 ZRAM 提升小内存设备性能

Armbian 默认启用了 ZRAM，它会在内存中创建一个压缩的交换分区。这对于内存较小（如 1GB 或 2GB）的设备尤其有用，可以有效提升多任务处理能力和系统响应速度。您可以通过 `zramctl` 命令查看其状态。

### 总结

掌握这些技巧，您将能更好地发挥 Armbian 系统的强大功能，并根据您的具体需求进行深度定制和优化。**首要建议始终是先探索 `armbian-config`**，因为它集合了最常用和最强大的功能，能帮您解决大部分配置问题。