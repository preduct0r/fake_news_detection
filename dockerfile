FROM python:latest
WORKDIR ./
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir crawler-service
COPY src/crawler_service/ ./
ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_USER=root
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=rss_news_feed
CMD ["python", "-u", "crawler.py"]