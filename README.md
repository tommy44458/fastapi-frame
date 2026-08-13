# fastapi-frame

一個乾淨的 FastAPI + PostgreSQL 樣板，支援非同步 SQLAlchemy、Pydantic Settings、JWT 認證與 Alembic migration。複製即用，移除大部分業務邏輯後可直接擴充新功能。

## 特色

- **FastAPI 0.141** + **Uvicorn**
- **SQLAlchemy 2.0** 純 async（asyncpg）
- **Pydantic v2** + `pydantic-settings` 統一管理環境變數
- **Alembic** 處理 production 結構遷移；dev 模式可開 `AUTO_CREATE_TABLES`
- **JWT 認證**（`python-jose` + `bcrypt`），內建 `/auth/register`、`/auth/token`、`/auth/me`
- **Docker / docker-compose** 一鍵起 Postgres + App
- **pytest + httpx ASGI** 測試骨架

## 專案結構

```
app/
├── main.py                # uvicorn 進入點
├── config.py              # Pydantic Settings + APP_VERSION（release 流程改寫，勿改其格式）
├── core/
│   ├── db.py              # async engine + session + get_db
│   ├── base_model.py      # DeclarativeBase + UUIDBase / IDBase（主鍵 abstract base）
│   ├── base_operator.py   # CRUD repository (async)
│   ├── security.py        # JWT + password hashing
│   └── logging.py         # logging 設定
├── api/
│   ├── app.py             # create_app + lifespan + middleware
│   ├── deps.py            # get_db, get_current_user
│   ├── routers/
│   │   ├── auth.py        # /auth/register, /auth/token, /auth/me
│   │   └── health.py      # /health
│   └── schemas/
│       └── auth.py
└── models/
    └── user.py            # User ORM + UserOperator
alembic/                   # migrations
tests/                     # pytest
```

## 快速開始

### 1. 用 Docker Compose（推薦）

```bash
docker compose up --build
```

啟動後：
- API：http://localhost:8000
- Swagger UI：http://localhost:8000/docs

`docker-compose.yml` 預設開啟 `AUTO_CREATE_TABLES=true`，第一次啟動會自動建立 `users` 表。

### 2. 本地開發

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# 編輯 .env，至少設定 DB_* 與 JWT_SECRET_KEY

# 啟動 Postgres（任一方式）
docker run --name fastapi-frame-pg -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=fastapi_frame \
  -p 5432:5432 -d postgres:16

# 建立資料表（dev 模式：用程式自動建）
# 或正式做法：alembic upgrade head（見下節）

uvicorn api.app:app --app-dir app --reload --port 8000
# 也可以：python app/main.py
```

## 環境變數

完整列表見 [.env.example](.env.example)。關鍵欄位：

| 變數 | 說明 | 預設 |
|---|---|---|
| `DB_HOST` / `DB_PORT` / `DB_NAME` / `DB_USER` / `DB_PASSWORD` | PostgreSQL 連線 | `127.0.0.1:5432` |
| `JWT_SECRET_KEY` | JWT 簽章密鑰，**正式環境務必更換** | `change-me-in-production` |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token 有效時間 | `1440` |
| `AUTO_CREATE_TABLES` | 啟動時是否自動 `create_all`（僅供開發） | `false` |
| `CORS_ORIGINS` | 允許的 CORS 來源（JSON list） | `["*"]` |
| `DEV` | reload 模式 | `false` |

env 檔載入順序：`APP_ENV_FILE` 環境變數 > `.env` > 指令列第一個參數。

## Alembic Migration

```bash
# 產生 migration（會比對 models 與 DB）
alembic revision --autogenerate -m "init users"

# 套用到最新版本
alembic upgrade head

# 回退一版
alembic downgrade -1
```

正式環境請關閉 `AUTO_CREATE_TABLES` 並改用 alembic。

## 認證流程

```bash
# 註冊
curl -X POST http://localhost:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice","email":"alice@example.com","password":"hunter2!!"}'

# 登入取得 token
curl -X POST http://localhost:8000/auth/token \
  -d 'username=alice&password=hunter2!!'

# 用 token 取得自己的資料
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## 新增功能的標準流程

1. 在 [app/models/](app/models/) 建立 SQLAlchemy model，依主鍵型式繼承 `core.base_model.UUIDBase`（uuid 主鍵）或 `IDBase`（自增整數主鍵），主鍵欄位由 base 提供，不需自行宣告；再建立對應 Operator（分別繼承 `UUIDOperator` 或 `IDOperator`）。直接繼承 `Base` 的 model 無法通過 `UUIDOperator`／`IDOperator` 的型別檢查。
   **並把新 model 匯出到 [app/models/\_\_init\_\_.py](app/models/__init__.py)** —— [alembic/env.py](alembic/env.py) 只靠 `import models` 收集 metadata，沒匯出的 model 不會進 `Base.metadata`，第 6 步的 autogenerate 會產生空的 migration。
2. 在 [app/api/schemas/](app/api/schemas/) 建立 Pydantic 請求/回應 model。
3. 在 [app/api/routers/](app/api/routers/) 建立 `APIRouter`，使用 `Depends(get_db)`、`Depends(get_current_user)`。
4. 在 [app/api/app.py](app/api/app.py) 的 `create_app` 裡 `include_router`。
5. 在 [tests/](tests/) 加測試，跑 `pytest`。
6. 產生 alembic migration 並 commit。

## 測試

```bash
pytest
```

`tests/conftest.py` 會把 `app/` 加到 `sys.path` 並注入測試用環境變數，DB 相關測試需另起測試資料庫或使用 fixture。

## 授權

見 [LICENSE](LICENSE)。
