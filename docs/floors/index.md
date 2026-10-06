---
title: "楼层图鉴"
aside: false
---

<script setup lang="ts">
import type { CatalogEntry } from "../.vitepress/theme/data/catalog"
import allEntries from "../.vitepress/theme/data/catalog/floors.json"
const entries = allEntries as CatalogEntry[]
</script>

# 楼层图鉴

<VersionBadge checked="2026-10" />

每种楼层独立说明前置、危险与路线出口，I / II 同页讲清；贪婪同名楼层分开列出，避免混用模式规则。

## 按名称与类型查找 {#floor-index}

<EntryCatalog :entries="entries" label="楼层图鉴" />

### 四条路线怎么选 {#route-map}

| 本局目标 | 推进顺序 | 必须提前准备 |
| --- | --- | --- |
| 主线宝箱 / 暗室 | 前三章 → 妈妈选照片 → 子宫 → 教堂 / 阴间 → 对应终局层 | 全家福走教堂，底片走阴间 |
| 死寂 | 前三章 → 子宫 II → 蓝子宫 | 先解锁蓝子宫，本局 30 分钟内击败心脏 / 它活着 |
| 母亲 | 下水道 II 镜面刀片 → 矿洞 II 逃亡刀片 → 陵墓 II 肉门 → 尸宫 II | 秘密出口已解锁；钥匙、炸弹、入门血量和两块刀片 |
| 祸兽 / 里角色 | 深处 II 妈妈取照片 → 传送回起点开奇怪的门 → 爸爸的便条 → 上行 → 家 | 奇怪的门已解锁；照片、传送、红钥匙或红钥匙碎片 |

**妈妈以后选的出口通常决定后续路线**。跳了普通活板门，不会再回当前层补刀片或开门。存档前置与结局编号见[结局与路线](/guide/unlocks/endings)，本局漏掉什么可用[路线检查](/tools/routes)复核。

## 第一章 {#chapter-one}

[地下室](/floors/basement) · [地窖](/floors/cellar) · [燃烧地下室](/floors/burning-basement)

## 第二章 {#chapter-two}

[洞穴](/floors/caves) · [墓穴](/floors/catacombs) · [淹水洞穴](/floors/flooded-caves)

## 第三章 {#chapter-three}

[深处](/floors/depths) · [坟场](/floors/necropolis) · [阴湿深处](/floors/dank-depths)

## 第四章 {#chapter-four}

[子宫](/floors/womb) · [血宫](/floors/utero) · [疤痕子宫](/floors/scarred-womb)

## 母亲替代路线 {#alt-path}

[下水道](/floors/downpour) · [污水渠](/floors/dross) · [矿洞](/floors/mines) · [灰坑](/floors/ashpit) · [陵墓](/floors/mausoleum) · [炼狱](/floors/gehenna) · [尸宫](/floors/corpse)

## 终局楼层 {#late-floors}

[蓝子宫](/floors/blue-womb) · [阴间](/floors/sheol) · [教堂](/floors/cathedral) · [暗室](/floors/dark-room) · [宝箱](/floors/chest) · [虚空](/floors/void) · [上行](/floors/ascent) · [家](/floors/home) · [XL 与迷宫诅咒](/floors/xl)

## 回家路线 {#home-path}

[蓝子宫](/floors/blue-womb) · [阴间](/floors/sheol) · [教堂](/floors/cathedral) · [暗室](/floors/dark-room) · [宝箱](/floors/chest) · [虚空](/floors/void) · [上行](/floors/ascent) · [家](/floors/home) · [XL 与迷宫诅咒](/floors/xl)

## 贪婪七层 {#greed-floors}

[贪婪 · 地下室](/floors/greed-basement) · [贪婪 · 洞穴](/floors/greed-caves) · [贪婪 · 深处](/floors/greed-depths) · [贪婪 · 子宫](/floors/greed-womb) · [贪婪 · 阴间](/floors/greed-sheol) · [贪婪 · 商店](/floors/greed-shop) · [贪婪 · 究极贪婪](/floors/ultra-greed)

## XL、诅咒与特殊地图 {#curses}

| 情况 | 到底改变什么 | 处理方法 |
| --- | --- | --- |
| 迷宫诅咒 / XL | 同章两层合并为一张大图，通常两个宝箱房、两个 Boss | 第一、第二 Boss 都处理；交易门与章终点看第二个 Boss；不能推导成“两家免费商店” |
| 黑暗诅咒 | 视野变暗 | 先看危险地面与弹幕，不盲目贴脸 |
| 迷失诅咒 | 隐藏地图 | 自己记起点、已走支路和关键门；路线物品仍需照常获取 |
| 致盲诅咒 | 底座效果以问号显示 | 当前组合已成型时少赌冲突道具，价签仍是实际消费依据 |
| 未知诅咒 | 隐藏生命显示 | 自己记录进出房伤害、交易和补血，不用不确定血量去献祭 |
| 混乱诅咒（Curse of the Maze） | 移动中可能错位或变化房间连接 | 错位后重新确认地图位置，不按前一扇门的方向盲走 |

XL 不是独立的地窖、陵墓或新结局，而是地图生成变化；“第 I 层变大了”常意味着这一章已经合并，不要等一个不会另出现的 II 层。镜面世界、矿车逃亡、夹层、黑市与错误房是区域 / 房间，也不计为独立主线章节。

挑战可能不生成宝箱房，路线和终点也不同；彩蛋种子和模组同样可能改图。查[挑战总表](/strategy/challenges#全部挑战总表)确认该挑战的终点，不要强套普通模式完整路线。

## 下层之前的检查单 {#before-exit}

1. **主线**：妈妈选了正确照片吗？心脏后的活板门 / 光柱选对了吗？
2. **死寂**：蓝子宫解锁了吗、时间够吗、准备区的钥匙和钱够吗？
3. **母亲**：下水道 II 的镜面刀片、矿洞 II 的逃亡刀片都拿了吗？陵墓用的是肉门出口吗？
4. **祸兽与里角色**：有返回起点的传送吗、用照片开门了吗、拿便条前留下饰品了吗、到家先开衣柜了吗？
5. **超级撒但 / 虚空**：金门需要的完整钥匙或开门道具有了吗？虚空是本局目标还是额外风险？
6. **贪婪**：可选交易波、两间宝箱房、最后购物处理完了吗？留下的硬币是否真能拿去捐？

<span id="参考资料"></span>

## 数据依据 {#sources}

[条目来源与更新方式](/about#entry-sources)。各详情页附原始资料链接；道具名称按类型与 ID 区分，同名的特殊形态不会相互覆盖。
