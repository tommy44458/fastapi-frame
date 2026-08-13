<!-- 不要手寫這份內容,用腳本產生:
       python3 scripts/render-pr-body.py > .local-reports/pr-body.md
     腳本會從 Test Evidence 渲染 Quality Gate 表格與風險區塊,數字永不手抄。
     只需填「摘要」、「需求依據」與「變更內容」三段。
     禁止貼上測試 log 或完整的 evidence JSON。 -->

## 摘要

<!-- 改了什麼、為什麼改 — 2–5 句,寫給沒看過這個分支的人。 -->

## 需求依據

<!-- ticket/spec ID 或連結 + 非敏感 acceptance criteria 摘要。
     若使用者明確確認無正式需求,請照實寫明;不得留白、猜測或貼入 secrets/個資。 -->

## 變更內容

<!-- 每個邏輯區域一個 bullet(與 aiAssessment.changedAreas 對齊)。
     描述行為變更,不要列檔案 — diff 已經列了。 -->

## Quality Gate

<!-- 渲染區塊(勿手寫):標題含 result badge,內容為
     | 檢查項目 | 結果 | 明細 | 表格 + 一行 coverage/sourceHash/generated。
     至少確認:
     - [ ] ./scripts/verify-pr-ready.sh --mode pr 通過(exit 0)
     - [ ] 表格數字來自 .github/pr-test-evidence.json,不是憑記憶 -->

## 風險與審查

<!-- 渲染區塊(勿手寫):固定五列的 | 項目 | 內容 | 表格 —
     風險等級 / 風險旗標 / 架構審查 / 審查重點 / 未測試情境。
     欄位不隨內容增減,無資料一律填 —,每個 PR 版面一致。 -->

## 五維度檢核

<!-- 渲染區塊(勿手寫):| 維度 | 結果 | 備註 | 表格,
     來自 evidence 的 aiAssessment.dimensions。 -->
