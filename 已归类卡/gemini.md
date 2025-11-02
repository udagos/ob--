---
up:
  - "[[../moc/网络|网络]]"
---
```
---
tags: 
---
```
# Gemini balance
## docker  
克隆gemini-balance下来改一下.env-example里面的mysql_password随便写一个密码上去然后保存出来在项目文件夹打开powershell运行docker-compose up -d就可以了然后去网页输入localhost:8000就可以进来了
## 爪子云

不太好用了


## 配置插件
http://localhost:8000/
gemini  
key
## 代理 
好的，我们来详细解释一下 Gemini Balance 界面里的“代理服务器”功能，这其实是它一个非常强大和实用的高级特性。

简单来说，这里的代理服务器是**一个跳板**，是给 **Gemini Balance 这个应用本身**使用的。

为了避免混淆，我们先理清两个“代理”的概念：

1. **Gemini Balance 自身**：它扮演了第一个代理的角色，对你的**应用程序**来说，它代理了对 Google Gemini API 的访问。
    
2. **代理服务器列表功能**：这是第二个代理，是**可选的**。它在 Gemini Balance 和 Google 服务器之间增加了一个**中转站**。
    

网络请求的流向是这样的：

你的应用程序 -> Gemini Balance (部署在你的VPS上) -> [**代理服务器列表中的跳板**] -> 真正的Google Gemini API服务器

---

### 一、这个代理服务器是用来做什么的？

它的核心作用是**解决你的 VPS 服务器无法直接、稳定地访问 Google API 的问题**。

主要有以下几个应用场景：

1. **解决网络访问问题 (最主要用途)**：
    
    - 如果你的 VPS 所在地区（例如：中国大陆、香港、俄罗斯等）直接访问 Google 的服务（包括 Gemini API）受限或被屏蔽，那么 Gemini Balance 就无法连接到 Google 的服务器，整个服务就瘫痪了。
        
    - 通过在这里添加一个能够正常访问 Google 的代理服务器（比如一个位于美国或欧洲的 SOCKS5/HTTP 代理），你就可以让 Gemini Balance 通过这个“跳板”去访问 Google，从而绕过网络限制。
        
2. **隐藏你的 VPS真实 IP**：
    
    - 当你通过这个功能设置了代理后，所有从 Gemini Balance 发往 Google 的请求，都会显示为来自你所设置的代理服务器的 IP，而不是你 VPS 本身的 IP。
        
    - 这可以在一定程度上避免你的 VPS IP 因为请求频率过高而被 Google 临时限制。
        
3. **更换网络出口以提升稳定性**：
    
    - 有时候，虽然你的 VPS 可以直连 Google，但网络链路质量不高，延迟大或丢包严重。
        
    - 你可以通过一个高质量的代理服务器来更换网络出口，可能会获得更稳定、更快速的连接。
        

---

### 二、如何使用这个代理服务器功能？

使用起来非常直观，基本流程是：**获取代理 -> 添加代理 -> 检测代理**。

#### **第一步：获取一个可用的代理服务器**

这个是最重要的前提。Gemini Balance 本身不提供代理，你需要从外部获取。你可以：

- 从专业的代理服务商处购买 (HTTP 或 SOCKS5 代理)。
    
- 使用机场提供的订阅节点信息（需要转换成相应的格式）。
    
- 自己搭建一个代理服务器。
    

你最终需要的是一个代理服务器的地址，格式通常如下。

#### **第二步：添加代理**

1. 点击界面上蓝色的 **[+] 添加代理** 按钮。
    
2. 在弹出的输入框中，填入你的代理服务器地址。**格式非常关键**，请根据你代理的类型填写：
    
    - **HTTP 代理**: `http://IP地址:端口`
        
        - 示例: `http://11.22.33.44:8888`
            
    - **SOCKS5 代理**: `socks5://IP地址:端口`
        
        - 示例: `socks5://11.22.33.44:1080`
            
    - **需要用户名和密码的代理**: `协议://用户名:密码@IP地址:端口`
        
        - 示例: `http://user123:pass456@11.22.33.44:8888`
            
    
    你可以添加多个代理，Gemini Balance 可能会在这些代理之间进行轮询或选择可用的一个。
    

#### **第三步：检测代理**

1. 添加完代理后，点击绿色的 **[检测所有代理]** 按钮。
    
2. 系统会自动尝试通过你添加的每一个代理去连接一个目标网站（通常是 Google），来测试这个代理是否可用。
    
3. 检测完成后，界面上通常会显示每个代理的状态，比如**延迟时间 (ms)** 或者 **可用/失败** 等标识。只有状态正常的代理才会被实际使用。
    

#### **第四步：管理代理**

- 如果某个代理失效了，你可以选中它，然后点击红色的 **[删除代理]** 按钮将其移除。
    

---

### 总结

总而言之，这个功能是一个**可选但非常强大的**工具，专门为了解决部署 Gemini Balance 的服务器本身的网络环境问题。

- **如果你的 VPS 可以流畅地访问 Google**：你完全**不需要**配置这个功能，将此项留空即可。
    
- **如果你的 VPS 无法访问 Google**：这个功能就是你的救星，你需要找到一个可用的代理服务器并在这里进行配置，你的 Gemini Balance 服务才能正常工作。
    

温馨提示：如要解锁所有应用的完整功能，请开启 [Gemini 应用活动记录](https://myactivity.google.com/product/gemini)。


# key 
ou
	AIzaSyBEoBQfBko-LYMUBAQ_cpmBU3nLjIFDMW0
changrui jing
	AIzaSyD1dzNatiiC9ZU2PTDz7ErG8P49KMj_5_k
changrui1   jing
	AIzaSyBznAWFX-wLfmvUhU8n3rYaqqd3I8PmRNI
changrui jing2
	AIzaSyBd6eDORBtid4Wpabh65vMolNms9G7pxsc
changrui3 jing   | jingchangrui3@gmail.com
	AIzaSyBTlHHa3DMMwOu61KBCJYmazURmElwD4rI
changrui5 jing
	AIzaSyANSKhkwPs1f3aWv-pArLznhF2tEe6wE7g
changrui4 jing 
	AIzaSyAOwN1YhjcnmIg79cEkR05rOdu-cVNYej0
# 1
[[谷歌注册]]