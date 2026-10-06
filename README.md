# astrbot_plugin_deepseek_balance

> **声明**：本插件的核心代码由 DeepSeek（AI）辅助生成，经人工调试与整理，仅供学习交流使用。

AstrBot 插件：查询 DeepSeek API 账户余额。

## 简介

本插件通过 DeepSeek 官方余额接口查询账户余额，支持在 QQ（NapCat / aiocqhttp）中通过指令触发。查询结果包含总余额、赠金余额和充值余额。仅管理员可用，避免余额信息在群内泄露。

## 功能特性

- 调用 DeepSeek 官方余额接口 `https://api.deepseek.com/user/balance`
- 支持多币种余额展示（CNY / USD）
- 仅管理员可触发查询
- 查询失败时返回友好提示
- 基于 AstrBot 异步框架，使用 `aiohttp` 请求

## 环境要求

- AstrBot 版本 >= 4.0.0
- 机器人平台：QQBOT（NapCat / aiocqhttp）
- 可访问 `api.deepseek.com` 的网络环境
- 有效的 DeepSeek API Key（以 `sk-` 开头）

## 安装

1. 在 AstrBot 的 `data/plugins/` 目录下创建文件夹：`astrbot_plugin_deepseek_balance`
2. 将以下文件放入该文件夹：
   - `metadata.yaml`
   - `_conf_schema.json`
   - `main.py`
3. 在 AstrBot WebUI 的插件页面点击刷新，加载插件。

## 配置

在 AstrBot WebUI -> 插件 -> DeepSeek 余额查询 -> 配置 中填写：

| 配置项 | 类型 | 说明 | 默认值 |
| --- | --- | --- | --- |
| `deepseek_api_key` | string | DeepSeek API Key，以 `sk-` 开头 | 空 |
| `request_timeout` | int | 请求超时时间（秒） | 10 |

> API Key 会以密文形式存储，但仍请勿在群聊或公开场合泄露。

## 使用

在 QQ 聊天中发送指令：`/dsbalance`

仅管理员可触发。机器人将返回格式化的账户余额信息。

```text
📊 DeepSeek 账户余额
━━━━━━━━━━━━━━
💰 总余额：¥12.34 CNY
   🎁 赠金：¥2.34
   💳 充值：¥10.00
━━━━━━━━━━━━━━
```

如果账户有美元余额，也会一并展示。

## 权限说明

插件使用 AstrBot 内置的管理员权限装饰器：`@filter.permission_type(filter.PermissionType.ADMIN)` 和 `@filter.command("dsbalance")`。

管理员 ID 在 AstrBot WebUI -> 配置 -> 其他配置 -> 管理员 ID 中设置。用户发送 `/sid` 可获取自己的 ID，再由管理员添加。

非管理员发送 `/dsbalance` 会收到权限不足提示，不会返回余额信息。

## 错误处理

| 情况 | 返回提示 |
| --- | --- |
| 未配置 API Key | 请先在插件配置中设置 DeepSeek API Key |
| API Key 无效或过期 | API Key 无效或已过期，请检查配置 |
| 网络连接失败 | 无法连接到 DeepSeek 服务器，请检查网络 |
| 接口返回非 200 | 查询失败，接口返回状态码 xxx |
| 无可用余额 | 当前账户无可用余额 |

## 注意事项

- 请确保 AstrBot 所在服务器能正常访问 `api.deepseek.com`。
- 本插件查询的是 DeepSeek 账户余额，不是单个 API Key 的独立额度。
- 频繁查询可能触发平台风控，建议按需使用。
- 请勿将 API Key 写入公开代码仓库或分享给他人。

## 文件结构

- `metadata.yaml`
- `_conf_schema.json`
- `main.py`
- `README.md`

## 许可证

MIT License