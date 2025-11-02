---
up:
  - "[[../moc/linux|linux]]"
---
[moc 兴趣](moc%20兴趣)
#ed 

在 WSL2（Windows Subsystem for Linux 2）中，Linux 系统的根目录（`/`）是虚拟化的，它并不直接映射到 Windows 文件系统中的某个具体路径。WSL2 使用虚拟硬盘（VHD）来存储 Linux 文件系统，**因此它的根目录实际上是存储在 Windows 中的一个虚拟磁盘文件中。**

### WSL2 根目录的存储位置
WSL2 的根目录通常存储在以下路径：
```
C:\Users\<Windows用户名>\AppData\Local\Packages\<WSL发行版包名>\LocalState\ext4.vhdx
```
其中：
- `<Windows用户名>` 是你的 Windows 用户名。
- `<WSL发行版包名>` 是你安装的 Linux 发行版的包名，例如：
  - 对于 **Ubuntu**，可能是 `CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc`。
  - 对于 **Debian**，可能是 `Debian.DeveloperEdition_76v4gfsz19hv5`。

### 如何找到具体的包名
可以通过以下方法找到具体的发行版包名：
1. 打开 PowerShell 或命令提示符。
2. 输入以下命令：
   ```bash
   wsl -l -v
   ```
   这将列出所有安装的 WSL 发行版及其状态。

3. 如果需要找到具体的包名，可以使用以下命令：
   ```bash
   Get-AppxPackage | Where-Object { $_.Name -like "*Ubuntu*" }
   ```
   将 `*Ubuntu*` 替换为你安装的发行版名称，例如 `*Debian*` 或 `*Fedora*`。

### 注意事项
1. **不要直接修改 `.vhdx` 文件**：
   - WSL2 的根目录存储在虚拟硬盘文件（`.vhdx`）中，直接修改这个文件可能会损坏 WSL 文件系统。
   - 如果需要访问或修改文件，建议通过 WSL 终端操作。

2. **访问 WSL2 文件系统**：
   - 在 WSL2 中，你可以通过 `/` 访问根目录。
   - 在 Windows 中，可以通过 `\\wsl$\<发行版名称>` 访问 WSL2 的文件系统。

3. **查看 WSL2 文件系统路径**：
   - 如果需要在 Windows 中查看 WSL2 的文件路径，可以使用以下命令：
     ```bash
     wsl --update-ux
     ```
   - 然后在 Windows 文件资源管理器中输入：
     ```
     \\wsl$\<发行版名称>
     ```

### 总结
WSL2 的根目录实际上存储在 Windows 的一个虚拟硬盘文件（`.vhdx`）中，而不是直接映射到某个具体的文件夹路径。如果你需要访问 WSL2 的文件系统，建议通过 WSL 终端或 Windows 的 `\\wsl$` 网络路径进行操作，而不是直接修改 `.vhdx` 文件。

# 2 共享
在 Windows Subsystem for Linux (WSL) 中，可以通过多种方式实现 Windows 和 Linux 系统之间的文件共享。以下是常见的方法：

### 1. **Windows 访问 WSL 文件**
#### 方法 1：通过网络路径访问
==WSL 的文件系统可以通过网络路径 `\\wsl$` 访问==。在 Windows 文件资源管理器或命令行中输入以下路径即可访问：
```
\\wsl$\<发行版名称>\
```
例如：
```
\\wsl$\Ubuntu\home\<用户名>
```
优点是无需额外配置，文件路径自动挂载且无权限问题。

#### 方法 2：通过挂载路径访问
**WSL 的文件系统实际存储在 Windows 用户目录下：**
```
C:\Users\<用户名>\AppData\Local\Packages\<WSL发行版ID>\LocalState\rootfs
```
**但不建议直接修改此路径下的文件，以免损坏 WSL 文件系统。**

### 2. **WSL 访问 Windows 文件**
==WSL 会自动挂载 Windows 的文件系统，挂载路径为 `/mnt/<盘符>`。==例如：
- `C:\` 对应 `/mnt/c`
- `D:\` 对应 `/mnt/d`

在 WSL 中可以通过以下方式访问和操作 Windows 文件：
```bash
ls /mnt/c/Users/<用户名>/Documents
cp /mnt/c/Users/<用户名>/Documents/文件.txt ~/
```


### 3. **实现 WSL 和 Windows 共享目录**
#### 方法 1：在 WSL 中创建软链接
如果需要频繁访问某些 Windows 目录，可以在 WSL 中创建软链接。例如：
```bash
ln -s /mnt/c/Users/<用户名>/Documents ~/windows-documents
```
之后可以直接通过 `~/windows-documents` 访问。

#### 方法 2：共享 WSL 的目录给 Windows
在 WSL 中创建一个目录，例如：
```bash
mkdir ~/shared-folder
```
然后在 Windows 中通过 `\\wsl$` 访问：
```
\\wsl$\Ubuntu\home\<用户名>\shared-folder
```
。

### 4. **在 WSL 和 Windows 间传输文件**
#### 方法 1：直接复制文件
使用 `cp` 或 `mv` 命令在 WSL 和 Windows 之间传输文件。例如：
- 从 Windows 复制到 WSL：
  ```bash
  cp /mnt/c/Users/<用户名>/Desktop/文件.txt ~/
  ```
- 从 WSL 复制到 Windows：
  ```bash
  cp ~/文件.txt /mnt/c/Users/<用户名>/Desktop/
  ```
。

#### 方法 2：使用 `explorer.exe` 打开 WSL 文件夹
在 WSL 终端中输入以下命令，可以直接用 Windows 文件资源管理器打开当前路径：
```bash
explorer.exe .
```
。

### 5. **其他高级方法**
#### 方法 1：使用 `rsync` 同步文件
安装 `rsync` 后，可以使用以下命令同步文件：
```bash
rsync -av /mnt/c/Users/<用户名>/Documents/file.txt /home/<用户名>/
```
。

#### 方法 2：使用 Docker Desktop 的文件共享功能
如果使用 Docker Desktop，可以通过其设置中的 `File Sharing` 功能，将 Windows 目录共享到 WSL2 中。

通过以上方法，可以轻松实现 WSL 和 Windows 之间的文件共享和交互。根据具体需求选择合适的方式即可。


