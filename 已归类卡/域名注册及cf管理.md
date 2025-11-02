---
up:
  - "[[vps]]"
---
dns 域名转ip，将域名托管到cf

# 购买
[域名注册 \| 新手指引 \| 域名注册商推荐 \| Newbie Village](https://blog.nbvil.com/server/domainreg/)

# 管理
[登入 - Spaceship](https://www.spaceship.com/zh-HK/application/domain-list-application/)

用cf名称服务器更改spaceship
[请稍候…](https://dash.cloudflare.com/7b4e9b0e1f904094657208b21fa1288a/809479884.xyz)


## cf  ddns
![](../../fujian/Pasted%20image%2020250901214002.png)





![](../../fujian/Pasted%20image%2020250901214752.png)
一期是将自己的域名代理到GITHUB配置上, 做个人博客使用, 还有一期是使用自己的域名做DDN, 从而达成外网访问家庭服务器的内网
![](../../fujian/Pasted%20image%2020250901214844.png)


如果想要搭建网站,并且要保证网站在国内被访问到,那就需要使用国内的域名服务商,加国内的云服务器,并且做好备案,保证网站的全产品链路都使用国内厂商,这样最保险,如果不做网站,只是做个普通的API接口,或者类似前几期视频,我使用的DDNS给家庭宽带做远程桌面,做SMB文件共享等等,那大可不必备案,也无所谓,国内或者国外的域名服务商,哪里域名便宜,去哪里买就可以了,下面我们来看如何获取免费域名



上面已经将dns从spaceship转移到cf管理
绑定ip也在cf管理，如下添加记录
![](../../fujian/Pasted%20image%2020250902084408.png)


接下来，您需要填写几个关键信息来将域名指向您的服务器 IP。通常，我们需要设置两条记录，一条用于主域名 (`yourdomain.com`)，另一条用于 `www` 子域名 (`www.yourdomain.com`)。

**1. 绑定主域名 (例如 `yourdomain.com`)**

- **Type (类型):** 选择 `A`。
    
- **Name (名称):** **填写 `@`**。在 Cloudflare 中，`@` 符号代表您的根域名或主域名本身。
    
- **IPv4 address (IPv4 地址):** 在这里**填写您 VPS 或服务器的 IP 地址** (例如: `192.0.2.1`)。
    
- **Proxy status (代理状态):** 这是 Cloudflare 最核心的功能。
    
    - **橙色云 (Proxied):** 这是默认和推荐的选项。流量会经过 Cloudflare 的全球网络。这会隐藏您的真实服务器 IP，并为您提供免费的 CDN 加速、DDoS 防护和 SSL 证书。**对于网站，请务必开启此项。**
        
    - **灰色云 (DNS-only):** 流量将直接连接到您的服务器，不经过 Cloudflare 的保护和加速。Cloudflare 只提供 DNS 解析服务。**在某些特定情况下使用，例如用于游戏服务器、邮件服务(MX记录)或需要直接 SSH 连接时。**
        
- **TTL (生存时间):** 当代理状态为橙色云时，通常为 `Auto` (自动)，您无需更改。
    

填写完毕后，点击 **"Save" (保存)**。

**2. 绑定 `www` 子域名 (例如 `www.yourdomain.com`)**

为了确保用户输入 `www.yourdomain.com` 也能访问，您需要再添加一条记录。

- 点击 **"+ Add record"**。
    
- **Type (类型):** 选择 `A`。(或者您也可以选择 `CNAME`，Name填`www`，Content填`@`，效果类似)。
    
- **Name (名称):** **填写 `www`**。
    
- **IPv4 address (IPv4 地址):** **再次填写您服务器的同一个 IP 地址**。
    
- **Proxy status (代理状态):** 同样，保持**橙色云**状态。
    
- **TTL:** 保持 `Auto`。
    

再次点击 **"Save" (保存)**。
**接下来做什么？**

- **等待生效:** Cloudflare 的 DNS 解析速度非常快，通常在全球范围内**几分钟内**就会生效。
    
- **SSL/TLS 设置:** 确保在左侧菜单的 **"SSL/TLS"** 选项中，加密模式设置为 **"Full (Strict)"** (完全-严格)。这是最安全的方式，但要求您的源服务器上也已经安装了 SSL 证书（可以使用免费的 Let's Encrypt 证书）。如果您的源服务器还没有证书，可以先设置为 **"Flexible"** (灵活)，但这安全性较低。
    
- **访问测试:** 稍等几分钟后，尝试在浏览器中访问您的域名 `yourdomain.com` 和 `www.yourdomain.com`，看看是否能成功显示您服务器上的内容。
    

至此，您已成功通过 Cloudflare 将域名绑定到了您的 IP 地址，并获得了强大的网络安全和加速功能。

ipv6为aaaa

