FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copying utils functions
COPY utils/processing_utils.py /app/
COPY utils/scraping_and_api_utils.py /app/

# COPY scraping/Link_scrape.py /app/
# COPY scraping/project_scraper.py /app/
COPY scraping/igdb_api_caller.py /app/

CMD ["python", "igdb_api_caller.py"]
