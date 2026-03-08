FROM python:3.13-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./
COPY shared /app/shared/
COPY routers /app/routers/
COPY services /app/services/
COPY main.py dependencies.py ./

RUN pip install pipenv && \
    pipenv install --system --deploy

ENV PYTHONPATH=/app

ARG ENVIRONMENT=prod
ENV ENVIRONMENT=${ENVIRONMENT}

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 $( [ \"$ENVIRONMENT\" = \"dev\" ] && echo '--reload' )"]
