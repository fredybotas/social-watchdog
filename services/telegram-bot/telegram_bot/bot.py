from .watchable_service import LimitExceededError, NotFoundError, WatchableService
from telegram_bot.watchable_service import InvalidProcessingTypeError
from liblog import get_logger
from telegram.ext import Updater
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackContext, CommandHandler
import os


logger = get_logger(__name__)


class BotHandler:
    def __init__(self, watchable_service: WatchableService) -> None:
        self.watchable_service = watchable_service
        self.updater = Updater(os.getenv("TELEGRAM_API_KEY"))
        self._add_handlers()

    def _add_handlers(self) -> None:
        self.updater.dispatcher.add_handler(
            CommandHandler("start", self._start_command)
        )
        self.updater.dispatcher.add_handler(CommandHandler("list", self._list_command))
        self.updater.dispatcher.add_handler(CommandHandler("add", self._add_command))
        self.updater.dispatcher.add_handler(
            CommandHandler("remove", self._remove_command)
        )

    def _start_command(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            """I'm Reddit watchdog bot! Start by typing one of command: list, add, remove.
            """,
        )

    def _list_command(self, update: Update, context: CallbackContext):
        try:
            watchables = self.watchable_service.get_all_watchables_for_user(
                str(update.effective_user.id)
            )
            watchables = [
                str((str(w.id), w.subreddit, w.processor_type.value, w.watch))
                for w in watchables
            ]
            update.message.reply_text(
                "Your watchlist:\n{}".format("\n".join(watchables)),
            )
        except Exception as e:
            logger.error(e)
            update.message.reply_text("Error occured. Please try again")

    def _remove_command(self, update: Update, context: CallbackContext):
        try:
            self.watchable_service.remove_watchable(
                str(update.effective_user.id), update.message.text.split(" ")[1]
            )
            update.message.reply_text("Watchable sucessfully removed!")
        except NotFoundError:
            update.message.reply_text(
                "Watchable was not found! Please provide correct id"
            )
        except Exception as e:
            logger.error(e)
            update.message.reply_text("Error occured. Please try again")

    def _add_command(self, update: Update, context: CallbackContext):
        try:
            subreddit = update.message.text.split(" ")[1]
            processing_type = update.message.text.split(" ")[2]
            watch = " ".join(update.message.text.split(" ")[3:])
            self.watchable_service.add_watchable(
                provider_user_id=str(update.message.from_user.id),
                effective_chat_id=str(update.effective_chat.id),
                subreddit=subreddit,
                processing_type=processing_type,
                watch=watch,
            )
            update.message.reply_text("Watchable sucessfully added!")
            logger.info("User added watchable")
        except LimitExceededError:
            update.message.reply_text(
                """You have exceeded limit for your watchables.\nPlease buy premium or remove some current watchables."""
            )
        except InvalidProcessingTypeError:
            update.message.reply_text("""Invalid processing type.""")
        except Exception as e:
            logger.error(e)
            update.message.reply_text("Error occured. Please try again")

    def run(self) -> None:
        self.updater.start_polling()

    def send_message(self, to: str, text: str):
        logger.info(f"Sending message to {to}: {text}")
        try:
            self.updater.bot.send_message(to, text=text)
        except TelegramError as e:
            logger.error(e)


class Bot:
    def __init__(self, watchable_service: WatchableService) -> None:
        self.handler = BotHandler(watchable_service=watchable_service)

    def run(self) -> None:
        self.handler.run()

    def send_message(self, to: str, text: str):
        self.handler.send_message(to, text=text)
