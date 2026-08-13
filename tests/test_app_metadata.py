"""版本號來源的回歸測試。

`APP_VERSION` 是模組常數而非 settings 欄位,release 流程會直接改寫
`app/config.py` 的那一行。這裡鎖住三件事:值真的傳到對外的 OpenAPI 文件、
環境變數不能再覆寫它、以及 release 流程賴以改寫的文字格式沒有被動過。
"""

import json
import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent


def test_app_version_reaches_openapi() -> None:
    import config
    from api.app import create_app

    app = create_app()

    assert app.version == config.APP_VERSION
    assert app.openapi()["info"]["version"] == config.APP_VERSION


def test_app_version_is_not_a_settings_field(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """把 APP_VERSION 放回 ServerConfig 會讓環境變數重新取得覆寫權。

    這個迴歸不會被型別檢查或其他測試攔下 —— ServerConfig 設了
    `extra="ignore"`,多出來的欄位不會報錯,只會安靜地改變行為。
    """
    import config

    monkeypatch.setenv("APP_VERSION", "9.9.9")

    assert not hasattr(config.ServerConfig(), "APP_VERSION")


def test_release_flow_can_still_rewrite_the_version_line() -> None:
    """.pr-quality.json 的 versioning pattern 必須恰好命中版本檔一次。

    release 流程是純文字取代:改成 `APP_VERSION: str = "..."`、換成單引號、
    或多出第二處同樣寫法,都會讓 bump 失敗或改錯地方,而這些都不會被
    型別檢查或其他測試發現。
    """
    cfg = json.loads((REPO_ROOT / ".pr-quality.json").read_text(encoding="utf-8"))
    version_files = cfg["versioning"]["files"]
    assert version_files, "versioning.files 未設定,release 流程無法決定版本檔"

    for entry in version_files:
        source = (REPO_ROOT / entry["path"]).read_text(encoding="utf-8")
        # 允許 rc 後綴:release 流程在 RC 階段會寫入 X.Y.Z-rc-N,
        # 只認三段數字會讓 release/qa 分支上的測試假紅燈。
        probe = re.escape(entry["pattern"]).replace(
            r"\{version\}", r"\d+\.\d+\.\d+(?:-rc-\d+)?"
        )
        assert len(re.findall(probe, source)) == 1, (
            f"{entry['path']} 必須恰好一處符合 {entry['pattern']!r}"
        )
