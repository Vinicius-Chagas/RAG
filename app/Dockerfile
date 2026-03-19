FROM python:3.14-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["fastapi", "run", "./main.py", "--port", "3333"]