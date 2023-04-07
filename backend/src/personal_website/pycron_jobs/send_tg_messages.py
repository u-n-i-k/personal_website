import asyncio

import sqlalchemy as sa
import telebot
from sqlalchemy.pool import NullPool

from personal_website.core import constants as cst
from personal_website.core.config import Config
from personal_website.core.utils import PyCronJob
from personal_website.db.dbhelper import DBHelper
from personal_website.db.orm.common import ContactRequest


class TelegramMessagesSender(PyCronJob):
    def __init__(self, crontab: str, timeout: int | None = None):
        token = Config.instance.tg_sender.bot_token
        self.bot = telebot.TeleBot(token.get_secret_value())
        self.chat_id = Config.instance.tg_sender.notification_chat_id
        db_conn_config = Config.instance.db_conn
        self.dbhelper = DBHelper(
            sqlalchemy_async_database_uri=db_conn_config.sqlalchemy_async_database_uri,
            dbschema=db_conn_config.dbschema,
            poolclass=NullPool,
            echo=True,
        )
        return super().__init__(crontab, timeout)

    def safely_send_possibly_long_tg_message(self, msg: str) -> None:
        for x in range(0, len(msg), cst.TELEGRAM_MAX_MESSAGE_LEN):
            self.bot.send_message(
                self.chat_id, msg[x : x + cst.TELEGRAM_MAX_MESSAGE_LEN]
            )

    async def send_messages(self) -> None:
        async with self.dbhelper.create_async_session() as session, session.begin():
            contact_requests = (await session.scalars(sa.select(ContactRequest))).all()
            msg = "\n\n".join([req.tg_message for req in contact_requests])
            if msg:
                self.safely_send_possibly_long_tg_message(msg)
                delete_stmt = sa.delete(ContactRequest).where(
                    ContactRequest.id.in_([req.id for req in contact_requests])
                )
                await session.execute(delete_stmt)

    def do_job(self) -> None:
        asyncio.run(self.send_messages())
