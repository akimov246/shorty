FROM python:3.14-slim
WORKDIR /shorty
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Запрещает Python создавать файлы .pyc (скомпилированный байт-код) на диске
ENV PYTHONDONTWRITEBYTECODE=1
# Отключает буферизацию потоков stdout и stderr. Без этой переменной логи вашего приложения могут «застревать» в буфере
ENV PYTHONUNBUFFERED=1
# Добавляет указанную директорию в список путей, где Python ищет модули. Если ваша структура проекта сложная, это избавит вас от ошибок
ENV PYTHONPATH=/app
# Альтернатива флагу в командной строке. Любой pip install будет игнорировать кэш, экономя место
ENV PIP_NO_CACHE_DIR=1

COPY alembic.ini ./
COPY migrations/ ./migrations/
COPY app/ ./app/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]