---
title: "房间图鉴"
aside: false
---

<script setup lang="ts">
import type { CatalogEntry } from "../.vitepress/theme/data/catalog"
import allEntries from "../.vitepress/theme/data/catalog/rooms.json"
const entries = allEntries as CatalogEntry[]
</script>

# 房间图鉴

<VersionBadge checked="2026-10" />

每种房间独立说明进入条件、奖励、资源消耗与打法；镜面世界、矿车逃亡、红房间等特殊区域也有单独入口。

## 按名称与类型查找 {#room-index}

<EntryCatalog :entries="entries" label="房间图鉴" />

## 每层怎样安排顺序 {#room-order}

1. **先确定目标**：普通通关、赶 Boss Rush / 死寂、母亲刀片、祸兽照片各有不同必做事项。
2. **先留门票**：宝箱房钥匙、替代门炸弹、天使雕像炸弹、陵墓入门生命不要提前花光。
3. **稳定提升优先**：先拿可见的有效道具与补给，再按剩余生命评估诅咒、挑战、献祭、黑市。
4. **利用地形省成本**：确认隐藏房能否绕锁门，检查夹层是否有返回梯子；传送卡既能撤离战斗，也可能是回家路线的必需品。
5. **下楼前复核**：想要的交易、刀片、照片、留下的饰品都做好再跳；特殊活板门与光柱的目的地不同。

## 基础战斗与发育 {#basic}

[初始房间与普通房间](/rooms/normal) · [宝箱房](/rooms/treasure) · [商店](/rooms/shop) · [Boss 房](/rooms/boss) · [小头目房](/rooms/miniboss)

## 隐藏与交易 {#hidden-deals}

[隐藏房](/rooms/secret) · [超级隐藏房](/rooms/supersecret) · [究极隐藏房](/rooms/ultrasecret) · [恶魔房](/rooms/devil) · [天使房](/rooms/angel)

## 用生命和资源换奖励 {#resource-rooms}

[诅咒房](/rooms/curse) · [普通挑战房](/rooms/challenge) · [Boss 挑战房](/rooms/boss-challenge) · [献祭房](/rooms/sacrifice) · [图书馆](/rooms/library) · [赌博房](/rooms/arcade) · [宝库](/rooms/vault) · [骰子房](/rooms/dice)

## 特殊奖励 {#special-rewards}

[干净卧室](/rooms/clean-bedroom) · [肮脏卧室](/rooms/dirty-bedroom) · [夹层](/rooms/crawlspace) · [黑市](/rooms/black-market) · [星象房](/rooms/planetarium)

## 路线功能房 {#route-rooms}

[Boss Rush](/rooms/boss-rush) · [错误房](/rooms/error) · [替代章节入口房](/rooms/secret-exit) · [贪婪出口房](/rooms/greed-exit) · [蓝钥匙房](/rooms/blue) · [红房间](/rooms/red) · [镜面世界](/rooms/mirror) · [矿车与逃亡区域](/rooms/minecart) · [奇怪的门与便条房](/rooms/strange-door) · [Home 隐藏衣柜](/rooms/home-closet) · [创世记卧室](/rooms/genesis) · [遗骸坟墓房](/rooms/grave)

## 红房间与路线区域 {#special-areas}

[Boss Rush](/rooms/boss-rush) · [错误房](/rooms/error) · [替代章节入口房](/rooms/secret-exit) · [贪婪出口房](/rooms/greed-exit) · [蓝钥匙房](/rooms/blue) · [红房间](/rooms/red) · [镜面世界](/rooms/mirror) · [矿车与逃亡区域](/rooms/minecart) · [奇怪的门与便条房](/rooms/strange-door) · [Home 隐藏衣柜](/rooms/home-closet) · [创世记卧室](/rooms/genesis) · [遗骸坟墓房](/rooms/grave)

<span id="参考资料"></span>

## 数据依据 {#sources}

[条目来源与更新方式](/about#entry-sources)。各详情页附原始资料链接；道具名称按类型与 ID 区分，同名的特殊形态不会相互覆盖。
