FROM python:3.12-slim

WORKDIR /app

# libheif for HEIC support
RUN apt-get update && apt-get install -y --no-install-recommends \
    libheif-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py bot.py parser.py ./

CMD ["python", "bot.py"]
