FROM python:3.14.3-alpine3.23

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD ["fastapi", "run", "src/main.py", "--port", "3333"]