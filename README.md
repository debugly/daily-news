# Daily News

每天精选 **3 条全球科技与互联网新闻 + 2 条重要国际新闻**，生成中文 Markdown 简报，按北京时间归档。

## 内容与目录

- `news/YYYY/MM/YYYY-MM-DD.md`：按北京时间日期归档的简报
- `.github/workflows/auto-merge.yml`：自动合并 Pull Request

## 自动合并

提交到 `main` 的 Pull Request 会自动合并（merge commit，合并后删除源分支）：

- 需要人工审核时，请以 **Draft PR** 方式提交；转为 Ready for review 后才会触发自动合并。
- 存在合并冲突时会跳过，等待人工处理。
