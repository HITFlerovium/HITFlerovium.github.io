+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '绘制 2D 图形'
+++

# 绘制 2D 图形

## 简介

正如你在前面的教程中所学到的，SFML 的 window 模块提供了一种打开 OpenGL 窗口并处理其事件的简便方法，但在涉及到绘制东西时，它就爱莫能助了。
留给你的唯一选择就是使用强大，但却复杂且底层的 OpenGL API。

幸运的是，SFML 提供了一个 graphics 图形模块，它将帮助你以比 OpenGL 简单得多的方式绘制 2D 实体。

## 绘图窗口

要绘制 graphics 模块提供的实体，你必须使用一个专门的窗口类：[`sf::RenderWindow`](../../../../documentation/3.1.0/classsf_1_1RenderWindow.html "sf::RenderWindow documentation")。
这个类派生自 [`sf::Window`](../../../../documentation/3.1.0/classsf_1_1Window.html "sf::Window documentation")，并继承了它的所有功能。
你所学到的关于 [`sf::Window`](../../../../documentation/3.1.0/classsf_1_1Window.html "sf::Window documentation") 的所有知识（创建、事件处理、控制帧率、与 OpenGL 混合等）同样适用于 [`sf::RenderWindow`](../../../../documentation/3.1.0/classsf_1_1RenderWindow.html "sf::RenderWindow documentation")。

除此之外，[`sf::RenderWindow`](../../../../documentation/3.1.0/classsf_1_1RenderWindow.html "sf::RenderWindow documentation") 还添加了高级函数来帮助你轻松地绘制物体。
在本教程中，我们将重点关注其中的两个函数：`clear` 和 `draw`。
正如它们的名字所暗示的那样简单：`clear` 使用你选择的颜色清除整个窗口，而 `draw` 绘制你传递给它的任何对象。

下面是使用渲染窗口时，典型的游戏主循环的样子：

```cpp
#include <SFML/Graphics.hpp>

int main()
{
    // 创建窗口
    sf::RenderWindow window(sf::VideoMode({800, 600}), "My window");

    // 只要窗口开着，就一直运行程序
    while (window.isOpen())
    {
        // 检查自上一次循环迭代以来触发的所有窗口事件
        while (const std::optional event = window.pollEvent())
        {
            // “关闭请求”事件：我们关闭窗口
            if (event->is<sf::Event::Closed>())
                window.close();
        }

        // 用黑色清除窗口
        window.clear(sf::Color::Black);

        // 在这里绘制所有的东西...
        // window.draw(...);

        // 结束当前帧
        window.display();
    }
}
```

在绘制任何东西之前调用 `clear` 是强制性的，否则前几帧的残影将会出现在你绘制的任何东西的后面。
唯一的例外是，当你绘制的东西覆盖了整个窗口，使得每一个像素都被重新绘制时。
在这种情况下，你可以不调用 `clear`（尽管调用它也不会对性能产生明显的负面影响）。

调用 `display` 也是强制性的，它接收自上次调用 `display` 以来绘制的内容，并将它们显示在窗口上。
事实上，所有的东西并不是直接绘制到窗口上的，而是绘制到一个隐藏的缓冲区中。
当你调用 `display` 时，这个缓冲区才会被复制到窗口上——这被称为双缓冲技术。

这种 clear/draw/display 的循环是绘制事物的唯一好方法。
请不要尝试其他策略，例如保留上一帧的像素、“擦除”像素，或是绘制一次后多次调用 display。
由于双缓冲技术的存在，你会得到奇怪的绘制结果。

现代图形硬件和 API 实际上就是为了这种重复的 clear/draw/display 循环而设计的，在主循环的每一次迭代中，所有的东西都会被彻底刷新。
不要害怕每秒 60 次绘制 1000 个精灵。
你离电脑能够处理的数百万个三角形的极限还差得很远呢。

## 我现在能画什么了？

既然你现在已经拥有了一个随时可以用来绘制图形的主循环，那么让我们来看看你到底能在那里画些什么，以及如何去画。

SFML 提供了四种可绘制的实体：其中三种是可以直接使用的（精灵、文本和形状），最后一种是帮助你创建自定义可绘制实体的基石（顶点数组）。

尽管它们拥有一些共同的属性，但这些实体中的每一种都有其自身的细微差别，因此它们将在各自专门的教程中进行讲解：

*   [精灵教程](../sprite/ "Learn how to create and draw sprites")
*   [文本教程](../text/ "Learn how to create and draw text")
*   [形状教程](../shape/ "Learn how to create and draw shapes")
*   [顶点数组教程](../vertex-array/ "Learn how to create and draw vertex arrays")

## 离屏绘制

SFML 还提供了一种将内容绘制到纹理（Texture）上，而不是直接绘制到窗口上的方法。
要做到这一点，请使用 [`sf::RenderTexture`](../../../../documentation/3.1.0/classsf_1_1RenderTexture.html "sf::RenderTexture documentation") 而不是 [`sf::RenderWindow`](../../../../documentation/3.1.0/classsf_1_1RenderWindow.html "sf::RenderWindow documentation")。
它拥有相同的绘图函数，它们都继承自共同的基类：[`sf::RenderTarget`](../../../../documentation/3.1.0/classsf_1_1RenderTarget.html "sf::RenderTarget documentation")。

```cpp
// 创建一个 500x500 的渲染纹理
sf::RenderTexture renderTexture({500, 500});

// 绘图使用相同的函数
renderTexture.clear();
renderTexture.draw(sprite); // 或者任何其他可绘制的对象
renderTexture.display();

// 获取目标纹理（即刚刚绘制了东西的那个纹理）
const sf::Texture& texture = renderTexture.getTexture();

// 将其绘制到窗口上
sf::Sprite sprite(texture);
window.draw(sprite);
```

`getTexture` 函数返回一个只读的纹理，这意味着你只能使用它，而不能修改它。
如果在使用它之前你需要对其进行修改，你可以将其复制到你自己的 [`sf::Texture`](../../../../documentation/3.1.0/classsf_1_1Texture.html "sf::Texture documentation") 实例中，然后对后者进行修改。

[`sf::RenderTexture`](../../../../documentation/3.1.0/classsf_1_1RenderTexture.html "sf::RenderTexture documentation") 还拥有与 [`sf::RenderWindow`](../../../../documentation/3.1.0/classsf_1_1RenderWindow.html "sf::RenderWindow documentation") 相同的处理视图（View）和 OpenGL 的函数（有关详细信息，请参阅相应的教程）。

## 在多线程中绘图

SFML 支持多线程绘图，你甚至不需要做任何额外的工作就能让它跑起来。
唯一需要记住的是，在另一个线程中使用某个窗口之前，必须先将该窗口设置为非活跃状态。
这是因为一个窗口（更准确地说，是它的 OpenGL 上下文）不能同时在多个线程中处于活跃状态。

```cpp
void renderingThread(sf::RenderWindow* window)
{
    // 激活窗口的上下文
    window->setActive(true);

    // 渲染循环
    while (window->isOpen())
    {
        // 绘制...

        // 结束当前帧
        window->display();
    }
}

int main()
{
    // 创建窗口（请记住：由于操作系统的限制，在主线程中创建它更安全）
    sf::RenderWindow window(sf::VideoMode({800, 600}), "OpenGL");

    // 停用其 OpenGL 上下文
    window.setActive(false);

    // 启动渲染线程
    std::thread thread(&renderingThread, &window);

    // 事件/逻辑/其他各种东西的循环
    while (window.isOpen())
    {
        ...
    }

    thread.join();
}
```

如你所见，你甚至不需要在渲染线程中费心去激活窗口，SFML 会在需要的时候自动为你完成这一操作。

请记住，始终在主线程中创建窗口并处理它的事件以获得最大的可移植性。
这一点在[窗口教程](../../window/window/ "Window tutorial")中已经解释过了。
