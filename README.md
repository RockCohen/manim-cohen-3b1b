<p align="center">
    <a href="https://github.com/3b1b/manim">
        <img src="https://raw.githubusercontent.com/3b1b/manim/master/logo/cropped.png">
    </a>
</p>

[![pypi version](https://img.shields.io/pypi/v/manimgl?logo=pypi)](https://pypi.org/project/manimgl/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)
[![Manim Subreddit](https://img.shields.io/reddit/subreddit-subscribers/manim.svg?color=ff4301&label=reddit&logo=reddit)](https://www.reddit.com/r/manim/)
[![Manim Discord](https://img.shields.io/discord/581738731934056449.svg?label=discord&logo=discord)](https://discord.com/invite/bYCyhM9Kz2)
[![docs](https://github.com/3b1b/manim/workflows/docs/badge.svg)](https://3b1b.github.io/manim/)

Manim 是一个用于精确编程动画的引擎，专为创建解释性数学视频而设计。

请注意，Manim 有两个版本。这个仓库最初是 [3Blue1Brown](https://www.3blue1brown.com/) 的作者的个人项目，用于制作那些视频，视频特定的代码可在[这里](https://github.com/3b1b/videos)找到。2020年，一群开发者将其分叉成现在的[社区版](https://github.com/ManimCommunity/manim/)，目标是使其更加稳定、更好地测试、更快地响应社区贡献，并且总体上更容易上手。有关更多详细信息，请参阅[此页面](https://docs.manim.community/en/stable/faq/installation.html#different-versions)。

## 安装
> [!Warning]
> **警告：** 这些说明仅适用于 ManimGL。尝试使用这些说明安装 [Manim Community/manim](https://github.com/ManimCommunity/manim) 或使用那里的说明安装此版本将导致问题。您应该首先决定要安装哪个版本，然后仅遵循所需版本的说明。

> [!Note]
> **注意**：通过 pip 直接安装 manim 时，请注意已安装包的名称。此仓库是 3b1b 的 ManimGL。包名是 `manimgl` 而不是 `manim` 或 `manimlib`。请使用 `pip install manimgl` 安装此仓库中的版本。

Manim 运行在 Python 3.7 或更高版本上。

系统要求是 [FFmpeg](https://ffmpeg.org/)、[OpenGL](https://www.opengl.org/) 和 [LaTeX](https://www.latex-project.org)（可选，如果您想使用 LaTeX）。
对于 Linux，需要 [Pango](https://pango.gnome.org) 及其开发头文件。请参阅[此处](https://github.com/ManimCommunity/ManimPango#building)的说明。

### 直接安装

\`\`\`sh
# 安装 manimgl
pip install manimgl

# 试一试
manimgl
\`\`\`

有关更多选项，请查看下面的[使用 manim](#使用-manim) 部分。

如果您想修改 manimlib 本身，请克隆此仓库并在该目录中执行：

\`\`\`sh
# 安装 manimgl
pip install -e .

# 试一试
manimgl example_scenes.py OpeningManimExample
# 或
manim-render example_scenes.py OpeningManimExample
\`\`\`

### 直接安装（Windows）

1. [安装 FFmpeg](https://www.wikihow.com/Install-FFmpeg-on-Windows)。
2. 安装 LaTeX 发行版。推荐 [MiKTeX](https://miktex.org/download)。
3. 安装剩余的 Python 包。
    \`\`\`sh
    git clone https://github.com/3b1b/manim.git
    cd manim
    pip install -e .
    manimgl example_scenes.py OpeningManimExample
    \`\`\`

### Mac OSX

1. 使用 homebrew 在终端中安装 FFmpeg 和 LaTeX。
    \`\`\`sh
    brew install ffmpeg mactex
    \`\`\`
   
2. 使用这些命令安装最新版本的 manim。
    \`\`\`sh
    git clone https://github.com/3b1b/manim.git
    cd manim
    pip install -e .
    manimgl example_scenes.py OpeningManimExample
    \`\`\`

## Anaconda 安装

1. 如上所述安装 LaTeX。
2. 使用 `conda create -n manim python=3.8` 创建一个 conda 环境。
3. 使用 `conda activate manim` 激活环境。
4. 使用 `pip install -e .` 安装 manimgl。

## 使用 manim
尝试运行以下命令：
\`\`\`sh
manimgl example_scenes.py OpeningManimExample
\`\`\`
这应该会弹出一个窗口播放一个简单的场景。

查看[示例场景](https://3b1b.github.io/manim/getting_started/example_scenes.html)以了解库的语法、动画类型和对象类型的示例。在 [3b1b/videos](https://github.com/3b1b/videos) 仓库中，您可以看到所有 3blue1brown 视频的代码，尽管旧视频的代码可能与最新版本的 manim 不兼容。该仓库的 readme 还概述了如何设置更具交互性的工作流程的一些细节，例如在[这个 manim 演示视频](https://www.youtube.com/watch?v=rbu7Zu5X1zI)中所示。

在 CLI 中运行时，一些有用的标志包括：
* `-w` 将场景写入文件
* `-o` 将场景写入文件并打开结果
* `-s` 跳到结尾并仅显示最终帧。
    * `-so` 将最终帧保存为图像并显示
* `-n <number>` 跳到场景的第 `n` 个动画。
* `-f` 使播放窗口全屏

查看 custom_config.yml 以获取更多配置。要添加您的自定义设置，您可以编辑此文件，或者将另一个同名文件 "custom_config.yml" 添加到您运行 manim 的任何目录中。例如，[这是](https://github.com/3b1b/videos/blob/master/custom_config.yml) 3blue1brown 视频的配置文件。在那里，您可以指定视频应该输出到哪里，manim 应该在哪里查找您想要读入的图像文件和声音，以及关于样式和视频质量的其他默认设置。

### 文档
文档正在 [3b1b.github.io/manim](https://3b1b.github.io/manim/) 上进行中。还有一个由 [**@manim-kindergarten**](https://manim.org.cn) 维护的中文版本：[docs.manim.org.cn](https://docs.manim.org.cn/)（中文）。

[manim-kindergarten](https://github.com/manim-kindergarten/) 在 [manim_sandbox 仓库](https://github.com/manim-kindergarten/manim_sandbox) 中编写和收集了一些有用的额外类和视频代码。

## 贡献
始终欢迎贡献。如上所述，[社区版](https://github.com/ManimCommunity/manim) 拥有最活跃的贡献生态系统，包括测试和持续集成，但这里也欢迎拉取请求。请解释给定更改的动机及其效果示例。

## 许可证
该项目采用 MIT 许可证。