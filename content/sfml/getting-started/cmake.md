+++
date = '2026-07-10T10:00:00+08:00'
draft = false
title = '使用 CMake 项目模板的 SFML'
+++

# 使用 CMake 项目模板的 SFML

## 简介

本教程适用于任何操作系统、任何 IDE 以及任何编译器。
它将向你解释如何构建一个能够与 SFML 的任意发布版本、分支或 Git 提交配合使用的项目。
这种方法的独特性在于，它消除了发生链接器错误的可能性，并使未来升级 SFML 版本变得尽可能简单。
它甚至包含了一个 CI 流水线，能够自动验证你的项目是否能继续在 Windows、Linux 和 macOS 上成功编译。

## 创建你自己的 GitHub 项目

[https://github.com/SFML/cmake-sfml-project](https://github.com/SFML/cmake-sfml-project "CMake SFML Project Template Repository")

上述 GitHub 仓库就是 GitHub 所称的[仓库模板](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template "GitHub documentation about repository templates")。
查阅 GitHub 关于仓库模板的官方文档，了解如何利用此模板创建你自己的 GitHub 项目。
这一步骤可确保你的代码安全地存放在远程位置，从而避免意外丢失。

## 自定义 CMake 项目与可执行文件的名称

开箱即用时，本项目为项目名称和可执行文件名称使用了占位符。
这些名称可以是你想要的任何名字，并且它们不必保持一致。
项目名称定义在 `CMakeLists.txt` 文件顶部的 `project()` 调用中。

可执行文件的名称则定义在 `add_executable()` 调用中。
请务必替换掉所有旧可执行文件名称的实例。
在可执行文件被创建之后，该名称还会被多次使用。

## 添加你自己的源文件

项目初始时唯一的 C++ 源文件是 `src/main.cpp`。
你可以根据自己项目的需要，重命名、移除或添加新的源文件。
只需确保所有的 `.cpp` 文件都被包含在 `add_executable` 调用中，以此来避免链接器错误。

## 依赖要求

由于此模板通过源码来构建 SFML，因此 Linux 用户需要首先安装必需的系统包。
在 Ubuntu 或其他基于 Debian 的操作系统上，可以通过以下命令完成安装。
对于像 Fedora 这样非 Debian 系的 Linux 发行版，也会需要执行类似的流程。

```text
sudo apt update
sudo apt install \
    libxrandr-dev \
    libxcursor-dev \
    libxi-dev \
    libudev-dev \
    libfreetype-dev \
    libflac-dev \
    libvorbis-dev \
    libgl1-mesa-dev \
    libegl1-mesa-dev \
    libfreetype-dev
```

这个 CMake 模板要求必须安装 CMake。
你系统自带的包管理器是获取 CMake 的最佳途径。
它也会与 Visual Studio 一同安装。
如果由于某些原因前述选项无法运作，你可以访问 [https://cmake.org/download/](https://cmake.org/download/ "CMake download") 为你的操作系统安装 CMake。

[Git](https://git-scm.com/ "Git SCM") 也是必需的，因为 CMake 需要使用 Git 来克隆 SFML 仓库。
如果你克隆了你自己的 GitHub 项目，那么你一定已经安装了 Git。
如果没有 Git，CMake 将会以一种让人摸不着头脑的方式构建失败。

## 配置并构建你的项目

现在你已经对构建脚本完成了所有想要的修改，我们准备好进行构建了！
CMake 无疑是最受欢迎的 C++ 构建系统，因此你可能使用的任何 IDE 都会对 CMake 项目提供支持。
下方提供了一些链接，指向几种不同主流 IDE 设置 CMake 项目的官方文档。

*   [VS Code](https://code.visualstudio.com/docs/cpp/cmake-linux "VS Code CMake project documentation")
*   [Visual Studio](https://docs.microsoft.com/en-us/cpp/build/cmake-projects-in-visual-studio?view=msvc-170 "Visual Studio CMake project documentation")
*   [CLion](https://www.jetbrains.com/clion/features/cmake-support.html "CLion CMake project documentation")
*   [Qt Creator](https://doc.qt.io/qtcreator/creator-project-cmake.html "Qt Creator CMake project documentation")

如果你更倾向于通过命令行而不是通过 IDE 来构建此项目，那也非常容易。
你可以使用这两条 shell 命令来对项目进行 Release 构建。

```text
cmake -B build
cmake --build build
```
