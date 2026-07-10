FROM seleniumbase/seleniumbase:latest

WORKDIR /ap1

# Évite les installations interactives
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Prépare le driver SeleniumBase au build
RUN seleniumbase get chromedriver

COPY main3.py .

EXPOSE 8000

# Désactive l'entrypoint SeleniumBase qui peut interférer avec Render
ENTRYPOINT []

CMD ["uvicorn", "main3:app", "--host", "0.0.0.0", "--port", "8000"]
