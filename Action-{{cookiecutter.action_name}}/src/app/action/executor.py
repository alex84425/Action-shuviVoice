from app.action import models

ErrorTaskTable = dict()


async def monitor_task_error(workingDirectory: str):
    if workingDirectory in ErrorTaskTable.keys():
        return ErrorTaskTable.get(workingDirectory)
    else:
        return False


async def main_task_handler(act: models.MyActionPostModel):
    try:
        await main_task(act)
    except Exception as e:
        workingDirectory = act.context.workingDirectory
        ErrorTaskTable.update({workingDirectory: e})


async def main_task(act: models.MyActionPostModel):
    return True
