"""create tables

Revision ID: 25d1105a1c62
Revises:
Create Date: 2023-11-25 19:13:21.680499

"""
import datetime

import sqlalchemy as sa
from alembic import op

import personal_website

# revision identifiers, used by Alembic.
revision = "25d1105a1c62"
down_revision = None
branch_labels = None
depends_on = None


def insert_data() -> None:
    op.bulk_insert(
        personal_website.db.orm.common.Company.__table__,  # type: ignore
        [
            {"website": "https://sbertech.ru/"},
            {"website": "https://yandex.ru/company/"},
        ],
    )

    op.bulk_insert(
        personal_website.db.orm.common.CompanyLocalization.__table__,  # type: ignore
        [
            {"company_id": 1, "lang": "ru", "name": "АО «Сбертех»"},
            {"company_id": 1, "lang": "en", "name": "Sbertech"},
            {"company_id": 2, "lang": "ru", "name": "ООО «Яндекс»"},
            {"company_id": 2, "lang": "en", "name": "Yandex"},
        ],
    )

    op.bulk_insert(
        personal_website.db.orm.common.WorkExperience.__table__,  # type: ignore
        [
            {
                "company_id": 1,
                "start_dt": datetime.date(2018, 5, 1),
                "finish_dt": datetime.date(2021, 3, 31),
                "technologies": [
                    "C/C++",
                    "nginx",
                    "Ansible",
                    "docker",
                    "Jenkins",
                    "perl",
                    "Groovy",
                ],
            },
            {
                "company_id": 2,
                "start_dt": datetime.date(2021, 4, 1),
                "finish_dt": None,
                "technologies": [
                    "python2.7",
                    "python3.10",
                    "Oracle SQL",
                    "sqlalchemy",
                    "docker",
                    "nginx",
                ],
            },
        ],
    )

    op.bulk_insert(
        personal_website.db.orm.common.WorkExperienceLocalization.__table__,  # type: ignore
        [
            {
                "work_experience_id": 1,
                "lang": "ru",
                "position": "IT-инженер",
                "job_description": "Интеграция системы логирования Nginx в ClickHouse. Разработка и поддержка CI/CD для всех продуктов команды в Jenkins и Ansible. Доработка фреймворка для тестирования Nginx под нужды команды и написание тестов. Проведение нагрузочных тестирований для сравнения продукта с аналогами.",
            },
            {
                "work_experience_id": 1,
                "lang": "en",
                "position": "Software Development Engineer",
                "job_description": "Integration of Nginx logging system into ClickHouse. CI/CD development and support for all team products in Jenkins and Ansible. Finalizing the Nginx testing framework for the needs of the team and writing tests. Carrying out load testing to compare the product with analogues.",
            },
            {
                "work_experience_id": 2,
                "lang": "ru",
                "position": "Backend-разработчик в команде ядра Биллинга",
                "job_description": "Проектирование и разработка функционала для подписания договоров с помощью ЭЦП. Интеграции с сервисами для асинхронного пробития фискальных чеков. Доработки в API для личного кабинета пользователя сервиса. Поиск и исправление уязвимостей. Курирование новых сотрудников. Сопровождение проектов.",
            },
            {
                "work_experience_id": 2,
                "lang": "en",
                "position": "Billing Core Backend Developer",
                "job_description": "Designing and implementing functionality of contracts electronic signature. Integration with services for asynchronous creation of fiscal receipts. Improvements to the API for the service user's personal account. Finding and fixing vulnerabilities. Mentoring new employees. Managing projects.",
            },
        ],
    )

    op.bulk_insert(
        personal_website.db.orm.common.AboutMe.__table__,  # type: ignore
        [
            {
                "lang": "ru",
                "about": (
                    "Привет! Я Никита, и я люблю программировать. Имею опыт разработки и поддержки высоконагруженных приложений. "
                    "Занимался как организацией инфраструктуры, так и реализацией бизнес-логики, принимал участие в организации CI/CD, систем мониторинга и оповещения, оптимизировал производительность и рефакторил легаси код. "
                    "Мне нравится разбираться с нетривиальными проблемами, а также помогать товарищам по команде. "
                    "Окончил НИЯУ МИФИ по специальности 10.05.04 Информационно-аналитические системы безопасности со средним баллом 4.7"
                ),
            },
            {
                "lang": "en",
                "about": (
                    "Hi! My name is Nikita and I am a passionate software developer having a great experience in the development and support of data-intensive applications. "
                    "Experienced in implementing both technical anb business logic, took part in organizing CI/CD, monitoring and alerting systems, optimizing performance and refactoring legacy code. "
                    "I am a team player - like to help my teammates and share my knowledge with others and also really love solve complex problems. "
                    "Graduated from NRNU MEPhI with a specialist degree in Information and Analytical security systems (average grade - 4.7 / 5)"
                ),
            },
        ],
    )


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "about_me",
        sa.Column("lang", sa.String(length=10), nullable=False),
        sa.Column("about", sa.String(length=4000), nullable=False),
        sa.PrimaryKeyConstraint("lang"),
    )
    op.create_index(op.f("ix_about_me_lang"), "about_me", ["lang"], unique=False)
    op.create_table(
        "company",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("website", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_company_id"), "company", ["id"], unique=False)
    op.create_table(
        "company_localization",
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("lang", sa.String(length=10), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.id"],
        ),
        sa.PrimaryKeyConstraint("company_id", "lang"),
    )
    op.create_index(
        op.f("ix_company_localization_company_id"),
        "company_localization",
        ["company_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_company_localization_lang"),
        "company_localization",
        ["lang"],
        unique=False,
    )
    op.create_table(
        "work_experience",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("start_dt", sa.Date(), nullable=False),
        sa.Column("finish_dt", sa.Date(), nullable=True),
        sa.Column("technologies", personal_website.db.orm.base.Json(), nullable=False),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_work_experience_id"), "work_experience", ["id"], unique=False
    )
    op.create_table(
        "work_experience_localization",
        sa.Column("work_experience_id", sa.Integer(), nullable=False),
        sa.Column("lang", sa.String(length=10), nullable=False),
        sa.Column("position", sa.String(length=100), nullable=False),
        sa.Column("job_description", sa.String(length=500), nullable=False),
        sa.ForeignKeyConstraint(
            ["work_experience_id"],
            ["work_experience.id"],
        ),
        sa.PrimaryKeyConstraint("work_experience_id", "lang"),
    )
    op.create_index(
        op.f("ix_work_experience_localization_lang"),
        "work_experience_localization",
        ["lang"],
        unique=False,
    )
    op.create_index(
        op.f("ix_work_experience_localization_work_experience_id"),
        "work_experience_localization",
        ["work_experience_id"],
        unique=False,
    )
    op.create_table(
        "contact_request",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("message", sa.String(length=4000), nullable=False),
        sa.Column(
            "dt", sa.Date(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_contact_request_id"), "contact_request", ["id"], unique=False
    )

    insert_data()
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_work_experience_localization_work_experience_id"),
        table_name="work_experience_localization",
    )
    op.drop_index(
        op.f("ix_work_experience_localization_lang"),
        table_name="work_experience_localization",
    )
    op.drop_table("work_experience_localization")
    op.drop_index(op.f("ix_work_experience_id"), table_name="work_experience")
    op.drop_table("work_experience")
    op.drop_index(
        op.f("ix_company_localization_lang"), table_name="company_localization"
    )
    op.drop_index(
        op.f("ix_company_localization_company_id"),
        table_name="company_localization",
    )
    op.drop_table("company_localization")
    op.drop_index(op.f("ix_company_id"), table_name="company")
    op.drop_table("company")
    op.drop_index(op.f("ix_about_me_lang"), table_name="about_me")
    op.drop_table("about_me")
    op.drop_index(op.f("ix_contact_request_id"), table_name="contact_request")
    op.drop_table("contact_request")
    # ### end Alembic commands ###
