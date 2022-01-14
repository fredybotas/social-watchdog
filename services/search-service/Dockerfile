FROM python:3.10.0-slim

COPY lib/liblog/dist/*.whl ./
COPY lib/libmq/dist/*.whl ./
COPY lib/libcore/dist/*.whl ./
RUN pip install *.whl && rm -rf *.whl

COPY services/search-service/dist/*.whl ./
RUN pip install *.whl && rm -rf *.whl
RUN python -m spacy download en_core_web_sm

CMD ["python", "-m", "search_service.main"]
