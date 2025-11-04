---
up:
  - "[[../moc/moc软件工程]]"
---
#off
JavaScript（简称 JS）是一种用于编写动态网页应用程序的**脚本语言**，它可以用于实现客户端和服务器端的交互。它是一种基于原型的动态编程语言，它支持函数式编程，还支持面向对象的编程。

JSON（JavaScript Object Notation）是一种轻量级的**数据交换格式**，它可以用于在服务器端和客户端之间传输数据

  
  

其实在 yaml 出现之前 js+json 用的也不错
因为 yaml 在格式简化和体验上表现确实不错
是 YAML 支持了 注释。



- XML 指可扩展标记语言（EXtensible Markup Language）是用来定义其它语言的一种元语言
- XML 是一种标记语言，很类似 HTML
- 
HTML(HyperTextMark-upLanguage)即超文本标记语言

html 是用来显示数据的；xml 是用来描述数据、存放数据的，所以可以作为持久化的介质！**Html 将数据和显示结合在一起，在页面中把这数据显示出来；xml则将数据和显示分开。 XML被设计用来描述数据，其焦点是数据的内容**。HTML被设计用来显示数据，其焦点是数据的外观。
## 为什么 JSON 比 XML 更好？

XML 比 JSON 更难解析。

JSON 可以直接使用现有的 JavaScript 对象解析。

针对 AJAX 应用，JSON 比 XML 数据加载更快，而且更简单：




"
这些文件的背后其实都对应一种信息标记语言。标记语言是指通过在文档中的某部分穿插特别的字符串标签（Tag)，用来修饰文档的语言
传输复杂的信息时，网络是一个字节接着一个字节将信息从服务器传递到客户端的。为了避免传输后信息不混乱，这些语言采用标记协议将信息变的有条理，保证传输之后浏览器或者其他程序依然能够正确的读懂
样由HTML构成的文档经过浏览器的解析和渲染后、呈现出来的就是内容丰富的Web页面
XML在后端开发中非常常见，很多配置文件都是用XML写成的
HTML虽然功能强大，但是还是有一些缺陷，例如无法描述数据
XML对标签的功能进行了简化，同时可以自定义标签。这样的特点是的XML便于读取解析，适应复杂的数据结构。现在XML和HTML之间分工明确，XML用于存储和传输数据，HTML用于展示数据
它适合网页和后端进行数据交换，而且能够被浏览器端的JavaScript程序直接解析。虽然号称是JS对象简谱，实际上可以被Java、python等各种语言进行解析
因为Yaml语言是专门用来写配置文件的语言
" https://diigo.com/0v4qx5



# JSON vs XML

**JSON 和 XML 都用于接收 web 服务端的数据**。
![[Pasted image 20241012144012.png]]
**最大的不同是**：**XML 需要使用 XML 解析器来解析**，JSON 可以使用标准的 JavaScript 函数来解析。
- [JSON.parse()](https://www.runoob.com/js/javascript-json-parse.html): 将一个 JSON 字符串转换为 JavaScript 对象。
- [JSON.stringify()](https://www.runoob.com/js/javascript-json-stringify.html): 将 JavaScript 值转换为 JSON 字符串。


# YAML
YAML 虽然不如 JSON、XML 之类的语言流行，应用也没有那么广泛
- YAML广泛应用于配置文件、数据序列化、API设计和许多其他领域。它被许多编程语言和框架所支持，包括Python、Java、Ruby等。在Python中，可以使用PyYAML库来读取和写入YAML文件。

# 配置文件
配置文件用于存储软件程序的配置信息，以便程序能够根据这些信息进行自定义和调整。常用的配置文件格式包括INI、[XML](https://so.csdn.net/so/search?q=XML&spm=1001.2101.3001.7020)、JSON和YAML
![[Pasted image 20241012144656.png]]
总结
INI：适合简单配置，适用场景如应用程序的基本配置，易于阅读和编辑，但不适合复杂数据结构。
XML：适用于需要复杂结构和数据验证的场景，如文档格式和配置文件，工具支持丰富，但语法繁琐。
JSON：适用于数据交换和配置，广泛应用于Web应用和API，简洁高效，广泛支持，但不支持注释。
YAML：适合配置文件和数据序列化，尤其在需要频繁手动编辑的场景，语法简洁，支持复杂结构和注释，但对缩进敏感。
TOML：在保持简单易读的同时，提供丰富的数据类型，适合配置文件。