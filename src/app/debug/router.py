"""
https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
"""
import logging
import re
import secrets
import subprocess  # nosec
import tempfile
import traceback

from ansi2html import Ansi2HTMLConverter
from fastapi import APIRouter, Depends, File, HTTPException, Security, UploadFile, status
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader

from app.config import Settings, get_settings

router = APIRouter()
settings: Settings = get_settings()
api_key_header_auth = APIKeyHeader(
    name="X-API-KEY",
    description="API Token, required for debug",
    auto_error=True,
)


async def verify_api_key(api_key_header: str = Security(api_key_header_auth)):
    correct_api_key = secrets.compare_digest(api_key_header, settings.SOURCE_VERSION[::-1])
    if not correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )


TAIREGEX = re.compile(r"^(@[0-9a-f]{24})", re.IGNORECASE)


def replace_tai64n_to_local(link_name: str) -> str:
    if re.match(TAIREGEX, link_name):
        try:
            proc = subprocess.run(f"echo {link_name} | tai64nlocal", shell=True, capture_output=True, text=True, check=True)  # nosec: B602
            link_name = proc.stdout.strip()
        except Exception:
            logging.error("Failed to replace tai64n")
    return link_name


@router.get("/log", response_class=HTMLResponse)
def router_log():
    try:
        content = []
        for item in settings.LOG_FOLDER.iterdir():
            if item.is_file():
                link_name = replace_tai64n_to_local(item.name)
                content.append(f'<a href="./log/{item.name}">{link_name}</a>')

        return "<br>".join(content)
    except Exception:
        return traceback.format_exc()


@router.get("/log/{filename}", response_class=HTMLResponse)
def log_file(filename: str):
    try:
        with open(settings.LOG_FOLDER / filename, encoding="utf-8") as f:
            data = f.read()

        con = Ansi2HTMLConverter()
        data = con.convert(data)
        return data
    except Exception:
        return traceback.format_exc()


@router.post("/debug", response_class=HTMLResponse, dependencies=[Depends(verify_api_key)])
async def debug(cmd: str = ""):
    try:
        p = subprocess.run(cmd, capture_output=True, encoding="utf-8", shell=True, check=True)  # nosec
        return f"stdout:\n{p.stdout}\n\nstderr:\n{p.stderr}"
    except Exception:
        return traceback.format_exc()


@router.get("/taskid/{taskid}", response_class=HTMLResponse)
def taskid_log(taskid: str):
    """
    # Example:
    If workingDirectory is `c:/TestAutomation/TestJobs/6260f5a1c99ce10012a6eb79/00_Action`

    Then the url is `/taskid/6eb79_00`
    """
    try:
        content = []
        logs = []
        for item in settings.LOG_FOLDER.iterdir():
            if item.is_file() and item.name != "uut_proxy.log":
                logs.append(item)
        sorted(logs, key=lambda x: x.stat().st_mtime, reverse=True)

        for log in logs:
            with open(log, encoding="utf-8") as f:
                lines = f.read().splitlines()
            for line in lines:
                if f"[{taskid}]" in line:
                    content.append(line)

        con = Ansi2HTMLConverter()
        return con.convert("\n".join(content))
    except Exception:
        return traceback.format_exc()


@router.post("/upload", description="upload something to executor", dependencies=[Depends(verify_api_key)])
def upload(file: UploadFile = File(...)):
    with tempfile.TemporaryFile() as tmp:
        tmp.write(file.file.read())
    return {"result": "uploaded"}
