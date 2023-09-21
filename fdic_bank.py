from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
import requests as rq
import json

class Parameters(BaseModel):
    filters: str
    fields: str
    limit: str
    offset: str


class Index(BaseModel):
    name: str
    create_timestamp: str = Field(..., alias='createTimestamp')


class Meta(BaseModel):
    total: int
    parameters: Parameters
    index: Index


class Data(BaseModel):
    cert: int = Field(..., alias='CERT')
    name: str = Field(..., alias='NAME')
    id: str = Field(..., alias='ID')


class BankData(BaseModel):
    data: Data
    score: int


class Totals(BaseModel):
    count: int


class BankInformation(BaseModel):
    meta: Optional[Meta] = None
    data: Optional[List[BankData]] = None
    totals: Optional[Totals] = None



