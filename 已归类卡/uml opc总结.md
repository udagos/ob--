---
up:
  - "[[../moc/moc对象设计模式]]"
---
[moc  uml](../moc/moc%20%20uml.md)
#ed 
## 对象沟通方法
现设计 3 个软件对象 (Object)来组成一个 Light Controller。其中, Wall Switch 对象控制 Wall Switch Set 硬件设备, Door Switch  对象控制 Door Switch Set 硬件设备, 而 Light 对象控制多个 Light Bulb Set 电灯。这 3 个软件对象间的沟通情形如图 12-2 所示。
![[Pasted image 20240820182220.png]]
设计 OOPC 类
WallSwitch 和 DoorSwitch 对象的特性和行为是一样的，所以可归为同一个类，取名为 Switch 类。而 Light 对象可归到另一个类，取名为 Light 类。如图12-3所示。
![[Pasted image 20240820182340.png]]
刚才已经设计出类了，就拿类来生成对象
![[Pasted image 20240820182427.png]]
![[Pasted image 20240820182453.png]]
![[Pasted image 20240820182505.png]]
![[Pasted image 20240820182515.png]]
![[Pasted image 20240820182526.png]]
![[Pasted image 20240820182537.png]]
![[Pasted image 20240820182547.png]]



## uml 类图 
所以在类定义里, 不仅需要定义类的内部属性及函数, 还得定义类间的连接关系。这种连接关系包括组合 (Composition)关系及结合 (Association)关系等。
### 如何找到类
## 用例图
“达了系统提供用户哪些服务”
## 序列图
