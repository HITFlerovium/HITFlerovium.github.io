+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '用户数据流'
+++

# 用户数据流

## 简介

SFML 拥有几种资源类：图像、字体、声音等。
在大多数程序中，这些资源都将借助于它们的 `{load|open}FromFile` 函数或相应的构造函数从文件中加载。
在其他少数情况下，资源可能会被直接打包进可执行文件或一个大型数据文件中，并通过 `{load|open}FromMemory` 从内存中加载。
这些函数涵盖了**几乎**所有可能的用例——但并非全部。

有时你会想要从一些非同寻常的地方加载文件，比如一个被压缩或加密的压缩包中，再比如一个远程的网络地址。
针对这些特殊情况，SFML 提供了第三种加载选项：`loadFromStream` 或 `openFromStream`。
该函数使用一个抽象的 [`sf::InputStream`](../../../../documentation/3.1.0/classsf_1_1InputStream.html "sf::InputStream documentation") 接口来读取数据，这允许你提供一个与 SFML 兼容的自定义流类的实现。

在这篇教程中，你将学习如何编写和使用你自己的派生输入流。

## 那标准流呢？

像许多其他语言一样，C++ 已经拥有了一个用于输入数据流的类：`std::istream`。
事实上它有两个。
`std::istream` 仅仅是一个前端。
负责自定义数据的抽象接口是 `std::streambuf`。

不幸的是，这些类对用户并不十分友好，如果你想实现一些不那么简单的东西，它们会变得非常复杂。
[Boost.Iostreams](http://www.boost.org/doc/libs/1_49_0/libs/iostreams/doc/index.html "Boost.Iostreams") 库试图为标准流提供一个更简单的接口，但是 Boost 是一个庞大的依赖库，而 SFML 无法去依赖它。

这就是为什么 SFML 提供了自己的流接口，期望它能**更简单且更快速**。

## InputStream

[`sf::InputStream`](../../../../documentation/3.1.0/classsf_1_1InputStream.html "sf::InputStream documentation") 类声明了四个虚函数：

```cpp
class InputStream
{
public:
    virtual ~InputStream() = default;

    virtual std::optional<std::size_t> read(void* data, std::size_t size) = 0;

    virtual std::optional<std::size_t> seek(std::size_t position) = 0;

    virtual std::optional<std::size_t> tell() = 0;

    virtual std::optional<std::size_t> getSize() = 0;
};
```

**read** 必须从流中提取 *size* 字节的数据，并将它们复制到所提供的 *data* 地址处。
它返回读取的字节数，或者在发生错误时返回 `std::nullopt`。

**seek** 必须改变流中当前的读取位置。
它的 *position* 参数是要跳转到的绝对字节偏移量（所以它是相对于数据起始位置的，而不是相对于当前位置）。
它返回新的位置，或者在发生错误时返回 `std::nullopt`。

**tell** 必须返回流中当前的读取位置（以字节为单位），或者在发生错误时返回 `std::nullopt`。

**getSize** 必须返回流所包含的数据的总大小（以字节为单位），或者在发生错误时返回 `std::nullopt`。

为了创建你自己切实可行的流，你必须按照它们各自的要求实现这四个函数中的每一个。

## FileInputStream 与 MemoryInputStream

目前存在两个用于为内部音频管理提供数据流的类。
`sf::FileInputStream` 提供了对文件的只读数据流，而 `sf::MemoryInputStream` 则提供针对内存的只读流。
两者都派生自 `sf::InputStream`，因此能够被多态地使用。

## 使用 InputStream

使用一个自定义的流类非常直截了当：实例化它，并把它传递给你想要加载的对象的构造函数。

```cpp
sf::FileInputStream stream("image.png");
sf::Texture texture(stream);
```

## 范例

如果你需要一个能够帮助你将注意力集中于代码如何运作、而不至于迷失在实现细节中的演示，你可以去看看 `sf::FileInputStream` 或 `sf::MemoryInputStream` 的实现代码。

别忘了去查看论坛和 wiki。
很可能已经有其他用户编写了一个满足你需求的 [`sf::InputStream`](../../../../documentation/3.1.0/classsf_1_1InputStream.html "sf::InputStream documentation") 类。
并且，如果你写了一个新的类，同时觉得它可能对其他人也有用，千万不要犹豫，分享出来吧！

## 常见错误

有些资源类在调用了 `openFromStream` 之后并没有被完全加载。
相反，只要它们仍在使用中，它们就会继续从其数据源中读取数据。
[`sf::Music`](../../../../documentation/3.1.0/classsf_1_1Music.html "sf::Music documentation") 就是这种情况，它会在音频样本播放时对流进行读取；[`sf::Font`](../../../../documentation/3.1.0/classsf_1_1Font.html "sf::Font documentation") 也是如此，它会根据所显示的文本即时地加载字形（glyphs）。

因此，你用来加载音乐或字体的流实例，以及它的数据源，必须在资源使用它的这段时间内存活。
如果它在仍被使用时就被销毁了，就会导致未定义行为（可能会是崩溃、数据损坏，或者表面上看不出任何异常）。

另一个常见的错误是直接返回内部函数所返回的任何结果，但有时候它与 SFML 所期望的不匹配。
例如，在 `sf::FileInputStream` 代码中，有人可能会试图按如下方式编写 `seek` 函数：

```cpp
std::optional<std::size_t> FileInputStream::seek(std::size_t position)
{
    return std::fseek(m_file, position, SEEK_SET);
}
```

这段代码是错误的，因为 `std::fseek` 成功时返回零，而 SFML 期望返回的是新的位置。
