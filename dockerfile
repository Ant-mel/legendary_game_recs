FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# COPY scraping/Link_scrape.py /app/
COPY scraping/project_scraper.py /app/

CMD ["python", "project_scraper.py"]
