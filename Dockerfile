FROM seleniumbase/seleniumbase

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

RUN apt-get update && apt-get install -y \
    xvfb \
    python3-tk \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main3.py .

EXPOSE 8000

CMD ["xvfb-run", "-a", "uvicorn", "main3:app", "--host", "0.0.0.0", "--port", "8000"]
