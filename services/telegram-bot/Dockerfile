FROM python:3.10.0-slim

COPY lib/liblog/dist/*.whl ./
COPY lib/libmq/dist/*.whl ./
COPY lib/libcore/dist/*.whl ./
RUN pip install *.whl && rm -rf *.whl

COPY services/telegram-bot/dist/*.whl ./
RUN pip install *.whl && rm -rf *.whl

CMD ["python", "-m", "telegram_bot.main"]