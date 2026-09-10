# Literary Visual Card Skill

把诗歌、书摘、金句、散文片段和原创短文，变成让人愿意停下来读一眼的 `4:5` 文学视觉卡。

它不只是“给文字配一张漂亮图片”。技能会先阅读完整原文，选择一段能够独立传播的摘抄，再分别提取两层意向：整篇文字决定画面的世界、情绪与矛盾，摘取的金句决定一个能钉住视线的视觉焦点。确认意向后，再进入四套稳定的视觉系统。

原句、标点和诗歌分行会被完整保留。图像与文字分离生成，最终由内置排版器确定性合成，因此换摘抄、改署名或微调文字时，不必重新生成背景。

## 四种视觉风格

| 时光蜡笔 | 电影诗影 |
| --- | --- |
| [![时光蜡笔](examples/time-crayon.jpg)](examples/time-crayon.jpg) | [![电影诗影](examples/cinematic-poetry.jpg)](examples/cinematic-poetry.jpg) |
| 成人重新学习表达时画出的笨拙儿童画，叠加真实窗光、树影和钴蓝折射。 | 真实摄影、深蓝暖金光影和胶片颗粒，克制、朦胧而成熟。 |

| 旧梦丝网 | 梵高油画 |
| --- | --- |
| [![旧梦丝网](examples/vintage-screenprint.jpg)](examples/vintage-screenprint.jpg) | [![梵高油画](examples/van-gogh-oil.jpg)](examples/van-gogh-oil.jpg) |
| 三色实体丝网印刷质感，以大面积浓色和小面积互补色制造张力。 | 富有节奏的厚涂笔触与强化的自然色彩，明亮中带着忧伤。 |

## 使用方式

把文字和可选信息交给 Codex，并调用：

```text
$literary-visual-card
```

你可以指定风格：

```text
用电影诗影制作这段文字。
```

也可以让技能直接判断：

```text
直接做，帮我选择最适合的风格。
```

默认流程很短：

1. 技能给出「摘取金句＋画面意向」，由用户一次确认。
2. 意向确认后，用户从四种风格中选择一种。
3. 技能直接生成背景、渲染文字并检查成品。

如果用户已经指定风格，就不会重复询问。用户说“直接做”“你来选”或“不用确认”时，技能会自行完成选择并继续生成。

## 内容规则

- 摘抄保持原文，不改写、不润色、不拼接不相邻句子。
- 没有标题时默认使用无标题版式，不擅自创造标题。
- 只有用户明确提供作者、书名或出处时才显示署名信息。
- 无法确认的出处直接省略，不显示占位符。
- 默认不添加 `Visual: ChatGPT`、AI 标签、水印或创作者签名。

## 实跑画廊

下面的作品来自同一套 Skill 实际生成流程，而不是单独制作的视觉概念稿。

| 《家族列车》· 旧梦丝网 | 《事情发生》· 电影诗影 |
| --- | --- |
| [![家族列车](examples/family-train-screenprint.jpg)](examples/family-train-screenprint.jpg) | [![事情发生](examples/things-happen-cinematic.jpg)](examples/things-happen-cinematic.jpg) |

| 《不懂》· 电影诗影 | 《不是少数》· 梵高油画 |
| --- | --- |
| [![不懂](examples/not-understand-cinematic.jpg)](examples/not-understand-cinematic.jpg) | [![不是少数](examples/not-minority-oil.jpg)](examples/not-minority-oil.jpg) |

## 输出规范

- 画布：`1600 × 2000 px`，竖版 `4:5`。
- 中文字体：Source Han Serif SC Regular。
- 拉丁字体：Source Serif 4 Regular。
- 文字、署名和图像背景分别保存，方便后续调整。
- 最终输出为 PNG。

## 安装

把仓库克隆到个人 Skills 目录：

```bash
git clone <repository-url> ~/.agents/skills/literary-visual-card
```

排版器使用 Python 3 和 Pillow。如果当前环境尚未安装 Pillow：

```bash
python3 -m pip install Pillow
```

重新打开 Codex 后，即可通过 `$literary-visual-card` 调用。使用其他支持 Skills 的客户端时，也可以将仓库放进该客户端约定的 Skills 目录。

## 项目结构

```text
literary-visual-card/
├── SKILL.md
├── README.md
├── agents/
├── assets/fonts/
├── examples/
├── references/
└── scripts/render_card.py
```

字体文件随各自的 SIL Open Font License 一并分发，许可证文件位于 `assets/fonts/`。

## License

技能代码与文档采用 [MIT License](LICENSE)。随仓库分发的字体文件继续遵循 `assets/fonts/` 中各自的 SIL Open Font License。
