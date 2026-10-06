# 以撒路书

从第一局到白金神的中文《以撒的结合》学习路线，对齐忏悔 / 忏悔+ 版本。非官方粉丝站。

## 本地开发

```bash
npm install
npm run dev      # 本地预览 http://localhost:5173
npm run build    # 生成静态站点到 docs/.vitepress/dist
```

## 目录

| 路径 | 内容 |
| --- | --- |
| `docs/guide/` | 新手路线，五层，每层一个目录 |
| `docs/strategy/` | 攻略库与旧入口兼容页面 |
| `docs/characters/`、`docs/rooms/`、`docs/floors/`、`docs/items/` | 四类图鉴总览及独立详情页 |
| `docs/topics/` | 专题：联机、主机、配置与模组 |
| `docs/tools/tracker.md` | 解锁清单工具页 |
| `docs/.vitepress/theme/` | 主题：配色、首页、组件 |
| `docs/.vitepress/theme/data/` | 角色解锁条件、完成标记、路线阶段、攻略栏目数据 |

## 视觉风格

- 浅色 = 地下室：土褐色地面、深棕石墙、黑色粗描边、硬投影
- 深色 = 妈腿层（深处）：冷灰石板地面、近黑石墙、血红强调
- 标题和数字用站酷快乐体（OFL 授权，`@fontsource/zcool-kuaile` 自托管，按字符分片加载）
- 卡片、纸张的边缘用 `.sketch` 类 + `#ib-rough` SVG 滤镜画成手绘抖动线
- 首页首屏按原版画面布局：左上状态栏、右上小地图、右下口袋卡牌，四扇门对应四个区域
- 图标全部手写 SVG（`GameIcon.vue`），不使用游戏原图素材

## 写文章用的组件

- `<VersionBadge checked="2026-10" draft />`：文章顶部的适用版本、校对日期、草稿标记
- `<FloorTrack :current="1" compact />`：五层路线进度，标出当前在第几层
- `<StreakTitle title="标题" sub="小字" />`：仿游戏拾取道具时的黑色笔刷横幅
- `<GameIcon name="heart" />`：游戏风图标（heart、coin、bomb、key、skull、chest 等）
- `<KeyCap>E</KeyCap>`：按键样式

## 投稿

发现错误或想写攻略，直接提交 Pull Request。请用自己的文字和截图，不要搬运 wiki 或其他攻略站原文。

## 图鉴数据更新

人物、房间、楼层的编辑源稿在 `data/entry-guides/`；道具事实快照在 `data/item-source.json`，来源与版本见 `data/item-source.README.md`。不要只编辑生成后的详情页。

```bash
python3 scripts/generate-entry-pages.py
npm test
BASE=/Isaac-Wiki/ npm run build
python3 scripts/check-built-links.py
```

源数据更新时可运行 `python3 scripts/import-item-source.py <EID checkout> <IsaacDocs checkout>`，审阅差异后再生成。导入器只解析声明，不执行上游 Lua。旧页面与锚点保留兼容入口。
