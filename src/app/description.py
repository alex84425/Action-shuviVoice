from datetime import datetime, timedelta, timezone

import vcosmosapiclient

from app.config import get_settings

config = get_settings()

DESCRIPTION = f"""
    service: {config.PROJECT_NAME}
    version: {config.VERSION}
    history: {list(config.HISTORY.values())[0]}
    commit id: {config.SOURCE_VERSION}
    lib version: {vcosmosapiclient.VERSION}
    lib history: {list(vcosmosapiclient.HISTORY.values())[0]}
    deployed time: {datetime.now(timezone(timedelta(hours=+8))).ctime()}
    """

DESCRIPTION_DICT = {
    "service": config.PROJECT_NAME,
    "version": config.VERSION,
    "commit id": config.SOURCE_VERSION,
    "lib version": vcosmosapiclient.VERSION,
    "deployed time": datetime.now(timezone(timedelta(hours=+8))).ctime(),
}
