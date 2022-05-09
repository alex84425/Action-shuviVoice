from app.action import models


async def main_task(act: models.MyActionPostModel, *args, **kwargs):
    """
        Usage asyncio.create_task(executor.main_task(act, ...))
    """
    raise NotImplementedError("Add your code here")
