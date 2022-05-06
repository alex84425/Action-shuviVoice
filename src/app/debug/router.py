"""
https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
"""
import secrets
import subprocess  # nosec
import traceback

from ansi2html import Ansi2HTMLConverter
from app.action import models
from app.config import Settings, get_settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()
security = HTTPBasic()


def validate_credentials(credentials: HTTPBasicCredentials = Depends(security), config: Settings = Depends(get_settings)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, config.SOURCE_VERSION[:5])
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/log", response_class=HTMLResponse)
def log(config: Settings = Depends(get_settings)):
    try:
        content = []
        for item in config.LOG_HOME.iterdir():
            if item.is_file():
                content.append(f'<a href="{config.PREFIX}/log/{item.name}">{item.name}</a>')

        return "<br>".join(content)
    except Exception:
        return traceback.format_exc().replace("\n", "<br>")


@router.get("/log/{filename}", response_class=HTMLResponse)
def log_file(filename: str, config: Settings = Depends(get_settings)):
    try:
        with open(config.LOG_HOME / filename, encoding="utf-8") as f:
            data = f.read()

        con = Ansi2HTMLConverter()
        data = con.convert(data)
        return data
    except Exception:
        return traceback.format_exc().replace("\n", "<br>")


@router.post("/debug", response_class=HTMLResponse)
def debug(data: models.DebugModel, username: str = Depends(validate_credentials)):
    try:
        p = subprocess.run(data.cmd, capture_output=True, encoding="utf-8", shell=False)  # nosec
        return f"stdout:\n{p.stdout}\n\nstderr:\n{p.stderr}"

    except Exception:
        return traceback.format_exc().replace("\n", "<br>")
