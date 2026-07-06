import re
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator


_DATE_RE = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$')
_ESG_TYPES = {'Environmental', 'Social', 'Governance'}


class PhotoItem(BaseModel):
    url: str
    position: str = "50% 50%"


class PhotoPositionIn(BaseModel):
    url: str
    position: str

    @field_validator('position')
    @classmethod
    def position_format(cls, v: str) -> str:
        parts = v.strip().split()
        if len(parts) != 2 or not all(p.endswith('%') for p in parts):
            raise ValueError('「照片位置」格式須為 "X% Y%"，例如 "50% 50%"')
        return v.strip()


class SocialActivityOut(BaseModel):
    id: int
    name: str
    organization: str
    esgType: Optional[str] = None
    sdgNumbers: list[int] = []
    periodFrom: str
    periodTo: Optional[str] = None
    reflection: str = ""
    youtubeUrl: Optional[str] = None
    photos: list[PhotoItem] = []


class SocialActivityIn(BaseModel):
    name: str
    organization: str
    esgType: Optional[str] = None
    sdgNumbers: list[int] = []
    periodFrom: str           # ISO "YYYY-MM-DD"
    periodTo: Optional[str] = None
    reflection: str = ""
    youtubeUrl: Optional[str] = None
    photos: list[PhotoItem] = []   # 未直接使用，多張照片透過專用端點管理（與 experiences 一致）

    @field_validator('name', 'organization', 'reflection')
    @classmethod
    def not_empty(cls, v: str, info) -> str:
        if not v.strip():
            raise ValueError(f'「{info.field_name}」不可空白')
        return v

    @field_validator('esgType')
    @classmethod
    def esg_choices(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in _ESG_TYPES:
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

    @model_validator(mode='after')
    def exactly_one_classification(self):
        has_esg = bool(self.esgType)
        has_sdg = bool(self.sdgNumbers)
        if has_esg and has_sdg:
            raise ValueError('「ESG 類型」與「SDG 號碼」只能擇一分類，不能同時填寫')
        if not has_esg and not has_sdg:
            raise ValueError('請選擇「ESG 類型」或「SDG 號碼」其中一種分類方式')
        return self

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
