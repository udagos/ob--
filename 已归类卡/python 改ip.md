---
up:
  - "[[../moc/moc软件工程]]"
---
```
import pyperclip  
import datetime  
import os  
  
# 定义固定目录  
file_dir = "E:\\shiyan"  
  
# # 定义固定文件名  
# file_name = "aa.log"  
#  
# # 确保目录存在  
# if not os.path.exists(file_dir):  
#     os.makedirs(file_dir)  
#  
# # 获取剪切板内容  
# clipboard_content = pyperclip.paste()  
#  
# # 构建文件的完整路径  
# file_path = os.path.join(file_dir, file_name)  
  
  
# 定义文件名前缀和扩展名  
file_prefix = "log_"  
file_extension = ".log"  
  
# 确保目录存在  
if not os.path.exists(file_dir):  
    os.makedirs(file_dir)  
  
# 获取当前时间戳  
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  
  
# 获取剪切板内容  
clipboard_content = pyperclip.paste()  
  
# 构建文件的完整路径，包括时间戳  
file_name = f"{file_prefix}{timestamp}{file_extension}"  
file_path = os.path.join(file_dir, file_name)  
  
  
  
# 将剪切板内容写入文件  
with open(file_path, "w", encoding="utf-8") as file:  
    file.write(clipboard_content)  
  
# 将文件路径中的反斜杠替换为正斜杠，并拼接成Markdown链接  
file_path_markdown = file_path.replace("\\", "/")  
markdown_link = f"[{file_name}](file://{file_path_markdown})"  
  
# 将Markdown链接复制到剪切板  
pyperclip.copy(markdown_link)  
  
print(f"文件已保存到：{file_path}")
```
internet协议版本4属性，如果是自动获得改为使用固定ip，否则改为自动获得


```
import subprocess  
  
  
def get_current_ip_settings():  
    # 获取当前的IP设置  
    result = subprocess.run(['netsh', 'interface', 'ipv4', 'show', 'config'], capture_output=True, text=True)  
    output = result.stdout  
  
    if "DHCP enabled:            Yes" in output:  
        return "自动获得 IP 地址"  
    else:  
        return "使用固定 IP 地址"  
  
  
def set_ip_settings(mode):  
    if mode == "自动获得 IP 地址":  
        subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'address', 'name="以太网"', 'source=dhcp'])  
    elif mode == "使用固定 IP 地址":  
        # 这里需要指定固定的IP地址、子网掩码、默认网关和DNS服务器  
        subprocess.run(  
            ['netsh', 'interface', 'ipv4', 'set', 'address', 'name="以太网"', 'source=static', 'addr=192.168.1.100',  
             'mask=255.255.255.0', 'gateway=192.168.1.1'])  
        subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dns', 'name="以太网"', 'source=static', 'addr=8.8.8.8',  
                        'register=primary'])  
        subprocess.run(['netsh', 'interface', 'ipv4', 'add', 'dns', 'name="以太网"', 'addr=8.8.4.4', 'index=2'])  
  
  
def toggle_ip_settings():  
    current_mode = get_current_ip_settings()  
    if current_mode == "自动获得 IP 地址":  
        set_ip_settings("使用固定 IP 地址")  
        print("已切换到使用固定 IP 地址")  
    else:  
        set_ip_settings("自动获得 IP 地址")  
        print("已切换到自动获得 IP 地址")  
  
  
if __name__ == "__main__":  
    toggle_ip_settings()
```
切换回自动可用

```
import subprocess  
import re  
  
def get_current_ip_settings():  
    # 获取当前的IP设置  
    result = subprocess.run(['netsh', 'interface', 'ipv4', 'show',  'config'], capture_output=True, text=True)  
    output = result.stdout  
  
    lines = output.splitlines()  
  
    for i in range(len(lines) - 1):  
        # print(lines[i])  
        if "以太网" in lines[i] and "是" in lines[i + 1]:  
            print("启用")  
            return "自动获得 IP 地址"  
  
    print("没启用")  
    return "使用固定 IP 地址"  
  
  
  
  
def set_ip_settings(mode):  
    if mode == "自动获得 IP 地址":  
        subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'address', 'name="以太网"', 'source=dhcp'])  
    elif mode == "使用固定 IP 地址":  
        # 设置固定的IP地址、子网掩码、默认网关和DNS服务器  
        result = subprocess.run(  
            ['netsh', 'interface', 'ipv4', 'set', 'address', 'name="以太网"', 'source=static', 'addr=192.168.1.126',  
             'mask=255.255.255.0'])  
        print(result.stdout)  
        print(result.stderr)  
  
  
  
def toggle_ip_settings():  
    current_mode = get_current_ip_settings()  
    if current_mode == "自动获得 IP 地址":  
        set_ip_settings("使用固定 IP 地址")  
        print("已切换到使用固定 IP 地址 192.168.1.126")  
    else:  
        set_ip_settings("自动获得 IP 地址")  
        print("已切换到自动获得 IP 地址")  
  
  
if __name__ == "__main__":  
    toggle_ip_settings()
```