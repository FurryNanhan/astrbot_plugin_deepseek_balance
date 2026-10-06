import aiohttp
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger


class DeepSeekBalancePlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}
        self.session = None

    async def initialize(self):
        self.session = aiohttp.ClientSession()

    async def terminate(self):
        if self.session:
            await self.session.close()

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("dsbalance")
    async def query_balance(self, event: AstrMessageEvent):
        """查询 DeepSeek API 余额。用法：/dsbalance（仅管理员）"""
        api_key = self.config.get("deepseek_api_key", "")
        if not api_key:
            yield event.plain_result(
                "请先在插件配置中设置 DeepSeek API Key。\n"
                "路径：AstrBot WebUI -> 插件 -> DeepSeek 余额查询 -> 配置"
            )
            return

        timeout = self.config.get("request_timeout", 10)

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        try:
            async with self.session.get(
                "https://api.deepseek.com/user/balance",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as resp:
                if resp.status == 401:
                    yield event.plain_result("API Key 无效或已过期，请检查配置。")
                    return
                if resp.status != 200:
                    text = await resp.text()
                    logger.error(f"DeepSeek 余额接口返回 {resp.status}: {text}")
                    yield event.plain_result(f"查询失败，接口返回状态码 {resp.status}。")
                    return

                data = await resp.json()

        except aiohttp.ClientConnectorError:
            yield event.plain_result("无法连接到 DeepSeek 服务器，请检查网络。")
            return
        except Exception as e:
            logger.error(f"查询 DeepSeek 余额时出错: {e}")
            yield event.plain_result(f"查询出错：{type(e).__name__}")
            return

        is_available = data.get("is_available", False)
        balance_infos = data.get("balance_infos", [])

        if not is_available or not balance_infos:
            yield event.plain_result("当前账户无可用余额。")
            return

        lines = ["📊 DeepSeek 账户余额", "━━━━━━━━━━━━━━"]
        for info in balance_infos:
            currency = info.get("currency", "?")
            total = info.get("total_balance", "0")
            granted = info.get("granted_balance", "0")
            topped = info.get("topped_up_balance", "0")
            symbol = "¥" if currency == "CNY" else "$"
            lines.append(f"💰 总余额：{symbol}{total} {currency}")
            lines.append(f"   🎁 赠金：{symbol}{granted}")
            lines.append(f"   💳 充值：{symbol}{topped}")

        lines.append("━━━━━━━━━━━━━━")
        yield event.plain_result("\n".join(lines))