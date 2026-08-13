#!/usr/bin/env bash
# 從 .pr-quality.json 讀出某個 check 的指令並逐字執行。
#
# 存在的理由是避免漂移:fork PR 走 external-pr job、不套 evidence gate,
# CI 是唯一關卡。若把指令(特別是 pip-audit 的 --ignore-vuln 豁免清單)
# 另抄一份在 workflow 裡,日後只改 .pr-quality.json 時這裡會繼續沿用舊的
# 豁免,正好在最不該漏的路徑上漏掉。
#
# 指令不做任何改寫 —— workflow 會先建出 venv/,使 CI 的環境布局與設定檔裡
# 的 venv/bin/ 前綴一致。
set -euo pipefail

check="${1:?usage: run-configured-check.sh <check-name>}"

cmd="$(python - "$check" <<'PY'
import json, sys

name = sys.argv[1]
cfg = json.load(open(".pr-quality.json", encoding="utf-8"))
try:
    command = cfg["checks"][name]["command"]
except KeyError:
    sys.exit(f"check '{name}' is not declared in .pr-quality.json")
if command == "auto":
    sys.exit(f"check '{name}' is set to 'auto' in .pr-quality.json — "
             "external-pr needs an explicit command")
print(command)
PY
)"

echo "+ ${cmd}"
eval "${cmd}"
