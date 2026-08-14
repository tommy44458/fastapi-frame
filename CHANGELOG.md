# Changelog

本檔由 release 流程自動維護，內容取自進入 dev 的 conventional commit 標題，
請勿手動編輯 —— 手寫的內容不會被搬移或更新。版本號的唯一來源是
[app/config.py](app/config.py) 的 `APP_VERSION`，同樣由 release 流程改寫。

首次 release 前本檔沒有任何版本區塊。

## [0.1.1] - 2026-08-14

### Fixed / Changed
- Merge pull request #2 from tommy44458/chore/remove-ci-caller
- chore: 移除 CI caller,gate 改為 local-only
- Merge pull request #1 from tommy44458/chore/pr-quality-gate
- chore: 導入 PR Quality Gate 並修正其揭露的型別與依賴問題

