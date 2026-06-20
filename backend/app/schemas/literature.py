from pydantic import BaseModel


class TimelineEventOut(BaseModel):
    id: int
    year: str
    grade: str
    award: str
    result: str

    model_config = {"from_attributes": True}


class TimelineEventIn(BaseModel):
    year: str
    grade: str
    award: str
    result: str


class LiteratureWorkOut(BaseModel):
    id: int
    title: str
    year: str
    award: str
    category: str
    excerpt: str
    fullText: str

    model_config = {"from_attributes": True, "populate_by_name": True}

    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "full_text"):
            data = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
            data["fullText"] = data.pop("full_text")
            return cls(**data)
        return super().model_validate(obj, **kwargs)


class LiteratureWorkIn(BaseModel):
    title: str
    year: str
    award: str
    category: str
    excerpt: str
    fullText: str
