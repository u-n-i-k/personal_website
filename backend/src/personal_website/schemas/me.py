import datetime

from pydantic import BaseModel, Field, validator

from personal_website.core import utils as ut


class ContactMeParamsSchema(BaseModel):
    email: str
    message: str
    recaptcha_token: str


class AboutMeSchema(BaseModel):
    about: str

    class Config:
        orm_mode = True
