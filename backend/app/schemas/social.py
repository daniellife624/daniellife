import re
from typing import Optional
from pydantic import BaseModel, field_validator


_DATE_RE = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$')
_ESG_TYPES = {'Environmental', 'Social', 'Governance'}


class SocialActivityOut(BaseModel):
    id: int
    name: str
    organization: str
    esgType: str
    sdgNumbers: list[int] = []
    periodFrom: str
    periodTo: Optional[str] = None
    contribution: str
    reflection: str = ""
    photoUrl: Optional[str] = None


class SocialActivityIn(BaseModel):
    name: str
    organization: str
    esgType: str
    sdgNumbers: list[int] = []
    periodFrom: str           # ISO "YYYY-MM-DD"
    periodTo: Optional[str] = None
    contribution: str
    reflection: str = ""
    photoUrl: Optional[str] = None

    @field_validator('name', 'organization', 'contribution')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('esgType')
    @classmethod
    def esg_choices(cls, v: str) -> str:
        if v not in _ESG_TYPES:
            raise ValueError('「ESG 類型」須為 Environmental / Social / Governance')
        return v

    @field_validator('sdgNumbers', mode='before')
    @classmethod
    def sdg_range(cls, v) -> list:
        nums = v if isinstance(v, list) else []
        for n in nums:
            if not (1 <= int(n) <= 17):
                raise ValueError('「SDG 號碼」每個值須介於 1 到 17')
        return nums

    @field_validator('periodFrom')
    @classmethod
    def period_from_format(cls, v: str) -> str:
        if not _DATE_RE.match(v.strip()):
            raise ValueError('「開始日期」格式須為 YYYY-MM-DD')
        return v.strip()

    @field_validator('periodTo')
    @classmethod
    def period_to_format(cls, v: Optional[str]) -> Optional[str]:
        if v and not _DATE_RE.match(v.strip()):
            raise ValueError('「結束日期」格式須為 YYYY-MM-DD')
        return v.strip() if v else None
