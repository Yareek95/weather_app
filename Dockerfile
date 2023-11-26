FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

ENV NAME World

COPY . /app/

EXPOSE 5000

CMD ["python", "app.py"]
