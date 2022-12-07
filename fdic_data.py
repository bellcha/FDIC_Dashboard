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
    eqccompi: Optional[int] = Field(..., alias='EQCCOMPI')
    repdte: Optional[str] = Field(..., alias='REPDTE')
    asset: int = Field(..., alias='ASSET')
    eeffqr: Optional[float] = Field(..., alias='EEFFQR')
    roaq: float = Field(..., alias='ROAQ')
    netinc: int = Field(..., alias='NETINC')
    eq: Optional[int] = Field(..., alias='EQ')
    lnlsnet: int = Field(..., alias='LNLSNET')
    dep: int = Field(..., alias='DEP')
    roeq: float = Field(..., alias='ROEQ')
    id: str = Field(..., alias='ID')


class Datum(BaseModel):
    data: Data
    score: int


class Totals(BaseModel):
    count: int


class BankData(BaseModel):
    meta: Meta
    data: List[Datum]
    totals: Totals
