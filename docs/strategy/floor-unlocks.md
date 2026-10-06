---
title: 楼层解锁与 Boss 补缺检查
---
# 楼层解锁与 Boss 补缺检查

<VersionBadge checked="2026-10" />

楼层解锁看永久成就，通关这一层一次不等于击败该层所有要求的 Boss。不同区域或 Boss Rush 遇到同名 Boss 也可能推进原条件，不能只看自己是否走过 Basement / Caves / Depths。

| 目标 | 已核对的条件 | 当前版本排除项 | 解锁记录 |
| --- | --- | --- | --- |
| 地窖 | 击败地下室章节所需 Boss | 忏悔 / 忏悔+ 不要求 Baby Plum | [#86](/achievements/ids-001-100#achievement-86) |
| 墓穴 | 击败洞穴章节所需 Boss | 不要求 Bumbino | [#87](/achievements/ids-001-100#achievement-87) |
| 坟场 | 击败深处章节所需 Boss | 不要求 Reap Creep | [#88](/achievements/ids-001-100#achievement-88) |
| 污水渠 | 击败下水道的全部要求 Boss | 不从基础第一章 Boss 名单推导 | [#412](/achievements/ids-401-500#achievement-412) |
| 灰坑 | 击败矿洞的全部要求 Boss | 不从基础洞穴名单推导 | [#413](/achievements/ids-401-500#achievement-413) |
| 炼狱 | 击败陵墓的全部要求 Boss | 不从妈妈或深处名单推导 | [#414](/achievements/ids-401-500#achievement-414) |

## 怎么确认缺的是谁

1. 先用[本地进度工具](/tools/local-progress)检查对应成就是否已经解锁；解锁后不需要为了变体重复补这个条件。
2. 未解锁时，查看游戏图鉴的 Boss 遭遇 / 击败记录，区分见过与真正击败。
3. 用[前中期 Boss 图鉴](/bosses/)复习不会打的目标，继续可解锁的随机正常局。图鉴的章节分类是查询分组，不是官方完整必需名单。
4. 若某个目标只在已解锁变体出现，不应直接把它添成基础变体的前置，避免循环要求。

## 完整名单的核实状态

固定成就来源确认了“全部”条件和三个排除项，但没有保存完整 Boss 名单。当前无法访问对应 wiki 楼层页，本页不把章节开发枚举或猜测名单写成已核实的必需清单。完整名单仍需对照当前版本楼层资料或游戏解锁判定补录，详见[资料核实记录](/about-verification#pending)。

这一限制也适用于本地工具：它读取解锁位，暂不宣称能从怪物图鉴区段准确算出每个楼层还缺的 Boss。

## 来源

使用仓库固定 `data/achievement-source.json` 的 #86、#87、#88、#412–414 条件；对应条目保留原出处：[Cellar](https://bindingofisaacrebirth.wiki.gg/wiki/Cellar)、[Catacombs](https://bindingofisaacrebirth.wiki.gg/wiki/Catacombs)、[Necropolis](https://bindingofisaacrebirth.wiki.gg/wiki/Necropolis)、[Dross](https://bindingofisaacrebirth.wiki.gg/wiki/Dross)、[Ashpit](https://bindingofisaacrebirth.wiki.gg/wiki/Ashpit)、[Gehenna](https://bindingofisaacrebirth.wiki.gg/wiki/Gehenna)。
