# -*- coding: utf-8 -*-
import re

from fastapi import APIRouter, HTTPException, status

from app import schemas

router = APIRouter()


# API for ATC
@router.get("/meta")
async def router_meta():
    return {
        "name": "ActionInfo-WinPVT",
        "description": "Provide information between Action-WinPVT and ATC",
        "versions": "1.0.0",
    }


@router.post("/construct")
async def router_construct():
    return_body = {
        "schema": {
            "type": "object",
            "properties": {
                "platform_name": {"type": "string"},
                "milestone": {"type": "string"},
                "softpaq_id": {"type": "string"},
                "file_location": {"type": "string"},
            },
        }
    }
    return return_body


@router.post("/build")
async def router_build(req: schemas.ProviderInput):
    try:
        softpaq_list = re.findall(r"\d+", req.softpaq_id)
        softpaq_list = ["sp" + x for x in softpaq_list]
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide at least 1 softpaq_id, and split them with ',' if multiple.",
        )

    if req.file_location is not None:
        req.file_location = req.file_location.replace("/", "\\")
    else:
        req.file_location = "C:\\tmp"

    action_data = {
        "softpaq_list": softpaq_list,
        "remote_path": req.file_location,
    }
    return_body = {
        "message": "Successfully add SMR action",
        "showData": req,
        "action": {"name": "SMR", "version": "1.0", "data": action_data},
    }
    return return_body
