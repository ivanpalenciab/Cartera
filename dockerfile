# Usa una imagen oficial de Python
FROM python:3.13-slim

WORKDIR /app


COPY . /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y locales && \
    sed -i '/^# *es_ES.UTF-8 UTF-8/s/^# *//' /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=es_ES.UTF-8


EXPOSE 8050

CMD ["python", "app.py"]