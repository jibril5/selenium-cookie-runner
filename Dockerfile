FROM seleniumbase/seleniumbase

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main3.py .

EXPOSE 8000

CMD ["uvicorn", "main3:app", "--host", "0.0.0.0", "--port", "8000"]
