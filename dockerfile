FROM python:3.11

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y gcc python3-dev
RUN apt-get install -y libxml2-dev libxslt1-dev build-essential python3-lxml zlib1g-dev libsnappy-dev
RUN apt-get install -y default-mysql-client default-libmysqlclient-dev
RUN pip install poetry

WORKDIR /app

COPY ./pyproject.toml /app/


RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8024