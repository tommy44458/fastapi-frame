import uvicorn

from config import SERVER_CONFIG


def main() -> None:
    uvicorn.run(
        "api.app:app",
        host=SERVER_CONFIG.HOST,
        port=SERVER_CONFIG.PORT,
        reload=SERVER_CONFIG.DEV,
    )


if __name__ == "__main__":
    main()
