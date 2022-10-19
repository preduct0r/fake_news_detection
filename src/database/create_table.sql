CREATE TABLE IF NOT EXISTS rss_news_feed
(
    id               BIGSERIAL PRIMARY KEY,
    uid              TEXT        NOT NULL,
    title            TEXT        NOT NULL,
    source           TEXT        NOT NULL,
    description      TEXT        NOT NULL,
    publication_date TEXT NOT NULL
);