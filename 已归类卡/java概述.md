---
up:
  - "[[../moc/moc软件工程]]"
---
# 核心类
包装类
枚举类
记录类
	按照 `record` 声明的变量顺序自**动创建一个构造方法**
工具类
# 网络编程
**网络编程是Java最擅长的方向之一**，使用Java进行网络编程时，由虚拟机实现了底层复杂的网络协议，Java程序只需要调用Java标准库提供的接口，就可以简单高效地编写网络程序。
如果两台计算机计算出的**网络号**相同，说明两台计算机在同一个网络，可以****直接通信**
两台计算机**不在同一个网络**，不能直接通信，它们之间必须通过路由器或者交换机这样的网络设备间接通信，我们把这种设备称为**网关**。

域名解析服务器DNS负责把域名翻译成对应的IP，客户端再根据IP地址访问服务器
**本机域名localhost**，它对应的IP地址总是本机地址127.0.0.1
## TCP编程
socket是一个抽象概念，**一个应用程序通过一个Socket**来建立一个远程连接，而Socket内部通过TCP/IP协议把数据传输到网络：
![[Pasted image 20241130152433.png]]
一个Socket就是由IP地址和端口号，端口号总是由操作系统分配

Socket进行网络编程时，本质上就是两个进程之间的网络通信
一个进程必须充当服务器端
另一个进程必须充当客户端
### 服务器
```
ServerSocket ss = new ServerSocket(6666);
```
在指定端口 `6666` 监听。这里我们没有指定IP地址，表示在计算机的所有网络接口上进行监听。
**监听成功，我们就使用一个无限循环来处理客户端的连接：**
```
for (;;) {
    Socket sock = ss.accept();
    Thread t = new Handler(sock);
    t.start();
}
```
代码**ss.accept () 表示每当有新的客户端连接进来后，就返回一个Socket实例**
为每个**新的Socket创建一个新线程来处理**

### 客户端
客户端程序通过：
Socket sock = new Socket ("localhost", 6666);
**连接到服务器端**，如果**连接成功，将返回一个Socket实例，用于后续通信。**

当Socket**连接创建成功后**，我们都**使用Socket实例进行网络通信**
## udp编程
UDP没有创建连接，数据包也是一次收发一个，所以没有流的概念
仍然需要使用Socket，因为应用程序在使用UDP时必须指定网络接口（IP）和端口号
但他们是**两套独立的端口**，即一个应用程序用TCP占用了端口1234，不影响另一个应用程序用UDP占用端口1234。
### 服务器
服务器端首使用如下语句先在指定的端口监听UDP数据包：
```
DatagramSocket ds = new DatagramSocket(6666);

```
如果**没有其他应用程序占据这个端口**，那么监听成功，我们就使用一个_无限循环来处理收到的UDP数据包：

**接收一个UDP数据包**，需要准备一个byte[]缓冲区，并**通过DatagramPacket实现接收**：
```
byte[] buffer = new byte[1024];
DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
ds.receive(packet);
```
服务器**收到一个DatagramPacket后，通常必须立刻回复一个或多个UDP包**
**发送UDP包**，也是通过DatagramPacket实现的
```
byte[] data = ...
packet.setData(data);
ds.send(packet);
```
### 客户端
**只需要直接向服务器端发送UDP包，然后接收返回的UDP包**

## HTTP
浏览器请求访问某个网站时发送的HTTP请求-响应，浏览器希望访问某个网站时，

浏览器和网站服务器之间**首先建立TCP连接**，且**服务器总是使用80端口和加密端口443**
然后，浏览器向服务器发送一个HTTP请求，
服务器收到后，返回一个HTTP响应，**并且在响应中包含了HTML的网页内容**，这样，浏览器解析HTML后就可以给用户显示网页了
![[Pasted image 20241130155757.png]]

### HTTP请求的格式
GET请求
POST请求
## http编程
针对客户端编程和针对服务器端编程。
**服务器端的HTTP编程本质上就是编写Web服务器**，**JavaEE开发的核心内容**

**客户端的HTTP编程，它的行为本质上和浏览器是一样的**，即发送一个HTTP请求，接收服务器响应后，获得响应内容。只不过浏览器进一步把响应内容解析后渲染并展示给了用户，而我们使用**Java进行HTTP客户端编程仅限于获得响应内容**。*
### Java如何使用HTTP客户端编程

### 编写HTTP Server
==前面介绍的HTTP编程是以客户端的身份去请求服务器资源。现在，我们需要以服务器的身份响应客户端请求，编写服务器程序来处理客户端请求通常就称之为Web开发。==
#### WSGI接口
web应用的本质就是：
- 浏览器发送一个HTTP请求；
- 服务器收到请求，生成一个HTML文档；
- 服务器把HTML文档作为HTTP响应的Body发送给浏览器；
- 浏览器收到HTTP响应，从HTTPBody取出HTML文档并显示。
所以，**最简单的Web应用就是先把HTML用文件保存好，用一个现成的HTTP服务器软件，接收用户请求，从文件中读取HTML返回0
Apache、Nginx、Lighttpd等这些常见的静态服务器就是干这件事情的**

要**==动态生成HTML==**，就**需要把上述步骤自己来实现**
==接受HTTP请求、解析HTTP请求、发送HTTP响应都是苦力活，正确的做法是底层代码由专门的服务器软件实现==

==有了WSGI没有涉及到任何解析HTTP的部分，也就是说，底层代码不需要我们自己编写，我们只负责在更高层次上考虑如何响应请求就可以了==
#### 使用web框架
了解了WSGI框架，我们发现：其**实一个Web App，就是写一个WSGI的处理函数，针对每个HTTP请求进行响应。**

**处理HTTP请求不是问题，问题是如何处理100个不同的URL。**
每一个URL可以对应GET和POST请求，当然还有PUT、DELETE等请求
一个最简单的想法是从 `environ` 变量里取出HTTP请求的信息，然后逐个判断
```

def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    if method=='GET' and path=='/':
        return handle_home(environ, start_response)
    if method=='POST' and path='/signin':
        return handle_signin(environ, start_response)
    ...
```
只是这么写下去代码是肯定没法维护了。
**代码这么写没法维护的原因是因为WSGI提供的接口虽然比HTTP接口高级了不少，但和Web App的处理逻辑比，还是比较低级**
==**WSGI接口之上能进一步抽象，用一个函数处理一个URL，至于URL到函数的映射，就交给Web框架来做。**==
### 使用模板
**Web框架把我们从WSGI中拯救出来了。现在，我们只需要不断地编写函数，带上URL，就可以继续Web App的开发了。**

**Web App不仅仅是处理逻辑，展示给用户的页面也非常重要**返回一个**包含HTML的字符串的6000多行的HTML，你确信能在Python的字符串中正确地写出来么**
![[Pasted image 20241130162941.png]]
这就是传说中的**MVC**：Model-View-Controller，中文名“**模型-视图-控制器**”。
- **Python处理URL的函数就是C**：Controller，Controller负责**业务逻辑**，比如检查用户名是否存在，取出用户信息等等；
- 包含**变量 {{ name }} 的模板就是V**：View，View负责**显示逻辑**，通过简单地替换一些变量，View最终输出的就是用户看到的HTML。 
- MVC中的Model在哪？**Model是用来传给View的**，这样View在替换变量的时候，就可以从Model中取出相应的数据。上面的例子中，Model就是一个 `dict`：
**我们把上次直接输出字符串作为HTML的例子用高端大气上档次的MVC模式改写一下**
F**lask默认支持的模板是 [jinja2](http://jinja.pocoo.org/)**




**HTML定义了页面的内容，CSS来控制页面元素的样式，而JavaScript负责页面的交互逻辑。**
css比如，给标题元素 `<h1>` 加一个样式，变成48号字体，灰色，带阴影：
```
<html>
<head>
  <title>Hello</title>
  <style>
    h1 {
      color: #333333;
      font-size: 48px;
      text-shadow: 3px 3px 3px #666666;
    }
  </style>
</head>
<body>
  <h1>Hello, world!</h1>
</body>
</html>
```
如果我们希望当用户点击标题时把标题变成红色，就必须通过JavaScript来实现：
```
<html>
<head>
  <title>Hello</title>
  <style>
    h1 {
      color: #333333;
      font-size: 48px;
      text-shadow: 3px 3px 3px #666666;
    }
  </style>
  <script>
    function change() {
      document.getElementsByTagName('h1')[0].style.color = '#ff0000';
    }
  </script>
</head>
<body>
  <h1 onclick="change()">Hello, world!</h1>
</body>
</html>
```

# web开发

JavaEE最核心的组件就是基于Servlet标准的Web服务器
![[Pasted image 20241130171134.png]]
目前**流行的基于Spring的轻量级JavaEE开发架构**，使用**最广泛的是Servlet和JMS**，以及一系列开源组件

| 特性   | Java SE                  | Java EE                  |
| ---- | ------------------------ | ------------------------ |
| 目标   | 提供Java编程语言的核心功能和API      | 提供企业级应用开发的功能和API         |
| 适用场景 | 桌面应用、移动应用、嵌入式系统、小型服务器端应用 | Web应用、企业级服务、分布式系统、大型企业应用 |
# spring开发
Spring是一个支持快速**开发Java EE应用程序的框架**。它提供了一系列底层容器和基础设施，并可以和大量常用的开源框架无缝集成，可以说是**开发Java EE应用程序的必备**。
在Spring Framework基础上，又诞生了Spring Boot、Spring Cloud、Spring Data、Spring Security等一系列基于Spring Framework的项目
# 面向对象编程
# 正则
![[Pasted image 20241130171627.png]]
![[Pasted image 20241130171634.png]]


多行匹配，^表示开头，$表示结尾
![[Pasted image 20241130171700.png]]
# 注解
注解（Annotations）在Java中是一种元数据形式，它们为程序元素（如类、方法、字段等）提供额外的信息。**注解本身不会直接影响程序的运行**，但它们可以被编译器、工具或框架用来执行特定的操作。以下是注解的主要作用：

注解在Java中具有多种作用，包括提供元数据、代码生成、配置管理、运行时处理、测试框架、文档生成和代码检查。通过使用注解，你可以增强代码的可读性、可维护性和可扩展性，同时简化开发过程。

**删掉注解后，程序在大多数情况下仍然可以正常运行**

# maven
**项目描述文件**`pom.xml`
Maven是一个Java**项目管理和构建工具**，它可以定义**项目结构、项目依赖**，并使用**统一的方式进行自动化构建**



# 其他

ORM框架的主要目标是简化数据库操作，使开发者能够以面向对象的方式操作数据库，而不需要编写大量的SQL语句
springweb开发框架

vue是前端开发框架