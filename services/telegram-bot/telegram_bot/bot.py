from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import os


class BotHandler:
    def __init__(self) -> None:
        self.updater = Updater(os.getenv("TELEGRAM_API_KEY"))
        self._add_handlers()

    def _add_handlers(self) -> None:
        self.updater.dispatcher.add_handler(
            CommandHandler("start", self._start_command)
        )

    def _start_command(self, update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
        )

    def run(self) -> None:
        self.updater.start_polling()

    def send_message(self, to: str, text: str) -> None:
        return self.updater.bot.send_message(to, text=text)


class Bot:
    def __init__(self) -> None:
        self.handler = BotHandler(self.updater)

    def run(self) -> None:
        self.handler.run()

    def send_message(self, to: str, text: str):
        self.handler.send_message(to, text=text)
