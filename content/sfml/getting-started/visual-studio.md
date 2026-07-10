+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = 'SFML 与 Visual Studio'
+++

# SFML 与 Visual Studio

## 简介

如果你正在使用带有 Visual Studio IDE 以及 Visual C++ 编译器的环境来开发 SFML，那么这篇教程应该是你的首选阅读材料。
它将向你解释如何配置你的 SFML 项目。

> [!NOTE]
> [CMake 模板](../cmake/)是开始使用 SFML 的推荐方式。

## 安装 SFML

首先，你必须从[下载页面](../../../../download/ "Go to the download page")下载 SFML SDK。

然后，你可以将 SFML 压缩包解压到你喜欢的任何位置。
不推荐将头文件和库文件直接复制到你的 Visual Studio 安装目录中。更好的做法是将各种库保存在它们各自独立的位置，特别是当你打算使用同一个库的多个版本，或者使用多个编译器时。

## 创建并配置 SFML 项目

第一件事是选择创建什么类型的项目。
推荐选择“空项目”。
对话框窗口还提供了几个其他选项来定制项目：只有当你懂得如何使用预编译头文件时，才选择“控制台应用程序”或“Windows 应用程序”。

为了本教程的演示目的，你应该创建一个 `main.cpp` 文件并将其添加到项目中，这样我们就能访问 C++ 的各项设置（否则 Visual Studio 不知道你在这个项目中打算使用哪种语言）。
稍后我们会说明在其中填写什么内容。

首先我们需要配置编译器使用 SFML 3 所要求的 C++17 语言标准。

在项目的属性中，转到“C/C++”下的“语言”选项卡，将“C++ 语言标准”下拉菜单修改为“ISO C++ 17 标准”：

![设置 C++17 语言标准的对话框截图](/images/sfml/getting-started/vc-standard.png "设置 C++17 语言标准的对话框截图")

现在我们需要告诉编译器去哪里寻找 SFML 的头文件（.hpp 文件），并告诉链接器去哪里寻找 SFML 的库文件（.lib 文件）。

在项目的属性中，添加：

*   SFML 头文件的路径（`<sfml-install-path>/include`），添加到 C/C++ > 常规 > 附加包含目录
*   SFML 库文件的路径（`<sfml-install-path>/lib`），添加到 链接器 > 常规 > 附加库目录

这些路径在 Debug 和 Release 配置下是相同的，所以你可以为你的项目全局设置它们（选择“所有配置”）。

![设置搜索路径的对话框截图](/images/sfml/getting-started/vc-paths.png "设置搜索路径的对话框截图")

下一步是将你的应用程序链接到你的代码将需要的 SFML 库文件（.lib 文件）。
SFML 由 5 个模块组成（system、window、graphics、network 和 audio），每一个模块都有对应的一个库文件。

必须在项目的属性中，通过 链接器 > 输入 > 附加依赖项 来添加库。
添加所有你需要的 SFML 库，例如 "sfml-graphics.lib"、"sfml-window.lib" 和 "sfml-system.lib"。

![设置项目库文件的对话框截图](/images/sfml/getting-started/vc-link-libs.png "设置项目库文件的对话框截图")

务必要链接到与当前配置相匹配的库："sfml-xxx-d.lib" 用于 Debug，而 "sfml-xxx.lib" 用于 Release。
错误的混用可能会导致程序崩溃。

这里展示的设置将会使你的应用程序链接到 SFML 的动态版本，也就是需要 DLL 文件的版本。
如果你想要摆脱这些 DLL 并将 SFML 直接集成到你的可执行文件中，你必须链接到静态版本。
静态的 SFML 库带有 "-s" 后缀："sfml-xxx-s-d.lib" 用于 Debug，"sfml-xxx-s.lib" 用于 Release。

在这种情况下，你还需要在项目的预处理器选项中定义 `SFML_STATIC` 宏。

![定义 SFML_STATIC 宏的对话框截图](/images/sfml/getting-started/vc-static.png "定义 SFML_STATIC 宏的对话框截图")

当进行静态链接时，你还必须将 SFML 的所有依赖项也链接到你的项目中。
这意味着如果你链接了 sfml-window-s.lib 或 sfml-window-s-d.lib，你同样必须链接 opengl32.lib、winmm.lib 以及 gdi32.lib。
这些依赖库中的某些可能已经列在了“继承的值”下，但是你自己再次添加它们也不会引发任何问题。

以下是每个模块的依赖项，如果你想要链接 SFML 的 debug 库，请按照前面所述在名称后附加 -d：

| 模块 | 依赖项 |
| --- | --- |
| `sfml-graphics-s.lib` | - sfml-window-s.lib<br>- sfml-system-s.lib<br>- opengl32.lib<br>- freetype.lib |
| `sfml-window-s.lib` | - sfml-system-s.lib<br>- opengl32.lib<br>- winmm.lib<br>- gdi32.lib |
| `sfml-audio-s.lib` | - sfml-system-s.lib<br>- flac.lib<br>- vorbisenc.lib<br>- vorbisfile.lib<br>- vorbis.lib<br>- ogg.lib |
| `sfml-network-s.lib` | - sfml-system-s.lib<br>- ws2_32.lib |
| `sfml-system-s.lib` | - winmm.lib |

你可能已经从表格中注意到，SFML 模块彼此之间也可以存在依赖关系，例如 sfml-graphics-s.lib 同时依赖于 sfml-window-s.lib 和 sfml-system-s.lib。
如果你静态链接了一个 SFML 库，请确保链接了该特定库的依赖项，以及依赖项的依赖项，以此类推。
如果依赖链中有任何缺失，你*必然*会遭遇链接器错误。

如果你感到有些困惑，不必担心，初学者被这些关于静态链接的繁杂信息淹没是极其正常的。
如果第一次尝试时遇到问题，你可以牢记上文所述的要点继续尝试。
如果你仍然无法成功实现静态链接，你可以查看 [FAQ](../../../../faq/build-use/#link-static "Go to the FAQ page") 以及[论坛](http://en.sfml-dev.org/forums/index.php?board=4.0 "Go to the general help forum")中关于静态链接的主题帖。

如果你不了解动态库（也称共享库）和静态库之间的区别，也不知道该使用哪一个，你可以在互联网上搜索更多相关信息。
网络上有很多关于它们的优秀文章、博客和讨论帖。

你的项目已经准备就绪了，现在让我们写点代码来确保它能正常工作。
将以下代码填入 `main.cpp` 文件中：

```cpp
#include <SFML/Graphics.hpp>

int main()
{
    sf::RenderWindow window(sf::VideoMode({200, 200}), "SFML works!");
    sf::CircleShape shape(100.f);
    shape.setFillColor(sf::Color::Green);

    while (window.isOpen())
    {
        while (const std::optional event = window.pollEvent())
        {
            if (event->is<sf::Event::Closed>())
                window.close();
        }

        window.clear();
        window.draw(shape);
        window.display();
    }
}
```

如果你选择创建了一个“Windows 应用程序”项目，你的代码的入口点必须被设置为 "WinMain" 而非 "main"。
由于这是 Windows 特有的，因此你的代码将无法在 Linux 或 macOS 上编译，针对这种情况，SFML 提供了一种能够保持标准的 "main" 入口点的方法：将你的项目链接到 sfml-main 模块（Debug 下为 "sfml-main-d.lib"，Release 下为 "sfml-main.lib"），其方式就如同你链接 sfml-graphics、sfml-window 以及 sfml-system 一样。

编译它，如果你链接的是动态版本的 SFML，请别忘了将 SFML DLL 文件复制到与你编译出的可执行文件相同的目录下。
它们位于你的 SFML 安装路径的 bin/ 目录中。
运行它，如果一切正常，你应该会看到以下画面：

![Hello SFML 应用程序截图](/images/sfml/getting-started/vc-app.png "Hello SFML 应用程序截图")
