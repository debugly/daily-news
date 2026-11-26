# Daily News

按分类归档的中文内容简报，覆盖三类：

- **每日新闻**（`news/`）：每天 3 条全球科技与互联网新闻 + 2 条重要国际新闻
- **macOS 周报**（`macos/`）：macOS 音视频开发技术周报
- **AI 热门项目**（`ai/`）：GitHub AI 开源项目周报

## 在线门户

分类浏览入口：<https://debugly.github.io/daily-news/>

## 内容与目录

- `news/YYYY/MM/YYYY-MM-DD.md`：每日新闻，按北京时间归档
- `macos/YYYY/MM/YYYY-MM-DD.md`：macOS 周报，按统计周期归档
- `ai/YYYY/MM/YYYY-MM-DD.md`：AI 热门项目周报，按统计周期归档
- `.github/workflows/auto-merge.yml`：自动合并 Pull Request

## 自动合并

提交到 `main` 的 Pull Request 会自动合并（merge commit，合并后删除源分支）：

- 需要人工审核时，请以 **Draft PR** 方式提交；转为 Ready for review 后才会触发自动合并。
- 存在合并冲突时会跳过，等待人工处理。
