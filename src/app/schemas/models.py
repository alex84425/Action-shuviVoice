# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel


class Platform(BaseModel):
    platform_name: str
    milestone: Optional[str]


class ProviderInput(BaseModel):
    platform_name: Optional[str]
    milestone: Optional[str]
    softpaq_id: Optional[str]
    file_location: Optional[str]


class ProviderConstruct(BaseModel):
    body: ProviderInput
