---
up:
  - "[[../moc/MocN8n|MocN8n]]"
---

![](../../fujian/Pasted%20image%2020250909154017.png)



**上面这么弄还是不行**
1.在n8n的compose中加入
	 environment:
	      - WEBHOOK_URL= https://webhook.809479884.xyz/
2.cf隧道的端口是n8n服务的端口
3.https也不行，改为http，应该是没有证书
![](../../fujian/Pasted%20image%2020250909160854.png)


这样就能用webhook.809479884.xyz 直接访问本地部署的localhost:5678的n8n服务了