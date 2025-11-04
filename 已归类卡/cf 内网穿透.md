---
up:
  - "[[../moc/moc网络|moc网络]]"
---
[post.smzdm.com/p/admp85dn/](https://post.smzdm.com/p/admp85dn/)



## 1️⃣ 主机名（Hostname）

- **子域（Subdomain）**：填你想用的前缀，比如 `webhook`
    
- **域（Domain）**：从下拉框选择你在 Cloudflare 托管的域名，比如 `example.com`
    
- **路径（Path）**：一般留空，除非你只想映射某个路径（如 `/api`）
    

这样组合起来就是 `webhook.example.com`

## 2️⃣ 服务（Service）

- 从下拉框选择协议类型：
    
    - **HTTP** / **HTTPS** → 适合 Webhook、网站、API
        
    - **SSH** / **RDP** → 远程登录或桌面
        
- Webhook 场景一般选 **HTTP**（Cloudflare 会自动加 HTTPS）
## 3️⃣ URL

- 填你内网服务的地址和端口
    
- 例如：
    
    - `http://localhost:8080`（本机服务）
        
    - `http://192.168.1.100:5000`（局域网其他设备）
        
- 注意：这里的地址是 **cloudflared 运行所在机器能访问到的地址**
# [[n8n webhook  cf]]
