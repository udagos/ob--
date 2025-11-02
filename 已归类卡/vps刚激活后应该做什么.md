---
up:
  - "[[vps]]"
---
# vps刚激活后应该做什么
好的，这是一个非常重要的问题。刚刚激活的VPS就像一间刚拿到钥匙的“毛坯房”，虽然能用，但既不安全也不方便。

在您安装任何网站、代理或应用**之前**，强烈建议您按照以下清单，花15-30分钟对服务器进行一次全面的**基础安全设置和初始化**。这能避免90%以上的常见安全风险。

---

### VPS 新手服务器初始化安全清单 (必做)

这份清单按照操作的优先级排序，请依次执行。

ssh -p 40984 root@38.150.3.156

#### **第三阶段：强化 SSH 安全 (核心)**

这是提升服务器安全性的关键一步，我们将用更安全的密钥登录完全取代密码登录。

6. **配置 SSH 密钥登录**
    
    - A. 在你的本地电脑上生成密钥对：
        
        打开你自己的电脑（不是VPS）的终端，运行以下命令。如果已经有密钥了，可以跳过。
        
        Bash
        
        ```
        ssh-keygen -t rsa -b 4096
        ```
        
        一路按回车即可。
        
    - B. 将公钥复制到你的VPS服务器：
        
        还是在你的本地电脑上，运行以下命令。它会自动将你的公钥上传到服务器上你新创建的那个用户的家中。
        
        Bash
        
        ```
        ssh-copy-id your_username@你的VPS_IP地址
        ```
        
        这个过程会要求你输入一次新用户的密码。
        
    - C. 测试密钥登录：
        
        现在，新开一个终端窗口，尝试用新用户直接登录，看看是否不再需要密码。
        
        Bash
        
        ```
        ssh your_username@你的VPS_IP地址
        ```
        
        如果直接登录成功，说明密钥配置正确！
        
6. ==禁用密码登录和 Root 远程登录 (安全加固)==
    
    <br>
    
    ⚠️ 警告：在确认第6步的密钥登录成功之前，绝对不要执行此步骤，否则你可能会被锁在服务器外面！
    
    <br>
    
    - 用新用户登录到你的VPS上，编辑SSH配置文件：
        
        Bash
        
        ```
        sudo nano /etc/ssh/sshd_config
        ```
        
    - 找到并修改以下三项内容（如果没有就添加）：
        
        Ini, TOML
        
        ```
        PermitRootLogin no
        PasswordAuthentication no
        PubkeyAuthentication yes
        ```
        
    - 保存文件 (在`nano`编辑器中，按 `Ctrl+X`，然后按 `Y`，再按回车)。
        
    - 重启SSH服务使配置生效：
        
        Bash
        
        ```
        sudo systemctl restart sshd
        ```
        

---

#### **第四阶段：基础环境配置**

8. 配置防火墙 (UFW)
    
    一个好的防火墙能阻止绝大部分恶意扫描和攻击。ufw 是Ubuntu/Debian上最简单的防火墙。
    
    Bash
    
    ```
    # 允许我们刚刚配置好的SSH连接 (非常重要！)
    sudo ufw allow OpenSSH
    
    # 如果你要建网站，打开HTTP和HTTPS端口
    sudo ufw allow http
    sudo ufw allow https
    
    # 启用防火墙
    sudo ufw enable
    # 提示时输入 y 确认
    ```
    
9. 设置正确的时区
    
    这对于查看日志和运行定时任务至关重要。
    
    Bash
    
    ```
    # 查看所有可用时区
    timedatectl list-timezones
    
    # 设置你的时区 (例如设置为上海)
    sudo timedatectl set-timezone Asia/Shanghai
    ```
    
10. **(可选) 安装常用工具**
    
    Bash
    
    ```
    # htop - 更好看的进程监视器
    # fail2ban - 自动阻止SSH暴力破解的IP
    # unzip - 解压zip文件
    sudo apt install htop fail2ban unzip -y
    ```
    

---

**恭喜您！**

完成以上步骤后，您的VPS现在已经不再是脆弱的“毛坯房”，而是一个**安全、稳定、配置好个人专属访问权限的坚实地基**。

现在，您可以放心地在上面安装Docker、网站环境、代理服务或任何您想要的应用了。