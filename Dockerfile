FROM python:3.9-slim

ENV PYTHONUNBUFFERED True
ENV PORT 8888

ENV APP_HOME /app

RUN apt-get update \
    && apt-get install -y libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

WORKDIR $APP_HOME
COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app