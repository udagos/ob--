---
up:
  - "[[../moc/网络|网络]]"
---
# gemini blance 


## docker启动后Nginx 配置

将下面配置到自己的 Nginx 对应的 server 里面：

```
location / {
	proxy_pass http://127.0.0.1:8000;
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Forwarded-Proto $scheme;
	proxy_read_timeout 90;
}
```


这是一个非常好的问题，也是理解现代 Web 应用部署方式的关键。

简单来说，这步操作是在配置 Nginx 作为一个**反向代理 (Reverse Proxy)**。你的应用程序（比如一个用 Python, Node.js, Go 写的后端服务）实际上是在 `127.0.0.1:8000` 这个地址上运行，但它不应该直接暴露在公网上。

把 Nginx 想象成一个专业的“前台接待”或者“保安”，而你的应用程序是后台“办公室里的员工”。

### **为什么在 VPS 上部署需要这一步？原因如下：**

---
[[配置反代]]
#### 1. 安全性 (Security)

- **隐藏应用细节**：==直接将你的应用（例如一个 Python Gunicorn 服务）暴露在公网端口上是危险的。它可能会泄露版本信息，或者存在未知的安全漏洞。Nginx 作为一层屏障，可以隐藏你的后端服务==，只暴露 Nginx 这个身经百战、非常稳定的 Web 服务器。
    
- **攻击防护**：Nginx 可以配置防火墙规则、频率限制 (rate limiting) 等，来抵御常见的网络攻击，如 DDoS 攻击。这些功能你的应用程序通常不具备。
    

#### 2. 统一访问入口和端口管理 (Port Management)

- Web 流量的标准端口是 `80` (HTTP) 和 `443` (HTTPS)。用户在浏览器输入网址时，默认访问的就是这两个端口。
    
- 你的应用程序为了避免权限问题（1024 以下的端口通常需要 root 权限）和端口冲突，通常会运行在像 `8000`, `3000`, `8080` 这样的高位端口上。
    
- **Nginx 的作用就是监听标准的 `80/443` 端口，然后根据配置，将收到的请求“转发”给你在 `8000` 端口上运行的应用程序。** 这样用户就可以通过标准域名直接访问，而不需要在后面加上 `:8000`。
    

#### 3. 性能和负载均衡 (Performance & Load Balancing)

- **处理静态文件**：Nginx 处理静态文件（如图片、CSS、JavaScript）的性能极高。你可以配置 Nginx 直接处理这些静态文件请求，而不用麻烦后端的应用程序，从而大大减轻后端服务的压力。
    
- **负载均衡**：如果你的应用访问量变大，你可以在服务器上启动多个应用实例（比如在 8000, 8001, 8002 端口上）。Nginx 可以将进来的请求平均分配给这几个实例，实现负载均衡，提高整个服务的承载能力。
    
- **连接管理**：Nginx 在处理高并发连接方面非常高效，它可以维持大量与客户端的连接，然后优化地与后端应用进行通信，防止后端应用被大量慢速连接拖垮。
    

#### 4. 功能扩展 (Feature Expansion)

- **SSL/TLS 加密 (HTTPS)**：为网站配置 HTTPS 是现代 Web 的标配。在 Nginx 上配置 SSL 证书比在每个应用程序里单独配置要简单和高效得多。Nginx 可以处理所有的加密解密工作，你的后端应用只需要处理普通的 HTTP 请求即可，极大地简化了开发。
    
- **HTTP/2 和 HTTP/3 支持**：Nginx 支持最新的网络协议，可以提升网站加载速度，而你的后端应用无需关心这些协议的实现细节。
    
- **缓存 (Caching)**：Nginx 可以配置缓存，将后端应用生成的动态内容缓存一段时间，对于不经常变化的内容，可以直接从 Nginx 缓存中返回，极大地提升响应速度。
    

---

#### 配置代码逐行解释

让我们来解读一下你提供的这段配置：

Nginx

```
location / {
    // 这条规则匹配所有进入的请求

	// 核心指令：将所有匹配的请求转发到运行在本地 8000 端口的服务上
	proxy_pass http://127.0.0.1:8000;

	// 下面这些 proxy_set_header 指令非常重要，它们将原始的请求头信息传递给后端应用，
	// 否则你的应用只能看到请求是来自 Nginx (127.0.0.1)，而丢失了真实的用户信息。

	// 传递原始的 Host 请求头（例如 www.yourdomain.com），让后端应用知道用户访问的哪个域名
	proxy_set_header Host $host;

	// 传递用户的真实 IP 地址
	proxy_set_header X-Real-IP $remote_addr;

	// 传递完整的代理链 IP 地址，如果经过了多层代理
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

	// 告诉后端应用，原始请求是 http 还是 https
	proxy_set_header X-Forwarded-Proto $scheme;

	// 延长代理读取超时时间到 90 秒，防止后端处理耗时较长的请求时，Nginx 提前断开连接
	proxy_read_timeout 90;
}
```

#### 总结

总而言之，在 VPS 上部署应用时，直接把应用暴露在公网是一种不专业、不安全、低效且难以扩展的做法。使用 Nginx 作为反向代理，**将 Nginx 作为网站的“门面”，而你的应用在“幕后”工作**，这已经成为了现代 Web 服务部署的**标准实践**。它为你解决了安全、性能、扩展性和维护性等一系列重要问题。


### 配置
好的，配置 Nginx 文件是在 VPS 上部署应用的核心步骤。我们将遵循标准的、模块化的方式来配置，这样更安全且易于管理。

基本思路是：**为你的网站创建一个独立的配置文件，而不是直接修改 Nginx 的主配置文件。**

这套流程在 Ubuntu/Debian 等主流 Linux 发行版上是标准实践。

---

#### 详细配置步骤

请在你的 VPS 终端中按顺序执行以下命令。

##### 第一步：进入 Nginx 配置目录

Nginx 的网站配置文件通常存放在 `/etc/nginx/sites-available/` 目录中。我们先进入这个目录。

Bash

```
cd /etc/nginx/sites-available/
```

##### 第二步：创建新的配置文件

现在，为你的项目创建一个新的配置文件。建议使用你的域名或项目名来命名，以便识别。这里我们用 `your_project` 作为例子。

我们将使用 `nano` 这个对新手友好的文本编辑器。

Bash

```
sudo nano your_project
```

> **提示**：`sudo` 是必需的，因为这些是系统保护目录，需要管理员权限才能修改。

##### 第三步：编写并粘贴配置内容

执行上述命令后，会打开一个空白的文本编辑器。现在，**将下面的整个代码块复制并粘贴进去**。

这是一个完整的 Nginx `server` 配置块，其中包含了你之前提供的那段 `location` 配置。

Nginx

```
server {
    # 监听 80 端口 (标准的 HTTP 端口)
    listen 80;
    listen [::]:80;

    # 在这里填写你的域名或 VPS 的公网 IP 地址
    # 如果有多个域名，用空格隔开
    server_name your_domain.com www.your_domain.com; 

    # 访问日志和错误日志的存放位置，这对于排查问题很有用
    access_log /var/log/nginx/your_project.access.log;
    error_log /var/log/nginx/your_project.error.log;

    # 这里就是你之前提供的核心配置
    location / {
        # 将所有请求转发到运行在本地 8000 端口的应用程序
        proxy_pass http://127.0.0.1:8000;
        
        # 将原始的请求头信息传递给后端应用，这非常重要！
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 90;
    }
}
```

重要：

请务必将 server_name your_domain.com www.your_domain.com; 这一行中的 your_domain.com 替换成你自己的域名。如果你没有域名，可以暂时填你的 VPS 的公网 IP 地址。

##### 第四步：保存并退出文件

文件内容粘贴并修改好后，保存并退出 `nano` 编辑器：

1. 按 `Ctrl + X`
    
2. 编辑器会询问你是否要保存，按 `Y` (表示 Yes)
    
3. 最后按 `Enter` 键确认文件名。
    

##### 第五步：启用该配置文件

现在文件已经创建好了，但 Nginx 还不会读取它。我们需要在 `sites-enabled` 目录里创建一个指向它的**符号链接 (symbolic link)** 来“激活”这个配置。

Bash

```
sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled/
```

> **可选但建议**：为了避免冲突，最好禁用掉 Nginx 自带的默认欢迎页面配置。
> 
> Bash
> 
> ```
> sudo rm /etc/nginx/sites-enabled/default
> ```

##### 第六步：测试 Nginx 配置语法

这是**非常关键的一步**，可以检查你的配置文件有没有语法错误。如果这里报错，Nginx 将无法启动。

Bash

```
sudo nginx -t
```

如果你看到类似下面的成功信息，说明配置没有语法问题：

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

如果出现错误提示，请根据提示回去检查你在第二步创建的文件内容是否有拼写错误（比如漏了分号 `;`）。

##### 第七步：重启 Nginx 使配置生效

确认语法无误后，平滑地重新加载 Nginx 服务来应用你的新配置。

Bash

```
sudo systemctl reload nginx
```

---

至此，配置全部完成！现在，通过你的域名或 IP 地址访问服务器，Nginx 应该就会把请求转发给你在 8000 端口上运行的应用程序了。



## compose
```
volumes:
  sqlite_data:

services:
  gemini-balance:
    image: ghcr.io/snailyp/gemini-balance:latest
    container_name: gemini-balance
    restart: unless-stopped
    ports:
      - "8000:8000"
    env_file:
      - .env
    environment:
      - DATABASE_TYPE=sqlite
      - SQLITE_DATABASE=/app/data/default_db
    volumes:
      - sqlite_data:/app/data
    #depends_on:
      # 如需等待其他服务，可按需配置
    healthcheck:
      test: ["CMD-SHELL", "python -c \"import requests; exit(0) if requests.get('http://localhost:8000/health').status_code == 200 else exit(1)\""]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  # （移除或注释掉原 mysql 服务）
```

### .env
AUTH_TOKEN=