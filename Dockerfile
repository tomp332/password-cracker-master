FROM python:slim

WORKDIR /app

COPY requirements.txt .
COPY password_cracker_master ./password_cracker_master

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "password_cracker_master.src.server:main_api_router", "--host", "0.0.0.0", "--port", "5000"]
