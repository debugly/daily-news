# Daily News

每天精选 **3 条全球科技与互联网新闻 + 2 条重要国际新闻**，使用 AI 生成中文 Markdown 简报。

## 内容与目录

- `news/YYYY/MM/YYYY-MM-DD.md`：按北京时间日期归档
- `scripts/fetch_news.py`：获取公开 RSS 新闻候选
- `scripts/generate_digest.py`：AI 摘要与来源 URL 校验
- `.github/workflows/daily-news.yml`：每天北京时间 08:00 计划运行

## 启用

1. 审核并合并首次 PR。
2. 在仓库 Settings → Secrets and variables → Actions 添加 `OPENAI_API_KEY`，不要提交密钥。
3. 确认 Settings → Actions → General → Workflow permissions 允许 Read and write permissions。
4. 在 Actions → Daily News → Run workflow 手动试运行。
5. 确认输出后自动每天执行，GitHub 定时任务可能延迟。

**注意：** 使用 OpenAI API 单独计费。RSS 仅提供新闻候选，AI 摘要需要人工抽查。来源不足或校验失败时不发布。当前版本不自动添加配图（避免虚构或未经授权的图片），也不包含 Telegram 推送。

## 本地运行

```bash
python -m pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key"
python scripts/generate_digest.py
```
