from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

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


class Datum(BaseModel):
    data: Data
    score: int


class Totals(BaseModel):
    count: int


class Model(BaseModel):
    meta: Optional[Meta] = None
    data: Optional[List[Datum]] = None
    totals: Optional[Totals] = None