---
up:
  - "[[编程]]"
---
在源码中可能很常见如下做法：
文件 herder.h
```

#ifndef_HEADER_H
#define_HEADER_H
/*code*/
......
/*code*/
#endif
```
这种做法是防止文件重复包含，也叫做宏开关，比如 a 文件包含了 herder. h 和 b 文件，即
\#includeherder . h
\#b . h
b 文件若也包含了 header.h
不采取以上措施的话，则在程序编译的时候会造成重复编译，链接阶段就造成两个同源的链接错误

但是有时会看到程序中实实在在只有
\#define CL_API_ENTRY
并没有看到上下语句有 \#ifndef又是怎么回事呢 ？
**其实这样做主要是为了标记某些内容**，使程序阅读者能够清楚标记表明的意义，同时又不影响被编译的源代码。
**而且之后也有可能在别处被用到条件编译中:**
```

#ifdefCL_API_ENTRY
...
#else
...
#endif
```