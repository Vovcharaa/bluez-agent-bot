FROM python:3.9 as build
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv --system-site-packages $VIRTUAL_ENV 
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN python3 -m pip install wheel && python3 -m pip install -r requirements.txt --no-cache-dir

FROM python:3.9-slim
WORKDIR /app
RUN apt update && apt install python3-dbus -y && rm -rf /var/lib/apt/lists/*
COPY --from=build /app /app
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . /app
EXPOSE 8080/tcp
CMD ["python", "-m", "src"]
