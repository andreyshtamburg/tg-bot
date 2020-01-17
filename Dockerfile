FROM vspolam/python3.7-base

WORKDIR /home

RUN pip install -U pip aiogram pytz
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "main.py"]
