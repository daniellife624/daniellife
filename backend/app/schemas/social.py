from typing import Optional
from pydantic import BaseModel


class SocialActivityOut(BaseModel):
    id: int
    title: str
    org: str
    role: str
    period: str
    category: str
    sdgTag: Optional[str] = None
    description: str

    model_config = {"from_attributes": True, "populate_by_name": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "sdg_tag"):
            data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            data["sdgTag"] = data.pop("sdg_tag", None)
            return cls(**data)
        return super().model_validate(obj, **kwargs)


class SocialActivityIn(BaseModel):
    title: str
    org: str
    role: str
    period: str
    category: str
    sdgTag: Optional[str] = None
    description: str
