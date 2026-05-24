# Codex Pets

个人 Codex 宠物仓库。这里把每只宠物按可分发的包来存放，并为 README 自动生成动作预览，方便浏览、下载和标注作者。

## 宠物列表

### Diana

作者：[@flowersauce](https://github.com/flowersauce)  
目录：[pets/diana--flowersauce](pets/diana--flowersauce)

> 粉白偶像风像素宠物，灵感来自 Diana/Jiaran。非官方粉丝作品。

| idle | running-right | running-left |
| --- | --- | --- |
| ![Diana idle](assets/previews/diana--flowersauce/idle.gif) | ![Diana running right](assets/previews/diana--flowersauce/running-right.gif) | ![Diana running left](assets/previews/diana--flowersauce/running-left.gif) |

| waving | jumping | failed |
| --- | --- | --- |
| ![Diana waving](assets/previews/diana--flowersauce/waving.gif) | ![Diana jumping](assets/previews/diana--flowersauce/jumping.gif) | ![Diana failed](assets/previews/diana--flowersauce/failed.gif) |

| waiting | running | review |
| --- | --- | --- |
| ![Diana waiting](assets/previews/diana--flowersauce/waiting.gif) | ![Diana running](assets/previews/diana--flowersauce/running.gif) | ![Diana review](assets/previews/diana--flowersauce/review.gif) |

完整联系表：

![Diana contact sheet](assets/previews/diana--flowersauce/contact-sheet.png)

## 仓库结构

```text
pets/
  <pet-slug>--<author-slug>/
    pet.json
    spritesheet.webp
    submission.json
assets/
  previews/
    <pet-slug>--<author-slug>/
      idle.gif
      ...
      contact-sheet.png
scripts/
  generate-previews.py
  validate-pets.py
docs/
  zh-CN/
    STRUCTURE.md
```

`pet.json` 是 Codex 使用的最小运行时清单。`submission.json` 是这个仓库自己的展示清单，用来记录作者、标签、来源说明和资产许可证。

## 维护命令

生成或刷新所有动作预览：

```bash
python scripts/generate-previews.py
```

该脚本会为每只宠物生成九个棋盘格背景动作 GIF，并自动过滤透明占位帧。生成的 `contact-sheet.png` 不过滤占位格，用来核对原始 atlas。

检查宠物包结构：

```bash
python scripts/validate-pets.py
```

更多约定见 [docs/zh-CN/STRUCTURE.md](docs/zh-CN/STRUCTURE.md)。

## 许可证

仓库脚本和文档遵循 [MIT License](LICENSE)。宠物图像素材按各自目录里的 `submission.json` 和 [ASSET-LICENSE.md](ASSET-LICENSE.md) 标注。
