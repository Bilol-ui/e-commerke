FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN uv pip install -r requirements.txt

COPY . /app

CMD ["uv","run","python3","manage.py","runserver","0:8000"]
