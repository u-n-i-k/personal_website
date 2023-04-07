import re
from datetime import date
from typing import Any

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from personal_website.core import constants as cst
from personal_website.core import utils as ut
from personal_website.db.orm.base import Base, Json


@declared_attr.directive
def __tablename__(cls: Any) -> None:
    return None


class CompanyLocalization(Base):
    _repr_attrs: list[str] = ["company_id", "lang"]
    company_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("company.id"),
        primary_key=True,
        index=True,
    )
    lang: Mapped[str] = mapped_column(sa.String(10), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(sa.String(50), nullable=False)


class Company(Base):
    """base class for all localized companies"""

    _lang: str = ""
    _repr_attrs: list[str] = ["id", "website"]
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    website: Mapped[str] = mapped_column(sa.String(50), nullable=True)

    @property
    def localization(self) -> CompanyLocalization:
        raise NotImplementedError

    @property
    def name(self) -> str | None:
        return self.localization.name if self.localization else None


@declared_attr
def company_localization(cls: Company) -> Mapped[CompanyLocalization]:
    return relationship(
        CompanyLocalization,
        primaryjoin=(
            (CompanyLocalization.company_id == cls.id)
            & (CompanyLocalization.lang == cls._lang)
        ),
        uselist=False,
        lazy="joined",
    )


localized_companies: dict = {}

for lang in cst.SUPPORTED_LOCALES:
    if lang in localized_companies:
        raise RuntimeError("lang collisions occured")

    lang_camel_case = ut.string_to_camel_case(lang)
    localized_class = type(
        f"{lang_camel_case}{Company.__name__}",
        (Company,),
        {
            "_lang": lang,
            "__tablename__": None,
            "localization": company_localization,
        },
    )
    localized_companies[lang] = localized_class


class WorkExperienceLocalization(Base):
    _repr_attrs: list[str] = ["work_experience_id", "lang"]
    work_experience_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("work_experience.id"), primary_key=True, index=True
    )
    lang: Mapped[str] = mapped_column(sa.String(10), primary_key=True, index=True)
    position: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    job_description: Mapped[str] = mapped_column(sa.String(500), nullable=False)


class WorkExperience(Base):
    """base class for all localized work experiences"""

    _lang = ""
    _repr_attrs: list[str] = ["id", "company_id", "start_dt", "finish_dt"]
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(
        sa.Integer, sa.ForeignKey("company.id"), nullable=False
    )
    start_dt: Mapped[date] = mapped_column(sa.Date, nullable=False)
    finish_dt: Mapped[date] = mapped_column(sa.Date, nullable=True)
    technologies: Mapped[list[str]] = mapped_column(Json, nullable=False)

    @property
    def localization(self) -> WorkExperienceLocalization:
        raise NotImplementedError

    @property
    def position(self) -> str | None:
        return self.localization.position if self.localization else None

    @property
    def job_description(self) -> str | None:
        return self.localization.job_description if self.localization else None


@declared_attr
def company(cls: WorkExperience) -> Mapped[Company]:
    return relationship(
        localized_companies[cls._lang],
        uselist=False,
        lazy="joined",
    )


@declared_attr
def work_experience_localization(
    cls: WorkExperience,
) -> Mapped[WorkExperienceLocalization]:
    return relationship(
        WorkExperienceLocalization,
        primaryjoin=(
            (WorkExperienceLocalization.work_experience_id == cls.id)
            & (WorkExperienceLocalization.lang == cls._lang)
        ),
        uselist=False,
        lazy="joined",
    )


localized_work_experiences: dict = {"": WorkExperience}
for lang in cst.SUPPORTED_LOCALES:
    if lang in localized_work_experiences:
        raise RuntimeError("lang collisions occured")

    lang_camel_case = ut.string_to_camel_case(lang)
    localized_class = type(
        f"{lang_camel_case}WorkExperience",
        (WorkExperience,),
        {
            "_lang": lang,
            "__tablename__": None,
            "company": company,
            "localization": work_experience_localization,
        },
    )
    localized_work_experiences[lang] = localized_class


class AboutMe(Base):
    lang: Mapped[int] = mapped_column(sa.String(10), primary_key=True, index=True)
    about: Mapped[str] = mapped_column(sa.String(4000), nullable=False)


class ContactRequest(Base):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    message: Mapped[str] = mapped_column(sa.String(4000), nullable=False)
    dt: Mapped[date] = mapped_column(
        sa.Date, server_default=sa.text("CURRENT_TIMESTAMP")
    )

    @property
    def tg_message(self) -> str:
        return f"{self.dt}: Contact request from {self.email}:\n{self.message}"
