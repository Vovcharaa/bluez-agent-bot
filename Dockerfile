FROM python:3.9-slim
WORKDIR /app
RUN apt install python-dbus -y
RUN python3 -m pip install -r requirements.txt --no-cache-dir
COPY . /app
EXPOSE 8080/tcp
CMD ["python", "-m", "src"]
