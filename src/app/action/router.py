"""This module contains some mandatory endpoints.

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""

import logging
import subprocess, re
from fastapi import APIRouter, HTTPException, status
from vcosmosapiclient import errors
from vcosmosapiclient.api_proxy import execute_ps1_on_remote
from vcosmosapiclient.custom_logging import log_wrapper
from vcosmosapiclient.utils import validator

from app.action import executor, models

router = APIRouter()


def remove_between_double_asterisks(input_str):
    stack = []
    result = []

    for char in input_str:
        if char == "*":
            if stack and stack[-1] == "*":
                stack.pop()  # Remove the previous '*'
            else:
                stack.append(char)
        else:
            if not stack or stack[-1] != "*":
                result.append(char)

    return "".join(result)


@router.post("/vit")
@log_wrapper
async def vit(Text: str):
    try:
        # こんにちわ

        # Text = re.sub(r"\*\*.*?\*\*", "", Text)
        # Text = remove_between_double_asterisks(Text)
        Text = Text.replace("\n", " ")
        Text = Text.replace("\r", " ")
        print(f"{Text=}")
        process = subprocess.run(f"python /app/VITS-fast-fine-tuning/VC_inference_api.py --input_text '{Text}' ", shell=True)

        return {"process.stdout": process.stdout, "process.stderr": process.stderr}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot Start, because of an error {exc}, try again.",
        ) from exc
