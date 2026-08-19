# DSH Spotify Theme

A Spotify-inspired restyle for the [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) web client — near-black surfaces, layered gray cards, white/gray text and the signature Spotify green (`#1ed760` / `#1db954`) accent. Ships as a single drop-in CSS override plus two tiny optional patches.

> 中文用户请看文末「快速安装」。

## Preview

| Dark | Light |
| --- | --- |
| ![dark](./screenshots/dark.png) | ![light](./screenshots/light.png) |

| Hero + watermark | Collapsed rail |
| --- | --- |
| ![hero](./screenshots/hero.png) | ![collapsed](./screenshots/collapsed.png) |

## Features

**[English](#features-en) · [中文](#features-zh)**

### Features (EN)

**Theming**
- Dark + light palettes sharing one structure (Spotify green accents in both)
- Full `--dsw-*` design-token override, so the palette flows through every component

**Sidebar**
- Floating rounded-rectangle panel with matching margins when collapsed
- Green "New Session" pill, green section headers with dots, green folder icons
- Active session highlighted in bold green
- "Now playing"-style breathing green dot on running sessions
- Redesigned session-stats card with a cache-hit progress bar

**Main area**
- Task title promoted to a real headline; workspace breadcrumb demoted
- Green diffuse focus halo on the composer
- User bubbles tinted green to separate them from assistant content
- Large italic "Harness" watermark behind the conversation
- Fade + rise transition on every session switch / new session

**Polish & accessibility**
- Smooth hover/focus transitions, `:focus-visible` green outline
- Respects `prefers-reduced-motion`

---

### 功能特性（中文）

**主题**
- 深色 + 浅色双配色共享同一结构（均以 Spotify 绿为点缀）
- 完整覆写 `--dsw-*` 设计令牌，配色自动贯穿所有组件

**侧边栏**
- 折叠时浮起的圆角面板，四周留白对称
- 绿色"新建会话"胶囊按钮、带圆点的绿色分区标题、绿色文件夹图标
- 当前会话以加粗绿色高亮
- 运行中的会话显示"正在播放"风格的呼吸绿色圆点
- 重新设计的会话统计卡，带缓存命中率进度条

**主区域**
- 任务标题提升为真正的标题样式，工作区面包屑降级
- 输入框获得焦点时呈现绿色弥散光晕
- 用户气泡以绿色色调区分于助手内容
- 对话区域后方大面积斜体"Harness"水印
- 每次切换会话 / 新建会话时淡入上浮过渡动画

**细节与无障碍**
- 平滑的 hover/focus 过渡动画，`:focus-visible` 绿色描边
- 遵循 `prefers-reduced-motion` 偏好设置

## Install

### 1. Copy the stylesheet

Find your installed dsh frontend dist. For an `npx` install it lives under
`~/.npm/_npx/*/node_modules/@deepseek-ai/dsh-web-frontend/dist/`.

```bash
DIST="$(ls -d ~/.npm/_npx/*/node_modules/@deepseek-ai/dsh-web-frontend/dist | head -1)"
cp spotify-theme.css "$DIST/assets/spotify-theme.css"
```

### 2. Link it

Append one `<link>` to `"$DIST/index.html"`, **after** the existing stylesheets:

```html
<link rel="stylesheet" crossorigin href="/assets/spotify-theme.css">
```

### 3. Restart / refresh

Refresh `http://127.0.0.1:3080/`. To revert, remove the `<link>` (or the file).

## Optional patches

Two optional patches enable the wider collapsed rail and the stats-card
progress bar (both require editing the bundled client JS). Run from this repo:

```bash
python3 patches/patch_rail_width.py
python3 patches/patch_stats_card.py
```

Each accepts an optional path to your `@deepseek-ai` directory:

```bash
python3 patches/patch_rail_width.py ~/.npm/_npx/<hash>/node_modules/@deepseek-ai
```

> These patches are written against **dsh `0.1.0-rc.7`**. The CSS relies on a
> few hashed CSS-module class names from that build; the `--dsw-*` token
> overrides are version-stable, but the component-level rules may need
> retargeting on future releases.

## Compatibility

- Tested with DeepSeek Harness **`0.1.0-rc.7`**
- No secrets, paths, or personal data are included — this repo is CSS + two
  small patch scripts only.

## License

Your own theme work is yours to license. The patches target DeepSeek Harness,
which is MIT-licensed; this repo is provided as-is without warranty.

---

## 快速安装（中文）

1. 把 `spotify-theme.css` 复制到 dsh 前端目录：
   ```bash
   DIST="$(ls -d ~/.npm/_npx/*/node_modules/@deepseek-ai/dsh-web-frontend/dist | head -1)"
   cp spotify-theme.css "$DIST/assets/spotify-theme.css"
   ```
2. 在 `"$DIST/index.html"` 里，于现有样式表之后加一行：
   ```html
   <link rel="stylesheet" crossorigin href="/assets/spotify-theme.css">
   ```
3. 刷新页面即可；删除该 `<link>` 即恢复原样。

可选补丁（加宽折叠栏 + 统计卡进度条）：
```bash
python3 patches/patch_rail_width.py
python3 patches/patch_stats_card.py
```
