from app.action import models
from vcosmosapiclient.depends import ApiDepends

ErrorTaskTable = dict()


async def monitor_task_error(workingDirectory: str):
    if workingDirectory in ErrorTaskTable:
        return ErrorTaskTable.get(workingDirectory, False)
    else:
        return False


async def main_task_handler(act: models.MyActionPostModel, api: ApiDepends):
    try:
        return await main_task(act, api)
    except Exception as e:
        workingDirectory = act.context.workingDirectory
        ErrorTaskTable.update({workingDirectory: e})


async def main_task(act: models.MyActionPostModel, api: ApiDepends):
    bios = await api.bios.get_bios_on_remote(act)
    return bios
