"""
A股新闻自动抓取调度器

这个脚本不是一个独立的爬虫——它是 Claude 的"行动计划生成器"。
因为实际的网页抓取需要通过 Claude 的 web_search 和 web_fetch 工具执行，
所以这个脚本的作用是：生成结构化的抓取计划，让 Claude 知道该搜什么、抓什么、按什么顺序来。

三种模式：
  workflow   — 生成抓取工作流 JSON（供 Claude 按步骤执行）
  prompt     — 生成一段完整的提示词（用户可以直接发给 Claude 触发抓取+分析）
  schedule   — 生成定时任务配置（cron 表达式 + 每次执行的提示词模板）
  api_script — 生成可部署的 Python 定时脚本（通过 Anthropic API 调用）

用法：
  python fetch_news.py --mode workflow --topics "人工智能,新能源" [--scope full|quick]
  python fetch_news.py --mode prompt --topics "半导体" [--style 短线|中线|长线]
  python fetch_news.py --mode schedule --topics "AI,光伏,消费" --frequency daily
  python fetch_news.py --mode api_script --topics "AI,半导体" --output scheduled_analysis.py
"""

import json
import argparse
import sys
from datetime import datetime


# ══════════════════════════════════════════════════
# 新闻源配置
# ══════════════════════════════════════════════════

NEWS_SOURCES = {
    "P1_policy": {
        "priority": 1,
        "label": "政策源（必搜）",
        "sources": [
            {
                "name": "国务院",
                "search_query": "{topic} site:gov.cn",
                "fetch_urls": ["http://www.gov.cn/zhengce/zuixin.htm"],
                "description": "国务院最新政策文件，政策确定性最高"
            },
            {
                "name": "新华社",
                "search_query": "新华社 {topic} 最新",
                "fetch_urls": ["http://www.news.cn/politics/leaders/index.htm"],
                "description": "新华社权威发布，政策信号首发渠道"
            },
            {
                "name": "央行/证监会",
                "search_query": "央行 OR 证监会 {topic}",
                "fetch_urls": [],
                "description": "货币政策和监管动态"
            }
        ]
    },
    "P2_finance_flash": {
        "priority": 2,
        "label": "财经快讯（必搜）",
        "sources": [
            {
                "name": "财联社电报",
                "search_query": "财联社 {topic} 今日",
                "fetch_urls": ["https://www.cls.cn/telegraph"],
                "description": "最快的财经快讯，盘中消息第一手"
            },
            {
                "name": "东方财富",
                "search_query": "东方财富 {topic} 板块",
                "fetch_urls": [
                    "https://data.eastmoney.com/bkzj/hy.html",
                    "https://data.eastmoney.com/zjlx/detail.html"
                ],
                "description": "板块行情和资金流向数据最全"
            }
        ]
    },
    "P3_deep_analysis": {
        "priority": 3,
        "label": "深度报道（视额度搜）",
        "sources": [
            {
                "name": "新浪财经",
                "search_query": "新浪财经 {topic}",
                "fetch_urls": ["https://finance.sina.com.cn/"],
                "description": "综合财经报道，券商观点汇总"
            },
            {
                "name": "证券时报",
                "search_query": "证券时报 {topic}",
                "fetch_urls": [],
                "description": "证券行业深度分析"
            },
            {
                "name": "同花顺",
                "search_query": "同花顺 {topic} 概念",
                "fetch_urls": ["https://q.10jqka.com.cn/gn/"],
                "description": "概念板块和题材梳理"
            }
        ]
    }
}

MARKET_DATA_SOURCES = [
    {
        "name": "东方财富-板块涨跌",
        "search_query": "{topic}板块 今日涨跌 东方财富",
        "description": "板块整体表现"
    },
    {
        "name": "板块资金流向",
        "search_query": "{topic}板块 资金流向 今日",
        "description": "主力资金动向"
    },
    {
        "name": "个股行情",
        "search_query": "{topic} 龙头股 今日行情",
        "description": "龙头个股表现"
    },
    {
        "name": "ETF净值",
        "search_query": "{topic} ETF 今日净值 涨跌",
        "description": "相关ETF表现"
    }
]


# ══════════════════════════════════════════════════
# 模式一：工作流生成
# ══════════════════════════════════════════════════

def generate_workflow(topics, scope="full"):
    """生成结构化的抓取工作流，Claude 按 steps 顺序执行。"""
    steps = []
    step_id = 1
    today = datetime.now().strftime("%Y-%m-%d")

    for topic in topics:
        topic = topic.strip()

        source_groups = ["P1_policy", "P2_finance_flash"]
        if scope == "full":
            source_groups.append("P3_deep_analysis")

        for group_key in source_groups:
            group = NEWS_SOURCES[group_key]
            for source in group["sources"]:
                query = source["search_query"].format(topic=topic)
                steps.append({
                    "step_id": step_id,
                    "phase": "news_search",
                    "tool": "web_search",
                    "action": f"搜索{source['name']}关于「{topic}」的新闻",
                    "query": query,
                    "priority": group["priority"],
                    "source_name": source["name"],
                    "topic": topic,
                    "instructions": (
                        f"用 web_search 搜索: {query}\n"
                        f"从结果中提取：标题、来源、时间、摘要、URL\n"
                        f"只保留 {today} 前后3天内的新闻\n"
                        f"如果搜索失败或无结果，跳过继续下一步"
                    )
                })
                step_id += 1

                for url in source.get("fetch_urls", []):
                    steps.append({
                        "step_id": step_id,
                        "phase": "news_fetch",
                        "tool": "web_fetch",
                        "action": f"抓取{source['name']}页面",
                        "url": url,
                        "priority": group["priority"],
                        "source_name": source["name"],
                        "topic": topic,
                        "instructions": (
                            f"用 web_fetch 抓取: {url}\n"
                            f"从页面中提取与「{topic}」相关的新闻条目\n"
                            f"如果页面无法访问，跳过不要卡住"
                        )
                    })
                    step_id += 1

        for mds in MARKET_DATA_SOURCES:
            query = mds["search_query"].format(topic=topic)
            steps.append({
                "step_id": step_id,
                "phase": "market_data",
                "tool": "web_search",
                "action": f"获取「{topic}」{mds['description']}",
                "query": query,
                "topic": topic,
                "instructions": f"用 web_search 搜索: {query}\n提取板块/个股名称、涨跌幅、成交额、资金流向"
            })
            step_id += 1

    steps.append({
        "step_id": step_id,
        "phase": "consolidate",
        "tool": "none",
        "action": "整合去重所有抓取结果",
        "instructions": "1. 去重同一事件多个报道\n2. 按情绪影响力排序\n3. 将新闻与行情数据关联\n4. 输出结构化 JSON 进入分析流程"
    })

    return {
        "generated_at": datetime.now().isoformat(),
        "topics": topics,
        "scope": scope,
        "total_steps": len(steps),
        "estimated_search_calls": sum(1 for s in steps if s["tool"] == "web_search"),
        "estimated_fetch_calls": sum(1 for s in steps if s["tool"] == "web_fetch"),
        "steps": steps
    }


# ══════════════════════════════════════════════════
# 模式二：提示词生成
# ══════════════════════════════════════════════════

def generate_prompt(topics, style="全部"):
    """生成可直接发给 Claude 的完整提示词。"""
    topics_str = "、".join(topics)
    today = datetime.now().strftime("%Y年%m月%d日")

    style_map = {
        "短线": "请侧重短线（1-5天）视角，关注热点轮动和游资动向。",
        "中线": "请侧重中线（1-3个月）视角，关注政策落地节奏和行业景气度。",
        "长线": "请侧重长线（半年以上）视角，关注产业空间和估值水平。",
        "全部": "请分别从短线、中线、长线三个维度给出建议，让我自己选择。"
    }
    style_instruction = style_map.get(style, style_map["全部"])

    search_blocks = []
    for topic in topics:
        topic = topic.strip()
        search_blocks.append(
            f"### {topic}\n"
            f"1. 搜索「新华社 {topic} 最新政策」\n"
            f"2. 搜索「财联社 {topic} 今日」\n"
            f"3. 搜索「{topic}板块 今日涨跌 资金流向」\n"
            f"4. 搜索「{topic} ETF 今日净值」\n"
            f"5. 发现重要链接时用 web_fetch 获取全文"
        )

    return f"""请帮我进行A股新闻驱动选股分析。

**日期**：{today}
**关注主题**：{topics_str}
**投资风格**：{style_instruction}

## 第一步：自动抓取新闻和行情

请依次搜索以下信息（某个搜索失败则跳过继续）：

{chr(10).join(search_blocks)}

## 第二步：分析

对抓取到的所有新闻：
1. 判断情绪倾向（-5到+5评分）
2. 识别政策信号强度
3. 产业链上下游联动分析
4. 结合实时行情数据验证

## 第三步：输出建议

请输出：
1. 新闻摘要与情绪判断表
2. 推荐标的列表（名称、代码、推荐逻辑、情绪评分、时间维度、风险等级、建议仓位、关键风险）
3. 板块资金流向概览
4. 同时生成一份 Excel 分析报告

⚠️ 请务必包含风险提示和免责声明。"""


# ══════════════════════════════════════════════════
# 模式三：定时任务配置
# ══════════════════════════════════════════════════

SCHEDULE_TEMPLATES = {
    "pre_market": {
        "name": "盘前扫描",
        "description": "每个交易日开盘前（9:00）抓取隔夜新闻和政策",
        "cron": "0 9 * * 1-5",
        "cron_readable": "每周一到周五早上 9:00",
        "scope": "full",
        "focus": "重点关注隔夜发布的政策文件、央行公告、国际市场影响"
    },
    "midday": {
        "name": "午间快报",
        "description": "午休时段（11:35）快速扫描上午盘面异动新闻",
        "cron": "35 11 * * 1-5",
        "cron_readable": "每周一到周五中午 11:35",
        "scope": "quick",
        "focus": "重点关注上午涨停板块催化剂、突发消息、资金异动"
    },
    "post_market": {
        "name": "盘后复盘",
        "description": "收盘后（15:30）全面复盘当日新闻与行情",
        "cron": "30 15 * * 1-5",
        "cron_readable": "每周一到周五下午 15:30",
        "scope": "full",
        "focus": "全面复盘当日涨跌原因，发现次日可能延续的主线"
    },
    "weekly": {
        "name": "周末研判",
        "description": "周六上午进行周度总结和下周展望",
        "cron": "0 10 * * 6",
        "cron_readable": "每周六上午 10:00",
        "scope": "full",
        "focus": "本周政策梳理、板块轮动总结、下周重要事件预告、中线布局建议"
    }
}


def generate_schedule(topics, frequency="daily", style="全部"):
    """生成定时任务配置，包含多种环境的使用说明。"""
    freq_map = {
        "daily": ["pre_market", "midday", "post_market"],
        "weekly": ["pre_market", "post_market", "weekly"],
        "pre_market_only": ["pre_market"],
        "all": list(SCHEDULE_TEMPLATES.keys())
    }
    selected = freq_map.get(frequency, ["pre_market", "post_market"])

    schedules = []
    for key in selected:
        tmpl = SCHEDULE_TEMPLATES[key]
        base_prompt = generate_prompt(topics, style)
        full_prompt = f"【{tmpl['name']} - 自动触发】\n{tmpl['focus']}\n\n{base_prompt}"

        schedules.append({
            "task_name": tmpl["name"],
            "description": tmpl["description"],
            "cron_expression": tmpl["cron"],
            "cron_readable": tmpl["cron_readable"],
            "scope": tmpl["scope"],
            "topics": topics,
            "prompt": full_prompt,
        })

    usage_guide = {
        "方案A_Claude_Code": {
            "description": "在 Claude Code 中用 cron + claude CLI 实现全自动",
            "steps": [
                "1. 将定时脚本保存到服务器",
                "2. 用 crontab -e 添加定时任务",
                "3. 每次触发会调用 claude -p '提示词' 并保存结果"
            ],
            "example_cron": [
                f"{s['cron_expression']}  claude -p \"$(cat ~/prompts/{s['task_name']}.txt)\" "
                f"> ~/reports/$(date +\\%Y\\%m\\%d)_{s['task_name']}.md 2>&1"
                for s in schedules
            ]
        },
        "方案B_API定时脚本": {
            "description": "用 Anthropic API + Python 脚本 + cron/云函数 实现全自动",
            "steps": [
                "1. 运行 --mode api_script 生成 Python 脚本",
                "2. 部署到服务器或云函数（阿里云FC / AWS Lambda）",
                "3. 配置定时触发器",
                "4. 结果可发送到邮箱、微信、钉钉等"
            ]
        },
        "方案C_Claude_AI手动": {
            "description": "在 Claude.ai 中按时间手动触发（最简单）",
            "steps": [
                "1. 设置手机闹钟提醒（9:00 / 11:35 / 15:30）",
                "2. 打开 Claude.ai 新对话",
                "3. 粘贴对应时段的提示词",
                "4. 等待分析完成，下载报告"
            ],
            "prompts": {s["cron_readable"]: s["task_name"] for s in schedules}
        },
        "方案D_iOS快捷指令": {
            "description": "iPhone 用户可用快捷指令半自动触发",
            "steps": [
                "1. 创建「快捷指令」→ 自动化 → 每天固定时间",
                "2. 动作：打开 Claude app",
                "3. （可选）通过 Anthropic API 直接调用并推送结果到备忘录"
            ]
        }
    }

    return {
        "generated_at": datetime.now().isoformat(),
        "topics": topics,
        "frequency": frequency,
        "style": style,
        "schedules": schedules,
        "usage_guide": usage_guide
    }


# ══════════════════════════════════════════════════
# 模式四：API 定时脚本生成
# ══════════════════════════════════════════════════

def generate_api_script(topics, style="全部"):
    """生成可部署的 Python 定时调用脚本。"""
    topics_json = json.dumps(topics, ensure_ascii=False)
    prompt_text = generate_prompt(topics, style)
    # 安全转义
    prompt_escaped = prompt_text.replace("\\", "\\\\").replace('"', '\\"')

    return f'''#!/usr/bin/env python3
"""
A股新闻自动分析 - 定时任务脚本

部署方式：
  1. pip install anthropic
  2. export ANTHROPIC_API_KEY="your-key"
  3. crontab: 0 9 * * 1-5 python3 scheduled_analysis.py
  
也可部署到：阿里云函数计算、AWS Lambda、腾讯云SCF 等 Serverless 平台。

可选增强：
  - 结果推送：接入企业微信/钉钉/邮件 webhook
  - 历史存储：保存到数据库追踪推荐准确率
  - 行情接入：用 akshare/tushare 获取实时行情补充分析
"""

import os
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

try:
    import anthropic
except ImportError:
    print("请先安装: pip install anthropic")
    exit(1)


# ── 配置区 ──
TOPICS = {topics_json}
OUTPUT_DIR = os.path.expanduser("~/stock-reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 可选：邮件通知配置（取消注释并填写）
# EMAIL_CONFIG = {{
#     "smtp_server": "smtp.qq.com",
#     "smtp_port": 465,
#     "sender": "your@qq.com",
#     "password": "授权码",
#     "receiver": "your@email.com"
# }}
EMAIL_CONFIG = None

# 可选：企业微信/钉钉 webhook（取消注释并填写）
# WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
WEBHOOK_URL = None


def get_current_session_type():
    """根据当前时间判断是哪个时段的分析。"""
    hour = datetime.now().hour
    if hour < 10:
        return "盘前扫描", "重点关注隔夜政策、央行公告、外盘影响"
    elif hour < 13:
        return "午间快报", "重点关注上午异动板块、突发消息"
    elif hour < 16:
        return "盘后复盘", "全面复盘当日行情，寻找次日主线"
    elif datetime.now().weekday() == 5:
        return "周末研判", "周度总结，下周展望和中线布局"
    else:
        return "盘后复盘", "复盘当日新闻与行情"


def run_analysis():
    """执行分析并保存结果。"""
    client = anthropic.Anthropic()

    session_name, focus = get_current_session_type()
    prompt = f"""【{{session_name}} - 自动触发】
{{focus}}

{prompt_escaped}"""

    print(f"[{{datetime.now()}}] 开始 {{session_name}}: {{', '.join(TOPICS)}}")

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{{"role": "user", "content": prompt}}]
    )

    result = response.content[0].text

    # 保存 Markdown 报告
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{{session_name}}_{{ts}}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {{session_name}} - {{datetime.now().strftime('%Y-%m-%d %H:%M')}}\\n\\n")
        f.write(result)

    print(f"[{{datetime.now()}}] 已保存: {{filepath}}")

    # 可选：发送通知
    if EMAIL_CONFIG:
        send_email(session_name, result)
    if WEBHOOK_URL:
        send_webhook(session_name, result)

    return filepath


def send_email(subject, content):
    """通过邮件发送分析结果。"""
    try:
        msg = MIMEText(content, "plain", "utf-8")
        msg["Subject"] = f"A股分析: {{subject}} - {{datetime.now().strftime('%m/%d')}}"
        msg["From"] = EMAIL_CONFIG["sender"]
        msg["To"] = EMAIL_CONFIG["receiver"]

        with smtplib.SMTP_SSL(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"]) as s:
            s.login(EMAIL_CONFIG["sender"], EMAIL_CONFIG["password"])
            s.send_message(msg)
        print("邮件已发送")
    except Exception as e:
        print(f"邮件发送失败: {{e}}")


def send_webhook(session_name, content):
    """通过企业微信/钉钉 webhook 发送通知。"""
    try:
        import urllib.request
        # 截取摘要（webhook 消息有长度限制）
        summary = content[:2000] + "\\n\\n...（完整报告见本地文件）" if len(content) > 2000 else content
        data = json.dumps({{"msgtype": "text", "text": {{"content": f"【{{session_name}}】\\n{{summary}}"}}}})
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=data.encode("utf-8"),
            headers={{"Content-Type": "application/json"}}
        )
        urllib.request.urlopen(req)
        print("Webhook 通知已发送")
    except Exception as e:
        print(f"Webhook 发送失败: {{e}}")


if __name__ == "__main__":
    run_analysis()
'''


# ══════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="A股新闻抓取调度器")
    parser.add_argument("--mode", required=True,
                        choices=["workflow", "prompt", "schedule", "api_script"],
                        help="运行模式")
    parser.add_argument("--topics", required=True,
                        help="关注主题，逗号分隔")
    parser.add_argument("--scope", default="full", choices=["full", "quick"],
                        help="搜索范围")
    parser.add_argument("--style", default="全部",
                        choices=["短线", "中线", "长线", "全部"],
                        help="投资风格")
    parser.add_argument("--frequency", default="daily",
                        choices=["daily", "weekly", "pre_market_only", "all"],
                        help="定时频率（仅 schedule 模式）")
    parser.add_argument("--output", default=None,
                        help="输出文件路径")

    args = parser.parse_args()
    topics = [t.strip() for t in args.topics.split(",")]

    if args.mode == "workflow":
        result = generate_workflow(topics, args.scope)
        output = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.mode == "prompt":
        output = generate_prompt(topics, args.style)
    elif args.mode == "schedule":
        result = generate_schedule(topics, args.frequency, args.style)
        output = json.dumps(result, ensure_ascii=False, indent=2)
    elif args.mode == "api_script":
        output = generate_api_script(topics, args.style)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"已保存到: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
