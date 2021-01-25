FROM python:3.9-slim
WORKDIR /app
RUN api install python-dbus -y
RUN python3 -m pip install -r requirements.txt --no-cache-dir
COPY . /app
EXPOSE 8080/tcp
#CMD ["python", "-m", "transmission-telegram-bot"]
