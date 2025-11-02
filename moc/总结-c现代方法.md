
有助于编写大型程序的技术
如何将 C 程序看作一组相互提供服务的模块。如何使用信息隐藏和抽象数据类型来改进程序模块
# 模块设计
独立的模块。**模块是一组服务的集合**。每个模块都有一个接口来描述所提供的服务
这些服务就是函数。**模块的接口就是头文件**, 头文件中包含那些可以被程序中其他文件调用的函数原型。

如计算器程序。这个程序由 calc. c 文件和一个栈模块组成。栈模块则存储在 stack. h 和 stack. c 文件中 (见下面的图)。文件 calc. c 是栈模块的客户。文件 stack. h 是栈模块的接口, 它提供了客户需要了解的全部信息。
![[Pasted image 20240813084453.png]]

**一旦确定要进行模块化设计, 设计程序的过程就变成了确定究竟应该定义哪些模块, 每个模块应该提供哪些服务, 以及各个模块之间的相互关系是什么**。
## 内聚性和耦合性
好的模块接口，模块应该具有内聚性和耦合性两个性质

文件 calc. c 依赖于 stack. h (当然 stack. c 也依赖于 stack. h), 但除此之外就没有其他明显的依赖关系了。
## 模块的类型
模块通常分为下面几类
数据池：
	数据池是一些相关的变量或常量的集合。在 C 语言中, **这类模块通常只是一个头文件**
	**通常不建议将变量放在头文件中**, 但建议把相关常量放在头文件中
	在 C 库中,<float.h>和<limits.h>都属于数据池。
库
	一个相关函数的集合。例如<string.h>头就是字符串处理函数库的接口
抽象对象
	抽象对象是指对于隐藏的数据结构进行操作的**函数的集合**
	在 C 语言术语中, 对象仅仅是可以存储值的一块内存, 而在本章中, 对象是一组数据以及针对这些数据的操作的集合
抽象数据类型
	将具体数据实现方式隐藏起来**的数据类型**叫作抽象数据类型
	**客户模块可以使用该类型来声明变量, 但不会知道这些变量的具体数据结构。如果客户模块需要对这种变量进行操作, 则必须调用抽象数据类型模块所提供的函数**
## 信息隐藏
例如, 我们的**栈模块的客户就不需要知道栈是用数组、链表还是其他形式存储的**。这种故意对客户隐藏信息的方法叫作信息隐藏。
在 C 语言中, 强制信息隐藏的主要工具是 static 存储类型。

下面例子可以清楚地看到信息隐藏所带来的好处
```
stack.h
#ifndef STACK H
#define STACK H
#include <stdbool.h>

void make_empty (void);
bool is_empty (void);
bool is_full(void);
void push(int i);
int pop(void);
#endif
```

```
#define PUBLIC 
#define PRIVATE static

PRIVATE int contents [STACK SIZE];
PRIVATE int top =0;
PRIVATE void terminate(const char *message){...
PUBLIC void make_empty (void){...
PUBLIC bool is_empty (void){...
PUBLIC bool is_full(void){...
PUBLIC void push(int i){...
PUBLIC int pop(void)
{...}
```

我们的栈示例清晰地展示了信息隐藏带来的好处: 使用 stack 1. c 还是使用 stack 2. c 来实现栈模块无关紧要。这两个版本都能匹配模块的接口定义, 因此相互替换时不需要修改程序的其他部分。
# 面向对象的c
## 抽象方法
==作为抽象对象的模块 (像上一节中的栈模块) 有一个严重的缺点: 无法拥有该对象的多个实例 (本例中指多个栈)。达到这个目的, 需要创建一个新的类型==

一旦定义了 Stack 类型, 就可以有任意个栈了。下面的程序片段显示了如何在同一个程序中有两个栈:
```
Stack s1,s2;
make_empty (&s1);
make_empty (&s2);
push(&s1,1);
push(&s2,2);
if (!is_empty (&s1))
{
	printf ("&d\n",pop(&s1));
}

```
**我们并不知道 s1和 s2究竟是什么 (是结构, 还是指针), 但这并不重要。对于栈模块的客户, s1和 s2是抽象,它只响应特定的操作 (make_empty、is_empty、is_full、push 以及 pop)。**

接下来将 stack. h 改成提供 Stack 类型的方式, 其中 Stack 是结构。这需要给每个函数增加一个 Stack 类型 (或 Stack\*) 的形式参数
```
#define STACK SIZE 100
typedef struct{
	int contents [STACK SIZE];
	int t
	top;
}Stack;
void make_empty (stack *s);
bool is_empty (const stack *s);
bool is_full(const stack *s);
void push(stack *s,int i);
int pop(stack *s);
```
函数 make_empty、push 和 pop 参数的栈变量应为指针, 因为这些函数会改变栈的内容。is_empty 和 is_full 函数的参数并不需要是指针, 但这里我们仍然使用了指针。给这两个函数传递 Stack 指针比传递 Stack 值更有效, 因为传递值会导致整个数据结构被复制
### 封装
==遗憾的是, 上面的 Stack 不是抽象数据类型, 因为 stack. h 暴露了 Stack 类型的具体实现方式, 因此无法阻止客户将 Stack 变量作为结构直接使用:==
```
Stack s1;
s1.top =0;
s1.contents[top++]1;
```
由于提供了对 top 和 contents 成员的访问, 模块的客户可以破坏栈。**更糟糕的是, 由于无法评估客户的修改所产生的效果, 我们不能改变栈的存储方式。**

我们真正需要的是一种阻止客户知道 Stack 类型的具体实现的方式。
### 不完整类型 
==C 语言提供的唯一封装工具为不完整类型。==

C 标准对不完整类型的描述: 描述了对象但缺少定义对象大小所需的信息。例如, 声明
struct t;

告诉编译器 t 是一个结构标记, 但并没有描述结构的成员。因此, 编译器并没有足够的信息来确定该结构的大小。这样做的意图是, 不完整类型会在程序的其他地方将信息补充完整。
**因为编译器不知道不完整类型的大小, 所以不能用它来声明变量:**
struct t s;

==但是完全可以定义一个指针类型引用不完整类型==:
typedef struct struct t *T;

但我们不能对这些变量使用->运算符。


## 面向对象的c
经典栈的实现方法
```
经典栈的实现方法 stack.h
#ifndef STACK H
#define STACK H
bool push(int val);
bool pop(int *pRet);
#endif

stack.c
#include <stdbool.h>
#include "stack.h"
int buf {16];
int top 0;

bool isstackFull(void){
	return top =sizeof(buf)sizeof(int);
}

bool isstackEmpty (void){
	return top ==0;
}

/true:成功，false:失败
bool push(int val){
	if (isStackFull（）)return false;
	buf [top++]val;
	return true;
}

/true:成功，false:失败
bool pop(int *pRet){
	if (isStackEmpty（）)return false;
	*pRet buf [--top]
	return true;
}
```


但是通常情况下，这种代码都会暴露出问题。问题之一是变量、函数的作用域
stack, c 中，buf、top, isStackFull, isStackEmpty 都被公开在全局命名空间中
为了解决这个问题, 我们可以使用 static 修饰符。
像这样在头文件中声明对外公开的函数和变量，对其他无需对外公开的变量和函数指定 static 修饰符，是 C 开发中常用的**模块化方法**。这样可以提高栈实现的独立性, 使其可以与其他程序结合运行。
## 使用结构体使数据结构与代码块分离 
上一节实现方法中仅有 1 个栈，**如果有==多个栈==的时候怎么做才好呢？一种方法是编写两个名字不同，功能相同的函数**。即上一节的方法或是仅仅是 struct 而没有定义新类型。

另一种将栈的**==实现中所需的数据整合在一起==, 并允许内部持有多个栈**。
```
typedef struct{
	int top;
	const size t size;
	int const pBuf;
}Stack;

bool push(Stack *p,int val);
bool pop(Stack *p,int *pRet);
```

## 使用 c 面向对象编程
### 带检查功能的栈
栈中保存的值限定在一定范围内应该怎么做呢

一个办法是再编写一个函数代替 push 函数。但是这种实现方法传递的参数太多，而且每次 push 的时候都要传递允许的范围，非常麻烦。
**改进一下，在生成栈的时候将允许范围传递过去**
```
typedef struct{
	int top;
	const size t size;
	int ** const pBuf;
	
	const bool needRangeCheck;
	const int min;
	const int max;
}Stack;

#define newstack(buf){\
	0,sizeof(buf)/sizeof(int),(buf),\
	false,0,0\
}

#define newstackwithRangeCheck (buf,min,max){\
	0,sizeof(buf)/sizeof (int),(buf),\
	true,min,max\
}


static bool isRangeok(const Stack *p,int val){
	return p->needRangeCheck ||
		(p->min <val &val <p->max);
}

//true:成功，false:失败
bool push(Stack *p,int val){
	if (isRangeok(p,val) || isstackFull(p)) return false;
	p->pBuf [p->top++]val;
	return true;
}
```


### 带范围检查功能栈的缺点 
上面的代码中仍然有以下问题・
- 使耍生成的是不带范围检杏功能的栈. 栈内也需要保存 needRangeCheck、min. max 等多余的结构体成员，浪费了内存
- 在栈内增加其他校验功能. 就必须在结构体内再增加其他成员。push 函数也会因这些功能变得臃肿

**这次增加的结构体成员 needRangeCheck、min, max 真的必须和结构体的其他成员放在相同的位置吗? 这些成员只在 isRangeOk 函数中被使用**。
将它们作为结构体成员让所有函数都可以看到是不合适的作用域污染问题。

==首先我们要把这些成员分离出去==
```
typedef struct{
	const int min;
	const int max;
}Range;

typedef struct{
	int top;
	const size t size;
	int * const pBuf;
	const Range const pRange;
}stack;

#define newstack (buf){\
	0,sizeof(buf)sizeof(int),(buf),\
	NULL\
}

#define newstackwithRangeCheck(buf,pRange){\
	0,sizeof(buf)/sizeof(int),(buf),\
	pRange\
}



static bool isRangeok(const Range *p,int val){
	return p ==NULL ||
		(p->min <val &val <p->max);
}

//true:成功，false:失败
bool push(Stack *p,int val){
	if (isRangeok(p->pRange,val)isstackFull(p)) return false;
	p->pBuf [p->top++]val;
	return true;
}
```

### 检查功能的通用化
之前我们对校加入了输入值上限和尸限的检查功能, 但一般情况下, 检查并不限于范围检查, 例如, 如果要求每次 push 到栈中的值都必须比上次的值 (最开始是 0 以上)大 (虽然一般不会行这种要求, 这里只是以此为例讨论增加其他校验时的情况), 目前的设计还无法实现该需求, **但是只要将输入值检查变得更通用化就能解决这个问题**。

**==将检查输入值的通用职责转移到Validator结构体中==**。


**验证功能被转移至了通用函数** validate 中。如果它是 NULL, 也就是说当 Validator 不存在的时候返回 true; 如果非 NULL, 则调用 Validator 内部的函数指针所指向的函数进行校验处理, 并返回其校验结果。
```
stack.h
#ifndef STACK H
#define STACK H
#include <stddef.h>

typedef struct Validator{
	bool (*const validate)(struct Validator *pThis,int val);
	void const pData;
}Validator;

typedef struct{
	const int min;
	const int max;
}Range;

typedef struct{
	int previousValue;
}Previousvalue;


typedef struct{
	int top;
	const size t size;
	int const pBuf;
	Validator const pValidator;
}Stack;

bool validateRange(Validator *pThis,int val);
bool validatePrevious (Validator *pThis,int val);

bool push(Stack *p,int val);
bool pop(Stack *p,int *pRet);

#define newstack(buf){			\
	0,sizeof (buf)sizeof(int),(buf),\
	NULL							\
}

#define rangevalidator(pRange){\
	validateRange,				\
	pRange\
}

#define previousValidator(pPrevious){\
	validatePrevious,\
	pPrevious\
}

#define newstackwithvalidator(buf,pValidator){\
	0,sizeof(buf)/sizeof(int),(buf),\
	pValidator\
}

#endif
#endif
```

```
stack.c
#include <stdbool.h>
#include "stack.h"

static bool isStackFull(const Stack *p){
	return p->top =p->size;
}

static bool isstackEmpty(const stack *p){
	return p->top ==0;
}

bool validateRange(Validator *pThis,int val){
	Range*pRange=(Range)(pThis->pData)；
	return pRange->min <val &val <pRange->max;
}

bool validatePrevious (Validator *pThis,int val){
	Previousvalue *pPrevious =(PreviousValue *)pThis->pData;
	if (val pPrevious->previousvalue)return false;
	pPrevious->previousvalue val;
	return true;
}

bool validate(Validator *p,int val){
	if(!p)return true;
	return p->validate(p,val);
}

//true:成功，false:失败
bool push(Stack *p,int val){
	if (validate(p->pValidator,val)isstackFull(p))return false;
	p->pBuf [p->top++]val;
	return true;
}

/true:成功，fale:失败
bool pop(Stack *p,int *pRet){
	if (isStackEmpty(p))return false;
	*pRet p->pBuf [--p->top];
	return true;
}
```





## 面向对象和多态性 
**面向对象的基本思考方式是将数据和处理数据的行为放到一起**. 降低耦合性。要点就是不要将数据和处理数据的行为分开。
上节中的带检杳功能的栈的示例代码就将上限数据、下限数据和栈自身的数据都放在栈结构体中. 结果增加了耦合性也就是说，**仅将数据整合在一起. 是绝对无法降低耦合性的**。

**之后我们通过将校验处理和校验处理中所需数据从 Stack 结构体中分离出来, 将它们移至 Validator 结构体中，使得校验处理被解耦**, 从而可以方便地为栈中添加各种各样的校验功能，同时**这些功能也很容易地在其他功能中被复用**。
```
bool validate(Validator *p,int val){
	if (!p)return true;
	return p->validate(p,val);
}
```


像这样，**==通过将数据和处理成对分离==**，并使用结构体和函数指针实现多态性，就将校验职责 (赋予对象的任务)分离至 Validator 中了，而被分离出来的部分也可以作为组件被重复利用。
### 继承 
**实际上继承在前面的例子中已经有所体现。首先有一个校验器, 之后扩展出了范围检查校验器和 push 值递增校验器这两个校验器**。
虽然上面的例子中父类的存在比较模糊, 但是如果将没有设定 pData 的 Validator 看作父类，那么就可以将设定了 Range. PreviousValue 的 Validator 看作子类。
```
typedef struct Validator {  
	bool (* const validate)(struct Validator *pThis, int val); 
 	void * const pData;  
 } Validator;
 
 typedef struct{
	const int min;	
	const int max;
}Range;

bool validateRange(validator *pThis,int val){
	Range *pRange (Range *)(pThis->pData);
	return pRange->min <val &val <pRange->max;
}
```


**这个方法适用于简单情况, 但情况稍微复杂一些, 就显得很麻烦了。**
范围检查校验器中, 这个 pData 指向的是 Range 结构体。假设现在需要扩展范围检查校验器的功能, 使得栈中只能接受奇数或者偶数, 那么仅是简单地扩展 Range 的话, Range 在程序中的角色就会变得很模糊。
```
typedef struct
	const int min;	
	const int max;
	const bool needoddEvenCheck;//true表示需要进行奇偶校验
	const bool needToBeOdd; //true表示必须是奇数
}Range;
```

**Range 表示范围, 在这里加入奇偶校验本就很奇怪**, 而且即使不需要奇偶校验时, 也需要在结构体中保存两个多余的成员, 浪费内存。**虽然 C 不是面向对象语言, 无法使用继承功能优雅地解决这个问题, 但稍好一点的解决办法还是有的**




将**目前的两个校验器按照下面的方法重新编写,**
使用c实现对象继承
```
typedef struct Validator { 
 	bool (* const validate)(struct Validator *pThis, int val); 
} Validator; 

typedef struct { 
   Validator base; 
   const int min;  
   const int max;  
} RangeValidator; 

typedef struct { 
     Validator base; 
      int previousValue;  
} PreviousValueValidator; 
     
bool validateRange(Validator *pThis, int val);  
bool validatePrevious(Validator *pThis, int val);  
       
#define newRangeValidator(min, max) \ 
 	{{validateRange), (min), (max)}  
 
 #define newPreviousValueValidator \ 
 	{{validatePrevious}, 0}
```

```
bool validateRange(Validator *p, int val) {  
	RangeValidator *pThis = (RangeValidator *)p; 
	return pThis->min <= val && val <= pThis->max;  
}

bool validatePrevious(Validator *p, int val) {  			
	PreviousValueValidator *pThis = (PreviousValueValidator *)p; 
	if (val < pThis->previousValue) return false; 
	 pThis->previousValue = val;  
	 return true;  
 }
```

使用此方法就可以通过继承解决本节中最开始的提出的扩展 Range 的问题。具体而言，就是只'需要按照以下方**法将 RangeValidator 作为 base 使用即可扩展 RangeValidator**。
```
typedef struct{
	Rangevalidator base;
	const bool needoddEvenCheck;//true表示需要进行奇偶校验
	const bool needToBeOdd;//txue表示必须是奇数
}OddEvenRangevalidator;
```

==这样. c 中就也可以使用继承了==
### 封装
将对象的状态和行为集中在一起，并规定其与外部的接口来进行抽象化的过程
那么把状态认为是结构体中函数指针以外的成员, 把行为认为是函数指针成员。

也就是说 FILE 结构体中的内容对调用者来说是怎样都好, **不必在意的内部信息**, 只需将指向 FILE 结构体的指针当作参数传递给函数, 或是从函数接收指向 FILE 结构体的指针返回值即。

几乎所有的面向对象语言都提供了==访问控制功能以帮助程序员进行封装==, 这样就可以让**外部无法看见 Rangevalidator 中的内容** (数据隐藏，试图访问内部成员时会出错)。但是遗憾的是 **C 中没有提供访问控制功能，无法实现数据隐藏**。
实际上在前面的例子中, **我们使用了 const 修饰符, 这样就不必担心会从外部不小心修改内部数据了**. 此外, 还可以规定成员命名规则来回避这个问题, 例如不允许直接访问的成员在命名时以下划线**\_"开头。
```
typedef struct {
   Validator base,
   const int min
   const int max;
 }RangeValidator;
 
 typedef struct Validator{
	bool (const validate)(struct Validator *pThis,int val);
}Validator;
```

调用者只需要关注将 validate 函数身 (pThis)和校验时象的值 (val)传递过去, 就会得到 bool 类型的校验结果。
### 虚函数表
**各对象都持有函数指针，这样可能会导致内存浪费**
如果出现以下情况
•有多个对象都具有相同的行为 (即函数指针集相同)
•其中持有较多的函数指针
•需要生成较多数量的对象
持有函数指针的部分就很可能会浪费内存
此时, 如果引入虚函数表就可以避免回避内存浪费问题
```
typedef struct FooVtbl {  
	void (* const funcO)(struct Foo *pThis);  
	void (* const fund) (struct Foo *pThis);  
	void (* const func2)(struct Foo *pThis);  
} FooVtbl;  

static FooVtbl foo_vtbl = {func0_impl, funcl_impl, func2_impl};  

typedef struct Foo { 
 	const int count;  
 	const FooVtbl * const pVtbl;  
 } Foo;
 
 Foo fooO = {0, &foo_foo_vtbl};  
 Foo fool = {1, &foo_foo_vtbl); 
  Foo foo2 = {2, &foo_foo_vtbl};
```

这样的代码结构仅需要在对象中持有指向虚函数表的指针即可，而无需持有函数指针，因此可以节约内存。
但另一方面，由于函数调用必须经过虚函数表, 所以需要使用如下的调用方法，程序的结构也变得复杂了。
```
pFoo->pVtbl->func(pFoo);
```

### 非虚函数
通过在==**对象内持有函数指针，可以让对象的行为根据对象不同而发生变化**==。
但是==**某些函数在不同的对象中处理也可能是相同的，这时就无需在对象内持有函数指针了**==
```
typedef struct Foo {  
	int count;  
	void (*funcO)(structFoo *pThis);  
	void (*funcl)(structFoo *pThis);  
	void (*func2)(structFoo *pThis);  
} Foo;
```
假设这里需要**增加一个将 count 复位为 0 的函数**，这时增加一个虚函数倒也可以
```
typedef struct Foo {  
	int count;  
	void (*funcO)(structFoo *pThis);  
	void (*funcl)(structFoo *pThis);  
	void (*func2)(structFoo *pThis); 
	 void (*reset_counter) (struct Foo *pThis) ; // 增加结构体成员 
 } Foo;
```

但如果只==是将 count 恢复为 0. 就没有必要动态地根据对象不同改变函数行为: 这种情况下，也可以单独使用一个函数来实现==
```
typedef struct Foo { //保持不变  
	int count;  
	void (*funcO)(struct Foo *pThis);  
	void (*funcl)(struct Foo *pThis);  
	void (*func2)(struct Foo *pThis);  
} Foo;  

void reset_foo_counter(Foo *pThis) {  
	pThis->count = 0; 
 }
```

如果是 c 语言的话还有一个命名空间的问题函数命名为 resst_foo_counter 表明该函数是 Foo 使用的函数, 如果简单地以 reset_counter 命名的话, 碰巧 Bar 结构体也有一个名为 count 的成员和一个复位函数 reset_counter,则会发生函数命名冲突
static 修饰符可以避免命名冲
本书后面的章节也会提及, 相比非虚函数, 使用函数指针的方式更加容易测试

**一般情况下, 请优先使用函数指针, 只有在内存非常有限、对象行为不会变化的情况下, 或者是非常有把握的情况下才考虑使用非虚函数**


首先如果内存使用量过多，请考虑使用虚函数表并将其保存在 ROM 空间中。由于虚函数表不会改变，所以存储在 ROM 上也没有问题
关于运行效率问题，当函数指针的调用成为性能瓶颈的时候，就应该考虑使用非虚函数或是使用宏


**==在结构体内持有函数指针的方法来实现多态==**
但是, 这种方法可能会造成内存浪费。接着本章又介绍了虚函数表来解决这个问题
本章**==还介绍了在不需要多态性的函数时可以使用非虚函数==**。




在工程中，面向对象的C语言编程方法有助于提高代码的可维护性、可扩展性和模块化程度。通过将数据和处理数据的行为封装在一起，可以降低代码的耦合性，增强代码的独立性和可复用性。使用抽象数据类型和信息隐藏技术，可以隐藏内部实现细节，使模块的接口更加简洁和稳定。此外，通过引入多态性和继承机制，可以灵活地扩展功能，避免重复代码，并提高代码的可读性和可测试性。面向对象的C语言编程方法在处理复杂系统时尤为重要，它能够帮助开发者更好地组织代码，应对需求变化，并提高系统的可靠性和性能。

工程中为什么需要面向对象c，及其总结分别列出，300字内不分点

在工程中，面向对象的C语言编程方法能够显著提升代码的可维护性和可扩展性。通过将数据和处理数据的行为封装在一起，可以降低代码的耦合性，增强模块的独立性和复用性。使用抽象数据类型和信息隐藏技术，可以隐藏内部实现细节，使模块接口更加简洁和稳定，从而减少外部依赖，便于维护和升级。此外，通过引入多态性和继承机制，可以灵活地扩展功能，避免重复代码，并提高代码的可读性和可测试性。面向对象的C语言编程方法在处理复杂系统时尤为重要，它能够帮助开发者更好地组织代码，应对需求变化，并提高系统的可靠性和性能。通过合理设计模块接口和数据结构，可以有效减少开发和维护成本，提升开发效率和代码质量。




随着软件项目的规模和复杂性增加，代码的可维护性和可扩展性变得越来越重要。
C语言的代码通常是面向过程的，容易导致代码结构混乱，难以维护。
C语言本身不支持面向对象编程，C语言没有类和对象的概念，缺乏面对对象的机制，但通过结构体和函数指针，可以模拟对象的行为，帮助开发者模拟面向对象的特性，如封装、继承和多态，可以将功能模块化，减少代码的耦合性。