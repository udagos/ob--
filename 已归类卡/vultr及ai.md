---
up:
  - "[[mocai]]"
---
[moc 兴趣](moc%20兴趣)
#ed 


vultr cpu共享  ubuntu

下载xui
bash <(curl -Ls https://raw.githubusercontent.com/FranzKafkaYu/x-ui/956bf85bbac978d56c0e319c5fac2d6db7df9564/install.sh ) 0.3.4.4
设置用户名密码端口

关闭防火墙或打开端口
	sudo ufw disable

游览器打开ip加端口

添加入站
	协议vmess 传输ws 添加用户，地址把id前面复制过去

直接粘贴即可



# 2 lm studio
导入本地gguf模型需要在当前目录下两层才可以
# 3 ob cursor
chat
	openapi format
	基地址 http而不是https   从api文档获取 
嵌入
	使用lm studio
