FROM seleniumbase/seleniumbase

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-tk \
    python3-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main3.py .

EXPOSE 8000

CMD ["uvicorn", "main3:app", "--host", "0.0.0.0", "--port", "8000"]
