"""
https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
"""
import secrets
import subprocess  # nosec
import traceback

from ansi2html import Ansi2HTMLConverter
from app.config import Settings, get_settings
from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security.api_key import APIKeyHeader

router = APIRouter()
security = HTTPBasic()
api_key_header_auth = APIKeyHeader(
    name="X-API-KEY",
    description="API Token, required for debug",
    auto_error=True,
)


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


async def verify_api_key(api_key_header: str = Security(api_key_header_auth), config: Settings = Depends(get_settings)):
    correct_api_key = secrets.compare_digest(api_key_header, config.SOURCE_VERSION[::-1])
    if not correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )


@router.get("/log", response_class=HTMLResponse)
def log(config: Settings = Depends(get_settings)):
    try:
        content = []
        for item in config.LOG_HOME.iterdir():
            if item.is_file():
                content.append(f'<a href="{config.PREFIX}/log/{item.name}">{item.name}</a>')

        return "<br>".join(content)
    except Exception:
        return traceback.format_exc()


@router.get("/log/{filename}", response_class=HTMLResponse)
def log_file(filename: str, config: Settings = Depends(get_settings)):
    try:
        with open(config.LOG_HOME / filename, encoding="utf-8") as f:
            data = f.read()

        con = Ansi2HTMLConverter()
        data = con.convert(data)
        return data
    except Exception:
        return traceback.format_exc()


@router.post("/debug", response_class=HTMLResponse)
async def debug(cmd: str = "", username: str = Depends(validate_credentials)):
    try:
        p = subprocess.run(cmd, capture_output=True, encoding="utf-8", shell=True)  # nosec
        return f"stdout:\n{p.stdout}\n\nstderr:\n{p.stderr}"

    except Exception:
        return traceback.format_exc()


@router.post("/debug2", response_class=HTMLResponse, dependencies=[Depends(verify_api_key)])
async def debug2(cmd: str = ""):
    try:
        p = subprocess.run(cmd, capture_output=True, encoding="utf-8", shell=True)  # nosec
        return f"stdout:\n{p.stdout}\n\nstderr:\n{p.stderr}"

    except Exception:
        return traceback.format_exc()


@router.get("/taskid/{taskid}", response_class=HTMLResponse)
def taskid_log(taskid: str, config: Settings = Depends(get_settings)):
    try:
        content = []
        logs = []
        for item in config.LOG_HOME.iterdir():
            if item.is_file() and item.name != "uut_proxy.log":
                logs.append(item)
        sorted(logs, key=lambda x: x.stat().st_mtime, reverse=True)

        for log in logs:
            with open(log) as f:
                lines = f.read().splitlines()
            for line in lines:
                if f"[{taskid}]" in line:
                    content.append(line)

        con = Ansi2HTMLConverter()
        return con.convert("\n".join(content))
    except Exception:
        return traceback.format_exc()
