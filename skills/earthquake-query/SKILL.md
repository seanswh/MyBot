---
name: earthquake-query
description: 查询Wolfx.jp地震API，获取最新地震信息
metadata: {"openclaw": {"emoji": "🌍"}}
---

# Earthquake Query Skill

查询Wolfx.jp地震API，获取全球最新地震信息。

## API信息
- **数据源**: https://api.wolfx.jp/cenc_eqlist.json
- **格式**: JSON
- **内容**: 最新50条地震记录
- **更新**: 实时或近实时

## 使用方法

### 1. 直接查询API
使用`web_fetch`工具获取原始数据：
```yaml
web_fetch: https://api.wolfx.jp/cenc_eqlist.json
```

### 2. 运行查询脚本
已有一个Python查询脚本在项目目录：
```bash
cd /workspaces/MyBot && python3 earthquake_check.py
```

**注意**: 这个脚本主要用于定时监控，会对比上次状态。对于单次查询，建议使用第一种方法直接获取API数据。

### 3. 手动分析数据
获取数据后，可以：
1. 解析JSON格式的地震信息
2. 提取最新地震记录（No1是最新的）
3. 格式化输出重要信息

## 数据结构
每条地震记录包含：
- `EventID`: 唯一事件ID（如"AU.20260130152659.000"）
- `time`: 地震发生时间（UTC+8格式）
- `location`: 地震位置（中文）
- `magnitude`: 震级
- `depth`: 深度（公里）
- `latitude`: 纬度
- `longitude`: 经度
- `intensity`: 烈度（1-12级）

## 查询示例

### 获取最新地震
```json
获取API数据，提取"No1"记录
```

### 获取前10条地震
```json
获取API数据，提取"No1"到"No10"记录
```

### 搜索特定地区
```json
获取API数据，筛选location包含"甘肃"的记录
```

## 输出格式化建议
当地震信息时，使用以下格式：
```
🌍 地震报告 🌍
📍 地点: [location]
⏰ 时间: [time]
📊 震级: [magnitude]级
📏 深度: [depth]公里
💥 烈度: [intensity]级
🆔 事件ID: [EventID]
🔗 数据来源: Wolfx.jp
```

## 注意事项
1. 时间格式为UTC+8（北京时间）
2. API返回最新50条地震记录
3. 震级范围：通常2.0-8.0级
4. 烈度范围：1-12级（中国标准）

## 开发记录
- **创建时间**: 2026-02-01
- **开发者**: 小j
- **项目**: MyBot地震监控系统
- **功能**: 单次地震信息查询