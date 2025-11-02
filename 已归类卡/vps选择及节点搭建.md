---
up:
  - "[[vps]]"
---
[uuuvps怎么样？实测下联通AS4837线路+原生IP的洛杉矶VPS](https://www.zhujiceping.com/71731.html)
vmiss
evoxt  3dao
  [搬瓦工biggerbox pro限量款VPS详细测评，电信CN2/联通&移动CMIN2](https://www.zhujiceping.com/77623.html)
次
	zgo




**落地鸡**家庭**原生IP**，**线路鸡**大概率**机房ip**
流媒体可能对一些机房ip屏蔽




[国外主机测评-国外VPS、国外云服务器、国外独立服务器](https://www.zhujiceping.com/)
[测评版块](https://www.nodeseek.com/categories/review)


![vps刚激活后应该做什么](vps刚激活后应该做什么.md)




# 在vps上搭建节点

好的，在VPS上“搭建节点”这个说法通常指的是创建一个代理服务器，用于加密网络流量、绕过地理限制或增强个人隐私。最常见的类型是基于 V2Ray/Xray 和 Shadowsocks 等协议的代理节点。

本指南将为您详细介绍如何在您的VPS上搭建一个节点，主要以目前最流行、功能最强大的 **Xray (V2Ray-core 的继任者)** 为例，因为它兼容V2Ray的配置和客户端。

---

### **重要声明**

在开始之前，请务必了解并遵守您所在国家/地区以及VPS服务商所在地的法律法规。使用代理服务器进行任何非法活动都可能导致法律后果或VPS被封禁。本指南仅用于技术学习和研究目的。

---

### **第一步：准备工作**

在搭建节点之前，您需要准备好以下几样东西：

1. **一台VPS:**
    
    - 您已经有了一台VPS。请确保您拥有`root`权限或一个具有`sudo`权限的用户。
        
    - **操作系统:** 推荐选择 **Ubuntu 20.04/22.04** 或 **Debian 10/11** 的最新LTS（长期支持）版本，因为它们的社区支持最好，本教程也将以此为基础。
        
    - **IP地址:** 记下您的VPS的公网IP地址。
        
2. **SSH 客户端:**
    
    - 用于连接到您的VPS。Windows用户可以使用 [PuTTY](https://www.putty.org/)、[MobaXterm](https://mobaxterm.mobatek.net/) 或 Windows Terminal。macOS和Linux用户可以直接使用系统自带的终端（Terminal）。
        
3. **一个域名 (可选但强烈推荐):**
    
    - **为什么需要？** 直接使用IP地址搭建节点很容易被识别和封锁。使用域名并开启TLS（HTTPS）可以极大地提高连接的稳定性和安全性，将其伪装成正常的网站流量。
        
    - **如何获取？** 您可以在 [Namecheap](https://www.namecheap.com/)、[GoDaddy](https://www.godaddy.com/) 等域名注册商处购买一个便宜的域名。
        

### **第二步：连接VPS并解析域名**

1. 连接到您的VPS:
    
    打开您的SSH客户端，使用以下命令登录您的服务器（将YOUR_VPS_IP替换为您的真实IP）：
    
    Bash
    
    ```
    ssh root@YOUR_VPS_IP
    ```
    
    输入您的密码完成登录。
    
2. 更新系统:
    
    登录后，首先更新系统软件包，这是一个好习惯。
    
    Bash
    
    ```
    apt update && apt upgrade -y
    ```
    
1. ==**解析域名 (如果您准备了域名):**==
    
    - 登录到您的域名注册商的管理后台。
        
    - 找到DNS或域名解析设置。
        
    - ==添加一条 **A 记录**，将您的域名（或一个子域名，如 `proxy.yourdomain.com`）指向您VPS的IP地址。==
        
    - 等待几分钟到半小时，让DNS记录生效。您可以使用`ping yourdomain.com`命令来检查是否解析成功。
        

### **第三步：使用一键脚本安装 Xray (推荐)**

对于新手来说，手动配置Xray可能比较复杂。社区开发者提供了非常强大且易于使用的==一键安装脚本，可以自动完成安装、配置、申请SSL证书等所有步骤==。

这里我们==推荐使用 **`XrayR-project/XrayR`** 或 **`XTLS/Xray-install`** 脚本。我们以 `XTLS/Xray-install` 为例==，因为它最接近官方且功能纯粹。

1. 执行安装命令:
    
    在您的VPS终端中，复制并粘贴以下命令，然后按回车执行：
    
    Bash
    
    ```
    bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
    ```
    
    这个脚本会自动下载最新版本的Xray核心并安装到您的系统中。
    
2. 验证安装:
    
    安装成功后，您可以使用以下命令来查看Xray的版本，以确认安装成功：
    
    Bash
    
    ```
    /usr/local/bin/xray --version
    ```
    

### **第四步：配置 Xray (核心步骤)**

Xray的配置文件位于 `/usr/local/etc/xray/config.json`。我们需要编辑这个文件来设置我们的节点。==最常用和推荐的协议是 **VLESS + TCP + XTLS Vision** 或 **VLESS + WebSocket + TLS**。==

#### **方案A: VLESS + WebSocket + TLS (伪装成网站)**

这是目前最主流、兼容性最好的伪装方案。它可以将流量伪装成正常的HTTPS网站访问，穿透性很强。

1. 安装 Nginx (Web服务器):
    
    我们需要**Nginx来处理网站流量和转发流量给Xray。**
    
    Bash
    
    ```
    apt install nginx -y
    ```
    
2. 申请SSL证书:
    
    我们需要一个**SSL证书来启用HTTPS。使用 acme.sh 脚本可以自动申请免费的Let's Encrypt证书。**
    
    Bash
    
    ```
    # 安装 acme.sh
    curl https://get.acme.sh | sh
    source ~/.bashrc
    
    # 申请证书 (将 yourdomain.com 替换为您的真实域名)
    acme.sh --issue -d yourdomain.com --standalone
    ```
    
    证书文件会被保存在 `~/.acme.sh/yourdomain.com/` 目录下。
    
3. 配置 Xray (config.json):
    
    使用文本编辑器（如nano）打开配置文件：
    
    Bash
    
    ```
    nano /usr/local/etc/xray/config.json
    ```
    
    将里面的内容 **全部删除**，然后粘贴以下配置模板。
    
    **请务必修改以下三处:**
    
    - `"id"`: 您的用户UUID，可以从 [UUID Generator](https://www.uuidgenerator.net/) 网站生成一个新的。这是您的连接凭证。
        
    - 将 `"path"` 中的 `/your_websocket_path` 改成一个您自定义的、不容易被猜到的路径（例如 `/myapp-123`）。
        
    
    JSON
    
    ```
    {
      "log": {
        "loglevel": "warning"
      },
      "inbounds": [
        {
          "listen": "127.0.0.1",
          "port": 10000, // 监听本地端口
          "protocol": "vless",
          "settings": {
            "clients": [
              {
                "id": "替换成你自己的UUID", // ！！！必须修改
                "level": 0
              }
            ],
            "decryption": "none"
          },
          "streamSettings": {
            "network": "ws",
            "wsSettings": {
              "path": "/your_websocket_path" // ！！！必须修改
            }
          }
        }
      ],
      "outbounds": [
        {
          "protocol": "freedom",
          "settings": {}
        }
      ]
    }
    ```
    
    修改完毕后，按 `Ctrl + X`，然后按 `Y` 和回车保存文件。
    
4. 配置 Nginx:
    
    编辑Nginx的默认配置文件：
    
    Bash
    
    ```
    nano /etc/nginx/sites-available/default
    ```
    
    同样，将里面的内容 **全部删除**，粘贴以下配置。
    
    **请务必修改以下四处:**
    
    - `server_name`: 替换成您的域名。
        
    - `ssl_certificate` 和 `ssl_certificate_key`: 替换成您刚刚申请到的证书路径。
        
    - `location /your_websocket_path`: 路径要和您在`config.json`中设置的完全一样。
        
    
    Nginx
    
    ```
    server {
        listen 80;
        listen [::]:80;
        server_name yourdomain.com; # 替换成你的域名
        # 将所有HTTP请求重定向到HTTPS
        return 301 https://$host$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name yourdomain.com; # 替换成你的域名
    
        ssl_certificate /root/.acme.sh/yourdomain.com/fullchain.cer; # 替换成你的证书路径
        ssl_certificate_key /root/.acme.sh/yourdomain.com/yourdomain.com.key; # 替换成你的私钥路径
        ssl_session_timeout 1d;
        ssl_session_cache shared:MozSSL:10m;
        ssl_session_tickets off;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    
        location /your_websocket_path { # ！！！必须和Xray配置中的path一致
            if ($http_upgrade != "websocket") {
                return 404;
            }
            proxy_pass http://127.0.0.1:10000; # 转发到Xray的监听端口
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    
        # （可选）添加一个伪装网站
        location / {
            root /var/www/html;
            index index.html index.htm;
        }
    }
    ```
    
    保存并退出。
    
5. **重启服务:**
    
    Bash
    
    ```
    systemctl restart xray
    systemctl restart nginx
    ```
    

### **第五步：客户端配置**

现在您的服务器端已经搭建好了。您需要在您的设备（电脑、手机）上安装客户端软件来连接。

- **全平台推荐:** **v2rayN** (Windows), **v2rayNG** (Android), **Shadowrocket** / **Quantumult X** / **Stash** (iOS), **V2RayX** / **V2RayU** (macOS)
    

以 `v2rayN` (Windows) 为例，您的配置参数如下：

- **地址 (Address):** 您的域名 (`yourdomain.com`)
    
- **端口 (Port):** `443`
    
- **用户ID (User ID / UUID):** 您在`config.json`中设置的UUID
    
- **传输协议 (Network):** `ws` (WebSocket)
    
- **伪装路径 (Path):** 您设置的路径 (`/your_websocket_path`)
    
- **底层传输安全 (TLS):** 开启 `tls`
    

填写好这些信息后，您就可以连接并开始使用了。

---

### **其他方案和提示**

- **Shadowsocks:** 是一个更轻量级的协议，配置简单，但流量特征相对明显。您同样可以使用一键脚本在VPS上快速部署。
    
- **BBR加速:** Google BBR是一个TCP拥塞控制算法，可以显著提升服务器的网络速度。在较新的Linux内核中（如Ubuntu 20.04+）已默认编译，您只需执行几条命令即可开启。
    
- **定期更新:** 保持Xray核心和系统软件的更新，以获得最新的性能改进和安全修复。
    
- **使用管理面板:** 如果您觉得手动配置很麻烦，可以考虑使用一些图形化的管理面板（如 `3X-UI`），它们可以在网页上管理用户、查看流量，并自动生成配置链接或二维码，非常方便。
    

希望这份详细的指南能帮助您成功搭建自己的VPS节点！


# tls_vision与xtls
好的，我们来详细解释一下 TLS Vision 和 XTLS 这两个在网络代理工具（尤其是 Xray 项目）中常见的技术术语，以及它们之间的关系和区别。

简单来说，它们的关系是：**XTLS 是一种底层的、具有开创性的技术协议，而 Vision 是在 XTLS 协议基础上发展出来的一种具体的流控（flow control）模式。** 你可以将 XTLS 理解为一种创新的加密数据处理方法，而 Vision 则是该方法的一种更成熟、更优化的实现方式。

下面我们进行详细的拆解说明。

### 什么是 XTLS？

XTLS 的全称是 "Extended TLS"，即扩展的 TLS。它的诞生主要是为了解决一个长期以来在代理技术中存在的性能和特征问题，即 **“TLS in TLS”**。

- **传统代理的问题 (TLS in TLS)**：在传统的代理模式下，比如 VLESS + TLS，你的数据首先会被协议（如 VLESS）本身进行一次处理，然后为了伪装成正常的网页浏览，整个数据流（包括 VLESS 的数据）会被再次放进一个标准的 TLS 加密通道中。这就好比你把一个已经加了密的箱子，又放进另一个同样加了密的箱子里。这种“双重加密”不仅会带来额外的性能开销（CPU 需要做更多加密解密工作），更重要的是，它会形成一种独特的流量特征，可能会被高级的防火墙（GFW）识别并加以干扰或阻断。
    
- **XTLS 的解决方案**：XTLS 协议的作者创新地提出，既然内外两层都是 TLS 加密，为什么我们不能想办法“合并”或者“减少”一层呢？XTLS 通过对 TLS 记录（TLS Record）进行处理，巧妙地将需要代理的数据直接“插入”到外层的 TLS 数据流中，而无需对其进行再次的 TLS 加密。这样一来，它就**消除了“TLS in TLS”的特征**，使得流量看起来更像是一个普通的、长时间活动的 HTTPS 网站连接，同时因为减少了一层加密，也**显著提升了数据转发的性能**。
    

### 什么是 TLS Vision？

随着 XTLS 技术的不断发展和完善，开发者在原始的 XTLS 基础上进行了优化和改进，推出了更强大的流控模式，其中最核心、最被广泛使用的就是 **Vision**。

在 Xray 的配置中，你通常会看到 `flow` 这个选项，其值被设置为 `xtls-rprx-vision`。这里的 `vision` 就是我们所说的 TLS Vision。

Vision 的主要特点和优势包括：

1. **更强的伪装性**：Vision 在处理数据流时，引入了更精细的填充（Padding）和读取机制（`rprx` 代表 `read-proxy, read-exactly`）。它能够更智能地处理数据包的长度和读取方式，使得数据流在统计学上更难被识别。简单来说，它让你的代理流量在“行为”上更像真实的网页浏览。
    
2. **集成了 XTLS 的核心优势**：Vision 本质上是 XTLS 协议的一种实现和演进，因此它完全继承了 XTLS 解决“TLS in TLS”问题的能力，具有高性能和低特征的优点。
    
3. **内建强大的功能**：Vision 模式会自动启用一些高级功能，如 `Splice`（零拷贝），在符合条件的系统上可以进一步提升数据转发效率，降低延迟。
    

### 总结：核心区别与关系

|特性|XTLS|TLS Vision (`xtls-rprx-vision`)|
|---|---|---|
|**定义**|一种底层的、旨在消除“TLS in TLS”问题的技术协议。|基于 XTLS 协议的一种更高级、更完善的流控模式。|
|**关系**|基础技术，是 Vision 的前身和核心。|XTLS 的一种具体实现和演进版本，功能更强。|
|**配置**|在早期版本中可能直接指代该技术，现在通常通过具体的 `flow` 模式来体现。|在 Xray 配置中，通过设置 `flow: "xtls-rprx-vision"` 来启用。|
|**主要优势**|解决了双重加密带来的性能和特征问题。|继承 XTLS 优势的同时，通过更精细的流控和填充机制，提供了更强的伪装性和安全性。|
|**当前使用**|作为一个概念依然存在，但在实际配置中，**基本已被 Vision 全面取代**。|**当前 Xray 项目在使用 VLESS + TCP + TLS 方案时的主流和推荐选择**。|

**通俗的比喻：**

- 如果说 **XTLS** 是发明了“喷气式发动机”这项革命性技术。
    
- 那么 **TLS Vision** 就是基于这项技术制造出的一款性能优异、稳定可靠的“F-22 猛禽战斗机”。
    

因此，在当下的网络环境中，当你配置 Xray 并且希望使用这种高效、高伪装性的 TLS 代理方式时，直接选择并配置 `flow` 为 `xtls-rprx-vision` 即可。你无需再单独去寻找一个名为 "XTLS" 的协议选项，因为你选择的 Vision 已经包含了 XTLS 的所有精华并在此之上做了优化和增强。


# ==另一个脚本==
## 安装
[mack-a 一键脚本，快速搭建教程 \| mack-a](https://www.v2ray-agent.com/archives/1682491479771)
![](../../fujian/Pasted%20image%2020250902212227.png)

## 1
[搭建最新的VLESS Vision和VLESS Reality防止VPS端口封禁 \| mack-a](https://www.v2ray-agent.com/archives/1680104902581)
为了应对 **TLS in TLS** 和**指纹识别**等阻断或封禁的风险，Xray-core 团队推出了 VLESS **Vision** 和 VLESS **Reality** 两种新颖的技术方案。它们能够有效地**隐藏**和**保护流量的特征**，提高**安全性**和**稳定性**。

Reality不支持CDN

### 1.Vision被封答疑【 [以下内容来源](https://github.com/XTLS/Xray-core/issues/1544#issuecomment-1402118517) 】

首先，如果你特别不想被封，**请先选择一个干净的 IP**，并按照 **配置正确** 去搭建、使用 XTLS Vision。

**但是，即使你这样做了，也无法保证 100% 不被封**。自去年底始，很多人的未知流量秒封 IP，TLS in TLS 流量隔天封端口。XTLS Vision 不是未知流量，且完整处理了 TLS in TLS 特征，目前看来效果显著。**但这并不意味着，用 XTLS Vision 可以 100% 不被封，认识到这一点是非常、非常重要的，不要自己偶然被封就大惊小怪**。

**因为除了协议本身，还有很多角度能封你**。以 IP 为例，你无法保证 IP 真的干净，无法避免被邻居波及，无法避免整个 IP 段被重点拉清单。也有可能某些地区的 GFW 有独特的标准，比如某个 IP 只有寥寥数人访问连却能跑那么多流量，封。**如果你的 XTLS Vision 被封了，但没有出现去年底 TLS 那样的大规模被封报告，我真心建议你换端口、换 IP、换服务商依次试一遍**。
- 打开[[ping.pe](http://ping.pe/)]
- 输入 IP 检测ping可用
- 输入 IP:Port 检查端口是否可用
- 主要是看最后几个是否为绿色