+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '键盘、鼠标与手柄'
+++

# 键盘、鼠标与手柄

## 简介

本教程解释了如何访问全局输入设备：键盘、鼠标和手柄。
千万不要将它与事件混淆。
实时输入允许你在任何时候查询键盘、鼠标和手柄的全局状态（“**这个按钮现在被按下了吗？**”，“**鼠标现在在哪里？**”），而事件则是在有事情发生时通知你（“**这个按钮被按下了**”，“**鼠标移动了**”）。

## 键盘

提供访问键盘状态的命名空间是 [`sf::Keyboard`](../../../../documentation/3.1.0/namespacesf_1_1Keyboard.html "sf::Keyboard documentation")。
它包含同一个函数 `isKeyPressed` 的两个重载，用于检查按键的当前状态（按下或释放）。

此函数直接读取键盘状态，并忽略你窗口的焦点状态。
这意味着即使你的窗口处于非活跃状态，`isKeyPressed` 也可能返回 true。

```cpp
if (sf::Keyboard::isKeyPressed(sf::Keyboard::Key::Left))
{
    // 左方向键被按下了：移动我们的角色
    character.move({-1.f, 0.f});
}
```

键码（Key codes）定义在 `sf::Keyboard::Key` 枚举中。

```cpp
if (sf::Keyboard::isKeyPressed(sf::Keyboard::Scan::Right))
{
    // 右方向键被按下了：移动我们的角色
    character.move({1.f, 0.f});
}
```

扫描码（Scancodes）定义在 `sf::Keyboard::Scancode` 枚举中。

## 鼠标

提供访问鼠标状态的命名空间是 [`sf::Mouse`](../../../../documentation/3.1.0/namespacesf_1_1Mouse.html "sf::Mouse documentation")。

你可以检查鼠标按键是否被按下：

```cpp
if (sf::Mouse::isButtonPressed(sf::Mouse::Button::Left))
{
    // 鼠标左键被按下了：开火
    gun.fire();
}
```

鼠标按键代码定义在 `sf::Mouse::Button` 枚举中。
SFML 支持最多 5 个按键：左键、右键、中键（滚轮），以及两个可能对应任何功能的附加按键。

你还可以获取和设置鼠标的当前位置，这可以是相对于桌面的，也可以是相对于某个窗口的：

```cpp
// 获取全局鼠标位置（相对于桌面）
sf::Vector2i globalPosition = sf::Mouse::getPosition();

// 获取局部鼠标位置（相对于一个窗口）
sf::Vector2i localPosition = sf::Mouse::getPosition(window); // window 是一个 sf::Window
```

```cpp
// 全局设置鼠标位置（相对于桌面）
sf::Mouse::setPosition({10, 50});

// 局部设置鼠标位置（相对于一个窗口）
sf::Mouse::setPosition({10, 50}, window); // window 是一个 sf::Window
```

目前没有用于读取鼠标滚轮当前状态的函数。
由于滚轮只能进行相对移动，它没有可被查询的绝对状态。
通过观察一个按键，你可以分辨出它是被按下还是被释放了。
通过观察鼠标光标，你可以分辨出它在屏幕上的具体位置。
然而，仅仅观察鼠标滚轮并不能告诉你它处于哪个“刻度”上。
你只能在它移动时收到通知（`MouseWheelScrolled` 事件）。

有关如何使用事件的更多信息，请参阅[事件教程](../events/)。

## 手柄

提供访问手柄状态的命名空间是 [`sf::Joystick`](../../../../documentation/3.1.0/namespacesf_1_1Joystick.html "sf::Joystick documentation")。

手柄通过它们的索引来标识（从 0 到 7，因为 SFML 最多支持 8 个手柄）。
因此，[`sf::Joystick`](../../../../documentation/3.1.0/namespacesf_1_1Joystick.html "sf::Joystick documentation") 中每个函数的第一个参数就是你想要查询的手柄的索引。

你可以检查某个手柄是否已连接：

```cpp
if (sf::Joystick::isConnected(0))
{
    // 0 号手柄已连接
    ...
}
```

你也可以获取已连接手柄的能力信息：

```cpp
// 检查 0 号手柄有多少个按钮
unsigned int buttonCount = sf::Joystick::getButtonCount(0);

// 检查 0 号手柄是否拥有 Z 轴
bool hasZ = sf::Joystick::hasAxis(0, sf::Joystick::Axis::Z);
```

手柄轴定义在 `sf::Joystick::Axis` 枚举中。
由于按钮没有特殊含义，它们只是简单地从 0 编号到 31。

最后，你同样可以查询手柄的轴和按钮的状态：

```cpp
// 0 号手柄的 1 号按钮被按下了吗？
if (sf::Joystick::isButtonPressed(0, 1))
{
    // 是的：开火！
    gun.fire();
}

// 0 号手柄 X 轴和 Y 轴的当前位置是什么？
float x = sf::Joystick::getAxisPosition(0, sf::Joystick::Axis::X);
float y = sf::Joystick::getAxisPosition(0, sf::Joystick::Axis::Y);
character.move({x, y});
```

当你检查事件时，手柄的状态会被自动更新。
如果你不去检查事件，或者需要在启动游戏循环之前查询手柄状态（例如，检查连接了哪些手柄），你就必须手动调用 `sf::Joystick::update()` 函数来确保手柄状态是最新的。
