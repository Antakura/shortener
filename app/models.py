from pydantic import computed_field, field_validator, HttpUrl
from sqlmodel import Field, SQLModel

from app.config import encryptor, get_settings


class UrlBase(SQLModel):
    full_url: str = Field(...)


class Url(UrlBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UrlPublic(UrlBase):
    id: int

    @computed_field
    @property
    def short_code(self) -> str:
        return encryptor.encode(self.id)

    @computed_field
    @property
    def short_url(self) -> str:
        return f"{get_settings().BASE_URL}/url/{self.short_code}"


class UrlCreate(UrlBase):
    full_url: str

    @field_validator('full_url', mode="before")
    @classmethod
    def validate_full_url(cls, url_value):
        validated_url = HttpUrl(url_value)
        return str(validated_url)
