# 仓库结构约定

这个仓库按“一个目录就是一个可分发宠物包”的方式组织。

## 宠物目录命名

宠物目录使用：

```text
pets/<pet-slug>--<author-slug>/
```

例如：

```text
pets/diana--flowersauce/
```

这样做可以避免不同作者提交同名宠物时发生冲突，也能在文件路径里直接保留作者归属。

## 每个宠物包

每个宠物包至少包含：

```text
pet.json
spritesheet.webp
submission.json
```

`pet.json` 是 Codex 读取的运行时清单，保持最小化：

```json
{
  "id": "diana--flowersauce",
  "displayName": "Diana",
  "description": "Short runtime description.",
  "spritesheetPath": "spritesheet.webp"
}
```

`submission.json` 是仓库展示和分发用的清单，记录作者、标签、分类、许可证和预览目录。它不要求 Codex 读取，但能让仓库以后很容易生成索引页、画廊或发布包。

## 图集约定

`spritesheet.webp` 使用 Codex pet atlas 约定：

- 单格尺寸：`192x208`
- 列数：`8`
- 行数：`9`
- 总尺寸：`1536x1872`

行顺序：

```text
idle
running-right
running-left
waving
jumping
failed
waiting
running
review
```

## 预览资源

动作预览生成到：

```text
assets/previews/<pet-id>/
```

脚本会为每一行生成一个棋盘格背景 GIF，并额外生成 `contact-sheet.png`：

```bash
python scripts/generate-previews.py
```

新增或替换 `spritesheet.webp` 后重新运行这条命令即可刷新 README 里的预览。GIF 会跳过完全透明的占位帧，并先把半透明边缘合成到透明棋盘格背景，避免 GIF 透明色造成边缘杂色；`contact-sheet.png` 会保留原始透明图集和占位格。

## 校验

提交前运行：

```bash
python scripts/validate-pets.py
```

校验内容包括：

- `pet.json`、`spritesheet.webp`、`submission.json` 是否存在
- 宠物目录名是否和 `pet.json` 的 `id` 一致
- `spritesheetPath` 是否指向当前目录里的图集
- 图集尺寸是否符合 `1536x1872`
- `submission.json` 是否包含作者信息
