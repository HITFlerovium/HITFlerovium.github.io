+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '事件详解'
+++

# 事件详解

## 简介

本教程详细列出了所有的窗口事件。
它对这些事件进行了描述，并展示了如何（以及不该如何）使用它们。

## sf::Event 类型

SFML 使用类型安全的 API 来处理事件。
有两种主要方式可以使用此 API。
有关这两种方法的综合示例，请查看 [EventHandling 示例程序](https://github.com/SFML/SFML/tree/master/examples/event_handling "EventHandling example on GitHub")。

### `sf::Event::getIf<T>`

第一种选择是基于 `sf::Event` 的成员函数 `getIf<T>` 和 `is<T>`。
模板参数 `T` 必须是一个事件子类型，例如 `sf::Event::Resized` 或 `sf::Event::MouseMoved`。
如果模板参数与当前活跃的事件子类型相匹配，`getIf<T>` 将返回指向该特定事件子类型的指针。
否则，它将返回 `nullptr`。

如果模板参数与当前活跃的事件子类型相匹配，`is<T>` 将返回 `true`。
否则，它将返回 `false`。
这对于像 `sf::Event::Closed` 这种不包含任何数据的子类型特别有用。

请注意获取事件的 API 与 SFML 2 相比发生了微小的变化。
`sf::WindowBase::pollEvent` 和 `sf::WindowBase::waitEvent` 返回一个 `std::optional<sf::Event>`。
这两个函数**可能**会返回一个事件，但也可能不会。

它的代码如下所示：

```cpp
while (window.isOpen())
{
    while (const std::optional event = window.pollEvent())
    {
        if (event->is<sf::Event::Closed>())
        {
            window.close();
        }
        else if (const auto* keyPressed = event->getIf<sf::Event::KeyPressed>())
        {
            if (keyPressed->scancode == sf::Keyboard::Scancode::Escape)
                window.close();
        }
    }

    // 主循环的其他部分
}
```

C++ 允许你推导模板参数，这就是为什么你可以写成 `const std::optional event` 而不是 `const std::optional<sf::Event> event` 的原因。
如果你更喜欢简短的表达式，`const auto event` 也是一个有效的选择。

### `sf::WindowBase::handleEvents`

处理事件的第二种选择是通过 `sf::WindowBase::handleEvents` 函数。
这个函数执行事件访问（event visitation）。
这意味着你可以提供 lambda 表达式或其他可调用对象，它们将不同的事件子类型作为参数。
或者，你也可以提供一个（或多个）实现了 `operator()` 的对象来处理你想要处理的事件子类型。
根据当前活跃的事件子类型，将调用相应的回调函数。

> [!NOTE]
> 你无需为所有可能的事件子类型都提供回调函数。

它的代码如下所示：

```cpp
const auto onClose = [&window](const sf::Event::Closed&)
{
    window.close();
};

const auto onKeyPressed = [&window](const sf::Event::KeyPressed& keyPressed)
{
    if (keyPressed.scancode == sf::Keyboard::Scancode::Escape)
        window.close();
};

while (window.isOpen())
{
    window.handleEvents(onClose, onKeyPressed);

    // 主循环的其他部分
}
```

## Closed 事件

当用户希望通过窗口管理器提供的任何可能方式（“关闭”按钮、键盘快捷键等）关闭窗口时，会触发 `sf::Event::Closed` 事件。
此事件仅代表一个关闭请求，这意味着在收到事件时窗口尚未关闭。

通常，针对此事件，我们只需调用 `window.close()` 就能真正关闭窗口。
但是，你可能还想先做些其他事情，例如保存当前的应用程序状态，或者询问用户要执行什么操作。
如果你什么都不做，窗口将保持打开状态。

此事件没有关联的事件数据。

```cpp
if (event->is<sf::Event::Closed>())
    window.close();
```

## Resized 事件

当窗口被调整大小时（无论是通过用户操作还是通过调用 `window.setSize` 以编程方式触发），都会触发 `sf::Event::Resized` 事件。
你可以使用此事件来调整渲染设置：如果你直接使用 OpenGL 则调整视口（viewport）；如果你使用 sfml-graphics，则调整当前视图（view）。

与此事件关联的数据包含了窗口的新尺寸。

```cpp
if (const auto* resized = event->getIf<sf::Event::Resized>())
{
    std::cout << "new width: " << resized->size.x << std::endl;
    std::cout << "new height: " << resized->size.y << std::endl;
}
```

## FocusLost 与 FocusGained 事件

当窗口失去或获得焦点时（即当用户切换当前活跃窗口时），会触发 `sf::Event::FocusLost` 和 `sf::Event::FocusGained` 事件。
当窗口失去焦点时，它将不会接收到键盘事件。
例如，如果你想在窗口处于非活跃状态时暂停游戏，就可以使用此事件。

这两个事件都没有关联的事件数据。

```cpp
if (event->is<sf::Event::FocusLost>())
    myGame.pause();

if (event->is<sf::Event::FocusGained>())
    myGame.resume();
```

## TextEntered 事件

当键入一个字符时，会触发 `sf::Event::TextEntered` 事件。
千万不要将它与 `KeyPressed` 事件混淆。
`TextEntered` 会解析用户输入并生成合适的可打印字符。
例如，在法语键盘上先按 '^' 再按 'e' 会产生两个 `KeyPressed` 事件，但只会产生一个包含 'ê' 字符的 `TextEntered` 事件。
它适用于操作系统提供的所有输入法，即使是最特殊或最复杂的输入法也是如此。

此事件通常用于捕获文本字段中的用户输入。

与此事件关联的数据包含了所输入字符的 Unicode 值。
你可以将此数据直接存入 [`sf::String`](../../../../documentation/3.1.0/classsf_1_1String.html "sf::String documentation") 中，或者在确保其位于 ASCII 范围（0 - 127）内之后，将其强制转换为 `char` 类型。

```cpp
if (const auto* textEntered = event->getIf<sf::Event::TextEntered>())
{
    if (textEntered->unicode < 128)
        std::cout << "ASCII character typed: " << static_cast<char>(textEntered->unicode) << std::endl;
}
```

请注意，由于它们属于 Unicode 标准的一部分，一些不可打印字符（如退格键）也会由此事件生成。
在大多数情况下，你需要将它们过滤掉。

> [!WARNING]
> 许多程序员喜欢使用 `KeyPressed` 事件来获取用户输入，并试图通过编写疯狂的算法来解析所有可能的按键组合以生成正确的字符。
> 千万不要这么做！

## KeyPressed 与 KeyReleased 事件

当按下或释放键盘按键时，会触发 `sf::Event::KeyPressed` 和 `sf::Event::KeyReleased` 事件。

如果按住某个按键不放，系统将按照操作系统的默认延迟间隔持续生成多个 `KeyPressed` 事件（即与在文本编辑器中按住某个字母时适用的延迟相同）。
要禁用重复的 `KeyPressed` 事件，你可以调用 `window.setKeyRepeatEnabled(false)`。
另一方面，显而易见 `KeyReleased` 事件是永远无法重复的。

如果你想在按下或释放按键时恰好触发一次操作（比如按空格键让角色跳跃，或者按 Esc 退出某事），那么这个事件就是你的最佳选择。

有时，人们会试图直接对 `KeyPressed` 事件做出反应来实现平滑移动。
这样做**不会**产生预期的效果，因为当你按住按键时，你只能得到寥寥几个事件（还记得上面提到的重复延迟吗？）。
为了通过事件实现平滑移动，你必须使用一个布尔变量，在 `KeyPressed` 时将其设为 true，在 `KeyReleased` 时将其清空；然后，只要这个布尔变量为 true，你就可以（独立于事件）进行移动了。

实现平滑移动的另一个（更简单的）解决方案，是使用 [`sf::Keyboard`](../../../../documentation/3.1.0/namespacesf_1_1Keyboard.html "sf::Keyboard documentation") 进行实时键盘输入监控（参阅[相关的教程](../inputs/ "Real-time inputs tutorial")）。

与这些事件关联的数据包含了按下或释放按键的扫描码（scancode）和键码（key code），以及修饰键（alt、control、shift、system）的当前状态。

扫描码对于键盘上的每个物理按键来说都是唯一的值，不受语言或布局的影响，而键码则表示基于用户所选布局的按键。
例如，在美式键盘布局下，Z 键位于 X 键左侧的最底下一排。
如果你引用 Z 键的扫描码，就可以在任何键盘上定位到这一个物理按键的位置。
然而，在德语布局下，同一个物理按键的标签是 Y。
因此，使用 Y 的键码可能会指向不同的物理按键位置，这取决于所选择的布局。

如果按键的物理位置（例如使用 WASD 键进行移动）比受制于键盘布局的按键值更重要的话，强烈建议使用扫描码而不是键码。

```cpp
if (const auto* keyPressed = event->getIf<sf::Event::KeyPressed>())
{
    if (keyPressed->scancode == sf::Keyboard::Scan::Escape)
    {
        std::cout << "the escape key was pressed" << std::endl;
        std::cout << "scancode: " << static_cast<int>(keyPressed->scancode) << std::endl;
        std::cout << "code: " << static_cast<int>(keyPressed->code) << std::endl;
        std::cout << "control: " << keyPressed->control << std::endl;
        std::cout << "alt: " << keyPressed->alt << std::endl;
        std::cout << "shift: " << keyPressed->shift << std::endl;
        std::cout << "system: " << keyPressed->system << std::endl;
        std::cout << "description: " << sf::Keyboard::getDescription(keyPressed->scancode).toAnsiString() << std::endl;
        std::cout << "localize: " << static_cast<int>(sf::Keyboard::localize(keyPressed->scancode)) << std::endl;
        std::cout << "delocalize: " << static_cast<int>(sf::Keyboard::delocalize(keyPressed->code)) << std::endl;
    }
}
```

> [!NOTE]
> 请注意，某些按键对操作系统具有特殊含义，可能会导致意料之外的行为。
> 例如 Windows 上的 F10 键会“窃取”焦点，而在使用 Visual Studio 时，F12 键会启动调试器。

## MouseWheelScrolled 事件

当鼠标滚轮向上或向下滚动时，或者如果鼠标支持横向滚动时，也会触发 `sf::Event::MouseWheelScrolled` 事件。

与此事件关联的数据包含了滚轮滚动的刻度数、滚轮滚动的方向以及当前鼠标光标的位置。

```cpp
if (const auto* mouseWheelScrolled = event->getIf<sf::Event::MouseWheelScrolled>())
{
    switch (mouseWheelScrolled->wheel)
    {
        case sf::Mouse::Wheel::Vertical:
            std::cout << "wheel type: vertical" << std::endl;
            break;
        case sf::Mouse::Wheel::Horizontal:
            std::cout << "wheel type: horizontal" << std::endl;
            break;
    }
    std::cout << "wheel movement: " << mouseWheelScrolled->delta << std::endl;
    std::cout << "mouse x: " << mouseWheelScrolled->position.x << std::endl;
    std::cout << "mouse y: " << mouseWheelScrolled->position.y << std::endl;
}
```

## MouseButtonPressed 与 MouseButtonReleased 事件

当鼠标按键被按下或释放时，会触发 `sf::Event::MouseButtonPressed` 和 `sf::Event::MouseButtonReleased` 事件。
SFML 支持 5 个鼠标按键：左键、右键、中键（滚轮）、附加键 #1 和附加键 #2（侧键）。

与这些事件关联的数据包含了按下或释放按键的代码，以及鼠标光标的当前位置。

```cpp
if (const auto* mouseButtonPressed = event->getIf<sf::Event::MouseButtonPressed>())
{
    if (mouseButtonPressed->button == sf::Mouse::Button::Right)
    {
        std::cout << "the right button was pressed" << std::endl;
        std::cout << "mouse x: " << mouseButtonPressed->position.x << std::endl;
        std::cout << "mouse y: " << mouseButtonPressed->position.y << std::endl;
    }
}
```

## MouseMoved 事件

当鼠标在窗口内移动时，会触发 `sf::Event::MouseMoved` 事件。

> [!NOTE]
> 即使窗口没有焦点，此事件也会被触发，但仅当鼠标在窗口的内部区域移动时有效，如果鼠标移动到标题栏或窗口边框上方，则不会触发。

与此事件关联的数据包含了鼠标光标相对于窗口的当前位置。

```cpp
if (const auto* mouseMoved = event->getIf<sf::Event::MouseMoved>())
{
    std::cout << "new mouse x: " << mouseMoved->position.x << std::endl;
    std::cout << "new mouse y: " << mouseMoved->position.y << std::endl;
}
```

## MouseMovedRaw 事件

只要鼠标在窗口内移动，甚至在鼠标移动距离微小到难以察觉时，也会触发 `sf::Event::MouseMovedRaw` 事件。

`sf::Event::MouseMoved` 的位置值受限于屏幕分辨率，而此事件的原始数据则不然。
如果物理鼠标的移动量太小，甚至不足以让屏幕上的光标移动哪怕一个像素，那么将不会生成 `sf::Event::MouseMoved` 事件。
相比之下，无论鼠标传感器的分辨率如何，任何鼠标生成的移动信息都会始终触发 `sf::Event::MouseMovedRaw` 事件。

与此事件关联的数据包含了鼠标光标相对于窗口的位置变化量。

```cpp
if (const auto* mouseMovedRaw = event->getIf<sf::Event::MouseMovedRaw>())
{
    std::cout << "new mouse x: " << mouseMoved->delta.x << std::endl;
    std::cout << "new mouse y: " << mouseMoved->delta.y << std::endl;
}
```

> [!NOTE]
> 目前，原始鼠标输入事件仅在 Windows 和 Linux 系统上生成。

## MouseEntered 与 MouseLeft 事件

当鼠标光标进入或进入离开窗口时，会触发 `sf::Event::MouseEntered` 和 `sf::Event::MouseLeft` 事件。
这两个事件没有关联的事件数据。

```cpp
if (event->is<sf::Event::MouseEntered>())
    std::cout << "the mouse cursor has entered the window" << std::endl;

if (event->is<sf::Event::MouseLeft>())
    std::cout << "the mouse cursor has left the window" << std::endl;
```

## JoystickButtonPressed 与 JoystickButtonReleased 事件

当手柄（摇杆）按钮被按下或释放时，会触发 `sf::Event::JoystickButtonPressed` 和 `sf::Event::JoystickButtonReleased` 事件。

SFML 支持最多 8 个手柄和 32 个按钮。

与这些事件关联的数据包含了手柄的标识符以及按下或释放按钮的索引。

```cpp
if (const auto* joystickButtonPressed = event->getIf<sf::Event::JoystickButtonPressed>())
{
    std::cout << "joystick button pressed!" << std::endl;
    std::cout << "joystick id: " << joystickButtonPressed->joystickId << std::endl;
    std::cout << "button: " << joystickButtonPressed->button << std::endl;
}
```

## JoystickMoved 事件

当手柄轴发生移动时，会触发 `sf::Event::JoystickMoved` 事件。
手柄轴通常非常敏感。
这就是为什么 SFML 使用检测阈值来避免大量 `JoystickMoved` 事件淹没你的事件循环的原因。
你可以通过 `sf::Window::setJoystickThreshold` 函数来更改此阈值，以便接收更多或更少的手柄移动事件。

SFML 支持 8 个手柄轴：X、Y、Z、R、U、V、POV X 和 POV Y。
它们如何映射到你的手柄，取决于手柄驱动程序。

与此事件关联的数据包含了手柄的标识符、轴的名称，以及它的当前位置（范围在 [-100, 100] 之间）。

```cpp
if (const auto* joystickMoved = event->getIf<sf::Event::JoystickMoved>())
{
    if (joystickMoved->axis == sf::Joystick::Axis::X)
    {
        std::cout << "X axis moved!" << std::endl;
        std::cout << "joystick id: " << joystickMoved->joystickId << std::endl;
        std::cout << "new position: " << joystickMoved->position << std::endl;
    }
}
```

## JoystickConnected 与 JoystickDisconnected 事件

当手柄连接或断开时，会触发 `sf::Event::JoystickConnected` 和 `sf::Event::JoystickDisconnected` 事件。

与此事件关联的数据包含了已连接或已断开手柄的标识符。

```cpp
if (const auto* joystickConnected = event->getIf<sf::Event::JoystickConnected>())
    std::cout << "joystick connected: " << joystickConnected->joystickId << std::endl;

if (const auto* joystickDisconnected = event->getIf<sf::Event::JoystickDisconnected>())
    std::cout << "joystick disconnected: " << joystickDisconnected->joystickId << std::endl;
```
