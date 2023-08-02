FROM python:3.10.0-slim

ENV PYTHONUNBUFFERED=1
ENV PATH=/etc/poetry/bin:$PATH
ENV POETRY_VIRTUALENVS_CREATE=0
ENV POETRY_HOME=/etc/poetry/

WORKDIR /app
ADD . /app/

RUN pip3 install --upgrade pip setuptools

RUN apt clean && apt autoclean

RUN apt update -y && \
    apt upgrade -y

RUN apt install -y --no-install-recommends \
    gcc \
    libc-dev \
    libmagic1

ADD https://raw.githubusercontent.com/python-poetry/install.python-poetry.org/main/install-poetry.py /tmp/install-poetry.py
RUN python /tmp/install-poetry.py --version 1.3.1

RUN addgroup --gid 999 chargeapigroup && \
    useradd --uid 999 --gid chargeapigroup chargeapiuser

RUN poetry install --no-dev --no-root

EXPOSE 8000

USER chargeapiuser