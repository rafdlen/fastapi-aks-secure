FROM python:3.11-slim AS build
WORKDIR /w
COPY app/requirements.txt .
RUN pip wheel -r requirements.txt -w /wheels

FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/*
COPY app/ .
EXPOSE 8080
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8080"]
