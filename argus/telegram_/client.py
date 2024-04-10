from typing import Union

import telegram

from argus.logger import logger
from argus.telegram_.messages import NewListingMessage, ErrorMessage

Message = Union[NewListingMessage, ErrorMessage]


class TelegramClient:
    def __init__(self, token: str):
        self.token = token
        self.bot = telegram.Bot(token=self.token)
        self.logger = logger

    async def send(self, message: Message, chat_id: int) -> None:
        try:
            logger.info(f"Sending message to chat {chat_id}")
            await self.bot.send_message(chat_id, message.text, parse_mode="MarkdownV2")
        except Exception as e:
            logger.error(f"Error while sending message: {str(e)}")
            raise e
