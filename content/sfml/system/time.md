+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '处理时间'
+++

# 处理时间

## SFML 中的时间

与许多其他库将时间表示为 uint32 类型的毫秒数或是 float 类型的秒数不同，SFML 没有对时间值强加任何特定的单位或类型。
相反，它通过一个灵活的类将这个选择权交给了用户：[`sf::Time`](../../../../documentation/3.1.0/classsf_1_1Time.html "sf::Time documentation")。
所有操作时间值的 SFML 类和函数都使用这个类。

[`sf::Time`](../../../../documentation/3.1.0/classsf_1_1Time.html "sf::Time documentation") 代表的是一个时间段（换句话说，就是两个事件之间流逝的时间）。
它**不是**一个用于表示当前年/月/日/时/分/秒的时间戳（日期时间类）。
它仅仅是一个代表一定时长的时间值，至于如何解释它，则取决于它被使用的上下文。

## 转换时间

一个 [`sf::Time`](../../../../documentation/3.1.0/classsf_1_1Time.html "sf::Time documentation") 值可以从不同的源单位构造而来：秒、毫秒和微秒。
我们提供了一组自由函数（free function）来将它们各自转变为一个 [`sf::Time`](../../../../documentation/3.1.0/classsf_1_1Time.html "sf::Time documentation") 对象：

```cpp
sf::Time t1 = sf::microseconds(10000);
sf::Time t2 = sf::milliseconds(10);
sf::Time t3 = sf::seconds(0.01f);
```

请注意，这三个时间值是完全相等的。

类似地，一个 [`sf::Time`](../../../../documentation/3.1.0/classsf_1_1Time.html "sf::Time documentation") 也可以被转换回秒、毫秒或微秒：

```cpp
sf::Time time = ...;

std::int64_t usec = time.asMicroseconds();
std::int32_t msec = time.asMilliseconds();
float        sec  = time.asSeconds();
```

通过以下两种方式，SFML 支持与 C++ 标准库中的 `std::chrono::duration` 进行转换。

1.  一个接受任意 `std::chrono::duration` 特化类型的隐式构造函数。
2.  一个向任意 `std::chrono::duration` 特化类型的隐式转换运算符。

```cpp
sf::Time time = std::chrono::milliseconds(100); // (1) 从 std::chrono::milliseconds 隐式构造
std::this_thread::sleep_for(time); // (2) 隐式转换为 std::chrono::nanoseconds
```

这两种转换机制允许该类与使用 `<chrono>` 头文件的接口实现无缝的互操作。

## 操控时间值

由于 [`sf::Time`](../../../../documentation/3.1.0/classsf_1_1Time.html "sf::Time documentation") 仅仅是一个时间量，因此它支持诸如加、减、比较等算术运算。
时间值也可以是负数。

```cpp
sf::Time t1 = ...;
sf::Time t2 = t1 * 2;
sf::Time t3 = t1 + t2;
sf::Time t4 = -t3;

bool b1 = (t1 == t2);
bool b2 = (t3 > t4);
```

`sf::Time` 已经全面支持了 `constexpr`，所以所有这些操作都可以在编译期上下文中执行。

## 测量时间

既然我们已经了解了如何用 SFML 操作时间值，接下来让我们看看如何完成几乎每一个程序都会用到的功能：测量流逝的时间。

SFML 提供了一个非常简单的类用于测量时间：[`sf::Clock`](../../../../documentation/3.1.0/classsf_1_1Clock.html "sf::Clock documentation")。
它提供了一系列函数来操作和查询流逝的时间。

```cpp
sf::Clock clock; // 启动时钟
...
sf::Time elapsed1 = clock.getElapsedTime();
std::cout << elapsed1.asSeconds() << std::endl;
clock.restart();
...
sf::Time elapsed2 = clock.getElapsedTime();
std::cout << elapsed2.asSeconds() << std::endl;
...
clock.stop(); // 停止时钟
std::cout << std::boolalpha << clock.isRunning() << std::endl;
clock.reset(); // 将流逝的时间重置为零
...
clock.start(); // 启动时钟
sf::Time elapsed3 = clock.getElapsedTime();
std::cout << elapsed3.asSeconds() << std::endl;
```

请注意，`restart` 也会返回在此之前流逝的时间，这样你可以避免因为在调用 `restart` 之前显式调用 `getElapsedTime` 所产生的轻微时间差。

下面是一个利用游戏循环每次迭代所流逝的时间来更新游戏逻辑的示例：

```cpp
sf::Clock clock;
while (window.isOpen())
{
    sf::Time elapsed = clock.restart();
    updateGame(elapsed);
    ...
}
```
