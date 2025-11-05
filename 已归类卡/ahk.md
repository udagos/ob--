---
up:
  - "[[../moc/MocTool]]"
---
[[moc 兴趣]]
#ed 

### 2. 设置脚本为开机启动

为了让脚本在系统启动时自动运行，你可以将脚本添加到 Windows 的启动文件夹中。

#### 步骤：

1. **创建快捷方式**：
    
    - 右键点击你的 `run_python_script.ahk` 文件，选择“创建快捷方式”。
        
    - 将创建的快捷方式重命名为 `Run Python Script` 或其他你喜欢的名称。
        
2. **移动快捷方式到启动文件夹**：
    
    - 按 `Win + R`，输入 `shell:startup`，然后按回车。这将打开 Windows 的启动文件夹。
        
    - 将你创建的快捷方式拖到这个文件夹中。
        

### 3. 确保脚本在后台运行

AutoHotkey 脚本默认会在后台运行，并且会持续监听定义的快捷键。你不需要做额外的设置来确保这一点。

### 4. 测试脚本

重启你的电脑，然后按下 `Ctrl + Shift + C` 快捷键，看看你的 Python 脚本是否被触发。

### 5. 调试和日志记录

为了确保脚本在后台正常运行，你可以在脚本中添加一些调试信息和日志记录。例如：
```
; 定义快捷键 Ctrl + Shift + C
^!c::
Log("AutoHotkey script is running")
Run "C:\Path\To\Python\python.exe C:\Path\To\Your\python_script.py"
return

Log(message) {
    FileAppend message "`n", "C:\Path\To\Your\logfile.txt"
}
```
这样，每次快捷键被触发时，都会在指定的日志文件中记录一条信息。

### 6. 使用任务管理器检查

你可以使用任务管理器来检查 AutoHotkey 进程是否在后台运行。按 `Ctrl + Shift + Esc` 打开任务管理器，然后在“进程”或“详细信息”选项卡中查找 `AutoHotkey.exe`。