import datetime

from pydantic import BaseModel, Field, validator

from personal_website.core import utils as ut


class CompanySchema(BaseModel):
    name: str
    website: str

    class Config:
        orm_mode = True


class WorkExperienceSchema(BaseModel):
    company: CompanySchema
    position: str
    job_description: str
    start_dt: str
    finish_dt: str | None
    technologies: list[str]

    @validator("start_dt", pre=True)
    def format_start_dt(cls, start_dt: datetime.date) -> str:
        return ut.check_and_format_date_for_work_exp(start_dt)

    @validator("finish_dt", pre=True)
    def format_finish_dt(cls, finish_dt: datetime.date) -> str | None:
        if finish_dt is None:
            return None
        return ut.check_and_format_date_for_work_exp(finish_dt)

    class Config:
        orm_mode = True


class WorkHistorySchema(BaseModel):
    history: list[WorkExperienceSchema]

    class Config:
        orm_mode = True
