FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY scraping/Link_scrape.py /app/
COPY secrets/scraper_key.json /app/key.json

EXPOSE 8080

CMD ["python", "Link_scrape.py"]
