---
up:
  - "[[../moc/moc对象设计模式]]"
---
# c 对应的类属性
## 继承
```
#include <stdio.h>

// 基类：动物
typedef struct {
    int age;
} Animal;

// 派生类：狗，继承了动物的特征，并添加了自己的特征
typedef struct {
    Animal animal;  // 继承基类
    int barkVolume;
} Dog;

int main() {
    Dog myDog;
    myDog.animal.age = 5;        // 访问继承的特征
    myDog.barkVolume = 10;       // 访问派生特征

    printf("My dog is %d years old and barks at volume %d.\n", myDog.animal.age, myDog.barkVolume);
    return 0;
}

```
## 封装 
封装是将数据和操作数据的函数捆绑在一起，并隐藏内部实现细节。
C 语言没有内建的封装机制，但可以通过使用 static 关键字和函数指针模拟。

模拟封装的方式：
私有和公共接口：可以将结构体定义和相关函数放在一个文件中（例如. c 文件），而将接口函数声明放在另一个文件中（例如. h 文件）。这样可以隐藏实现细节，只暴露公共接口。

```
// device.h
#ifndef DEVICE_H
#define DEVICE_H

typedef struct {
    int batteryLevel;
} Device;

void chargeDevice(Device* device, int amount);
int getBatteryLevel(const Device* device);

#endif // DEVICE_H

```
```
// device.c
#include "device.h"

static void internalFunction() {
    // 可能是内部的、复杂的功能
}

void chargeDevice(Device* device, int amount) {
    device->batteryLevel += amount;
    internalFunction();  // 内部函数的调用
}

int getBatteryLevel(const Device* device) {
    return device->batteryLevel;
}


```
internalFunction 是 static 内部定义调用，并且没有在. h 中声明

解释：device. h 只提供了对外的接口，隐藏了内部的实现细节（如 internalFunction）。外部代码只需要关心如何使用 chargeDevice 和 getBatteryLevel 函数，而不必了解具体的实现。
## 多态
在 C 语言中，多态通常通过函数指针来实现，可以实现类似于接口的功能。
可以在结构体中定义函数指针，指向不同的实现函数，以实现不同的行为。
```
#include <stdio.h>

// 定义一个接口
typedef struct {
    void (*turnOn)();
} Appliance;

// 具体实现：电视
void tvTurnOn() {
    printf("TV is now ON.\n");
}

// 具体实现：音响
void speakerTurnOn() {
    printf("Speaker is now ON.\n");
}

int main() {
    Appliance tv;
    Appliance speaker;

    tv.turnOn = tvTurnOn;
    speaker.turnOn = speakerTurnOn;

    tv.turnOn();     // 输出: TV is now ON.
    speaker.turnOn(); // 输出: Speaker is now ON.

    return 0;
}


```