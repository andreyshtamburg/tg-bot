FROM vspolam/python3.7-base

WORKDIR /home

ENV TELEGRAM_API_TOKEN="1008447247:AAFRJio0ilWbFdh66i-ICwk09bXqJjhHCkA"
ENV TELEGRAM_ACCESS_ID="382850832"

RUN pip install -U pip aiogram pytz
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "main.py"]
