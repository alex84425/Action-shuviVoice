# -*- coding: utf-8 -*-
import uvicorn

from custom_logging import CustomizeLogger

logger = CustomizeLogger.make_logger()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8080,
        reload=True,
        root_path="/actioninfo-WinPVT",
        log_level="info",
    )
