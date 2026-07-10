+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '打开并管理 SFML 窗口'
+++

# 打开并管理 SFML 窗口

## 简介

本教程仅解释如何打开和管理一个窗口。
绘制内容超出了 sfml-window 模块的范畴：它是由 sfml-graphics 模块来处理的。
然而，窗口管理的机制是完全一样的，因此在任何情况下阅读本教程都是很重要的。

## 打开窗口

在 SFML 中，窗口由 [`sf::Window`](../../../../documentation/3.1.0/classsf_1_1Window.html "sf::Window documentation") 类定义。
一个窗口可以在构造时被直接创建和打开：

```cpp
#include <SFML/Window.hpp>

int main()
{
    sf::Window window(sf::VideoMode({800, 600}), "My window");
    ...
}
```

第一个参数——**视频模式**（video mode），定义了窗口的大小（即内部大小，不包括标题栏和边框）。
在这里，我们创建了一个大小为 800x600 像素的窗口。
[`sf::VideoMode`](../../../../documentation/3.1.0/classsf_1_1VideoMode.html "sf::VideoMode documentation") 类提供了一些非常实用的静态函数，用于获取桌面分辨率或是全屏模式下所有受支持的有效视频模式列表。
千万不要犹豫去查阅一下它的文档。

第二个参数就是窗口的标题。

这个构造函数接受第三个可选参数：样式（style），它允许你选择你想要的装饰和功能。
你可以使用以下样式的任意组合：

| 样式 | 描述 |
| --- | --- |
| `sf::Style::None` | 没有任何装饰（例如对于启动画面非常有用）<br>此样式不能与其他样式组合使用 |
| `sf::Style::Titlebar` | 窗口拥有一个标题栏 |
| `sf::Style::Resize` | 窗口可以调整大小并拥有一个最大化按钮 |
| `sf::Style::Close` | 窗口拥有一个关闭按钮 |
| `sf::Style::Default` | 默认样式，它是 `Titlebar | Resize | Close` 的组合简写 |

第四个参数定义了窗口的状态，让你可以在悬浮窗口或全屏窗口之间做出选择。

| 状态 | 描述 |
| --- | --- |
| `sf::State::Windowed` | 悬浮窗口 |
| `sf::State::Fullscreen` | 全屏窗口 |

还有第五个可选参数，它定义了 OpenGL 的特定选项，这在[专属的 OpenGL 教程](../opengl/ "OpenGL tutorial")中会有详细解释。

如果你想在 [`sf::Window`](../../../../documentation/3.1.0/classsf_1_1Window.html "sf::Window documentation") 实例构造**之后**再去创建窗口，或者想用不同的视频模式或标题重新创建它，你可以改用 `create` 函数。
它接受与构造函数完全相同的参数。

```cpp
#include <SFML/Window.hpp>

int main()
{
    sf::Window window;
    window.create(sf::VideoMode({800, 600}), "My window");

    ...
}
```

## 让窗口“活”起来

如果你尝试执行上面的代码（将 "..." 留空），你几乎什么也看不到。
首先，因为程序会立刻结束。
其次，因为没有事件处理——所以即使你在这段代码中添加了一个死循环，你看到的也将是一个“死”的窗口，无法被移动、调整大小或是关闭。

让我们添加一些代码，让这个程序变得稍微有趣一点：

```cpp
#include <SFML/Window.hpp>

int main()
{
    sf::Window window(sf::VideoMode({800, 600}), "My window");

    // 只要窗口开着，就运行程序
    while (window.isOpen())
    {
        // 检查自上次循环迭代以来所有被触发的窗口事件
        while (const std::optional event = window.pollEvent())
        {
            // “请求关闭”事件：我们关闭窗口
            if (event->is<sf::Event::Closed>())
                window.close();
        }
    }
}
```

上面的代码将打开一个窗口，并在用户关闭它时终止。
让我们详细看看它是如何运作的。

首先，我们添加了一个循环来确保应用程序能够持续刷新/更新，直到窗口被关闭。
绝大多数（如果不是全部的话）SFML 程序都会有这种类型的循环，它有时被称为**主循环**（main loop）或**游戏循环**（game loop）。

然后，我们在游戏循环里要做的第一件事就是检查是否发生了任何事件。
注意我们使用了一个 `while` 循环，这样如果挂起了多个事件，所有的待处理事件都将被一一处理。
如果有挂起的事件，`pollEvent` 函数将返回一个事件；如果没有，则返回 `std::nullopt`。

每当我们获取到一个事件，我们就必须检查它的类型（窗口关闭？按键按下？鼠标移动？手柄连接？...），如果我们对该类型事件感兴趣，就做出相应的反应。
在这里，我们只关心 `sf::Event::Closed` 事件，它会在用户想要关闭窗口时触发。
此时此刻，窗口其实仍处于打开状态，我们必须通过调用 `close` 函数来显式地关闭它。
这就允许你在窗口被关闭之前做点事情，比如保存应用程序的当前状态，或者显示一条消息。

人们经常犯的一个错误就是忘记编写事件循环，仅仅是因为他们暂时还不关心事件处理（他们通常直接使用实时输入代替）。
如果没有事件循环，窗口将会变得无法响应。
必须指出事件循环有两个作用：除了将事件提供给用户之外，它也给了窗口处理其内部事件的机会，这是必需的，以便窗口能够对移动或调整大小等用户操作做出反应。

在窗口被关闭之后，主循环退出，程序随之终止。

说到这里，你可能已经注意到了我们还没讨论如何向窗口**绘制东西**。
正如引言中所述，这不是 sfml-window 模块的职责，如果你想绘制精灵（sprites）、文本或各种形状，你将不得不跳转到 sfml-graphics 模块的教程。

为了绘制内容，你也可以直接使用 OpenGL 并完全无视 sfml-graphics 模块。
[`sf::Window`](../../../../documentation/3.1.0/classsf_1_1Window.html "sf::Window documentation") 内部创建了一个 OpenGL 绘图上下文，并且随时准备好接受你的 OpenGL 调用。
你可以在[相关的教程](../opengl/ "OpenGL tutorial")中了解更多详情。

不要指望在这个窗口中看到什么有趣的东西：你可能会看到一种纯色（黑色或白色），或是上一个使用过 OpenGL 的应用程序遗留的内容，抑或是……其他莫名其妙的东西。

## 操作窗口

当然，SFML 允许你对窗口进行一些操作。
诸如更改大小、位置、标题或图标等基本窗口操作都是受支持的，但与专门的 GUI 库（如 Qt、wxWidgets）不同，SFML 并不提供高级功能。
SFML 窗口仅仅旨在为 OpenGL 或 SFML 的绘制提供一个运行环境。

```cpp
// 更改窗口的位置（相对于桌面）
window.setPosition({10, 50});

// 更改窗口的大小
window.setSize({640, 480});

// 更改窗口的标题
window.setTitle("SFML window");

// 获取窗口的大小
sf::Vector2u size = window.getSize();
auto [width, height] = size;

// 检查窗口是否拥有焦点
bool focus = window.hasFocus();

...
```

你可以查阅 API 文档以获取 [`sf::Window`](../../../../documentation/3.1.0/classsf_1_1Window.html "sf::Window documentation") 的完整函数列表。

如果你真的需要为你的窗口添加一些高级功能，你可以使用其他的库来创建一个窗口（甚至是一个完整的 GUI），然后将 SFML 嵌入到其中。
要做到这一点，你可以使用 [`sf::Window`](../../../../documentation/3.1.0/classsf_1_1Window.html "sf::Window documentation") 的另一个构造函数（或 `create` 函数），它接收一个现有窗口的、特定于操作系统的句柄。
在这种情况下，SFML 将会在给定的窗口内部创建一个绘图上下文并捕获其所有的事件，而且绝不会干扰到父窗口的管理。

```cpp
sf::WindowHandle handle = /* 针对你正在做的事情和你所使用的库而定 */;
sf::Window window(handle);
```

如果你只想要一种额外的、非常特定于平台的功能，你也可以反其道而行之：创建一个 SFML 窗口并获取其底层操作系统的原生句柄，以此来实现 SFML 本身不支持的事务。

```cpp
sf::Window window(sf::VideoMode({800, 600}), "SFML window");
sf::WindowHandle handle = window.getNativeHandle();

// 你现在可以在特定于操作系统的函数中使用这个句柄了
```

将 SFML 与其他库集成需要做一些工作，这里不再赘述，但你可以参考相关的专门教程、示例或是论坛上的帖子。

## 控制帧率

有时候，当你的应用程序运行得非常快时，你可能会注意到一些画面瑕疵，比如画面撕裂（tearing）。
原因在于你的应用程序的刷新率与显示器的垂直刷新频率没有同步，从而导致前一帧的底部与下一帧的顶部混杂在了一起。
解决这个问题的方法是开启**垂直同步**（vertical synchronization）。
它由显卡自动处理，并且可以通过 `setVerticalSyncEnabled` 函数轻松开启或关闭：

```cpp
window.setVerticalSyncEnabled(true); // 在创建窗口后调用一次
```

在这次调用之后，你的应用程序将以与显示器刷新率相同的频率运行。

有时 `setVerticalSyncEnabled` 可能不起作用：这很有可能是因为在你的显卡驱动设置中，垂直同步被强制关闭了。
你应该将其改为“由应用程序控制”。

在其他情况下，你可能希望你的应用程序以给定的帧率运行，而不是受制于显示器的频率。
这可以通过调用 `setFramerateLimit` 来实现：

```cpp
window.setFramerateLimit(60); // 在创建窗口后调用一次
```

与 `setVerticalSyncEnabled` 不同，这个功能是由 SFML 自身实现的，它组合使用了 [`sf::Clock`](../../../../documentation/3.1.0/classsf_1_1Clock.html "sf::Clock documentation") 和 `sf::sleep`。
一个重要的后果是它并非 100% 绝对可靠，尤其是在高帧率下：`sf::sleep` 的精度取决于底层的操作系统和硬件，误差可能高达 10 甚至 15 毫秒。
千万不要依赖这个功能来实现精确的时序控制。

绝对不要同时使用 `setVerticalSyncEnabled` 和 `setFramerateLimit`！
它们会产生极其糟糕的相互作用并让情况变得更糟。

## 关于窗口你必须知道的事

这里有一份简要的清单，列出了你能用以及不能用 SFML 窗口做什么。

### 你可以创建多个窗口

SFML 允许你创建多个窗口，并且可以在主线程中统一处理它们，或者在各自独立的线程中单独处理每一个窗口（但是……请看下文）。
在这种情况下，别忘了为每个窗口都配备一个事件循环。

### 尚未对多显示器提供良好支持

SFML 目前并没有显式地管理多台显示器。
因此，你无法选择窗口将出现在哪台显示器上，并且你无法创建超过一个的全屏窗口。
这应该会在未来的版本中得到改善。

### 事件必须在窗口所在的线程中进行轮询

这是大多数操作系统的一个重要限制：事件循环（更准确地说，是 `pollEvent` 或 `waitEvent` 函数）必须在创建窗口的那个相同线程中被调用。
这意味着如果你想要创建一个专门用于事件处理的线程，你就必须确保窗口也是在这个线程中创建的。
如果你真的想在线程间分割事务，更方便的做法是将事件处理保留在主线程中，而把其余的工作（渲染、物理运算、逻辑等）移动到一个独立的线程里。
这样的架构同样也兼容下面所描述的另一个限制。

### 在 macOS 上，窗口和事件必须在主线程中管理

没错，这是真的；如果你尝试在除了主线程之外的其他线程里去创建窗口或处理事件，macOS 是绝对不会答应的。

### 在 Windows 上，大于桌面的窗口将无法正常表现

出于某些原因，Windows 并不喜欢比桌面尺寸还要大的窗口。
这同样包括使用 `VideoMode::getDesktopMode()` 创建的窗口：在加上了窗口装饰（边框和标题栏）之后，你最终得到的一个窗口会比桌面的尺寸略微大那么一点点。
