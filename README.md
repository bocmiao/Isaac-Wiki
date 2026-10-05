# 以撒路书

从第一局到白金神的中文《以撒的结合》学习路线，对齐 Repentance+ 版本。非官方粉丝站。

## 本地开发

```bash
npm install
npm run dev      # 本地预览 http://localhost:5173
npm run build    # 生成静态站点到 docs/.vitepress/dist
```

## 目录

| 路径 | 内容 |
| --- | --- |
| `docs/guide/` | 学习路线，五层，每层一个目录 |
| `docs/topics/` | 专题：联机、主机、配置与模组 |
| `docs/tools/tracker.md` | 解锁清单工具页 |
| `docs/.vitepress/theme/` | 主题：配色、首页、组件 |
| `docs/.vitepress/theme/data/` | 角色解锁条件、完成标记、路线阶段数据 |

## 写文章用的组件

- `<VersionBadge checked="2026-10" draft />`：文章顶部的适用版本、校对日期、草稿标记
- `<StageHeader :floor="1" />`：阶段页顶部的楼层进度
- `<KeyCap>E</KeyCap>`：按键样式

## 投稿

发现错误或想写攻略，直接提交 Pull Request。请用自己的文字和截图，不要搬运 wiki 或其他攻略站原文。
