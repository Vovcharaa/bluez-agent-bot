FROM python:3.10.6 as build
WORKDIR /app
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv --upgrade-deps $VIRTUAL_ENV && apt update && apt install libdbus-1-dev libgirepository1.0-dev -y
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN python3 -m pip install wheel && python3 -m pip install -r requirements.txt --no-cache-dir

FROM python:3.10.6
WORKDIR /app
COPY --from=build /app /app
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . /app
EXPOSE 8080/tcp
CMD ["python", "-m", "src"]
