from typing import Optional
from pydantic import BaseModel


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
