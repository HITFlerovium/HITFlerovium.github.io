+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '处理角度'
+++

# 处理角度

## SFML 中的角度

[`sf::Angle`](../../../../documentation/3.1.0/classsf_1_1Angle.html "sf::Angle documentation") 以一种与单位无关的方式来表示角度，这使得你可以无论是从度数还是从弧度的角度来考量它。
SFML 中定义角度遵循[右手定则](https://en.wikipedia.org/wiki/Right-hand_rule)。
这意味着如果窗口中 X 轴向右，Y 轴向下，那么正角度对应的是顺时针旋转。
所有与角度相关的 SFML 类都使用 `sf::Angle`。

所有的 `sf::Angle` 函数都启用了 `constexpr`，因此这里展示的所有操作都可以在编译期完成。

## 构造角度

有两个用于构造角度的工厂函数：`sf::degrees` 和 `sf::radians`。

```cpp
sf::Angle angle1 = sf::degrees(180);
sf::Angle angle2 = sf::radians(3.1415f);
```

这两个函数可以分别从度数或弧度构建出近似相等的角度，这样你在编写自己的代码时就无需再去费心考虑单位问题了。
请根据你的需要随意选用这两个函数。
`sf::Angle` 会在内部处理好任何必需的单位转换。

## 操作角度

`sf::Angle` 提供了一系列的运算符来进行算术操作。
你可以对角度进行加、减、乘、除运算。
同时还提供了取模、相等、不相等以及大小比较等运算符。

```cpp
sf::Angle angle1 = sf::degrees(10);
angle1 *= 2.f; // 20 度
sf::Angle angle2 = angle1 + sf::radians(0.5f); // 48.6 度
angle2 = -angle2; // -48.6 度
angle2 /= 3.f; // -16.2 度

bool equal = (angle1 == angle2); // false
bool inequal = (angle1 != angle2); // true
```

`sf::Angle` 可以存在于 [-pi, pi) 或 [0, 2pi) 范围之外。
例如，一个角度的值可能是 720 度。
如果你希望获取一个新角度，使其值等效地被限制（折叠）在一个更小的范围内，有两个函数可以做到这一点：`sf::Angle::wrapSigned` 和 `sf::Angle::wrapUnsigned`。

*   `wrapSigned` 将返回一个被限制在 [-pi, pi) 范围内的新角度。
*   `wrapUnsigned` 将返回一个被限制在 [0, 2pi) 范围内的新角度。

```cpp
sf::Angle angle1 = sf::degrees(540).wrapUnsigned(); // 180 度

sf::Angle angle2 = sf::radians(2 * 3.1415f).wrapSigned(); // 0 度
```

转换之后，这些角度在单位圆上将占据完全相同的位置。

## 用户定义字面量

C++ 的用户定义字面量为书写角度提供了一种便捷的简写形式。
这些字面量存在于 `sf::Literals` 命名空间中。
将该命名空间引入当前作用域即可使用它们。

```cpp
using namespace sf::Literals;
sf::Angle angle1 = 45_deg; // 45 度
sf::Angle angle2 = angle1 + 3.1415_rad; // 225 度
```

## 访问底层数值

如果你想将角度格式化为文本，或者把该数值传递给像 `std::sin` 这样的函数，可以使用两个将角度作为原始 `float` 浮点数进行访问的函数：`sf::Angle::asDegrees` 和 `sf::Angle::asRadians`。

```cpp
sf::Angle angle1 = sf::radians(2);
std::cout << angle1.asDegrees() << std::endl;

sf::Angle angle2 = sf::degrees(270);
std::cout << std::sin(angle2.asRadians()) << std::endl;
```
